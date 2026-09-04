import os
import logging
from telegram import Update, ReplyKeyboardMarkup
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

# ပုံသေ ရွေးချယ်စရာ ၅ ခု (Keyboard Buttons)
REPLY_OPTIONS = [
    ["ချာတိတ်ကို ရူးရူးမူးမူးချစ်နေတာ ဘယ်သူလဲသိလား"],
    ["ဒီနေ့ ဘာတွေလုပ်စရာရှိလဲ ပြောပြပေးဦး"],
    ["မင်းရဲ့ စိတ်ခံစားချက်က ဘယ်လိုရှိလဲ"],
    ["ငါ့ကို ချစ်စရာစကားလေး တစ်ခွန်းလောက်ဆိုပြပါ"],
    ["နောက်ပြောင်စရာ ဟာသလေးတစ်ခု ပြောပြပါ"]
]
markup = ReplyKeyboardMarkup(REPLY_OPTIONS, resize_keyboard=True)

# /start Command ကို Handle လုပ်ခြင်း
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "ဆွေရေချစ်တယ် 💕\n\nအောက်ပါ ရွေးချယ်စရာများထဲမှ ကြိုက်နှစ်သက်ရာကို နှိပ်ပြီး စကားပြောနိုင်ပါတယ် - "
    await update.message.reply_text(welcome_text, reply_markup=markup)

# စာာပို့လာပါက Groq AI ဖြင့် ပြန်ဖြေခြင်း
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
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
