#!/usr/bin/env bash
<<<<<<< HEAD
# Local development launcher for the Discord automation bot.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

if [[ ! -f .env ]]; then
=======
# Run the Discord bot locally.
# Requires a .env file with DISCORD_TOKEN set.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

if [ ! -f "$REPO_ROOT/.env" ]; then
>>>>>>> origin/main
  echo "ERROR: .env file not found. Copy .env.example to .env and set DISCORD_TOKEN." >&2
  exit 1
fi

<<<<<<< HEAD
exec python bot.py
=======
cd "$REPO_ROOT"
python bot.py
>>>>>>> origin/main
