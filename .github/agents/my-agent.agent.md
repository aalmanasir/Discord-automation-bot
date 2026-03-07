---
name: My Custom Agent
description: This agent serves various functions ranging from automation to communication using Discord.
---

## OpenClaw Responsibilities vs Copilot Responsibilities
- **OpenClaw**: Focuses on integration and communication.
- **Copilot**: Handles code generation and logical implementations.

## Autonomous Development Loop
- Continuous improvements based on feedback and testing results.

## Code Generation Policy
- Code must be clear, maintainable, and follow best practices. Automated tests should accompany all generated code.

## discord.py CommandTree/app_commands Conventions
- Use `CommandTree` for defining commands. Ensure to follow the standard patterns for slash commands.

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