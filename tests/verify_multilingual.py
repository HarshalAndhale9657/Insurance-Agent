
import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load env vars
load_dotenv()

from app.services.translation_service import detect_language, translate_to_english, translate_to_user_lang

def test_multilingual():
    print("🌍 Testing Multilingual Support...")

    # 1. Test Detection
    hindi_text = "Namaste, mujhe insurance plan chahiye."
    lang = detect_language(hindi_text)
    print(f"Test 1 (Detection): '{hindi_text}' -> Detected: {lang}")
    if lang not in ['hi', 'mix', 'in']: # accept flexible codes for now
        print(f"⚠️ Warning: Expected 'hi' or similar, got {lang}")
    
    # 2. Test Translation to English
    english_translation = translate_to_english(hindi_text, lang)
    print(f"Test 2 (To English): {english_translation}")
    
    # 3. Test Translation back to Hindi
    response_en = "Sure, I can help you with that. What is your age?"
    hindi_response = translate_to_user_lang(response_en, lang)
    print(f"Test 3 (To Hindi): {hindi_response}")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in .env")
    else:
        test_multilingual()
