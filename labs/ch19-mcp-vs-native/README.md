# Chapter 19 Lab: Read-Only `check_replication_lag` Built Two Ways (Native vs. MCP)

Verified as of late 2026 (November). Check current vendor API and official MCP SDK docs for updates.

This lab accompanies Chapter 19 (*MCP vs Native Tool Calls: Choosing Wisely*) of *AI Without the Jargon* by **Juan C. Irizarry, OCP**.

## What It Compares

Both implementations call the exact same read-only, allowlisted SQLite logic against a synthetic Northwind Parts replication-status table (`orders-ro-east`, `orders-ro-west`, `analytics-dg-01`):

1. **Option A (`native_repl_lag.py`):** Direct native tool call schema + validation + audit log inside your own Python app. Minimal moving parts, smallest token footprint, full control.
2. **Option B (`mcp_repl_lag_server.py`):** Thin official Python MCP SDK server (`MCPServer` in v2+, `FastMCP` in v1.x) exposing the same function over `stdio` so Claude Code, VS Code + Copilot, Cursor, Antigravity, Codex CLI, or n8n can share it.

## Run Both Locally (No Cloud API Key Needed)

```bash
python3 init_repl_lab_db.py --db repl_lab.db
python3 native_repl_lag.py --db repl_lab.db --dry-run
python3 mcp_repl_lag_server.py --db repl_lab.db --self-test
```

To inspect the MCP server interactively after installing `mcp[cli]`:

```bash
REPL_LAB_DB="$(pwd)/repl_lab.db" mcp dev mcp_repl_lag_server.py
```

## Real-Engine Read-Only Query Equivalents (DBA Reference, Lab Only)

When adapting this pattern for a real lab database (with a dedicated read-only role and query timeout):

- **PostgreSQL (on standby):** `SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::int AS lag_seconds, pg_is_in_recovery();`
- **Oracle Data Guard (on standby):** `SELECT name, value FROM v$dataguard_stats WHERE name IN ('transport lag', 'apply lag');`

Always test against a disposable lab replica first and never expose write or failover privileges to an AI tool.
