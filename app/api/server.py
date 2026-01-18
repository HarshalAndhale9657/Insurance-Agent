from fastapi import FastAPI, Form, Request, Response, BackgroundTasks
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests
import uuid
import tempfile
from dotenv import load_dotenv

# Import services
from app.services.voice_service import transcribe_audio
from app.services.query_service import query_agent
from app.agents.survey_agent import process_survey, get_session
from app.db.session_db import init_db, update_session
from app.services.translation_service import detect_language, translate_to_english, translate_to_user_lang

load_dotenv()

app = FastAPI()

from fastapi.staticfiles import StaticFiles
# Mount static directory
static_dir = os.path.join(os.path.dirname(__file__), "../static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized.")

# Twilio Client for Async Responses
def send_whatsapp_message(to_number: str, body_text: str):
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        
        # WhatsApp sandbox requires "whatsapp:" prefix
        from_number = "whatsapp:+14155238886" 
        
        message = client.messages.create(
            from_=from_number,
            body=body_text,
            to=to_number
        )
        print(f"📤 Sent Async Message SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending async message: {e}")

async def process_background_message(sender_id: str, final_text: str, media_url: str, media_type: str):
    """
    Background task to process the message and send a reply via Twilio API.
    """
    print(f"▶️ Starting Background Processing for {sender_id}")

    # 1. Handle Voice Note
    if media_url and media_type and "audio" in media_type:
        print(f"🎙️ Voice note detected: {media_url}")
        try:
            # Download audio
            audio_response = requests.get(media_url, auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")))
            
            if audio_response.status_code == 200:
                # Save to temp file
                suffix = ".ogg" if "ogg" in media_type else ".mp3"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(audio_response.content)
                    tmp_path = tmp_file.name
                
                # Transcribe
                print("📝 Transcribing...")
                transcription = transcribe_audio(tmp_path)
                final_text = transcription
                print(f"📝 Transcribed text: {final_text}")
                
                # Clean up
                os.remove(tmp_path)
            else:
                send_whatsapp_message(sender_id, "Sorry, I couldn't download your voice note.")
                return
        except Exception as e:
            print(f"❌ Error processing audio: {e}")
            send_whatsapp_message(sender_id, "Sorry, I had trouble processing your voice message.")
            return

    if not final_text:
        send_whatsapp_message(sender_id, "I didn't receive any text or audio.")
        return

    # 2. Load Session
    session = get_session(sender_id)
    session_data = session["data"]

    # 3. Detect Language
    user_lang = session_data.get("language", "en") 
    
    detected_lang = detect_language(final_text)
    
    # Logic: 
    # 1. If we detect a NEW language that is NOT English, switch immediately (e.g. "Namaste" -> 'hi').
    # 2. If we detect English, only switch if input is long enough to be sure it's not just "Ok" or "Ji".
    # 3. Actually, let's just trust the LLM but stick to Indian languages if detected.
    
    if detected_lang != "en":
        user_lang = detected_lang
        session_data["language"] = user_lang
    elif len(final_text.split()) > 2:
        # Only switch BACK to English if it's a full sentence. 
        # Prevents "Ok" (en) from disrupting a Hindi conversation.
        user_lang = detected_lang
        session_data["language"] = user_lang

    print(f"🌐 Language: {user_lang} (Detected: {detected_lang})")

    # 4. Translate to English
    english_text = translate_to_english(final_text, user_lang)
    print(f"🔤 English Input: {english_text}")

    # 5. Process (Survey or RAG)
    response_text_to_send = None

    # Flag to track if we should generate PDF
    should_generate_pdf = False

    # Check Survey State
    if session["step"] != "completed":
        # Pass current session to avoid double DB read (optimization)
        survey_result = process_survey(sender_id, english_text, current_session=session)
        
        if survey_result:
            survey_response_en = survey_result.get("response")
            # CRITICAL FIX: Update local session state immediately
            if survey_result.get("next_step"):
                session["step"] = survey_result["next_step"]
                
                # Check if we JUST completed the survey
                if session["step"] == "completed":
                    should_generate_pdf = True
                    
            if survey_result.get("data"):
                session["data"] = survey_result["data"]
                # Update local session_data reference too
                session_data = session["data"]
            
            if survey_response_en:
                response_text_to_send = translate_to_user_lang(survey_response_en, user_lang)

    # Fallback to RAG
    if not response_text_to_send:
        # Check reset
        if "survey" in english_text.lower():
            # Reset logic via survey agent
            survey_result = process_survey(sender_id, "reset", current_session=session)
            if survey_result:
                session["step"] = survey_result["next_step"]
                session_data = survey_result["data"]
                session["data"] = session_data
                survey_intro_en = survey_result.get("response")
                response_text_to_send = translate_to_user_lang(survey_intro_en, user_lang)
        else:
            # RAG Query
            print(f"🔍 Querying RAG with: {english_text}") 
            try:
                rag_response = query_agent(english_text)
                
                if isinstance(rag_response, dict):
                    answer = rag_response.get("answer", "")
                    sources = rag_response.get("sources", [])
                    answer_translated = translate_to_user_lang(answer, user_lang)
                    
                    response_text_to_send = f"{answer_translated}"
                    if sources:
                        response_text_to_send += "\n\n📚 *Sources:*\n" + "\n".join([f"- {s}" for s in sources])
                else:
                    response_text_to_send = str(rag_response)

            except Exception as e:
                print(f"❌ RAG Error: {e}")
                response_text_to_send = "I encountered an error looking that up."

    # 6. Send Response
    irda_disclaimer = "\n\n_(IRDAI: Insurance is subject to market risk. Read strictly.)_"
    
    if response_text_to_send:
        # Check if we should reply with Voice (if input was audio)
        should_send_voice = False
        if media_url and "audio" in media_type:
            should_send_voice = True

        # Send Text/Voice
        if should_send_voice:
            print("🎙️ Generating Audio Reply (EdgeTTS)...")
            from app.services.voice_service import text_to_speech
            
            clean_text = response_text_to_send.replace("*", "")
            audio_path = await text_to_speech(clean_text, user_lang)
            
            if audio_path:
                filename = os.path.basename(audio_path)
                ngrok_url = os.getenv("NGROK_URL")
                
                if ngrok_url:
                    media_url = f"{ngrok_url}/static/voice_cache/{filename}"
                    try:
                        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
                        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
                        client = Client(account_sid, auth_token)
                        client.messages.create(
                            from_="whatsapp:+14155238886",
                            to=sender_id,
                            media_url=[media_url]
                        )
                    except Exception as e:
                        print(f"❌ Twilio Audio Error: {e}")
                        send_whatsapp_message(sender_id, response_text_to_send + irda_disclaimer)
                else:
                    send_whatsapp_message(sender_id, response_text_to_send + irda_disclaimer)
            else:
                send_whatsapp_message(sender_id, response_text_to_send + irda_disclaimer)
        else:
            send_whatsapp_message(sender_id, response_text_to_send + irda_disclaimer)
            
        # Enterprise Feature: PDF Roadmap
        if should_generate_pdf and session_data.get("recommendation"):
             try:
                 from app.services.report_service import generate_pdf_report
                 print("📄 Generating Enterprise PDF Report...")
                 pdf_filename = f"Roadmap_{sender_id}_{uuid.uuid4().hex[:6]}.pdf"
                 pdf_path = generate_pdf_report(session_data, session_data["recommendation"], pdf_filename)
                 
                 ngrok_url = os.getenv("NGROK_URL")
                 if ngrok_url:
                     pdf_url = f"{ngrok_url}/static/reports/{pdf_filename}"
                     
                     # Send as Media Attachment
                     try:
                        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
                        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
                        client = Client(account_sid, auth_token)
                        
                        client.messages.create(
                            from_="whatsapp:+14155238886",
                            to=sender_id,
                            media_url=[pdf_url],
                            body="📥 *Here is your Personal Insurance Roadmap*"
                        )
                        print(f"✅ PDF Sent as Attachment: {pdf_url}")
                     except Exception as e:
                        print(f"❌ Twilio PDF Error: {e}")
                        # Fallback to link if attachment fails
                        send_whatsapp_message(sender_id, f"📥 *Download Your Roadmap*:\n{pdf_url}")

             except Exception as e:
                 print(f"❌ PDF Gen Error: {e}")

    # 7. Persist Session
    update_session(sender_id, session["step"], session_data)


@app.post("/webhook")
async def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    From: str = Form(...),
    Body: str = Form(default=""),
    MediaUrl0: str = Form(default=None),
    MediaContentType0: str = Form(default=None)
):
    """
    Handle incoming WhatsApp messages (Async).
    Returns 200 OK immediately to satisfy Twilio.
    """
    sender_id = From
    print(f"📩 Received message from {sender_id}. Queuing background task...")
    
    # Add to background queue
    background_tasks.add_task(
        process_background_message, 
        sender_id, 
        Body, 
        MediaUrl0, 
        MediaContentType0
    )
    
    # Return empty TwiML to stop Twilio from waiting
    return Response(content=str(MessagingResponse()), media_type="application/xml")

@app.get("/")
def health_check():
    return {"status": "running", "service": "Insurance Agent API (Async Mode)"}
