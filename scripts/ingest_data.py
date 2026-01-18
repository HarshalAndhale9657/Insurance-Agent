
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.rag.ingestion import split_documents, index_documents
from langchain_community.document_loaders import TextLoader, PyPDFLoader

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def ingest_folder():
    print(f"📂 Scanning for documents in: {DATA_DIR}")
    
    if not os.path.exists(DATA_DIR):
        print(f"❌ Data directory not found: {DATA_DIR}")
        return

    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt") or f.endswith(".pdf")]
    
    if not files:
        print("⚠️ No documents found.")
        return

    all_chunks = []
    
    for filename in files:
        filepath = os.path.join(DATA_DIR, filename)
        print(f"📄 Processing: {filename}...")
        
        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
            else:
                loader = TextLoader(filepath, encoding='utf-8')
            
            docs = loader.load()
            print(f"   - Loaded {len(docs)} pages/sections.")
            
            # Add metadata if missing
            for doc in docs:
                doc.metadata["source"] = filename
            
            chunks = split_documents(docs)
            print(f"   - Split into {len(chunks)} chunks.")
            all_chunks.extend(chunks)
            
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

    if all_chunks:
        print(f"💾 Indexing {len(all_chunks)} total chunks to ChromaDB...")
        count = index_documents(all_chunks)
        print(f"✅ Success! Indexed {count} new knowledge chunks.")
    else:
        print("⚠️ No chunks created.")

if __name__ == "__main__":
    ingest_folder()
