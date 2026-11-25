#!/usr/bin/env python3
"""Capstone D4 (Way 2): Read-Only Database MCP Server using the Official Python MCP SDK.

# Format as of November 2026; check current official Python MCP SDK docs.

Install the pinned official Python MCP SDK before running as a stdio MCP server:
    pip install -r requirements.txt
    # installs mcp[cli]==2.3.0 (check PyPI and re-pin periodically)

Both Way 1 (`native_db_tool.py`) and Way 2 (`mcp_db_server.py`) delegate every
query to `db_policy.py` so least privilege (`mode=ro`, `PRAGMA query_only = ON`),
static query allowlists, row caps (`MAX_ROWS = 50`), timeouts, and append-only
JSONL audit logging remain identical across both interfaces.

Run `--self-test` to exercise the read-only tool handlers and audit log locally
even before installing the `mcp` package.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from db_policy import execute_allowlisted_tool

# CRITICAL for stdio MCP servers: log ONLY to stderr, never stdout!
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [northwind-d4-mcp] %(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("northwind-d4-mcp")

DEFAULT_DB_PATH = Path(
    os.environ.get(
        "NORTHWIND_LAB_DB",
        str(Path(__file__).resolve().parent.parent / "d1-sql-tuning" / "northwind_lab.db"),
    )
)
DEFAULT_AUDIT_LOG = Path(
    os.environ.get(
        "NORTHWIND_AUDIT_LOG",
        str(Path(__file__).resolve().parent / "audit_log.jsonl"),
    )
)


def call_readonly_tool(
    tool_name: str,
    arguments: dict[str, Any],
    *,
    db_path: Path = DEFAULT_DB_PATH,
    audit_log: Path = DEFAULT_AUDIT_LOG,
) -> dict[str, Any]:
    """Run one allowlisted read-only lab tool through the shared policy layer."""
    outcome = execute_allowlisted_tool(
        db_path=db_path,
        audit_log=audit_log,
        caller_channel="mcp_stdio",
        tool_name=tool_name,
        arguments=arguments,
    )
    logger.info(
        "audit channel=mcp_stdio tool=%s ok=%s rows=%s",
        tool_name,
        outcome.get("ok"),
        outcome.get("row_count", 0),
    )
    return outcome


def build_mcp_server(
    db_path: Path = DEFAULT_DB_PATH,
    audit_log: Path = DEFAULT_AUDIT_LOG,
) -> Any:
    """Create and configure the MCP server using the official Python MCP SDK (v2 or v1)."""
    try:
        from mcp.server import MCPServer as _ServerClass  # Official Python MCP SDK v2+
    except ImportError:
        from mcp.server.fastmcp import FastMCP as _ServerClass  # Official Python MCP SDK v1.x

    server = _ServerClass("northwind-lab-readonly-db")

    @server.tool()
    def get_order_summary_by_status(region: str, limit: int = 10) -> str:
        """Return read-only count and total order value grouped by status for an allowlisted lab region (EAST, NORTH, SOUTH, WEST). Capped at 50 rows."""
        result = call_readonly_tool(
            "get_order_summary_by_status",
            {"region": region, "limit": limit},
            db_path=db_path,
            audit_log=audit_log,
        )
        return json.dumps(result, indent=2)

    @server.tool()
    def list_recent_disputed_orders(
        since_date: str,
        status: str = "DISPUTED",
        limit: int = 10,
    ) -> str:
        """Return read-only fictional lab orders matching an allowlisted status (DISPUTED, PENDING, SHIPPED) since YYYY-MM-DD. Capped at 50 rows."""
        result = call_readonly_tool(
            "list_recent_disputed_orders",
            {"status": status, "since_date": since_date, "limit": limit},
            db_path=db_path,
            audit_log=audit_log,
        )
        return json.dumps(result, indent=2)

    return server


# Module-level export so `mcp dev mcp_db_server.py` discovers the server automatically,
# while guarded so `--self-test` still runs even before the `mcp` package is installed.
try:
    mcp = build_mcp_server()
except ImportError:
    mcp = None


def run_self_test(db_path: Path, audit_log: Path) -> int:
    """Verify allowed reads, blocked non-allowlisted writes, and audit logging locally."""
    allowed_summary = call_readonly_tool(
        "get_order_summary_by_status",
        {"region": "EAST", "limit": 5},
        db_path=db_path,
        audit_log=audit_log,
    )
    allowed_orders = call_readonly_tool(
        "list_recent_disputed_orders",
        {"status": "DISPUTED", "since_date": "2026-10-01", "limit": 3},
        db_path=db_path,
        audit_log=audit_log,
    )
    blocked_write = call_readonly_tool(
        "run_raw_sql",
        {"sql": "DROP TABLE orders;"},
        db_path=db_path,
        audit_log=audit_log,
    )

    print("1. Allowed read-only summary:")
    print(json.dumps(allowed_summary, indent=2))
    print("\n2. Allowed read-only disputed orders:")
    print(json.dumps(allowed_orders, indent=2))
    print("\n3. Blocked non-allowlisted tool call:")
    print(json.dumps(blocked_write, indent=2))
    print(f"\nAudit log appended to: {audit_log}")

    ok = bool(allowed_summary.get("ok")) and bool(allowed_orders.get("ok")) and not bool(blocked_write.get("ok"))
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only lab DB MCP stdio server (Capstone D4).")
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to northwind_lab.db (or set NORTHWIND_LAB_DB).",
    )
    parser.add_argument(
        "--audit-log",
        type=Path,
        default=DEFAULT_AUDIT_LOG,
        help="Append-only JSONL audit log path (or set NORTHWIND_AUDIT_LOG).",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run local validation and audit-log checks without requiring the mcp package.",
    )
    args = parser.parse_args()

    if args.self_test:
        return run_self_test(args.db, args.audit_log)

    server = build_mcp_server(db_path=args.db, audit_log=args.audit_log)
    logger.info("Starting northwind-lab-readonly-db MCP server on stdio (db=%s)", args.db.resolve())
    server.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
