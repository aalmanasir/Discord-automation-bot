# GitHub Copilot Instructions

## Project overview

This is a Discord bot written in Python that provides SHA256 hashing and verification
commands as Discord slash commands. All responses are ephemeral (only visible to the
invoking user).

### Slash commands

| Command | Description |
|---|---|
| `/sha256 <text>` | Compute the SHA256 hash of any text |
| `/sha256_verify <text> <expected_hash>` | Verify that the SHA256 hash of text matches an expected value |
| `/sha256_file <file> [expected_hash]` | Compute (or verify) the SHA256 hash of an uploaded file |

## Architecture

```
bot.py              – Discord client setup, slash-command handlers, and entry point
sha256_helpers.py   – Pure-Python SHA256 utilities (no Discord dependency)
tests/
  test_sha256.py    – unittest tests for sha256_helpers
requirements.txt    – Runtime dependencies (discord.py, python-dotenv)
requirements-dev.txt – Dev/test dependencies (pytest)
.env.example        – Template for the required DISCORD_TOKEN environment variable
```

Keep Discord-specific logic in `bot.py` and pure hashing logic in `sha256_helpers.py`
so the helpers remain independently testable without a Discord connection.

## Coding conventions

- **Python version**: 3.10+
- **Style**: Follow PEP 8; use type hints where practical.
- **Docstrings**: One-line summary docstrings on every public function and class,
  matching the style already used in `bot.py` and `sha256_helpers.py`.
- **Imports**: Standard library → third-party → local, each group separated by a
  blank line.
- **Secrets**: Never hard-code credentials. Load them exclusively from environment
  variables via `python-dotenv` (see `.env.example`).
- **String formatting**: Use f-strings throughout.

## Testing

Tests live in `tests/test_sha256.py` and use the standard `unittest` module.  Run
them with:

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

- Place new tests in `tests/` following the `TestClassName` / `test_method_name`
  naming convention already used in `test_sha256.py`.
- Test pure-logic helpers (`sha256_helpers.py`) with plain unit tests; mock the
  Discord `Interaction` when testing bot command handlers.
- Every new helper function should have at least one test for a known value, one for
  an edge case (empty input), and one for an error/mismatch case.

## Adding new commands

1. Add any new pure helper functions to `sha256_helpers.py` with docstrings and
   corresponding tests in `tests/test_sha256.py`.
2. Register the slash command in `bot.py` using `@tree.command` and
   `@app_commands.describe` decorators, following the pattern of the existing
   commands.
3. Always `defer` the interaction with `ephemeral=True` for commands that perform
   I/O (e.g. file reads) before doing any async work.
4. All user-facing bot messages must be `ephemeral=True`.

## Environment variables

| Variable | Description |
|---|---|
| `DISCORD_TOKEN` | Discord bot token (required) — obtain from the [Discord Developer Portal](https://discord.com/developers/applications) |
