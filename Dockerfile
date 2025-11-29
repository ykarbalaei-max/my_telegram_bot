# استفاده از Python سبک و پایدار
FROM python:3.11-slim

# فولدر کاری داخل کانتینر
WORKDIR /app

# کپی فایل‌های پروژه
COPY requirements.txt .
COPY main.py .

# نصب کتابخانه‌ها
RUN pip install --no-cache-dir -r requirements.txt

# دستور اجرای ربات
CMD ["python3", "main.py"]
