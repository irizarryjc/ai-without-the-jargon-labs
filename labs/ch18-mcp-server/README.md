# Chapter 18 Lab: Minimal Read-Only SQLite MCP Server

Verified as of late 2026 (November). Check the official Python MCP SDK repository (`modelcontextprotocol/python-sdk`) for version updates.

This lab accompanies Chapter 18 (*The Model Context Protocol (MCP)*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

## What This Server Exposes

- **Tools (all strictly read-only):**
  - `list_approved_tables`: returns the allowlisted lab tables (`customers`, `orders`, `order_lines`).
  - `get_table_row_count(table_name)`: counts rows in one allowlisted table using SQLite `?mode=ro` and `PRAGMA query_only = ON`.
  - `get_order_status_summary`: returns aggregate counts grouped by order status (no customer rows).
- **Resource:**
  - `lab://northwind/schema`: read-only schema overview.

## Step 1: Create the Lab Database and Run the Local Self-Test

No MCP SDK installation is required just to verify the database and allowlist checks:

```bash
python3 init_lab_db.py --db northwind_lab.db
python3 server.py --db northwind_lab.db --self-test
```

## Step 2: Install the Official Python MCP SDK and Test With MCP Inspector

Python 3.11+ is required by the official SDK:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
NORTHWIND_LAB_DB="$(pwd)/northwind_lab.db" mcp dev server.py
```

## Step 3: Register in an MCP Host

See `companion-repo/configs/mcp/` for ready-to-adapt templates for Claude Code (`.mcp.json`), VS Code (`.vscode/mcp.json`), Google Antigravity (`mcp_config.json`), and Codex CLI (`config.toml`). Replace `<project_root>` with your lab directory path.

## Safety Reminder

- Never write debug `print()` output to `stdout` in a `stdio` MCP server; `stdout` carries JSON-RPC protocol traffic. This server logs strictly to `stderr`.
- Keep this lab database synthetic and disposable. Never point a prototype MCP server at production credentials or live customer data.
