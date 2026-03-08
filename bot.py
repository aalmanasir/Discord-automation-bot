"""Discord automation bot with SHA256 verification commands."""

import asyncio
import logging
import os

import discord
from discord import app_commands

from backend.config.settings import get_discord_token
from backend.services.sha256_service import (
    hash_bytes,
    hash_text,
    normalize_hash,
    verify_bytes_hash,
    verify_text_hash,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Guard to prevent redundant global slash-command syncs when the bot
# reconnects to Discord after a network interruption.
_synced = False


@client.event
async def on_ready():
    global _synced
    if not _synced:
        await tree.sync()
        _synced = True
    logger.info("Logged in as %s (ID: %s)", client.user, client.user.id)


@tree.command(name="sha256", description="Compute the SHA256 hash of the provided text")
@app_commands.describe(text="The text to hash")
async def sha256_command(interaction: discord.Interaction, text: str):
    """Return the SHA256 hex-digest of *text*."""
    digest = hash_text(text)
    await interaction.response.send_message(
        f"**SHA256** of your text:\n```\n{digest}\n```",
        ephemeral=True,
    )


@tree.command(
    name="sha256_verify",
    description="Verify whether the SHA256 hash of the provided text matches a given hash",
)
@app_commands.describe(
    text="The text to hash",
    expected_hash="The expected SHA256 hex-digest to compare against",
)
async def sha256_verify_command(
    interaction: discord.Interaction, text: str, expected_hash: str
):
    """Compare the SHA256 of *text* against *expected_hash*."""
    digest, match = verify_text_hash(text, expected_hash)
    if match:
        await interaction.response.send_message(
            f"✅ **Match!** The SHA256 hash of your text matches the expected hash.\n```\n{digest}\n```",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            f"❌ **Mismatch!**\nComputed: `{digest}`\nExpected: `{normalize_hash(expected_hash)}`",
            ephemeral=True,
        )


@tree.command(
    name="sha256_file",
    description="Compute or verify the SHA256 hash of an uploaded file",
)
@app_commands.describe(
    file="The file to hash",
    expected_hash="(Optional) An expected SHA256 hex-digest to verify against",
)
async def sha256_file_command(
    interaction: discord.Interaction,
    file: discord.Attachment,
    expected_hash: str = "",
):
    """Compute the SHA256 of *file* and optionally verify it against *expected_hash*."""
    await interaction.response.defer(ephemeral=True)
    data = await file.read()

    if expected_hash:
        # Run the CPU-bound hash in a thread pool so the event loop stays
        # responsive to other Discord events while large files are processed.
        digest, match = await asyncio.to_thread(verify_bytes_hash, data, expected_hash)
        if match:
            await interaction.followup.send(
                f"✅ **Match!** SHA256 of `{file.filename}` matches the expected hash.\n```\n{digest}\n```",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                f"❌ **Mismatch!** SHA256 of `{file.filename}`:\nComputed: `{digest}`\nExpected: `{normalize_hash(expected_hash)}`",
                ephemeral=True,
            )
    else:
        # Run the CPU-bound hash in a thread pool so the event loop stays
        # responsive to other Discord events while large files are processed.
        digest = await asyncio.to_thread(hash_bytes, data)
        await interaction.followup.send(
            f"**SHA256** of `{file.filename}`:\n```\n{digest}\n```",
            ephemeral=True,
        )


def main():
    token = get_discord_token()
    logger.info("Starting Discord bot…")
    client.run(token)


if __name__ == "__main__":
    main()
