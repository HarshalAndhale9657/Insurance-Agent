import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.rag.retrieval import get_retriever

load_dotenv()

def get_llm():
    """
    Returns the Google Gemini LLM instance.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    
    return ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model="gemini-1.5-flash",
        temperature=0.3
    )

def query_agent(question: str):
    """
    Queries the RAG agent with a question.
    """
    llm = get_llm()
    retriever = get_retriever()
    
    system_prompt = (
        "You are an expert, warm, and highly intelligent Rural Insurance Advisor named 'Suraksha Sahayak'. "
        "Your mission is to empower rural families with clear, actionable insurance advice. "
        "\n\n"
        "**Core Guidelines:**\n"
        "1.  **Be Relatable**: Speak like a trusted, wise friend. Use analogies if it helps."
        "\n2.  **Simplify Ruthlessly**: Never use jargon like 'premium' or 'sum assured' without instantly explaining it in simple words."
        "\n3.  **Answer Directly**: Start your answer immediately. Do NOT repeat the question or say 'Here is the answer'."
        "\n4.  **Empathy First**: If the user mentions a problem (crops, illness), acknowledge it before answering."
        "\n5.  **Context Aware**: Use the provided documents to answer. If the answer isn't there, say you don't know but offer general wisdom."
        "\n\n"
        "**Context:**\n"
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
        "You are the senior-most Insurance Strategist for rural India. "
        "Analyze the user's profile deeply and recommend the single best policy from the context. "
        "\n\n"
        "**Your Response Logic:**"
        "\n1.  **Acknowledge the Situation**: 'I see you are a farmer with a family of 4...'"
        "\n2.  **The Perfect Match**: 'Based on your worry about crop failure, I strongly recommend...'"
        "\n3.  **Why?**: Explain the specific benefits (low cost, high coverage) that matter to *them*."
        "\n4.  **Next Steps**: Encouragingly tell them how to proceed."
        "\n\n"
        "Make the recommendation feel personalized and confident."
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
