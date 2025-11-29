FROM python:3.11-slim

# نصب build-essential و pip upgrade
RUN apt-get update && apt-get install -y build-essential && \
    python3 -m pip install --upgrade pip

WORKDIR /app

# کپی dependencies و نصب
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی فایل اصلی
COPY main.py .

# دستور اجرا
CMD ["python3", "main.py"]
