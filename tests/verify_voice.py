
import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from app.services.voice_service import text_to_speech

def test_voice_gen():
    print("🎙️ Testing Voice Generation (TTS)...")
    
    text = "Hello! I am your Insurance Agent. How can I assist you today?"
    
    output_path = text_to_speech(text)
    
    if output_path and os.path.exists(output_path):
        print(f"✅ Success: Audio generated at: {output_path}")
        print(f"   Size: {os.path.getsize(output_path)} bytes")
    else:
        print("❌ Failure: Audio file was not created.")

if __name__ == "__main__":
    test_voice_gen()
