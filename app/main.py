import streamlit as st
import os
import sys
import time

# Add project root to sys.path to allow importing from 'app' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import RAG services (safeguarded)
try:
    from app.rag.ingestion import load_document, split_documents, index_documents
    from app.services.query_service import query_agent
except ImportError as e:
    st.error(f"Failed to import RAG modules: {e}")
    st.stop()

# Import Admin DB
from app.db.session_db import get_all_sessions

def main():
    st.set_page_config(page_title="Insurance Agent", page_icon="🛡️", layout="wide")

    # --- Custom CSS for Premium Look ---
    st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stChatMessage {
            background-color: #262730;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        div[data-testid="stSidebar"] {
            background-color: #262730; 
        }
        h1 {
            color: #4F8BF9;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar Navigation ---
    with st.sidebar:
        st.title("🛡️ Insurance Agent")
        page = st.radio("Navigate", ["🤖 Virtual Agent", "📊 Admin Dashboard"])
        st.divider()

    if page == "🤖 Virtual Agent":
        show_chat_interface()
    else:
        show_admin_dashboard()

def show_admin_dashboard():
    st.title("📊 Admin Dashboard - Rural Leads")
    
    # metrics
    sessions = get_all_sessions()
    
    # Process Data
    import pandas as pd
    
    data_list = []
    for s in sessions:
        user_data = s["data"]
        # Only interested in people who started the survey
        if not user_data:
            continue
            
        row = {
            "User ID": s["user_id"],
            "Status": s["step"],
            "Name": user_data.get("name", "N/A"),
            "Age": user_data.get("age", "N/A"),
            "Occupation": user_data.get("occupation", "N/A"),
            "Family": user_data.get("family", "N/A"),
            "Worry": user_data.get("worry", "N/A"),
            "Recommendation": user_data.get("recommendation", "Pending")
        }
        data_list.append(row)
        
    if not data_list:
        st.info("No survey data available yet.")
        return

    df = pd.DataFrame(data_list)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads", len(df))
    col2.metric("Completed Surveys", len(df[df["Status"] == "completed"]))
    
    if "Occupation" in df.columns:
        top_occupation = df["Occupation"].mode()
        if not top_occupation.empty:
            col3.metric("Top Occupation", top_occupation[0])

    st.divider()
    
    st.subheader("📋 Recent Leads")
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    st.download_button(
        label="Download Leads CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='rural_leads.csv',
        mime='text/csv',
    )

def show_chat_interface():
    st.title("Insurance Agent AI 🛡️")
    st.write("Current LLM: **Groq (Qwen 2.5)** | Embeddings: **HuggingFace**")

    # --- Sidebar for Document Ingestion ---
    with st.sidebar:
        st.header("📄 Document Upload")
        uploaded_file = st.file_uploader("Upload Policy (PDF/Text)", type=["pdf", "txt"])
        
        if uploaded_file:
            if st.button("Ingest Document", type="primary"):
                with st.spinner("Processing document..."):
                    try:
                        docs = load_document(uploaded_file)
                        chunks = split_documents(docs)
                        count = index_documents(chunks)
                        st.success(f"Successfully indexed {count} chunks!")
                    except Exception as e:
                        st.error(f"Error processing document: {e}")
        
        st.divider()
        st.info("Upload an insurance policy to ask questions about it.")
        
        st.divider()
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # --- Chat Interface ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        avatar = "🛡️" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Ask a question about your insurance policy..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant", avatar="🛡️"):
            with st.spinner("Thinking..."):
                try:
                    result = query_agent(prompt)
                    
                    # Check if result is dict (new format) or str (compatibility)
                    if isinstance(result, dict):
                        answer = result["answer"]
                        sources = result.get("sources", [])
                        
                        st.markdown(answer)
                        
                        if sources:
                            with st.expander("📚 Sources"):
                                for s in sources:
                                    st.caption(f"- {s}")
                                    
                        # Add assistant response to history
                        st.session_state.messages.append({"role": "assistant", "content": answer}) # Store just text for history to keep it simple
                    else:
                        st.markdown(result)
                        st.session_state.messages.append({"role": "assistant", "content": result})

                except ValueError as ve:
                    st.error(str(ve))
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
