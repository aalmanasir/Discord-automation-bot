# Discord-automation-bot

A production-grade Discord bot with SHA256 verification commands.

## Features

| Command | Description |
|---|---|
| `/sha256 <text>` | Compute the SHA256 hash of any text |
| `/sha256_verify <text> <expected_hash>` | Verify that the SHA256 hash of text matches an expected value |
| `/sha256_file <file> [expected_hash]` | Compute (or verify) the SHA256 hash of an uploaded file |

All responses are ephemeral (only visible to the invoking user).

## Project structure

```
Discord-automation-bot/
├── bot.py                  # Entry-point — starts the Discord client
├── sha256_helpers.py       # Backward-compatible re-export shim
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Dockerfile
│
├── backend/
│   ├── config/
│   │   └── settings.py     # Environment-variable configuration
│   ├── utils/
│   │   └── sha256_helpers.py  # Core SHA256 primitives
│   └── services/
│       └── sha256_service.py  # Business-logic service layer
│
├── scripts/
│   └── run_bot.sh          # Local dev launcher
│
└── tests/
    ├── test_sha256.py             # Unit tests for sha256 utilities
    └── test_sha256_service.py     # Unit tests for the service layer
```

## Setup

### Prerequisites

- Python 3.12+
- A Discord application and bot token ([Discord Developer Portal](https://discord.com/developers/applications))

### Installation

```bash
# Clone the repository
git clone https://github.com/aalmanasir/Discord-automation-bot.git
cd Discord-automation-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set DISCORD_TOKEN to your bot token

# Run the bot
python bot.py
# — or use the helper script —
bash scripts/run_bot.sh
```

### Docker

```bash
# Build the image
docker build -t discord-automation-bot .

# Run the container
docker run --env-file .env discord-automation-bot
```

### Required bot permissions

- `applications.commands` (for slash commands)
- `bot` scope with **Send Messages** permission

## Running tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## Environment variables

| Variable | Description |
|---|---|
| `DISCORD_TOKEN` | Your Discord bot token (required) |