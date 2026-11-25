#!/usr/bin/env python3
"""Create a small, synthetic SQLite lab database for Chapter 17 (Tool Calling).

Fictional organization: Northwind Parts (industrial distributor).
Lab data only. Safe to delete and recreate at any time.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def create_lab_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.executescript(
            """
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                company_name TEXT NOT NULL,
                region TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
                order_date TEXT NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE order_lines (
                line_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders(order_id),
                sku TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price_cents INTEGER NOT NULL
            );

            INSERT INTO customers (customer_id, company_name, region, active) VALUES
                (1, 'Acme Hydraulics (Fictional)', 'Northeast', 1),
                (2, 'Summit Valves LLC (Fictional)', 'Midwest', 1),
                (3, 'Harbor Gaskets Co (Fictional)', 'West', 1),
                (4, 'Legacy Bearings Inc (Fictional)', 'South', 0);

            INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
                (1001, 1, '2026-11-18', 'shipped'),
                (1002, 1, '2026-11-20', 'processing'),
                (1003, 2, '2026-11-21', 'shipped'),
                (1004, 3, '2026-11-22', 'pending'),
                (1005, 2, '2026-11-23', 'shipped');

            INSERT INTO order_lines (line_id, order_id, sku, quantity, unit_price_cents) VALUES
                (1, 1001, 'HYD-400', 4, 12500),
                (2, 1001, 'GSK-019', 20, 450),
                (3, 1002, 'VLV-210', 2, 31000),
                (4, 1003, 'VLV-210', 5, 31000),
                (5, 1004, 'GSK-019', 50, 450),
                (6, 1005, 'BRG-880', 10, 8900),
                (7, 1005, 'HYD-400', 1, 12500);
            """
        )
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the Chapter 17 SQLite lab database.")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("northwind_lab.db"),
        help="Path to the SQLite lab database file (default: ./northwind_lab.db).",
    )
    args = parser.parse_args()
    create_lab_db(args.db)
    print(f"Created lab database at {args.db.resolve()} (customers=4, orders=5, order_lines=7)")


if __name__ == "__main__":
    main()
