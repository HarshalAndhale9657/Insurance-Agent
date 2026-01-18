# 🛡️ Insurance Agent RAG Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-v0.2-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Twilio](https://img.shields.io/badge/Twilio-API-F22F46?style=for-the-badge&logo=twilio)

An advanced, AI-driven Insurance Agent capable of interacting seamlessly via **WhatsApp**. Built with a robust **RAG (Retrieval-Augmented Generation)** architecture, it handles insurance policy queries, processes voice notes, detects languages, and maintains conversation context—all powered by **Groq**, **OpenAI**, and **LangChain**.

---

## 📖 Table of Contents
- [✨ Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [⚙️ Configuration](#-configuration)
- [⚡ Running the Application](#-running-the-application)
- [🧪 Testing & Verification](#-testing--verification)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)

---

## ✨ Features

- **📱 WhatsApp Integration**: Real-time bidirectional communication using Twilio's WhatsApp Business API.
- **🎙️ Voice Note Processing**: Automatically transcribes audio messages (OGG/MP3) and responds textually.
- **🧠 RAG Architecture**: Retrieval-Augmented Generation using **ChromaDB** to answer policy-related questions accurately from PDF documents.
- **🌐 Multilingual Support**: Automatically detects and speaks Indian languages (Hindi, Marathi, Tamil, etc.) while processing logic in English.
- **💾 Persistent Sessions**: SQLite-backed session management ensures conversation history is preserved across server restarts.
- **📊 Admin Dashboard**: A comprehensive **Streamlit** UI for document ingestion, agent testing, and system monitoring.
- **⚡ Async Architecture**: Built on **FastAPI** with background tasks to handle high-concurrency message queues.

---

## 🏗️ Architecture

The system follows a modular microservices-like pattern within a monolith structure:

1.  **Ingestion Layer**: WhatsApp messages (Text/Audio) $\rightarrow$ Twilio Webhook $\rightarrow$ FastAPI.
2.  **Processing Layer**:
    *   **Translation Service**: Detects language $\leftrightarrow$ Translates to English.
    *   **Survey Agent**: Handles structured user data collection (Names, DOB, etc.).
    *   **RAG Agent**: Queries Vector DB (ChromaDB) for unstructured policy Q&A.
3.  **Storage Layer**:
    *   **Session DB**: SQLite for user state.
    *   **Vector DB**: ChromaDB for document embeddings.
4.  **Presentation Layer**: Streamlit Dashboard for admins.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python, FastAPI, Uvicorn | High-performance async API server. |
| **Orchestration** | LangChain, LangGraph | State management and agent flows. |
| **LLM Inference** | Groq (Llama 3), OpenAI | Ultra-fast inference for translation & chat. |
| **Vector Store** | ChromaDB | Embeddings storage for RAG. |
| **Database** | SQLite | Lightweight persistent storage for sessions. |
| **Frontend** | Streamlit | Admin interface for testing and management. |
| **Tunneling** | Ngrok | Exposing localhost to public internet for Twilio. |

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Twilio Account** (Sandbox enabled)
- **Groq API Key** (for fast inference) & **OpenAI API Key** (for embeddings)
- **Ngrok** installed and in PATH

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/insurance-agent-bot.git
    cd insurance-agent-bot
    ```

2.  **Set up Virtual Environment**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the following credentials:

| Variable | Description |
| :--- | :--- |
| `OPENAI_API_KEY` | Required for OpenAI Embeddings (RAG). |
| `GROQ_API_KEY` | Required for Llama-3 inference (Chat & Translation). |
| `TWILIO_ACCOUNT_SID` | Found in Twilio Console. |
| `TWILIO_AUTH_TOKEN` | Found in Twilio Console. |
| `TWILIO_WHATSAPP_NUMBER` | Sandbox Number (e.g., `whatsapp:+14155238886`). |

---

## ⚡ Running the Application

For a full local deployment, you need three terminal instances:

### 1. Start the Backend API
This serves the webhook for Twilio.
```powershell
# Terminal 1
uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start the Admin Dashboard
This launches the Streamlit UI.
```powershell
# Terminal 2
streamlit run app/main.py --server.port 8501
```

### 3. Expose via Ngrok
Connects your local API to the internet.
```powershell
# Terminal 3
ngrok http 8000
```

> **CRITICAL**: Copy the Forwarding URL from Ngrok (e.g., `https://xyz.ngrok-free.app`) and update your **Twilio Sandbox Webhook** to:
> `https://xyz.ngrok-free.app/webhook`

---

## 🧪 Testing & Verification

We have included automated test scripts in the `tests/` directory:

- **Verify Database**:
    ```bash
    python tests/verify_db.py
    ```
- **Verify Multilingual Support**:
    ```bash
    python tests/verify_multilingual.py
    ```

---

## 📂 Project Structure

```text
d:\Insurance Agent\
├── app\
│   ├── agents\        # Agentic logic (Survey, RAG, Graph)
│   ├── api\           # FastAPI endpoints and webhook logic
│   ├── db\            # Database connection & schema (SQLite)
│   ├── rag\           # RAG implementation (Loader, Splitter, VectorStore)
│   ├── services\      # External services (Twilio, Voice, Translation)
│   └── main.py        # Streamlit entry point
├── tests\             # Verification scripts
├── .env               # Secrets (Not committed)
├── requirements.txt   # Python dependencies
├── run_services.sh    # Convenience script for startup
└── README.md          # Project Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
