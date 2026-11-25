#!/usr/bin/env python3
"""Read-only helper script for the db-runbook-check Agent Skill (Capstone D2).

Inspects a local SQLite lab database in strict read-only URI mode (mode=ro)
and reports file size, table row counts, and status thresholds. Optionally prints
verified read-only check templates for Oracle, PostgreSQL, MySQL, or SQL Server.
Never executes DDL, DML, or filesystem writes.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ENGINE_SNIPPETS: dict[str, list[str]] = {
    "postgresql": [
        "SELECT pg_database_size(current_database()) AS db_bytes;",
        "SELECT client_addr, state, replay_lag FROM pg_stat_replication;",
        "SELECT last_archived_wal, last_archived_time, failed_count FROM pg_stat_archiver;",
    ],
    "oracle": [
        "SELECT tablespace_name, used_percent FROM dba_tablespace_usage_metrics ORDER BY used_percent DESC;",
        "SELECT name, value, time_computed FROM v$dataguard_stats WHERE name IN ('transport lag', 'apply lag');",
        "SELECT status, input_type, start_time, end_time FROM v$rman_backup_job_details ORDER BY start_time DESC FETCH FIRST 5 ROWS ONLY;",
    ],
    "mysql": [
        "SELECT table_schema, ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb FROM information_schema.tables GROUP BY table_schema;",
        "SHOW REPLICA STATUS;",
    ],
    "sqlserver": [
        "SELECT name, size * 8 / 1024 AS size_mb FROM sys.database_files;",
        "SELECT database_name, MAX(backup_finish_date) AS last_backup FROM msdb.dbo.backupset GROUP BY database_name;",
    ],
}

ALLOWED_TABLES = ("customers", "orders", "order_lines")


def inspect_sqlite_lab(db_path: Path, warn_mb: float) -> dict[str, object]:
    if not db_path.is_file():
        raise FileNotFoundError(f"Lab database not found: {db_path}")

    size_mb = round(db_path.stat().st_size / (1024 * 1024), 3)
    uri = f"file:{db_path.resolve().as_posix()}?mode=ro"
    counts: dict[str, int] = {}

    conn = sqlite3.connect(uri, uri=True, timeout=5.0)
    try:
        conn.execute("PRAGMA query_only = ON;")
        cur = conn.cursor()
        for tbl in ALLOWED_TABLES:
            # Table names come strictly from the static ALLOWED_TABLES tuple.
            cur.execute(f"SELECT COUNT(*) FROM {tbl};")
            counts[tbl] = int(cur.fetchone()[0])
    finally:
        conn.close()

    storage_status = "WARN" if size_mb >= warn_mb else "OK"
    return {
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target": db_path.name,
        "mode": "read_only",
        "size_mb": size_mb,
        "warn_threshold_mb": warn_mb,
        "storage_status": storage_status,
        "table_row_counts": counts,
        "overall_status": storage_status,
        "rollback_required": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only lab database runbook check helper.")
    parser.add_argument("--db", type=Path, help="Path to local northwind_lab.db SQLite file.")
    parser.add_argument("--warn-mb", type=float, default=50.0, help="File size warning threshold in MB.")
    parser.add_argument(
        "--print-engine-sql",
        choices=sorted(ENGINE_SNIPPETS.keys()),
        help="Print read-only SQL check templates for another DB engine instead of querying SQLite.",
    )
    args = parser.parse_args()

    if args.print_engine_sql:
        print(f"-- Read-only check templates for {args.print_engine_sql} (verify on lab engine version):")
        for stmt in ENGINE_SNIPPETS[args.print_engine_sql]:
            print(stmt)
        return 0

    if not args.db:
        print("Error: supply --db <path_to_northwind_lab.db> or --print-engine-sql <engine>.", file=sys.stderr)
        return 2

    try:
        report = inspect_sqlite_lab(args.db, args.warn_mb)
    except (FileNotFoundError, sqlite3.Error) as exc:
        print(f"Error running read-only check: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
