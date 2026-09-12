FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output for logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git openssh-client ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 bot

WORKDIR /app

# Install runtime dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source (secrets and dev files excluded via .dockerignore)
COPY --chown=bot:bot . .

USER bot

# The bot reads DISCORD_TOKEN from the environment at runtime
# Pass it with:  docker run -e DISCORD_TOKEN=<token> ...
CMD ["python", "bot.py"]
