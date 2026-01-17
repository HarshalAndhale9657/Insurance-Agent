import os
import asyncio
import tempfile
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Services
from app.services.voice_service import transcribe_audio
from app.services.query_service import query_agent
from app.agents.survey_agent import process_survey, get_session
from app.db.session_db import init_db

load_dotenv()

# Configure Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Downloads voice note, transcribes it, and returns text.
    """
    try:
        file_id = update.message.voice.file_id
        new_file = await context.bot.get_file(file_id)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as tmp_file:
            await new_file.download_to_drive(tmp_file.name)
            tmp_path = tmp_file.name

        # Transcribe
        text = transcribe_audio(tmp_path)
        os.remove(tmp_path)
        return text
    except Exception as e:
        logging.error(f"Error handling voice: {e}")
        return None

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main handler for text and voice messages.
    """
    user_id = str(update.effective_user.id)
    user_text = ""

    # 1. Get Text (Direct or Transcribed)
    if update.message.voice:
        await update.message.reply_text("🎙️ I heard you! Transcribing...")
        user_text = await handle_voice(update, context)
        if not user_text:
            await update.message.reply_text("Sorry, I couldn't understand the audio.")
            return
        await update.message.reply_text(f"📝 You said: \"{user_text}\"")
    elif update.message.text:
        user_text = update.message.text
    else:
        return

    # 2. Check Survey State
    session = get_session(user_id)
    if session["step"] != "completed":
        response = process_survey(user_id, user_text)
        if response:
            await update.message.reply_text(response)
            return

    # 3. Fallback to RAG / Reset
    if "survey" in user_text.lower() or "reset" in user_text.lower():
         # Trigger reset via process_survey logic hack or direct force
         # Here we just pass "reset" to process_survey if it was completed
         response = process_survey(user_id, "reset")
         await update.message.reply_text(response)
         return

    # 4. RAG Query
    await update.message.reply_text("🤔 Thinking...")
    try:
        rag_response = query_agent(user_text)
        await update.message.reply_text(rag_response)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == '__main__':
    # Init DB
    init_db()
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env")
        exit(1)

    print("🤖 Telegram Bot Starting...")
    application = ApplicationBuilder().token(token).build()
    
    # Handle Text and Voice
    application.add_handler(MessageHandler(filters.TEXT | filters.VOICE, message_handler))
    
    application.run_polling()
