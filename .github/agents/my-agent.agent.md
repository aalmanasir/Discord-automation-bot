---
name: My Custom Agent
description: A full OpenClaw-compatible custom agent for a Discord bot.

# OpenClaw System Roles
roles:
  - role: command_handler
    description: Handles commands via CommandTree/app_commands.
  - role: event_listener
    description: Listens to Discord events and responds accordingly.

# Autonomous Loop
loop:
  interval: 5s
  on_tick: check_for_commands

# Discord Bot Specific Conventions

## Command Handling
- Uses `CommandTree` and `app_commands` to handle incoming commands.
- Implements ephemeral responses for sensitive data using `interaction.response.send_message` with ephemeral=True.

## File Handling
- Attachments are deferred using `await interaction.response.defer()` and followed up with `await interaction.followup.send()`.

## Environment Variables
- Uses the environment variable `DISCORD_TOKEN` for authorization.

## Data Normalization
- Implements SHA256 normalization for any user inputs.

## Testing
- Utilizes `pytest` for unit testing and ensuring the functionality of the agent.
