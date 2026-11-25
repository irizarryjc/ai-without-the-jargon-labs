#!/usr/bin/env python3
"""Shared least-privilege read-only policy and audit layer for Capstone D4.

Both the native tool wrapper (native_db_tool.py) and the MCP stdio server
(mcp_db_server.py) call this exact module so security controls stay identical:
- Strict SQLite read-only URI (`mode=ro`) plus `PRAGMA query_only = ON`
- Static allowlist of named parameterized SELECT queries (zero raw SQL input)
- Strict row limit (MAX_ROWS = 50) and query timeout (2.0s)
- Append-only JSONL audit log recording every allowed and blocked call
"""

from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MAX_ROWS = 50
ALLOWED_REGIONS = {"NORTH", "SOUTH", "EAST", "WEST"}
ALLOWED_STATUSES = {"SHIPPED", "PENDING", "DISPUTED"}

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "get_order_summary_by_status",
        "description": "Return read-only count and total order value grouped by status for a fictional Northwind lab region.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "enum": sorted(ALLOWED_REGIONS),
                    "description": "Allowlisted lab sales region.",
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": MAX_ROWS,
                    "default": 10,
                },
            },
            "required": ["region"],
            "additionalProperties": False,
        },
    },
    {
        "name": "list_recent_disputed_orders",
        "description": "Return read-only fictional lab orders matching an allowlisted status since a YYYY-MM-DD date (capped at 50 rows).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": sorted(ALLOWED_STATUSES),
                    "default": "DISPUTED",
                },
                "since_date": {
                    "type": "string",
                    "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
                    "description": "ISO date YYYY-MM-DD.",
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": MAX_ROWS,
                    "default": 10,
                },
            },
            "required": ["since_date"],
            "additionalProperties": False,
        },
    },
]


def _append_audit(audit_log: Path, entry: dict[str, Any]) -> None:
    audit_log.parent.mkdir(parents=True, exist_ok=True)
    with audit_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def execute_allowlisted_tool(
    *,
    db_path: Path,
    audit_log: Path,
    caller_channel: str,
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """Validate arguments, run allowlisted read-only query, and write audit log."""
    started = time.perf_counter()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def finish(decision: str, payload: dict[str, Any], row_count: int = 0) -> dict[str, Any]:
        duration_ms = round((time.perf_counter() - started) * 1000.0, 2)
        _append_audit(
            audit_log,
            {
                "timestamp_utc": timestamp,
                "channel": caller_channel,
                "tool": tool_name,
                "arguments": arguments,
                "decision": decision,
                "row_count": row_count,
                "duration_ms": duration_ms,
            },
        )
        return payload

    if not isinstance(arguments, dict):
        return finish("blocked", {"ok": False, "error": "Arguments must be a JSON object."})

    if tool_name not in {t["name"] for t in TOOL_DEFINITIONS}:
        return finish(
            "blocked",
            {"ok": False, "error": f"Tool {tool_name!r} is not on the read-only allowlist."},
        )

    if not db_path.is_file():
        return finish("error", {"ok": False, "error": f"Lab DB not found: {db_path.name}"})

    # Validate arguments deterministically before opening the database.
    limit = arguments.get("limit", 10)
    if not isinstance(limit, int) or isinstance(limit, bool) or not (1 <= limit <= MAX_ROWS):
        return finish("blocked", {"ok": False, "error": f"limit must be an integer between 1 and {MAX_ROWS}."})

    sql = ""
    params: tuple[Any, ...] = ()

    if tool_name == "get_order_summary_by_status":
        region = arguments.get("region")
        if region not in ALLOWED_REGIONS:
            return finish("blocked", {"ok": False, "error": f"region must be one of {sorted(ALLOWED_REGIONS)}."})
        sql = (
            "SELECT o.order_status, COUNT(*) AS order_count, SUM(o.total_cents) AS total_cents "
            "FROM orders o JOIN customers c ON c.customer_id = o.customer_id "
            "WHERE c.region = ? GROUP BY o.order_status ORDER BY order_count DESC LIMIT ?;"
        )
        params = (region, limit)
    elif tool_name == "list_recent_disputed_orders":
        status = arguments.get("status", "DISPUTED")
        since_date = str(arguments.get("since_date", ""))
        if status not in ALLOWED_STATUSES:
            return finish("blocked", {"ok": False, "error": f"status must be one of {sorted(ALLOWED_STATUSES)}."})
        if len(since_date) != 10 or since_date[4] != "-" or since_date[7] != "-":
            return finish("blocked", {"ok": False, "error": "since_date must use YYYY-MM-DD format."})
        sql = (
            "SELECT o.order_id, c.account_code, c.region, o.order_status, o.order_date, o.total_cents "
            "FROM orders o JOIN customers c ON c.customer_id = o.customer_id "
            "WHERE o.order_status = ? AND o.order_date >= ? "
            "ORDER BY o.order_date DESC, o.order_id DESC LIMIT ?;"
        )
        params = (status, since_date, limit)

    # Connect strictly read-only with busy_timeout and query_only pragma.
    uri = f"file:{db_path.resolve().as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=2.0)
    try:
        conn.execute("PRAGMA query_only = ON;")
        conn.execute("PRAGMA busy_timeout = 2000;")
        conn.row_factory = sqlite3.Row
        cur = conn.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
    except sqlite3.Error as exc:
        return finish("error", {"ok": False, "error": f"Database error: {exc}"})
    finally:
        conn.close()

    return finish(
        "allowed",
        {"ok": True, "tool": tool_name, "row_count": len(rows), "rows": rows},
        row_count=len(rows),
    )
