
import sys
import os
import asyncio
import time
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()

from app.services.voice_service import text_to_speech

async def test_voice_upgrade():
    print("🎙️ Testing Voice Upgrade (EdgeTTS + Caching)...")
    
    text = "Hello! This is an industry standard voice test."
    
    # 1. First Generation
    start_time = time.time()
    path1 = await text_to_speech(text, "en")
    duration1 = time.time() - start_time
    
    if path1 and os.path.exists(path1):
        print(f"✅ Run 1 (Gen): {path1} | Time: {duration1:.2f}s")
    else:
        print("❌ Run 1 Failed")
        return

    # 2. Second Generation (Should be Cached)
    start_time = time.time()
    path2 = await text_to_speech(text, "en")
    duration2 = time.time() - start_time
    
    if path2 == path1:
        print(f"✅ Run 2 (Cache): {path2} | Time: {duration2:.2f}s")
        if duration2 < 0.1:
            print("🚀 Caching is WORKING (Instant load)")
        else:
            print("⚠️ Caching might be slow?")
    else:
        print("❌ Run 2 Failed (Path mismatch)")

    # 3. Test Hindi
    print("\n🇮🇳 Testing Hindi Voice...")
    path_hi = await text_to_speech("नमस्ते, आप कैसे हैं?", "hi")
    if path_hi and os.path.exists(path_hi):
         print(f"✅ Hindi Audio: {path_hi}")

if __name__ == "__main__":
    asyncio.run(test_voice_upgrade())
