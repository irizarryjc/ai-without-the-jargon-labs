-- Verified Read-Only Execution Plan & Statistics Syntax by Engine (Late 2026)
-- Always run against a LAB database only; never paste production data into prompts.

-- 1. Oracle Database (EXPLAIN PLAN + DBMS_XPLAN.DISPLAY)
-- Note: For actual runtime row counts on a lab test, use DBMS_XPLAN.DISPLAY_CURSOR
-- with format => 'ALLSTATS LAST' after running with /*+ GATHER_PLAN_STATISTICS */.
EXPLAIN PLAN FOR
SELECT c.region, COUNT(DISTINCT o.order_id) AS open_orders
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_status = 'DISPUTED' AND o.order_date >= '2026-10-01'
GROUP BY c.region;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(
    table_name   => 'PLAN_TABLE',
    statement_id => NULL,
    format       => 'TYPICAL'
));

-- 2. PostgreSQL (EXPLAIN (ANALYZE, BUFFERS))
-- Note: ANALYZE actually executes the query; wrap write statements in ROLLBACK or
-- use read-only SELECTs in a lab clone.
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.region, COUNT(DISTINCT o.order_id) AS open_orders
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_status = 'DISPUTED' AND o.order_date >= '2026-10-01'
GROUP BY c.region;

-- 3. MySQL 8.0 / 8.4 (EXPLAIN ANALYZE)
-- Note: No parentheses around ANALYZE in MySQL syntax; outputs iterator tree.
EXPLAIN ANALYZE
SELECT c.region, COUNT(DISTINCT o.order_id) AS open_orders
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_status = 'DISPUTED' AND o.order_date >= '2026-10-01'
GROUP BY c.region;

-- 4. Microsoft SQL Server (SET STATISTICS IO, TIME ON + estimated/actual plan)
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
SELECT c.region, COUNT(DISTINCT o.order_id) AS open_orders
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_status = 'DISPUTED' AND o.order_date >= '2026-10-01'
GROUP BY c.region;
SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
