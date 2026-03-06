# Discord-automation-bot

A Discord bot with SHA256 verification commands.

## Features

| Command | Description |
|---|---|
| `/sha256 <text>` | Compute the SHA256 hash of any text |
| `/sha256_verify <text> <expected_hash>` | Verify that the SHA256 hash of text matches an expected value |
| `/sha256_file <file> [expected_hash]` | Compute (or verify) the SHA256 hash of an uploaded file |

All responses are ephemeral (only visible to the invoking user).

## Setup

### Prerequisites

- Python 3.10+
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