# Discord-automation-bot

A Discord bot with SHA256 verification commands and the OpenClaw git-push command.

## Features

| Command | Description |
|---|---|
| `/sha256 <text>` | Compute the SHA256 hash of any text |
| `/sha256_verify <text> <expected_hash>` | Verify that the SHA256 hash of text matches an expected value |
| `/sha256_file <file> [expected_hash]` | Compute (or verify) the SHA256 hash of an uploaded file |
| `/openclaw [remote] [branch]` | Push the configured repository using SSH / system credential manager |

All responses are ephemeral (only visible to the invoking user).

`/openclaw` is disabled by default. Set `OPENCLAW_ALLOWED_USER_IDS` to the explicit Discord user IDs allowed to push, and configure `OPENCLAW_REMOTE` on the host. Raw Git output and host paths are not returned to Discord.

## OpenClaw

The `/openclaw` command pushes the local repository configured by the
`OPENCLAW_REPO_PATH` environment variable.

* **Uses your local SSH / credential manager** — authentication is handled
  entirely by the host environment (SSH keys, `~/.netrc`, the system
  credential manager, etc.).
* **Pushes directly** — runs `git push` via subprocess; no intermediate layer.
* **Never asks for a PAT in chat** — no token or password parameter exists on
  the command; credentials cannot be leaked through Discord messages.

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `remote` | `origin` | Must match the operator-configured `OPENCLAW_REMOTE` name |
| `branch` | *(current branch)* | Branch ref to push |

## Project structure

```
Discord-automation-bot/
├── bot.py                  # Entry-point — starts the Discord client
├── sha256_helpers.py       # Backward-compatible re-export shim
├── git_helpers.py          # Git push helper for /openclaw
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
| `OPENCLAW_REPO_PATH` | Absolute path to the repository `/openclaw` will push (default: `.`) |

## Production configuration

The container runs as UID 10001 and includes Git and the SSH client. Supply DISCORD_TOKEN through the host secret store or an external env file; never bake it into the image. Hashing commands work without Git credentials. For optional OpenClaw use, mount only the intended repository, set OPENCLAW_REPO_PATH and the operator allowlist, and make its existing Git/SSH configuration accessible to UID 10001. Set trusted SSH host keys explicitly; do not disable host-key checking or mount the entire host home directory.

No production host is assumed by this repository. Deployment requires an owner-selected host and an existing bot token configured there. The CI container smoke test checks imports and dependencies without connecting to Discord.
