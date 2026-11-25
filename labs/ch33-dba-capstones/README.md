# Chapter 33 Labs: DBA and Sysadmin Track Capstones (D1 through D5)

Companion lab materials for Chapter 33 (*Capstones, DBA and Sysadmin Track (Safely)*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

All scripts use strictly fictional **Northwind Parts** lab data (`customers`, `orders`, `order_lines`) with zero production connections. Every offline demo and `--self-test` check runs locally with Python 3 standard library only, while optional live MCP stdio transport in `d4-readonly-db-tool/` uses the pinned official Python MCP SDK (`mcp[cli]==2.3.0` in `requirements.txt`).

## Folder Layout

- `d1-sql-tuning/`:
  - `lab_schema.sql`: Portable `customers`, `orders`, and `order_lines` lab DDL.
  - `seed_lab_db.py`: Builds a disposable SQLite lab database (`northwind_lab.db`) and demonstrates before/after `EXPLAIN QUERY PLAN` for Capstone D1.
  - `engine_explain_notes.sql`: Verified read-only execution-plan syntax across Oracle, PostgreSQL, MySQL 8.x, and SQL Server.
- `d3-log-triage/`:
  - `sample_alert_log_redacted.log`: Synthetic, redacted Linux/DB alert log fixture (RFC 5737 documentation IPs only).
  - `triage_pipeline.py`: Deterministic read-only error grouper and draft-ticket builder (never restarts services or modifies configs).
- `d4-readonly-db-tool/`:
  - `db_policy.py`: Shared least-privilege read-only SQLite policy engine (query allowlist, parameter validation, row cap, timeout, append-only JSONL audit log).
  - `native_db_tool.py`: Native function-calling wrapper + runnable `--demo` showing allowed reads and blocked writes.
  - `mcp_db_server.py`: Read-only stdio MCP server built on the official Python `mcp` SDK (`MCPServer` v2+ / `FastMCP` v1.x) exposing the exact same policy layer and audit log, with `--self-test` for offline checks.
  - `requirements.txt`: Pinned `mcp[cli]==2.3.0` dependency (check PyPI and re-pin periodically).
- `d5-change-review/`:
  - `sample_migration.sql`: Lab schema migration diff with intentional locking, missing-index, and destructive `DROP COLUMN` risks.
  - `change_review_preflight.py`: Deterministic pre-check flagging risky DDL patterns and enforcing human sign-off.

Note: Capstone D2's reusable Agent Skill lives at `companion-repo/skills/db-runbook-check/`.
