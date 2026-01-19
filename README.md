# 🌾 Insurance Accessibility for Rural India

A comprehensive digital platform designed to "Bridge the Insurance Gap" for rural communities in India. This application serves as a trusted guide, offering simplified education, AI-powered assistance, and multilingual support to help users understand and access government and private insurance schemes.

## 🚀 Key Features

### 1. 🎓 Interactive Education Hub
*   **Audio Guides:** Listen to insurance concepts in **English, Hindi, and Marathi** using our built-in TTS (Text-to-Speech) engine.
*   **Simplified Learning:** Cards covering Health, Life, Crop, and Vehicle insurance.
*   **Detailed Guides:** "Read More" functionality for deep dives into schemes like **Ayushman Bharat**, **PMFBY**, and **PMJJBY**.

### 2. 🤖 AI Insurance Assistant (RAG Chatbot)
*   **Contextual Answers:** Powered by a vector database of insurance policies.
*   **Multilingual Support:** Chat in your native language (Hindi/Marathi support via translation layer).
*   **WhatsApp Integration:** Extend accessibility to WhatsApp for low-bandwidth users (via Twilio).

### 3. 🛡️ User Dashboard & Tools
*   **Policy Vault:** Securely upload and store policy documents.
*   **AI Explainer:** Get simple summaries of complex policy PDFs.
*   **Insurance Roadmap:** Visual timeline of recommended coverage based on life stages.
*   **Progress Tracker:** Track your application status step-by-step.

### 4. 🌍 Localization
*   **Language Toggle:** Seamlessly switch the entire UI between English, Hindi, and Marathi.
*   **Voice Support:** Audio feedback for better accessibility.

## 🛠️ Tech Stack

*   **Frontend:** React, Vite, Tailwind-like CSS variables (Vanilla CSS), Lucide React Icons.
*   **Backend:** FastAPI (Python), Uvicorn.
*   **AI/ML:** 
    *   **LLM:** Groq / OpenAI (configurable).
    *   **Embeddings:** HuggingFace / OpenAI.
    *   **TTS:** Microsoft Edge TTS (`edge-tts`).
    *   **RAG:** ChromaDB / FAISS.
*   **Database:** SQLite (for session persistence).
*   **Integration:** Twilio (WhatsApp), ngrok (Tunneling).

## 📂 Project Structure

```
├── app/
│   ├── api/            # FastAPI endpoints (server.py)
│   ├── services/       # Business logic (agent_service.py, voice_service.py)
│   ├── static/         # Generated assets (voice cache, uploads)
│   └── db/             # Database session management
├── frontend/           # React Application
│   ├── src/            # Components, Pages, Assets
│   └── public/         # Static files
├── data/               # Knowledge base documents for RAG
└── main.py             # Streamlit entry point (depreciated in favor of React)
```

## ⚙️ Setup Instructions

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   Git

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/insurance-agent.git
cd insurance-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install edge-tts  # Required for Audio Guide

# Create .env file
cp .env.example .env
# Update .env with your GROQ_API_KEY, TWILIO info, etc.

# Run the API Server
uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run Development Server
npm run dev
# Access at http://localhost:5173
```

## 🤝 Contribution

This project was built for the **Hackathon 2024** to solve the problem of *low insurance penetration in rural India* due to complexity and lack of trust.

## 📜 License
MIT License.
