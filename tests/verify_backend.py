import os
import sys
import shutil

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.ingestion import split_documents, index_documents
from app.services.query_service import query_agent
from langchain.schema import Document

def verify_backend():
    print("--- Starting Backend Verification ---")
    
    # 1. Create Dummy Content
    print("1. Creating dummy document content...")
    text_content = """
    The 'SuperSafe' insurance policy covers water damage, fire damage, and theft.
    However, it explicitly excludes flood damage caused by natural disasters.
    The deductible for theft is $500.
    """
    doc = Document(page_content=text_content, metadata={"source": "test_policy.txt"})
    
    # 2. Ingest
    print("2. Ingesting document...")
    chunks = split_documents([doc])
    count = index_documents(chunks)
    print(f"   Indexed {count} chunks.")
    
    # 3. Query - Positive Case
    print("3. Testing Query (Positive Case)...")
    question1 = "What is the deductible for theft?"
    answer1 = query_agent(question1)
    print(f"   Q: {question1}")
    print(f"   A: {answer1}")
    
    if "$500" in answer1:
        print("   ✅ SUCCESS: Correct deductible found.")
    else:
        print("   ❌ FAILURE: Deductible not found in answer.")

    # 4. Query - Negative Case
    print("4. Testing Query (Negative Case)...")
    question2 = "Is flood damage covered?"
    answer2 = query_agent(question2)
    print(f"   Q: {question2}")
    print(f"   A: {answer2}")
    
    if "exclude" in answer2.lower() or "no" in answer2.lower():
         print("   ✅ SUCCESS: Exclusion correctly identified.")
    else:
        print("   ⚠️ WARNING: Check if answer correctly states exclusion.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    # Ensure .env is loaded
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for API Key
    if not os.getenv("GROQ_API_KEY"):
        print("❌ ERROR: GROQ_API_KEY not found in environment.")
    else:
        verify_backend()
