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
        "You are an intelligent and empathetic Rural Insurance Assistant. "
        "Your goal is to explain insurance concepts in simple, jargon-free English to people living in rural India. "
        "Adhere to these rules:"
        "\n1. **Be Respectful**: Use polite language (e.g., 'Please', 'It is important to know')."
        "\n2. **Simplify**: Explain terms like 'premium' or 'claim' immediately."
        "\n3. **Structure**: Use bullet points or short paragraphs."
        "\n4. **Empathy**: Acknowledge the user's situation."
        "\n5. **Source Check**: If the user is just saying 'Hi', 'Thanks', or asking a general question NOT based on the context, start your answer with `[NO_RAG]`."
        "\n\n"
        "Use the following context to answer the user's question. If you don't know, say so politely."
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
            
    import re
    cleaned_answer = re.sub(r'<think>.*?</think>', '', response["answer"], flags=re.DOTALL).strip()
    
    # Check for [NO_RAG] tag
    if "[NO_RAG]" in cleaned_answer:
        cleaned_answer = cleaned_answer.replace("[NO_RAG]", "").strip()
        sources = [] # Clear sources for chit-chat

    return {
        "answer": cleaned_answer,
        "sources": list(set(sources)) # Unique sources
    }

def recommend_products(profile: str):
    """
    Generates insurance product recommendations based on a user profile.
    This bypasses strict retrieval to allow the LLM to synthesize a recommendation, 
    but ideally checking the context if possible. 
    For now, we use a direct prompt with the retriever context to 'find' the best product.
    """
    llm = get_llm()
    retriever = get_retriever()
    
    system_prompt = (
        "You are a senior Insurance Advisor for rural families in India. "
        "Based on the user's profile, recommend the most suitable insurance policy from the context. "
        "\n\n"
        "**Your Response Format:**"
        "\n1. **Greeting**: A warm, personalized greeting."
        "\n2. **Analysis**: Briefly explain why their profile needs protection (e.g., 'As a farmer, crops are your life...')."
        "\n3. **Recommendation**: Clearly state the recommended policy."
        "\n4. **Why this fits**: 2-3 bullet points explaining the benefits in simple terms."
        "\n5. **Closing**: An encouraging closing statement."
        "\n\n"
        "Keep the tone professional yet caring."
        "\n\nContext:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "User Profile: {input}"),
        ]
    )
    
    # We use the StuffDocumentsChain pattern again but focused on recommendation
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # Search for products relevant to the profile keywords
    response = rag_chain.invoke({"input": profile})
    
    import re
    cleaned_answer = re.sub(r'<think>.*?</think>', '', response["answer"], flags=re.DOTALL).strip()
    
    return cleaned_answer
