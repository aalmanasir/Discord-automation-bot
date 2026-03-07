# Use a slim Python image to minimize image size
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output for logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY bot.py sha256_helpers.py ./

# The bot reads DISCORD_TOKEN from the environment at runtime
# Pass it with:  docker run -e DISCORD_TOKEN=<token> ...
CMD ["python", "bot.py"]
