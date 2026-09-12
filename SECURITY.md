# Security Policy

## Supported Scope

This repository contains a Discord bot and supporting SHA256 verification utilities. Security review should prioritize:

- Discord token handling and environment configuration
- command execution boundaries for OpenClaw-related behavior
- GitHub or shell automation surfaces
- dependency updates and supply-chain risk

## Reporting a Vulnerability

Do not open a public issue for a suspected vulnerability.

Report vulnerabilities privately through GitHub at `https://github.com/aalmanasir/Discord-automation-bot/security/advisories/new`. If you have repository write access, you may also open a draft private security advisory from the repository Security tab. Include:

- affected file or feature
- reproduction steps
- expected impact
- whether any token, credential, or private data may have been exposed

## Secret Handling

Never commit `.env` files, Discord tokens, GitHub tokens, SSH keys, recovery codes, or screenshots containing credentials. If a secret is exposed, revoke it immediately and replace it with a new value.

## Response Standard

Security fixes should be reviewed before merge, keep credentials out of logs, and include validation notes in the pull request.
