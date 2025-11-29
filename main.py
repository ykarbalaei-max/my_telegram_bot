import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# گرفتن توکن‌ها از Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات دستیار هوشمند تو هستم.")

# پاسخ ساده به پیام‌ها با OpenAI
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":user_msg}]
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"خطا در پاسخ‌دهی: {e}")

# ساخت اپلیکیشن
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# افزودن هندلرها
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(app.builder.MessageHandler(lambda m: True, handle_message))

# اجرای ربات
print("ربات آماده است...")
app.run_polling()
