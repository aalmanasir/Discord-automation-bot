"""Application configuration loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_discord_token() -> str:
    """Return the Discord bot token from the environment.

    Raises:
        RuntimeError: If DISCORD_TOKEN is not set.
    """
    discord_bot_token = os.getenv("DISCORD_TOKEN", "")
    if not discord_bot_token:
        raise RuntimeError(
            "DISCORD_TOKEN environment variable is not set. "
            "Copy .env.example to .env and fill in your bot token."
        )
    return discord_bot_token
