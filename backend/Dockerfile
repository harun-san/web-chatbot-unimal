FROM python:3.9-slim

WORKDIR /app

# Salin requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin sisa file aplikasi
COPY . .

# Buat user non-root (Standar keamanan Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app
COPY --chown=user . $HOME/app

# Hugging Face mengekspos port 7860 secara default
EXPOSE 7860

# Jalankan Uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]