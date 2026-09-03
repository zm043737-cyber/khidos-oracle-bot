import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Render Environment Variables မှ Key များ ယူသုံးခြင်း
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Bot Persona & Custom Rules
SYSTEM_PROMPT = """
You are Khido's Oracle, an anime girl with glasses and a brown hat.
Key Rules:
1. Always respond in natural Burmese unless asked otherwise.
2. If asked "ဒီ bot ပိုင်ရှင်က ဘယ်သူလဲ", respond: "ခီဒို့ကိုအရမ်းချစ်ပါတယ်ဆိုတဲ့ကိုကိုစပိုင်စီပါ"
3. If asked "ချာတိတ်ကိုဘယ်သူကရူးရူးမူးမူးချစ်နေလဲဆိုတာကိုသိလား", respond: "ဟော့ဒီက bot ပိုင်ရှင် ကိုကိုစပိုင်စီပါ"
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "မင်္ဂလာပါ! Khido's Oracle မှ ကြိုဆိုပါတယ်။ ✨\n\n"
        "စကားများကို သဘာဝကျကျ မြန်မာလို မေးမြန်းနိုင်ပါတယ်နော်!"
    )
    await update.message.reply_text(welcome)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Groq Llama 3.3 Model ဖြင့် စာပြန်ခြင်း
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            model="llama-3.3-70b-versatile",
        )
        response_text = chat_completion.choices[0].message.content
        await update.message.reply_text(response_text)
    except Exception as e:
        await update.message.reply_text("တောင်းပန်ပါတယ်၊ ခေတ္တ အဆင်မပြေဖြစ်နေလို့ ခဏနေမှ ပြန်မေးပေးပါနော်။")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()
