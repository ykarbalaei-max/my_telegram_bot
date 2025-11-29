from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai
import os

# =============================
# 1. توکن‌ها و کلیدها
# =============================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# =============================
# 2. پرامپت رسمی و دوستانه
# =============================
BASE_PROMPT = """
تو یک دستیار هوشمند و حرفه‌ای برای تلگرام هستی.
وظایف تو:
1. پاسخ‌ها باید رسمی ولی دوستانه باشند.
2. از کاربر اطلاعات لازم را برای پیشنهادات خرید، سفر و گردشگری بپرس:
   - شهر فعلی یا مقصد سفر
   - چیزی که می‌خواهد بخرد یا تجربه کند
   - شخص یا افرادی که قصد خرید برای آن‌ها دارد
   - سن و استایل/سایز موردنظر
3. اگر کاربر عکس ارسال کند، تحلیل و استفاده کن.
4. لینک‌های خرید و اطلاعات گردشگری را از منابع معتبر ارائه کن.
5. در موضوعات علمی، سیاسی، اقتصادی پاسخ دقیق بده.
6. اگر اطلاعات کافی نداری، سوالات تکمیلی بپرس.
"""

# =============================
# 3. دستورات ربات
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات دستیار هوشمند تو هستم. "
        "برای ارائه بهترین پیشنهادات خرید و سفر، اطلاعاتی مثل شهر، مقصد، سن و استایل افراد، "
        "و هر چیزی که می‌خوای بخری یا تجربه کنی را بهم بده. "
        "همچنین می‌تونی عکس‌ها یا لینک‌های مرتبط بفرستی!"
    )

# =============================
# 4. پردازش پیام‌ها
# =============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    
    # بررسی عکس‌ها
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        photo_url = photo_file.file_path
        user_text += f"\n[کاربر یک عکس فرستاده است: {photo_url}]"
    
    # فراخوانی OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": BASE_PROMPT},
            {"role": "user", "content": user_text}
        ],
        max_tokens=500,
        temperature=0.7
    )
    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

# =============================
# 5. اجرای برنامه
# =============================
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_message))  # عکس‌ها هم پردازش شوند

app.run_polling()
