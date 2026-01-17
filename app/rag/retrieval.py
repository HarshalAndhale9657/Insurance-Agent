import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = os.path.join(os.path.dirname(__file__), "../../chroma_db")

def get_embeddings():
    """
    Returns the HuggingFace embeddings model.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore():
    """
    Returns the ChromaDB vector store instance.
    """
    embeddings = get_embeddings()
    if os.path.exists(DB_PATH):
        return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    else:
        # If DB doesn't exist, return an empty one or handle gracefully
        # For now, we assume ingestion happens first
        return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

def get_retriever():
    """
    Returns a retriever object from the vector store.
    """
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": 3})
