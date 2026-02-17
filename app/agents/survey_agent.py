from typing import Dict, Any
from app.db.session_db import get_session, update_session

from app.services.query_service import recommend_products
from app.services.pdf_service import PdfService

SURVEY_STEPS = [
    "welcome",
    "ask_name",
    "ask_gender",
    "ask_age",
    "ask_occupation",
    "ask_family",
    "ask_worry",
    "completed"
]

def get_step_prompt(step: str) -> str:
    """Returns the question prompt for a given step."""
    if step == "ask_name":
        return "To begin, may I please know your **full name**?"
    elif step == "ask_gender":
        return "To better understand your profile, may I know your **Gender**? (e.g., Male, Female, Other)"
    elif step == "ask_age":
        return "Could you please share your **Age**? (e.g., 35)"
    elif step == "ask_occupation":
        return "What is your **main source of income**? (e.g., Farming, Small Business, Daily Wage, Service)"
    elif step == "ask_family":
        return "How many **family members** depend on you?"
    elif step == "ask_worry":
        return "What is your **biggest financial worry**? (e.g., Bad harvest, Hospital costs, Children's education)"
    elif step == "welcome":
        return "Namaste! I am 'Suraksha Sahayak'. How can I help you today?"
    return "How can I assist you?"

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
        next_step = "ask_gender"
        response_text = f"It is a pleasure to meet you, *{message_text}*. 🤝\n\nTo better understand your profile, may I know your **Gender**? (e.g., Male, Female, Other)"

    elif current_step == "ask_gender":
        session_data["gender"] = message_text
        next_step = "ask_age"
        response_text = "Thank you. \n\nTo recommend the best plan for your life stage, could you please share your **Age**? (e.g., 35)"

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
           # Generate PDF Report
           try:
               pdf_service = PdfService()
               pdf_filename = pdf_service.generate_report(session_data, recommendation)
               # Assuming static files are served at /static/
               pdf_link = f"http://localhost:8000/static/{pdf_filename}"
               
               response_text = (
                   f"💡 **My Expert Recommendation**:\n\n"
                   f"{recommendation}\n\n"
                   f"📄 **Download Your Personalized Report:**\n[Click here to download PDF]({pdf_link})\n\n"
                   "-----------------------------\n"
                   "Feel free to ask me questions like *'How do I claim?'* or *'What is the premium?'*"
               )
           except Exception as pdf_error:
               import traceback
               print(f"❌ PDF Generation Error: {pdf_error}")
               traceback.print_exc()
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
