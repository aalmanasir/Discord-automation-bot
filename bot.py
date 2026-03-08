"""Discord automation bot with SHA256 verification commands."""

import logging

import discord
from discord import app_commands

from backend.config.settings import get_discord_token
from backend.services.sha256_service import (
    hash_bytes,
    hash_text,
    verify_bytes_hash,
    verify_text_hash,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
command_tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await command_tree.sync()
    logger.info("Logged in as %s (ID: %s)", client.user, client.user.id)


@command_tree.command(name="sha256", description="Compute the SHA256 hash of the provided text")
@app_commands.describe(text="The text to hash")
async def sha256_command(interaction: discord.Interaction, text: str):
    """Return the SHA256 hex-digest of *text*."""
    digest = hash_text(text)
    await interaction.response.send_message(
        f"**SHA256** of your text:\n```\n{digest}\n```",
        ephemeral=True,
    )


@command_tree.command(
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
        normalized_expected = expected_hash.strip().lower()
        await interaction.response.send_message(
            f"❌ **Mismatch!**\nComputed: `{digest}`\nExpected: `{normalized_expected}`",
            ephemeral=True,
        )


@command_tree.command(
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
    file_bytes = await file.read()

    if expected_hash:
        digest, match = verify_bytes_hash(file_bytes, expected_hash)
        if match:
            await interaction.followup.send(
                f"✅ **Match!** SHA256 of `{file.filename}` matches the expected hash.\n```\n{digest}\n```",
                ephemeral=True,
            )
        else:
            normalized_expected = expected_hash.strip().lower()
            await interaction.followup.send(
                f"❌ **Mismatch!** SHA256 of `{file.filename}`:\nComputed: `{digest}`\nExpected: `{normalized_expected}`",
                ephemeral=True,
            )
    else:
        digest = hash_bytes(file_bytes)
        await interaction.followup.send(
            f"**SHA256** of `{file.filename}`:\n```\n{digest}\n```",
            ephemeral=True,
        )


def main():
    discord_bot_token = get_discord_token()
    logger.info("Starting Discord bot…")
    client.run(discord_bot_token)


if __name__ == "__main__":
    main()
