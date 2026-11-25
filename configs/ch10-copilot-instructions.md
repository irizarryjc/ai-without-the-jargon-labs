# Repository Copilot Instructions

_Format as of November 2026; check current GitHub Copilot documentation._

## Project Context

This repository holds small Python and Bash operational helper scripts for a fictional lab environment (Northwind Parts). All scripts target Python 3.11+ and POSIX-compatible Bash on Linux.

## Coding Standards

- Validate all external inputs (file paths, host labels, numeric bounds, and allowed enum values) and raise `ValueError` with a clear message on invalid data.
- Never build shell commands or SQL statements with string concatenation; use argument lists for `subprocess.run` and parameterized queries for database access.
- Use type hints on all Python function signatures and keep functions under 40 lines where practical.
- Never hardcode credentials, tokens, API keys, hostnames, or IP addresses; read configuration from environment variables or lab fixture files.

## Testing and Verification

- Run `pytest -v` after every Python change and `bash -n <script>` after every Bash change.
- Add unit tests for both happy paths and invalid-input edge cases whenever changing validation logic.
- Explain the risk of any configuration or script change and list verification steps before concluding.
