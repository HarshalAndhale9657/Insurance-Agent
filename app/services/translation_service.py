from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def get_translator_llm():
    api_key = os.getenv("GROQ_API_KEY")
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile", # Reliable model
        temperature=0.1
    )

def detect_language(text: str) -> str:
    """
    Detects if the text is English or an Indian language.
    Returns: 'en', 'hi', 'mr', 'ta', etc.
    """
    llm = get_translator_llm()
    prompt = ChatPromptTemplate.from_template(
        "Detect the language of this text. Return ONLY the 2-letter ISO code (e.g., en, hi, mr, ta). "
        "If it is mixed (Hinglish), return the dominant Indian language code. "
        "Text: {text}"
    )
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return result.content.strip().lower()

def translate_to_english(text: str, source_lang: str) -> str:
    """
    Translates Indian language text to English.
    """
    if source_lang == "en":
        return text
        
    llm = get_translator_llm()
    prompt = ChatPromptTemplate.from_template(
        "Translate the following {source_lang} text to English. "
        "Keep the meaning exact but simple. "
        "Text: {text}"
    )
    chain = prompt | llm
    result = chain.invoke({"source_lang": source_lang, "text": text})
    return result.content.strip()

def translate_to_user_lang(text: str, target_lang: str) -> str:
    """
    Translates English response back to user's language.
    Preserves WhatsApp formatting like *bold* and emojis.
    """
    if target_lang == "en":
        return text

    llm = get_translator_llm()
    prompt = ChatPromptTemplate.from_template(
        "Translate this English text to {target_lang}. "
        "IMPORTANT rules:\n"
        "1. PRESERVE all formatting like *bold* stars and emojis.\n"
        "2. Keep the tone professional, polite, and empathetic (use 'ji' or equivalent honorifics).\n"
        "3. Do not translate technical terms like 'Premium' completely if they are commonly used, but you can transliterate them.\n"
        "Text: {text}"
    )
    chain = prompt | llm
    result = chain.invoke({"target_lang": target_lang, "text": text})
    return result.content.strip()
