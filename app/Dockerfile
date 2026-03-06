FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

# Install Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# IMPORTANT: Path updated to app/ because that's where the file lives in your repo
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# IMPORTANT: Copy the contents of the app folder into the container
COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]