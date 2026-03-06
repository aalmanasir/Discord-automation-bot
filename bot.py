"""Discord automation bot with SHA256 verification commands."""

import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from sha256_helpers import compute_sha256_bytes, compute_sha256_text, verify_sha256

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} (ID: {client.user.id})")


@tree.command(name="sha256", description="Compute the SHA256 hash of the provided text")
@app_commands.describe(text="The text to hash")
async def sha256_command(interaction: discord.Interaction, text: str):
    """Return the SHA256 hex-digest of *text*."""
    digest = compute_sha256_text(text)
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
    digest = compute_sha256_text(text)
    match = verify_sha256(digest, expected_hash)
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
    digest = compute_sha256_bytes(data)

    if expected_hash:
        match = verify_sha256(digest, expected_hash)
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
        await interaction.followup.send(
            f"**SHA256** of `{file.filename}`:\n```\n{digest}\n```",
            ephemeral=True,
        )


def main():
    if not DISCORD_TOKEN:
        raise RuntimeError(
            "DISCORD_TOKEN environment variable is not set. "
            "Copy .env.example to .env and fill in your bot token."
        )
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
