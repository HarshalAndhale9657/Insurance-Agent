import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.rag.retrieval import get_retriever

load_dotenv()

def get_llm():
    """
    Returns the ChatGroq LLM instance.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    
    return ChatGroq(
        groq_api_key=api_key,
        model_name="qwen/qwen3-32b"
    )

def query_agent(question: str):
    """
    Queries the RAG agent with a question.
    """
    llm = get_llm()
    retriever = get_retriever()
    
    system_prompt = (
        "You are an intelligent insurance assistant. Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise."
        "\n\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    response = rag_chain.invoke({"input": question})
    
    # Extract sources
    sources = []
    if "context" in response:
        for doc in response["context"]:
            source_name = doc.metadata.get("source", "Unknown")
            page_num = doc.metadata.get("page", "N/A")
            sources.append(f"{os.path.basename(source_name)} (Page {page_num})")
            
    return {
        "answer": response["answer"],
        "sources": list(set(sources)) # Unique sources
    }
