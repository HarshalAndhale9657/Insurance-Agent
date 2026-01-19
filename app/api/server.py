from fastapi import FastAPI, Form, Request, Response, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import shutil
import uuid
import tempfile
from dotenv import load_dotenv
from pydantic import BaseModel

# Import services
from app.services.agent_service import AgentService
from app.services.voice_service import text_to_speech
from app.db.session_db import init_db
from fastapi.responses import FileResponse

load_dotenv()

app = FastAPI()

# Add CORS so React frontend (localhost:5173) can talk to FastAPI (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

# Mount static directory
static_dir = os.path.join(os.path.dirname(__file__), "../static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize Agent Service
agent_service = AgentService()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized.")

# --- Twilio Client for Async Responses ---
def send_whatsapp_message(to_number: str, body_text: str, media_url: str = None):
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        
        # WhatsApp sandbox requires "whatsapp:" prefix
        from_number = "whatsapp:+14155238886" 
        
        msg_args = {
            "from_": from_number,
            "to": to_number,
            "body": body_text
        }
        if media_url:
            msg_args["media_url"] = [media_url]

        message = client.messages.create(**msg_args)
        print(f"📤 Sent Async Message SID: {message.sid}")
    except Exception as e:
        print(f"❌ Error sending async message: {e}")

async def process_twilio_background(sender_id: str, text: str, media_url: str, media_type: str):
    """
    Background task wrapper for Twilio using AgentService.
    """
    result = await agent_service.process_message(
        session_id=sender_id,
        text=text,
        audio_url=media_url,
        audio_type=media_type
    )
    
    response_text = result.get("response_text", "")
    response_media = result.get("media_url") or result.get("audio_url")
    
    send_whatsapp_message(sender_id, response_text, media_url=response_media)

# --- REST API for Web App ---

class TTSRequest(BaseModel):
    text: str
    language: str

@app.post("/api/tts")
async def tts_endpoint(request: TTSRequest):
    """
    REST API for Text-to-Speech. Returns a static URL.
    """
    print(f"🗣️ TTS Request: {request.language} - {request.text[:30]}...")
    
    try:
        # Generate audio (returns absolute path)
        audio_path = await text_to_speech(request.text, request.language)
        
        if not audio_path or not os.path.exists(audio_path):
            return Response(content="Failed to generate audio file", status_code=500)
            
        # Convert path to URL
        filename = os.path.basename(audio_path)
        # Assuming server runs on port 8000; in prod use env var
        audio_url = f"http://localhost:8000/static/voice_cache/{filename}"
        
        return {"audio_url": audio_url}

    except Exception as e:
        print(f"❌ TTS Exception: {e}")
        return Response(content=str(e), status_code=500)

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    REST API for the Web Frontend.
    """
    result = await agent_service.process_message(
        session_id=request.session_id,
        text=request.message
    )
    return result

@app.post("/api/audio")
async def audio_endpoint(session_id: str = Form(...), file: UploadFile = File(...)):
    """
    REST API for Audio Uploads (Web Frontend).
    """
    # Save uploaded file
    file_path = os.path.join(static_dir, f"upload_{uuid.uuid4()}.wav")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    result = await agent_service.process_message(
        session_id=session_id,
        text=None,
        audio_url=file_path,
        audio_type="audio/wav"
    )
    
    # Clean up upload? Maybe keep for debugging.
    # os.remove(file_path) 
    
    return result

# --- Twilio Webhook ---

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
    """
    sender_id = From
    print(f"📩 Received message from {sender_id}. Queuing background task...")
    
    # Add to background queue
    background_tasks.add_task(
        process_twilio_background, 
        sender_id, 
        Body, 
        MediaUrl0, 
        MediaContentType0
    )
    
    return Response(content=str(MessagingResponse()), media_type="application/xml")

@app.get("/")
def health_check():
    return {"status": "running", "service": "Insurance Agent API (Web + WhatsApp)"}
