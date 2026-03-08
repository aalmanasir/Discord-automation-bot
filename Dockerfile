FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application entrypoint to avoid copying unintended local files
COPY bot.py .

CMD ["python", "bot.py"]
