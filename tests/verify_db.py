import sys
import os
import json

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session_db import get_all_sessions, init_db

def test_db_retrieval():
    print("Testing DB Retrieval for Dashboard...")
    sessions = get_all_sessions()
    
    print(f"Found {len(sessions)} sessions.")
    
    for s in sessions:
        print(f"\nUser: {s['user_id']} | Status: {s['step']}")
        print(f"Data: {json.dumps(s['data'], indent=2)}")
        
    if len(sessions) > 0:
        print("✅ DB Retrieval Test Passed")
    else:
        print("⚠️ No sessions found. Run 'verify_rural_flow.py' first to generate data.")

if __name__ == "__main__":
    init_db()
    test_db_retrieval()
