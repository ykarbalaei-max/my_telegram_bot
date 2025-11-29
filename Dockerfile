FROM python:3.11-slim

# نصب build tools و آپدیت pip
RUN apt-get update && \
    apt-get install -y build-essential && \
    python3 -m pip install --upgrade pip

WORKDIR /app

# کپی و نصب dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی فایل اصلی
COPY main.py .

# دستور اجرای ربات
CMD ["python3", "main.py"]
