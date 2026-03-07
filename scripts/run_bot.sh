#!/usr/bin/env bash
# Local development launcher for the Discord automation bot.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

if [[ ! -f .env ]]; then
  echo "ERROR: .env file not found. Copy .env.example to .env and set DISCORD_TOKEN." >&2
  exit 1
fi

exec python bot.py
