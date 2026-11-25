#!/usr/bin/env python3
"""Build the disposable Northwind Parts SQLite lab database for Chapter 33.

Populates fictional customers, orders (with realistic status skew), and
order_lines, then optionally prints BEFORE/AFTER EXPLAIN QUERY PLAN output for
Capstone D1. Uses Python 3 standard library only.
"""

from __future__ import annotations

import argparse
import sqlite3
import time
from pathlib import Path

TARGET_QUERY = """
SELECT c.region,
       COUNT(DISTINCT o.order_id) AS open_orders,
       SUM(ol.quantity * ol.unit_cents) AS backlog_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_lines ol ON ol.order_id = o.order_id
WHERE o.order_status = 'DISPUTED'
  AND o.order_date >= '2026-10-01'
GROUP BY c.region
ORDER BY backlog_cents DESC;
""".strip()


def build_lab_db(db_path: Path, schema_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_path.read_text(encoding="utf-8"))

        regions = ("NORTH", "SOUTH", "EAST", "WEST")
        tiers = ("STANDARD", "PREFERRED", "ENTERPRISE")
        customers = [
            (
                cid,
                f"NW-LAB-{cid:04d}",
                regions[cid % len(regions)],
                tiers[cid % len(tiers)],
                f"2025-{(cid % 12) + 1:02d}-{(cid % 28) + 1:02d}",
            )
            for cid in range(1, 201)
        ]
        conn.executemany(
            "INSERT INTO customers VALUES (?, ?, ?, ?, ?);",
            customers,
        )

        # Realistic status skew: ~80% SHIPPED, ~15% PENDING, ~5% DISPUTED.
        orders = []
        lines = []
        line_id = 1
        for oid in range(1, 3001):
            cid = ((oid * 7 + (oid // 20)) % 200) + 1
            mod = oid % 20
            status = "DISPUTED" if mod == 0 else ("PENDING" if mod <= 3 else "SHIPPED")
            month = ((oid // 250) % 12) + 1
            day = (oid % 28) + 1
            order_date = f"2026-{month:02d}-{day:02d}"
            order_total = 0
            for item_idx in range(3):
                qty = ((oid + item_idx) % 4) + 1
                unit_cents = 1500 + ((oid + item_idx * 7) % 10) * 500
                order_total += qty * unit_cents
                lines.append((line_id, oid, f"PART-{(oid + item_idx) % 50:03d}", qty, unit_cents))
                line_id += 1
            orders.append((oid, cid, status, order_date, order_total))

        conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?);", orders)
        conn.executemany("INSERT INTO order_lines VALUES (?, ?, ?, ?, ?);", lines)
        conn.execute("ANALYZE;")
        conn.commit()
    finally:
        conn.close()


def show_plan(conn: sqlite3.Connection, label: str) -> None:
    print(f"=== {label} ===")
    for row in conn.execute(f"EXPLAIN QUERY PLAN {TARGET_QUERY}"):
        print(" ", row)
    t0 = time.perf_counter()
    rows = conn.execute(TARGET_QUERY).fetchall()
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    print(f"  Result rows: {len(rows)} | Elapsed (lab illustrative): {elapsed_ms:.2f} ms")
    for r in rows:
        print("  ", r)


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed disposable northwind_lab.db for Chapter 33.")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent / "northwind_lab.db",
        help="Destination SQLite file path.",
    )
    parser.add_argument(
        "--demo-tuning",
        action="store_true",
        help="Run BEFORE plan, create composite indexes, run AFTER plan, then roll back indexes.",
    )
    args = parser.parse_args()

    schema_path = Path(__file__).parent / "lab_schema.sql"
    build_lab_db(args.db, schema_path)
    print(f"Created lab database at {args.db} (200 customers, 3,000 orders, 9,000 order_lines).")

    if args.demo_tuning:
        conn = sqlite3.connect(args.db)
        try:
            show_plan(conn, "BEFORE INDEXES")
            conn.execute(
                "CREATE INDEX idx_orders_status_date ON orders(order_status, order_date, customer_id);"
            )
            conn.execute(
                "CREATE INDEX idx_order_lines_order_id ON order_lines(order_id);"
            )
            conn.execute("ANALYZE;")
            show_plan(conn, "AFTER COMPOSITE + FK INDEXES")
            # Roll back so the lab database stays clean for reader experimentation.
            conn.execute("DROP INDEX idx_orders_status_date;")
            conn.execute("DROP INDEX idx_order_lines_order_id;")
            conn.commit()
            print("Rolled back lab indexes cleanly so you can test manually.")
        finally:
            conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
