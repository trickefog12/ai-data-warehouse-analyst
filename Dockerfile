# Χρησιμοποιούμε μια ελαφριά έκδοση Python
FROM python:3.11-slim

# Ρυθμίσεις για να μην δημιουργεί ο Streamlit cache και να βλέπουμε τα logs αμέσως
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Εγκατάσταση ΜΟΝΟ των απολύτως απαραίτητων
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Αντιγραφή των requirements και εγκατάσταση
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Αντιγραφή όλου του φακέλου
COPY . .

# Το Streamlit τρέχει στην 8501
EXPOSE 8501

# Εντολή εκτέλεσης
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]