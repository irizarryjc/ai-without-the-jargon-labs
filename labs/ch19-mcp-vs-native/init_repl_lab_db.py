#!/usr/bin/env python3
"""Create a synthetic SQLite lab database simulating database replica lag metrics.

Fictional organization: Northwind Parts (industrial distributor).
Lab data only. Lets readers test both native tool calling and MCP without
provisioning a live multi-node database cluster.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def create_repl_lab_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(
            """
            CREATE TABLE replication_status (
                replica_name TEXT PRIMARY KEY,
                engine TEXT NOT NULL,
                primary_host TEXT NOT NULL,
                lag_seconds INTEGER NOT NULL,
                replay_paused INTEGER NOT NULL DEFAULT 0,
                last_checked_utc TEXT NOT NULL,
                health_note TEXT NOT NULL
            );

            INSERT INTO replication_status VALUES
                ('orders-ro-east', 'postgresql', 'lab-pg-primary-01', 2, 0, '2026-11-24T22:00:00Z', 'healthy'),
                ('orders-ro-west', 'postgresql', 'lab-pg-primary-01', 47, 0, '2026-11-24T22:00:00Z', 'elevated_lag_during_batch_load'),
                ('analytics-dg-01', 'oracle', 'lab-ora-primary-01', 185, 1, '2026-11-24T22:00:00Z', 'mrp_apply_paused_in_lab');
            """
        )
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize Chapter 19 replication-lag lab DB.")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("repl_lab.db"),
        help="Path to SQLite lab database (default: ./repl_lab.db).",
    )
    args = parser.parse_args()
    create_repl_lab_db(args.db)
    print(f"Created replication-lag lab database at {args.db.resolve()} (3 synthetic replicas)")


if __name__ == "__main__":
    main()
