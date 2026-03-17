#!/usr/bin/env python3
"""
Unified Bot - Receives from both bots
"""
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Both bots
PERSONAL_BOT_TOKEN = "8677779317:AAEaxRQmEpymFeer0sVPXe1YNMUqcURZACg"
COMPANY_BOT_TOKEN = "8689117372:AAHWWbJqpIazdy1TxCOxFbJs1YrofmAGfVw"

# Keywords for auto-routing
COMPANY_KEYWORDS = ["company", "business", "leads", "sales", "build", "research", 
                    "client", "project", "service", "automation", "money", "job", 
                    "upwork", "fiverr", "freelance"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! Send me anything - I'll route it correctly!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Determine routing
    if any(kw in text.lower() for kw in COMPANY_KEYWORDS):
        bot = "company"
        response = f"🏢 [Company] Got: {text}"
    else:
        bot = "personal"  
        response = f"🏠 [Personal] Got: {text}"
    
    await update.message.reply_text(response)

# Run both bots
def run_personal():
    app = Application.builder().token(PERSONAL_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("👤 Personal Bot running...")
    app.run_polling(drop_pending_updates=True)

def run_company():
    app = Application.builder().token(COMPANY_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🏢 Company Bot running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    import threading
    t1 = threading.Thread(target=run_personal)
    t2 = threading.Thread(target=run_company)
    t1.start()
    t2.start()
