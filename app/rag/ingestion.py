import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = os.path.join(os.path.dirname(__file__), "../../chroma_db")

def get_embeddings():
    """
    Returns the HuggingFace embeddings model.
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_document(uploaded_file):
    """
    Loads and processes an uploaded file (PDF or Text).
    Returns a list of Document objects.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        if uploaded_file.name.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path)
        
        docs = loader.load()
        return docs
    finally:
        os.remove(tmp_path)

def split_documents(docs):
    """
    Splits documents into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_documents(docs)

def index_documents(chunks):
    """
    Indexes document chunks into ChromaDB using HuggingFace embeddings.
    """
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    vectorstore.persist()
    return len(chunks)
