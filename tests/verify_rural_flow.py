import sys
import os
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mocking RAG for recommendation test to avoid API call if needed, 
# but we will try to run it if environment variables are present.
from app.agents.survey_agent import process_survey, get_session, update_session

def test_survey_flow():
    user_id = "test_farmer_1"
    
    # 1. Start survey (Welcome)
    update_session(user_id, "welcome", {})
    resp = process_survey(user_id, "hi")
    print(f"Step 1 (Welcome): {resp}")
    
    # 2. Name
    resp = process_survey(user_id, "Ramesh")
    print(f"Step 2 (Name): {resp}")
    
    # 3. Age
    resp = process_survey(user_id, "45")
    print(f"Step 3 (Age): {resp}")
    
    # 4. Occupation
    resp = process_survey(user_id, "Farmer")
    print(f"Step 4 (Occupation): {resp}")
    
    # 5. Family
    resp = process_survey(user_id, "5 people, wife and 3 kids")
    print(f"Step 5 (Family): {resp}")
    
    # 6. Worry (Triggers Recommendation)
    print("Step 6: Sending Worry (should trigger recommendation)...")
    try:
        resp = process_survey(user_id, "My crops failing due to rain")
        print(f"\n✅ Final Response (Recommendation):\n{resp}\n")
    except Exception as e:
        print(f"❌ Error getting recommendation: {e}")

if __name__ == "__main__":
    try:
        from app.db.session_db import init_db
        init_db()
        test_survey_flow()
    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
