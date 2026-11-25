-- Northwind Parts (Fictional) Lab Schema for Capstones D1, D2, D4, and D5
-- Portable standard SQL (tested on SQLite 3; see engine_explain_notes.sql for
-- Oracle, PostgreSQL, MySQL, and SQL Server syntax notes).
-- Zero real customer records, credentials, or production data.

CREATE TABLE IF NOT EXISTS customers (
    customer_id   INTEGER PRIMARY KEY,
    account_code  VARCHAR(20) NOT NULL UNIQUE,
    region        VARCHAR(16) NOT NULL,
    tier          VARCHAR(16) NOT NULL,
    created_at    VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL,
    order_status  VARCHAR(16) NOT NULL,
    order_date    VARCHAR(20) NOT NULL,
    total_cents   INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_lines (
    line_id       INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL,
    sku           VARCHAR(24) NOT NULL,
    quantity      INTEGER NOT NULL,
    unit_cents    INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
