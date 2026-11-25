-- LAB MIGRATION DIFF FIXTURE FOR CAPSTONE D5 (Change-Review Agent)
-- Deliberately contains four risks for the change-review workflow to catch:
-- 1. Table-locking ALTER TABLE with NOT NULL and no engine-safe online note
-- 2. Destructive DROP COLUMN with permanent data loss and no archive step
-- 3. New foreign-key column added without a supporting index
-- 4. No explicit rollback section or pre-check query

ALTER TABLE orders ADD COLUMN billing_notes VARCHAR(255) NOT NULL DEFAULT 'UNSET';

ALTER TABLE orders ADD COLUMN warehouse_id INTEGER REFERENCES customers(customer_id);

ALTER TABLE customers DROP COLUMN tier;

UPDATE orders SET order_status = 'ARCHIVED' WHERE order_date < '2026-02-01';
