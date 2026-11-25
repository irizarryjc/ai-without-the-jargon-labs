#!/usr/bin/env python3
"""Chapter 18 lab: Minimal read-only MCP server over SQLite lab data.

# Format as of November 2026; check current official Python MCP SDK docs.

Install the official Python MCP SDK before running as an MCP server (pinned as of
November 2026; check PyPI for newer security releases and re-pin):
    pip install "mcp[cli]==2.3.0"
    # or: uv add "mcp[cli]==2.3.0"

Safety rules built into this server:
- Strictly read-only SQLite URI (?mode=ro) plus PRAGMA query_only = ON.
- Hard-coded table allowlist (never constructs SQL from model-supplied strings).
- All diagnostic and audit logs go to stderr (never stdout, which carries stdio JSON-RPC).
- Lab data only (Northwind Parts synthetic database).

Run --self-test to verify read-only query and allowlist logic without the MCP SDK installed.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

# CRITICAL for stdio MCP servers: log ONLY to stderr, never stdout!
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [northwind-mcp] %(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("northwind-mcp")

DEFAULT_DB_PATH = Path(os.environ.get("NORTHWIND_LAB_DB", "northwind_lab.db"))

ALLOWED_COUNT_QUERIES: dict[str, str] = {
    "customers": "SELECT COUNT(*) FROM customers",
    "orders": "SELECT COUNT(*) FROM orders",
    "order_lines": "SELECT COUNT(*) FROM order_lines",
}

ALLOWED_STATUS_QUERY = (
    "SELECT status, COUNT(*) AS order_count "
    "FROM orders GROUP BY status ORDER BY status LIMIT 20"
)


def _open_readonly(db_path: Path) -> sqlite3.Connection:
    resolved = db_path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Lab database not found at {resolved}")
    uri = f"file:{resolved.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=3.0)
    conn.execute("PRAGMA query_only = ON;")
    return conn


def query_approved_tables() -> dict[str, Any]:
    """Return the fixed list of approved read-only lab tables."""
    logger.info("audit tool=list_approved_tables status=ok")
    return {
        "ok": True,
        "mode": "read_only",
        "tables": sorted(ALLOWED_COUNT_QUERIES.keys()),
    }


def query_table_row_count(table_name: str, db_path: Path = DEFAULT_DB_PATH) -> dict[str, Any]:
    """Count rows in one allowlisted lab table using read-only SQLite access."""
    if not isinstance(table_name, str) or table_name not in ALLOWED_COUNT_QUERIES:
        logger.warning("audit tool=get_table_row_count status=rejected table=%r", table_name)
        return {
            "ok": False,
            "error": (
                f"Table {table_name!r} is not on the approved allowlist: "
                f"{sorted(ALLOWED_COUNT_QUERIES.keys())}."
            ),
        }

    conn = _open_readonly(db_path)
    try:
        row = conn.execute(ALLOWED_COUNT_QUERIES[table_name]).fetchone()
        count = int(row[0]) if row else 0
        logger.info("audit tool=get_table_row_count status=ok table=%s rows=%d", table_name, count)
        return {
            "ok": True,
            "table_name": table_name,
            "row_count": count,
            "mode": "read_only",
        }
    finally:
        conn.close()


def query_order_status_summary(db_path: Path = DEFAULT_DB_PATH) -> dict[str, Any]:
    """Return aggregate order counts by status with no customer PII."""
    conn = _open_readonly(db_path)
    try:
        rows = conn.execute(ALLOWED_STATUS_QUERY).fetchall()
        summary = {str(status): int(cnt) for status, cnt in rows}
        logger.info("audit tool=get_order_status_summary status=ok buckets=%d", len(summary))
        return {"ok": True, "mode": "read_only", "orders_by_status": summary}
    finally:
        conn.close()


def build_mcp_server(db_path: Path = DEFAULT_DB_PATH) -> Any:
    """Create and configure the MCP server using the official Python MCP SDK (v2 or v1)."""
    try:
        from mcp.server import MCPServer as _ServerClass  # Official Python MCP SDK v2+
    except ImportError:
        from mcp.server.fastmcp import FastMCP as _ServerClass  # Official Python MCP SDK v1.x

    server = _ServerClass("northwind-readonly-lab")

    @server.tool()
    def list_approved_tables() -> str:
        """List approved read-only tables in the Northwind Parts LAB SQLite database."""
        return json.dumps(query_approved_tables())

    @server.tool()
    def get_table_row_count(table_name: str) -> str:
        """Return the exact row count for one approved table (customers, orders, or order_lines).

        Read-only lab tool. Cannot run arbitrary SQL or modify data.
        """
        return json.dumps(query_table_row_count(table_name, db_path=db_path))

    @server.tool()
    def get_order_status_summary() -> str:
        """Return aggregate order counts grouped by status from the LAB database (no PII)."""
        return json.dumps(query_order_status_summary(db_path=db_path))

    @server.resource("lab://northwind/schema")
    def get_lab_schema() -> str:
        """Read-only description of the fictional Northwind Parts lab tables."""
        return (
            "Northwind Parts LAB Schema (read-only):\n"
            "- customers(customer_id, company_name, region, active)\n"
            "- orders(order_id, customer_id, order_date, status)\n"
            "- order_lines(line_id, order_id, sku, quantity, unit_price_cents)\n"
        )

    return server


# Module-level export required so `mcp dev server.py` discovers the server automatically,
# while guarded so `--self-test` still runs even before the `mcp` package is installed.
try:
    mcp = build_mcp_server()
except ImportError:
    mcp = None


def run_self_test(db_path: Path) -> None:
    """Verify read-only tool handlers locally without requiring an MCP host."""
    print(json.dumps(query_approved_tables(), indent=2))
    print(json.dumps(query_table_row_count("orders", db_path=db_path), indent=2))
    print(json.dumps(query_table_row_count("sqlite_master", db_path=db_path), indent=2))
    print(json.dumps(query_order_status_summary(db_path=db_path), indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Chapter 18 minimal read-only SQLite MCP server.")
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to northwind_lab.db (or set NORTHWIND_LAB_DB).",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run local validation checks and exit (does not require mcp package).",
    )
    args = parser.parse_args()

    if args.self_test:
        run_self_test(args.db)
        return

    mcp = build_mcp_server(db_path=args.db)
    logger.info("Starting northwind-readonly-lab MCP server on stdio (db=%s)", args.db.resolve())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
