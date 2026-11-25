# AGENTS.md

_Format as of November 2026; check current AGENTS.md (AAIF) documentation._

## Project Overview

Fictional Linux and database operations helper scripts for Northwind Parts (lab environment only). Stack: Python 3.11+ (standard library plus `pytest`), POSIX Bash, and lab SQL scripts targeting synthetic `customers`, `orders`, and `order_lines` tables.

## Always-On Rules

- Never hardcode passwords, API keys, tokens, hostnames, or IP addresses; use environment variables or placeholders (`<db_host>`, `<db_readonly_user>`).
- Validate all external inputs and reject relative or `..` traversal paths before touching the filesystem.
- Use parameterized SQL queries and list-based `subprocess.run([...])` calls; never concatenate untrusted strings into SQL or shell commands.
- Add a `--dry-run` flag to any script that deletes, rotates, or modifies files or records.
- Do not modify files under `archive/` or change CI workflows without explicit human approval.

## Verification Commands

- Python syntax and tests: `python3 -m py_compile <file>.py && pytest -v`
- Bash syntax check: `bash -n <script>.sh`
- Confirm clean scope with `git status` and `git diff --stat` before finishing.

## Output Expectations

Keep diffs narrow, state any assumptions clearly, and list the exact verification commands you ran (or ask me to run them).
