import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.survey_agent import process_survey, get_session, update_session

def test_survey_reset():
    user_id = "test_user_reset"
    
    # 1. Start survey
    update_session(user_id, "welcome", {})
    resp = process_survey(user_id, "hi")
    print(f"Initial: {resp}")
    
    # 2. Advance to ask_age
    process_survey(user_id, "MyName")
    
    # Check state
    session = get_session(user_id)
    print(f"State before reset: {session['step']}")
    
    # 3. Send reset
    resp = process_survey(user_id, "I want to reset")
    print(f"Reset Response: {resp}")
    
    # 4. Check state
    session = get_session(user_id)
    print(f"State after reset: {session['step']}")
    
    if session["step"] == "welcome" and "reset" in resp.lower():
        print("✅ Survey Reset Test Passed")
    else:
        print("❌ Survey Reset Test Failed")

def test_formatting_logic():
    # Mock RAG response
    rag_response = {
        "answer": "This is a test answer.",
        "sources": ["doc1.pdf (Page 1)", "doc2.txt (Page 5)"]
    }
    
    # Logic from server.py
    if isinstance(rag_response, dict):
        answer = rag_response.get("answer", "")
        sources = rag_response.get("sources", [])
        
        response_text = f"{answer}"
        if sources:
            response_text += "\n\n📚 *Sources:*\n" + "\n".join([f"- {s}" for s in sources])
            
    print("\n--- Formatted Output ---")
    print(response_text)
    print("------------------------")
    
    expected_part = "This is a test answer.\n\n📚 *Sources:*\n- doc1.pdf (Page 1)"
    if expected_part in response_text:
         print("✅ Formatting Logic Test Passed")
    else:
         print("❌ Formatting Logic Test Failed")

if __name__ == "__main__":
    try:
        from app.db.session_db import init_db
        init_db()
        test_survey_reset()
        test_formatting_logic()
    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
