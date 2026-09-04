import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# Logging စနစ် ဖွင့်ခြင်း
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# API Keys များကို Environment Variables မှ ယူမည်
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq Client ချိတ်ဆက်ခြင်း
groq_client = Groq(api_key=GROQ_API_KEY)

# /start Command ကို Handle လုပ်ခြင်း (ပုံနှင့် စာပို့ရန်)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = "https://images.unsplash.com/photo-1534528741775-53994a69daeb" # လိုချင်သော ပုံလင့်ခ်ပြောင်းနိုင်သည်
    caption_text = "ဆွေရေများကြီးချစ်တယ်နော် 💕"
    
    try:
        await update.message.reply_photo(photo=photo_url, caption=caption_text)
    except Exception:
        # ပုံလင့်ခ် အလုပ်မလုပ်ပါက စာသားသက်သက် ပို့မည်
        await update.message.reply_text(caption_text)

# စာပို့လာပါက Groq AI ဖြင့် ပြန်ဖြေခြင်း
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Khido's Oracle, a loving, sweet, and caring AI companion to 'Swe'."
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        bot_reply = chat_completion.choices[0].message.content
        await update.message.reply_text(bot_reply)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("တောင်းပန်ပါတယ်၊ ခေတ္တ အဆင်မပြေဖြစ်နေလို့ ခဏနေမှ ထပ်ကြိုးစားပေးပါနော်။")

def main():
    if not TELEGRAM_TOKEN or not GROQ_API_KEY:
        print("Error: TELEGRAM_TOKEN or GROQ_API_KEY is missing!")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Handlers များ ချိတ်ဆက်ခြင်း
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Bot စတင် Run ခြင်း
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()    
    try:
        # Groq API သို့ ပို့၍ အဖြေထုတ်ခြင်း (mixtral သို့မဟုတ် llama မော်ဒယ်ကို သုံးနိုင်သည်)
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Khido's Oracle, a loving, sweet, and caring AI companion to 'Swe'."
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        bot_reply = chat_completion.choices[0].message.content
        await update.message.reply_text(bot_reply, reply_markup=markup)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("တောင်းပန်ပါတယ်၊ ခေတ္တ အဆင်မပြေဖြစ်နေလို့ ခဏနေမှ ထပ်ကြိုးစားပေးပါနော်။", reply_markup=markup)

def main():
    if not TELEGRAM_TOKEN or not GROQ_API_KEY:
        print("Error: TELEGRAM_TOKEN or GROQ_API_KEY is missing!")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Handlers များ ချိတ်ဆက်ခြင်း
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Bot စတင် Run ခြင်း
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
