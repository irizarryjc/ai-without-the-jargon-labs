#!/usr/bin/env python3
"""Read-only SQLite lab database health-check helper for the db-health-check skill.

# Format as of November 2026; uses Python 3 standard library only.

Safety controls:
- Opens SQLite strictly read-only via URI ?mode=ro and PRAGMA query_only = ON.
- Checks only allowlisted lab table names (no dynamic SQL from user input).
- Caps query timeout at 3 seconds and outputs structured JSON.
- Never writes, repairs, vacuums, or modifies database files.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APPROVED_TABLE_QUERIES: dict[str, str] = {
    "customers": "SELECT COUNT(*) FROM customers",
    "orders": "SELECT COUNT(*) FROM orders",
    "order_lines": "SELECT COUNT(*) FROM order_lines",
}


def run_health_check(db_path: Path) -> dict[str, Any]:
    resolved = db_path.resolve()
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not resolved.exists() or not resolved.is_file():
        return {
            "ok": False,
            "overall_status": "FAIL",
            "checked_at_utc": checked_at,
            "target_file": resolved.name,
            "error": f"Lab database file not found: {resolved.name}",
        }

    uri = f"file:{resolved.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=3.0)
    try:
        conn.execute("PRAGMA query_only = ON;")

        quick_rows = [str(r[0]) for r in conn.execute("PRAGMA quick_check;").fetchall()]
        integrity_ok = quick_rows == ["ok"]

        existing_tables = {
            str(r[0])
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

        table_counts: dict[str, int] = {}
        warnings: list[str] = []

        for tbl, sql in APPROVED_TABLE_QUERIES.items():
            if tbl not in existing_tables:
                warnings.append(f"Expected lab table missing: {tbl}")
                continue
            count = int(conn.execute(sql).fetchone()[0])
            table_counts[tbl] = count
            if count == 0:
                warnings.append(f"Lab table {tbl} has 0 rows")

        orders_by_status: dict[str, int] = {}
        if "orders" in existing_tables:
            for status, cnt in conn.execute(
                "SELECT status, COUNT(*) FROM orders GROUP BY status ORDER BY status LIMIT 20"
            ).fetchall():
                orders_by_status[str(status)] = int(cnt)

        if not integrity_ok:
            overall = "FAIL"
        elif warnings:
            overall = "WARN"
        else:
            overall = "OK"

        return {
            "ok": integrity_ok,
            "mode": "read_only",
            "overall_status": overall,
            "checked_at_utc": checked_at,
            "target_file": resolved.name,
            "size_bytes": resolved.stat().st_size,
            "quick_check": quick_rows,
            "table_counts": table_counts,
            "orders_by_status": orders_by_status,
            "warnings": warnings,
        }
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read-only health check for a synthetic Northwind Parts SQLite lab DB."
    )
    parser.add_argument(
        "--db",
        type=Path,
        required=True,
        help="Path to the disposable SQLite lab database file.",
    )
    args = parser.parse_args()
    report = run_health_check(args.db)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report.get("overall_status") in {"OK", "WARN"} else 1)


if __name__ == "__main__":
    main()
