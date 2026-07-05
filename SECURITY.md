# Security Policy

## Supported Scope

This repository contains a Discord bot and supporting SHA256 verification utilities. Security review should prioritize:

- Discord token handling and environment configuration
- command execution boundaries for OpenClaw-related behavior
- GitHub or shell automation surfaces
- dependency updates and supply-chain risk

## Reporting a Vulnerability

Do not open a public issue for a suspected vulnerability.

Use GitHub's private vulnerability reporting or contact the repository owner through a trusted private channel. Include:

- affected file or feature
- reproduction steps
- expected impact
- whether any token, credential, or private data may have been exposed

## Secret Handling

Never commit `.env` files, Discord tokens, GitHub tokens, SSH keys, recovery codes, or screenshots containing credentials. If a secret is exposed, revoke it immediately and replace it with a new value.

## Response Standard

Security fixes should be reviewed before merge, keep credentials out of logs, and include validation notes in the pull request.
