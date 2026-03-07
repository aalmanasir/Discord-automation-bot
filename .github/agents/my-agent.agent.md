---
name: My Custom Agent
description: A full OpenClaw-compatible custom agent for a Discord bot.
---

# OpenClaw System Roles

## Command Handler
Handles commands via `CommandTree` and `app_commands`.

## Event Listener
Listens to Discord events and responds accordingly.

# Autonomous Loop

- Interval: 5s
- On tick: `check_for_commands`

## Ephemeral Response Default
- Default responses should be ephemeral to protect user privacy unless specified otherwise.

## Attachment Defer + Follow-up Pattern
- Use the defer method to acknowledge commands and then follow up with the actual response containing attachments.

## DISCORD_TOKEN Env Var Usage
- Store the `DISCORD_TOKEN` in environment variables and access it securely within your application.

## SHA256 Expected Hash Normalization
- Always normalize using `strip().lower()` for consistent hash checks.

## Testing Requirements (pytest)
- All functionality must be covered with tests using `pytest`. Aim for 100% coverage where feasible.

## Documentation/Security Rules
- Maintain comprehensive documentation of all functionalities. Follow standard security practices, including input validation and handling sensitive data securely.