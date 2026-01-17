from fastapi import FastAPI, Form, Request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import uuid
import tempfile
from dotenv import load_dotenv

# Import services
from app.services.voice_service import transcribe_audio
from app.services.query_service import query_agent
from app.agents.survey_agent import process_survey, get_session
from app.db.session_db import init_db

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ Database initialized.")

@app.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(default=""),
    MediaUrl0: str = Form(default=None),
    MediaContentType0: str = Form(default=None)
):
    """
    Handle incoming WhatsApp messages (Text or Voice).
    """
    sender_id = From
    print(f"📩 Received message from {sender_id}")

    final_text = Body

    # 1. Handle Voice Note
    if MediaUrl0 and MediaContentType0 and "audio" in MediaContentType0:
        print(f"🎙️ Voice note detected: {MediaUrl0}")
        try:
            # Download audio
            audio_response = requests.get(MediaUrl0, auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")))
            
            if audio_response.status_code == 200:
                # Save to temp file
                suffix = ".ogg" if "ogg" in MediaContentType0 else ".mp3"
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
                return str(MessagingResponse().message("Sorry, I couldn't download your voice note."))
        except Exception as e:
            print(f"❌ Error processing audio: {e}")
            return str(MessagingResponse().message("Sorry, I had trouble processing your voice message."))

    # 2. Process Text (from Body or Transcription)
    response_msg = MessagingResponse()
    
    if not final_text:
        response_msg.message("I didn't receive any text or audio.")
        return str(response_msg)

    # 3. Check Survey State
    session = get_session(sender_id)
    
    # If in survey mode, prioritize survey agent
    if session["step"] != "completed":
        survey_response = process_survey(sender_id, final_text)
        if survey_response:
            response_msg.message(survey_response)
            return str(response_msg)
    
    # 4. Fallback to RAG Agent for queries
    # Also handle "survey" keyword to restart
    if "survey" in final_text.lower():
        # Force reset survey
        session["step"] = "welcome"
        survey_intro = process_survey(sender_id, "") # trigger welcome
        response_msg.message(survey_intro)
        return str(response_msg)

    # 5. RAG Query
    print(f"🔍 Querying RAG with: {final_text}")
    try:
        rag_response = query_agent(final_text)
        response_msg.message(rag_response)
    except Exception as e:
        response_msg.message(f"I encountered an error looking that up: {e}")

    return str(response_msg)

@app.get("/")
def health_check():
    return {"status": "running", "service": "Insurance Agent API"}
