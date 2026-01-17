import sys
import os
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.survey_agent import process_survey, get_session, update_session

def test_natural_language_age():
    user_id = "test_voice_user"
    
    # 1. Start survey and get to Age question here
    update_session(user_id, "ask_name", {})
    process_survey(user_id, "MyName") # Advances to ask_age
    
    print("Testing Natural Language Input for Age...")
    
    # 2. Simulate voice input "I am 45 years old"
    input_text = "I am 45 years old"
    resp = process_survey(user_id, input_text)
    
    session = get_session(user_id)
    saved_age = session["data"].get("age")
    
    print(f"Input: '{input_text}'")
    print(f"Response: {resp}")
    print(f"Saved Age: {saved_age}")
    
    if saved_age == "45":
        print("✅ Natural Language Age Test Passed")
    else:
        print("❌ Natural Language Age Test Failed")

if __name__ == "__main__":
    try:
        from app.db.session_db import init_db
        init_db()
        test_natural_language_age()
    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
