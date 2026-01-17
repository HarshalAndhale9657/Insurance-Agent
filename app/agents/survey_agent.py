from typing import Dict, Any
from app.db.session_db import get_session, update_session

from app.services.query_service import recommend_products

SURVEY_STEPS = [
    "welcome",
    "ask_name",
    "ask_age",
    "ask_occupation",
    "ask_family",
    "ask_worry",
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
    
    # --- Global Reset Handler ---
    if "reset" in message_text.lower():
        # Reset to welcome state
        session_data = {} # Clear data
        next_step = "welcome"
        response_text = "🔄 *Survey Reset*\n\nNamaste! Let's start over. \n\nTo begin, may I know your **full name**?"
        update_session(user_id, next_step, session_data)
        return response_text

    # --- Logic ---
    if current_step == "welcome":
        next_step = "ask_name"
        response_text = (
            "🙏 *Namaste! Welcome to your Rural Insurance Assistant.*\n\n"
            "I am here to help you secure the future of your family with the right insurance.\n\n"
            "To better assist you, I need to ask a few simple questions.\n\n"
            "🔹 First, could you please tell me your **Name**?"
        )

    elif current_step == "ask_name":
        session_data["name"] = message_text
        next_step = "ask_age"
        response_text = f"Thank you, *{message_text} ji*. \n\n🔹 Could you please tell me your **Age**? (e.g., 30)"

    elif current_step == "ask_age":
        # Extract number from text (simple robust method for "I am 45" etc)
        import re
        age_match = re.search(r'\d+', message_text)
        
        if not age_match:
            response_text = "🙏 Apologies, I did not catch that.\n\nPlease reply with just the **number** of your age. \n\n*Example:* 45"
            next_step = "ask_age" 
        else:
            session_data["age"] = age_match.group()
            next_step = "ask_occupation"
            response_text = (
                "✅ Noted.\n\n"
                "🔹 What is your **main occupation**?\n"
                "_(e.g., Farmer, Shopkeeper, Teacher, Driver)_"
            )

    elif current_step == "ask_occupation":
        session_data["occupation"] = message_text
        next_step = "ask_family"
        response_text = "🔹 Do you have a family? How many **members** cover your household?"

    elif current_step == "ask_family":
        session_data["family"] = message_text
        next_step = "ask_worry"
        response_text = (
            "🔹 One last question:\n\n"
            "What is your **biggest financial worry** right now?\n"
            "_(e.g., Crop failure, Medical bills for parents, Accident, Daughter's marriage)_"
        )

    elif current_step == "ask_worry":
        session_data["worry"] = message_text
        next_step = "completed"
        
        # unique profile string
        profile_str = f"Name: {session_data.get('name')}, Age: {session_data.get('age')}, Job: {session_data.get('occupation')}, Family: {session_data.get('family')}, Main Worry: {message_text}"
        
        response_text = "🙏 Thank you. I am analyzing the best insurance plan for you... please wait a moment."
        
        # Generate Recommendation immediately
        try:
           recommendation = recommend_products(profile_str)
           session_data["recommendation"] = recommendation # SAVE TO DB
           response_text = (
               f"✅ **My Recommendation for You**:\n\n"
               f"{recommendation}\n\n"
               "-----------------------------\n"
               "Type 'reset' to start over, or simply **ask me any question** about this policy!"
           )
        except Exception as e:
           response_text = "🙏 Thank you. Our experts will review your profile and get back to you shortly."

    elif current_step == "completed":
        if "reset" in message_text.lower():
            next_step = "welcome"
            response_text = "🔄 Survey reset. What is your name?"
        else:
             return None # Return None to indicate we should fall back to RAG/Query Agent

    if response_text is None and next_step != current_step:
         return "🙏 Apologies, something went wrong. Type 'reset' to start over."

    # Save changes to DB
    update_session(user_id, next_step, session_data)
    
    return response_text
