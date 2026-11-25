#!/usr/bin/env python3
"""Chapter 19 lab (Option A): Native tool-calling implementation of check_replication_lag.

# Format as of November 2026; check current vendor API docs.

Demonstrates full application-level control:
- Single compact JSON Schema definition (no unused tools loaded into context).
- Strict allowlist of approved replica identifiers.
- Read-only SQLite URI (?mode=ro) + PRAGMA query_only = ON + short timeout.
- Explicit structured JSON audit logging directly under your application's control.
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [native-repl-tool] %(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("native-repl-tool")

ALLOWED_REPLICAS = frozenset({"orders-ro-east", "orders-ro-west", "analytics-dg-01"})

# Compact native tool schema (OpenAI Responses API shape as of November 2026).
NATIVE_TOOL_SCHEMA: dict[str, Any] = {
    "type": "function",
    "name": "check_replication_lag",
    "description": (
        "Check read-only replication lag in seconds for one approved Northwind Parts "
        "LAB database replica. Never modifies replication state or runs arbitrary SQL."
    ),
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "replica_name": {
                "type": "string",
                "enum": sorted(ALLOWED_REPLICAS),
                "description": "Approved lab replica identifier.",
            },
            "warn_threshold_seconds": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3600,
                "description": "Threshold in seconds above which status is flagged warning.",
            },
        },
        "required": ["replica_name", "warn_threshold_seconds"],
        "additionalProperties": False,
    },
}


def check_replication_lag(
    db_path: Path, replica_name: Any, warn_threshold_seconds: Any = 30
) -> dict[str, Any]:
    """Validate arguments strictly, query read-only, classify severity, and log audit event."""
    if not isinstance(replica_name, str) or replica_name not in ALLOWED_REPLICAS:
        logger.warning("audit mode=native tool=check_replication_lag status=rejected replica=%r", replica_name)
        return {
            "ok": False,
            "error": f"Unknown or disallowed replica_name {replica_name!r}. Allowed: {sorted(ALLOWED_REPLICAS)}",
        }

    if isinstance(warn_threshold_seconds, bool) or not isinstance(warn_threshold_seconds, int):
        return {"ok": False, "error": "warn_threshold_seconds must be an integer between 1 and 3600."}
    if not (1 <= warn_threshold_seconds <= 3600):
        return {"ok": False, "error": "warn_threshold_seconds out of range (1..3600)."}

    resolved = db_path.resolve()
    if not resolved.exists():
        return {"ok": False, "error": f"Lab database not found at {resolved}"}

    uri = f"file:{resolved.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=3.0)
    try:
        conn.execute("PRAGMA query_only = ON;")
        row = conn.execute(
            """
            SELECT replica_name, engine, primary_host, lag_seconds,
                   replay_paused, last_checked_utc, health_note
            FROM replication_status
            WHERE replica_name = ?
            LIMIT 1
            """,
            (replica_name,),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return {"ok": False, "error": f"No status row found for {replica_name!r}."}

    name, engine, primary, lag_s, paused, checked_utc, note = row
    if paused:
        severity = "critical"
    elif lag_s >= warn_threshold_seconds:
        severity = "warning"
    else:
        severity = "ok"

    result = {
        "ok": True,
        "mode": "read_only",
        "replica_name": name,
        "engine": engine,
        "primary_host": primary,
        "lag_seconds": int(lag_s),
        "replay_paused": bool(paused),
        "warn_threshold_seconds": warn_threshold_seconds,
        "severity": severity,
        "last_checked_utc": checked_utc,
        "health_note": note,
    }
    logger.info(
        "audit mode=native tool=check_replication_lag status=ok replica=%s lag_s=%d severity=%s",
        name,
        lag_s,
        severity,
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Chapter 19 native check_replication_lag lab.")
    parser.add_argument("--db", type=Path, default=Path("repl_lab.db"), help="Path to repl_lab.db.")
    parser.add_argument("--dry-run", action="store_true", help="Run sample valid and rejected calls.")
    args = parser.parse_args()

    schema_chars = len(json.dumps(NATIVE_TOOL_SCHEMA))
    print(f"Native single-tool schema footprint: {schema_chars} chars (~{schema_chars // 4} tokens)\n")

    tests = [
        ("orders-ro-west", 30),
        ("analytics-dg-01", 30),
        ("prod-billing-primary", 30),
    ]
    for replica, threshold in tests:
        res = check_replication_lag(args.db, replica, threshold)
        print(json.dumps(res, indent=2))
        print("-" * 50)


if __name__ == "__main__":
    main()
