# Security notes

This project is a learning application, not a security product.

## Current boundary

The assistant can only run commands registered in its local command router. Natural-language input is first mapped to one of those commands. If no match is found, the request is rejected.

User input is not executed in PowerShell, Command Prompt or another shell. The current system-status feature only reads CPU and memory usage.

## Not implemented yet

- authentication or multiple users
- cloud account integrations
- voice recording
- an audit log
- actions that change files or system settings

Any future state-changing action should require a clear confirmation and its own narrow permission.

## Reporting a problem

Please open a GitHub issue for normal bugs. If a report contains private information or a security-sensitive example, do not include that information in a public issue.

