
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session_db import get_all_sessions, update_session, get_session

def test_persistence():
    print("🧪 Testing Persistent Storage...")
    
    # 1. Check existing sessions
    sessions = get_all_sessions()
    print(f"📊 Current Sessions in DB: {len(sessions)}")
    for s in sessions:
        print(f"   - User: {s['user_id']}, Step: {s['step']}")

    # 2. Simulate a new session update
    test_user = "test_verifier_user"
    print(f"\n📝 Creating/Updating test user: {test_user}")
    update_session(test_user, "verification_step", {"status": "verified"})
    
    # 3. Verify it was saved
    saved_session = get_session(test_user)
    if saved_session["step"] == "verification_step":
        print("✅ SUCCESS: Session saved and retrieved from DB.")
    else:
        print("❌ FAILURE: Session not retrieved correctly.")

if __name__ == "__main__":
    test_persistence()
