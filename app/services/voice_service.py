import os
import hashlib
import edge_tts
import asyncio

# Cache Directory (Relative to project root, assuming this runs from app context)
# We want it to be inside app/static/voice_cache
CACHE_DIR = os.path.join(os.path.dirname(__file__), "../static/voice_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Voice Mapping
VOICE_MAP = {
    "en": "en-US-ChristopherNeural",  # Professional US Male
    "hi": "hi-IN-SwaraNeural",       # Natural Indian Female
    "mr": "mr-IN-AarohiNeural",      # Marathi
    "ta": "ta-IN-PallaviNeural"      # Tamil
}

def get_voice(lang: str) -> str:
    """Returns the best neural voice for the given language."""
    # Default to English if lang not found
    return VOICE_MAP.get(lang, "en-US-ChristopherNeural")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio file to text using Groq's Whisper model.
    (Kept synchronous as it calls an API that might be sync or we leave it as is for now)
    """
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment.")

    client = Groq(api_key=api_key)
    
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(file_path), file.read()),
            model="whisper-large-v3",
            response_format="text"
        )
    
    return transcription

async def text_to_speech(text: str, lang: str = "en") -> str:
    """
    Converts text to speech using Microsoft Edge's Neural TTS (Free).
    Uses filesystem caching to prevent re-generating common phrases.
    
    Returns: Absolute path to the generated .mp3 file.
    """
    if not text:
        return None
        
    # 1. Generate Cache Key (MD5 of text + voice)
    voice = get_voice(lang)
    cache_key = hashlib.md5(f"{text}_{voice}".encode()).hexdigest()
    filename = f"{cache_key}.mp3"
    file_path = os.path.join(CACHE_DIR, filename)
    
    # 2. Check Cache
    if os.path.exists(file_path):
        print(f"🔊 Serving from cache: {filename}")
        return file_path
        
    # 3. Generate New
    print(f"🎙️ Generating new audio ({voice})...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)
    
    return file_path
