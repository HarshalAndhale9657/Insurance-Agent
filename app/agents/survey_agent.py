from typing import Dict, Any
from app.db.session_db import get_session, update_session

SURVEY_STEPS = [
    "welcome",
    "ask_name",
    "ask_age",
    "ask_insurance_type",
    "completed"
]

def process_survey(user_id: str, message_text: str) -> str:
    """
    Processes the user's message and advances the survey state.
    Returns the response text to send back.
    """
    # Load session from DB
    session = get_session(user_id)
    current_step = session["step"]
    session_data = session["data"]
    
    response_text = None
    next_step = current_step

    # --- Logic ---
    if current_step == "welcome":
        next_step = "ask_name"
        response_text = "👋 Welcome to the Insurance Agent Bot! I can help you with queries or take a quick survey. \n\nLet's start. What is your full name?"

    elif current_step == "ask_name":
        session_data["name"] = message_text
        next_step = "ask_age"
        response_text = f"Nice to meet you, {message_text}! \n\nHow old are you?"

    elif current_step == "ask_age":
        if not message_text.isdigit():
            response_text = "Please enter a valid number for your age (e.g., 30)."
            # Stay on current step
            next_step = "ask_age" 
        else:
            session_data["age"] = message_text
            next_step = "ask_insurance_type"
            response_text = "Got it. What type of insurance are you looking for? (e.g., Health, Car, Home)"

    elif current_step == "ask_insurance_type":
        session_data["insurance_type"] = message_text
        next_step = "completed"
        response_text = f"Thank you! We have recorded your request for {message_text} insurance.\n\nYou can now ask me any questions about our policies!"

    elif current_step == "completed":
        # If survey is done, we assume the caller will handle routing to RAG, 
        # but if they explicitly ask to restart:
        if "reset" in message_text.lower():
            next_step = "welcome"
            response_text = "Survey reset. What is your name?"
        else:
             return None # Return None to indicate we should fall back to RAG/Query Agent

    if response_text is None and next_step != current_step:
         # Fallback error handling if logic flaw
         return "Sorry, something went wrong. Type 'reset' to start over."

    # Save changes to DB
    update_session(user_id, next_step, session_data)
    
    return response_text
