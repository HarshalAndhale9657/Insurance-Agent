import os
import uuid
import tempfile
import requests
from typing import Dict, Any, Optional

# Import services
from app.services.voice_service import transcribe_audio, text_to_speech
from app.services.query_service import query_agent
from app.agents.survey_agent import process_survey, get_session, get_step_prompt
from app.db.session_db import init_db, update_session
from app.services.translation_service import detect_language, translate_to_english, translate_to_user_lang

class AgentService:
    def __init__(self):
        # Ensure DB is initialized
        init_db()

    async def process_message(self, session_id: str, text: str = None, audio_url: str = None, audio_type: str = None, tts_enabled: bool = False) -> Dict[str, Any]:
        """
        Core logic to process a user message (Text or Audio).
        Returns a dict with: 'response_text', 'audio_path' (optional), 'sources' (optional), 'media_url' (optional)
        """
        print(f"▶️ Processing message for {session_id}")
        
        final_text = text

        # 1. Handle Voice Note
        if audio_url and audio_type and "audio" in audio_type:
            print(f"🎙️ Voice note detected: {audio_url}")
            try:
                # Determine how to download (Twilio vs generic URL)
                # For now assuming basic generic download or handling auth if needed specific to endpoint
                # NOTE: In server.py we used Twilio auth. For web app, this might be a direct file upload or static URL.
                # We'll adapt to try basic get first, or assume server.py passed a local path or accessible URL.
                
                # If it's a Twilio URL requires Auth, this service might need to know that. 
                # For simplicity, let's assume the caller handles auth-gated downloads OR this is a public/local URL.
                # BUT, to keep backward compat with the Twilio flow which we will refactor server.py to use this,
                # we might need to handle the download there or pass the auth'd content.
                # Let's assume the `audio_url` passed here is ACCESSIBLE. 
                
                # Check if it is a local file path (for web app uploads)
                if os.path.exists(audio_url):
                    tmp_path = audio_url
                    should_delete = False
                else:
                    # Download
                    auth = None
                    if "api.twilio.com" in audio_url:
                        auth = (os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
                    
                    audio_response = requests.get(audio_url, auth=auth)
                    
                    if audio_response.status_code == 200:
                        suffix = ".ogg" if "ogg" in audio_type else ".mp3"
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                            tmp_file.write(audio_response.content)
                            tmp_path = tmp_file.name
                        should_delete = True
                    else:
                        return {"response_text": "Sorry, I couldn't download your voice note."}

                # Transcribe
                print("📝 Transcribing...")
                transcription = transcribe_audio(tmp_path)
                final_text = transcription
                print(f"📝 Transcribed text: {final_text}")
                
                if should_delete and os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
            except Exception as e:
                print(f"❌ Error processing audio: {e}")
                return {"response_text": "Sorry, I had trouble processing your voice message."}

        if not final_text:
            return {"response_text": "I didn't receive any text or audio."}

        # 2. Load Session
        session = get_session(session_id)
        session_data = session["data"]

        # 3. Detect Language
        detected_lang = "en" 
        response_text_to_send = None # Initialize to avoid UnboundLocalError 
        
        # Check for explicit language requests (High Priority Override)
        text_lower = final_text.lower()
        explicit_lang = None
        
        if "english" in text_lower:
             explicit_lang = "en"
        elif "hindi" in text_lower or "हिंदी" in text_lower:
             explicit_lang = "hi"
        elif "marathi" in text_lower or "मराठी" in text_lower:
             explicit_lang = "mr"
             
        if explicit_lang:
            user_lang = explicit_lang
            session_data["language"] = explicit_lang
            print(f"🔄 Explicit Language Switch: {explicit_lang}")
            
            # Don't process this text as an answer. Re-prompt current step.
            current_prompt_en = get_step_prompt(session["step"])
            response_text_to_send = translate_to_user_lang(current_prompt_en, user_lang)
            # Prepend confirmation?
            # response_text_to_send = f"(Language switched to {user_lang})\n\n{response_text_to_send}"
        else:
            # Fallback to Sticky / Auto-detect
            if "language" not in session_data:
                detected_lang = detect_language(final_text)
                if detected_lang != "en" or len(final_text.split()) > 2:
                     session_data["language"] = detected_lang
                     user_lang = detected_lang
                else:
                     user_lang = "en" # Default to En
            else:
                user_lang = session_data["language"]

        print(f"🌐 Language: {user_lang} (Explicit: {explicit_lang}, Detected: {detected_lang})")

        # 4. Translate to English
        english_text = translate_to_english(final_text, user_lang)
        print(f"🔤 English Input: {english_text}")

        # 5. Process (Survey or RAG)
        response_text_to_send = response_text_to_send # Carry over if set
        sources = []
        should_generate_pdf = False

        # Only process survey logic if we haven't already handled an explicit command
        if not response_text_to_send:
            # Check Survey State
            if session["step"] != "completed":
                survey_result = process_survey(session_id, english_text, current_session=session)
                
                if survey_result:
                    survey_response_en = survey_result.get("response")
                    if survey_result.get("next_step"):
                        session["step"] = survey_result["next_step"]
                        if session["step"] == "completed":
                             should_generate_pdf = True
                            
                    if survey_result.get("data"):
                        session["data"] = survey_result["data"]
                        session_data = session["data"]
                    
                    if survey_response_en:
                        response_text_to_send = translate_to_user_lang(survey_response_en, user_lang)

        # Fallback to RAG
        if not response_text_to_send:
            if "survey" in english_text.lower():
                survey_result = process_survey(session_id, "reset", current_session=session)
                if survey_result:
                    session["step"] = survey_result["next_step"]
                    session_data = survey_result["data"]
                    session["data"] = session_data
                    survey_intro_en = survey_result.get("response")
                    response_text_to_send = translate_to_user_lang(survey_intro_en, user_lang)
            else:
                print(f"🔍 Querying RAG with: {english_text}") 
                try:
                    rag_response = query_agent(english_text)
                    
                    if isinstance(rag_response, dict):
                        answer = rag_response.get("answer", "")
                        sources = rag_response.get("sources", [])
                        answer_translated = translate_to_user_lang(answer, user_lang)
                        response_text_to_send = answer_translated
                    else:
                        response_text_to_send = str(rag_response)

                except Exception as e:
                    print(f"❌ RAG Error: {e}")
                    response_text_to_send = "I encountered an error looking that up."

        # 6. Response Preparation
        irda_disclaimer = "\n\n_(IRDAI: Insurance is subject to market risk. Read strictly.)_"
        full_response_text = (response_text_to_send or "") + irda_disclaimer
        
        result = {
            "response_text": full_response_text,
            "sources": sources,
            "user_language": user_lang,
            "session_data": session_data
        }

        # PDF Generation (Enterprise Feature)
        if should_generate_pdf and session_data.get("recommendation"):
             try:
                 from app.services.report_service import generate_pdf_report
                 print("📄 Generating Enterprise PDF Report...")
                 pdf_filename = f"Roadmap_{session_id}_{uuid.uuid4().hex[:6]}.pdf"
                 # Ensure reports dir exists
                 reports_dir = os.path.join(os.path.dirname(__file__), "../static/reports")
                 os.makedirs(reports_dir, exist_ok=True)
                 
                 # Report service likely needs just the filename if it saves to a fixed path, 
                 # or we need to check its implementation. 
                 # Checking server.py: generate_pdf_report(session_data, session_data["recommendation"], pdf_filename)
                 # It seems it handles the path internally or saves it relative to where? 
                 # We'll assume it behaves as existing server.py expects.
                 
                 generate_pdf_report(session_data, session_data["recommendation"], pdf_filename)
                 
                 ngrok_url = os.getenv("NGROK_URL")
                 if ngrok_url:
                     pdf_url = f"{ngrok_url}/static/reports/{pdf_filename}"
                     result["media_url"] = pdf_url
                     result["media_type"] = "application/pdf"
                     
             except Exception as e:
                 print(f"❌ PDF Gen Error: {e}")

        # Voice Reply (if input was audio OR tts_enabled is True)
        if (audio_url and "audio" in audio_type) or tts_enabled:
            print("🎙️ Generating Audio Reply (EdgeTTS)...")
            clean_text = full_response_text.replace("*", "")
            try:
                audio_path = await text_to_speech(clean_text, user_lang)
                
                if audio_path:
                    filename = os.path.basename(audio_path)
                    ngrok_url = os.getenv("NGROK_URL")
                    if ngrok_url:
                        # Return URL for Twilio/Web
                        result["audio_url"] = f"{ngrok_url}/static/voice_cache/{filename}"
                    else:
                        # Fallback to local path if no ngrok (for local web testing)
                        # Construct a localhost URL for the frontend
                        result["audio_url"] = f"http://localhost:8000/static/voice_cache/{filename}"
                        result["audio_path"] = audio_path 
            except Exception as e:
                print(f"❌ TTS Error: {e}") 

        # 7. Persist Session
        update_session(session_id, session["step"], session["data"])
        
        return result
