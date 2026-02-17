import os
import traceback
from dotenv import load_dotenv

load_dotenv()

try:
    print(f"Checking API Key: {'Found' if os.getenv('GOOGLE_API_KEY') else 'Missing'}")
    
    from app.services.query_service import query_agent
    print("Querying agent...")
    result = query_agent("What is insurance?")
    print("Result:", result)
except Exception as e:
    print(f"ERROR: {e}")
