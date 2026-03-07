# OpenClaw Agent

## Conventions

1. **discord.py CommandTree/app_commands**: Use `CommandTree` for organizing commands within the discord.py framework.

2. **Ephemeral Responses**: Ensure to utilize ephemeral responses where appropriate for user privacy and clarity.

3. **Attachment Deferral/Follow-up Pattern**: Implement a follow-up behavior for message attachments, ensuring users receive notifications about their file uploads.

4. **DISCORD_TOKEN Environment Variable**: Use the `DISCORD_TOKEN` environment variable for authentication purposes instead of hardcoding sensitive information in the code.

5. **Normalization Rules for Expected Hash**: To maintain consistency, follow normalization rules when comparing expected hash values.

6. **Testing with pytest**: All agents should have associated tests. While `pytest` is recommended, `unittest` is also acceptable.

---

## OpenClaw Cooperation Sections

Here we will outline how the OpenClaw framework collaborates with existing agents and provide guidelines for interaction protocols. Be sure to maintain clear communication channels with the OpenClaw team.

### Key Cooperation Protocols

- Regular updates on agent performance.
- Need to adhere to any established communication standards for collaborating with OpenClaw agents.

---