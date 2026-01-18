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

def process_survey(user_id: str, message_text: str, current_session: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Processes the user's message and calculates the next survey state.
    Returns: { "response": str, "next_step": str, "data": dict }
    Does NOT update the DB directly.
    """
    # Use passed session or load (fallback)
    if current_session:
        session = current_session
    else:
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
        return {"response": response_text, "next_step": next_step, "data": session_data}

    # --- Logic ---
    if current_step == "welcome":
        next_step = "ask_name"
        response_text = (
            "🙏 *Namaste! I am 'Suraksha Sahayak', your personal Insurance Advisor.*\n\n"
            "My goal is to find the perfect safety net for you and your family.\n\n"
            "To get started, may I please know your **full name**?"
        )

    elif current_step == "ask_name":
        session_data["name"] = message_text
        next_step = "ask_age"
        response_text = f"It is a pleasure to meet you, *{message_text}*. 🤝\n\nTo recommend the best plan for your life stage, could you please share your **Age**? (e.g., 35)"

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
                "✅ Got it.\n\n"
                "Your occupation helps us understand your risks. What is your **main source of income**?\n"
                "_(e.g., Farming, Small Business, Daily Wage, Service)_"
            )

    elif current_step == "ask_occupation":
        session_data["occupation"] = message_text
        next_step = "ask_family"
        response_text = "That is hard work! 💪\n\nNow, who do we need to protect? How many **family members** depend on you?"

    elif current_step == "ask_family":
        session_data["family"] = message_text
        next_step = "ask_worry"
        response_text = (
            "Understood.\n\n"
            "Finally, what keeps you up at night? What is your **biggest financial worry**?\n"
            "_(e.g., Bad harvest, Hospital costs, Children's education, Accidents)_"
        )

    elif current_step == "ask_worry":
        session_data["worry"] = message_text
        next_step = "completed"
        
        # unique profile string
        profile_str = f"Name: {session_data.get('name')}, Age: {session_data.get('age')}, Job: {session_data.get('occupation')}, Family: {session_data.get('family')}, Main Worry: {message_text}"
        
        response_text = "🙏 Thank you for sharing. Give me a moment to analyze the best protection plan for your specific situation..."
        
        # Generate Recommendation immediately
        try:
           recommendation = recommend_products(profile_str)
           session_data["recommendation"] = recommendation # SAVE TO DB
           response_text = (
               f"💡 **My Expert Recommendation**:\n\n"
               f"{recommendation}\n\n"
               "-----------------------------\n"
               "Feel free to ask me questions like *'How do I claim?'* or *'What is the premium?'*"
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
         return {"response": "🙏 Apologies, something went wrong. Type 'reset' to start over.", "next_step": current_step, "data": session_data}

    return {"response": response_text, "next_step": next_step, "data": session_data}
