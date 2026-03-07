#!/usr/bin/env bash
# Run the Discord bot locally.
# Requires a .env file with DISCORD_TOKEN set.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

if [ ! -f "$REPO_ROOT/.env" ]; then
  echo "ERROR: .env file not found. Copy .env.example to .env and set DISCORD_TOKEN." >&2
  exit 1
fi

cd "$REPO_ROOT"
python bot.py
