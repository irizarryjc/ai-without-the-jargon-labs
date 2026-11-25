---
# Format as of November 2026; check current docs
name: db-runbook-check
description: Run a read-only lab database health check covering tablespace or disk growth, backup freshness, and replication lag, then produce a structured ops report with escalation guidance. Use when asked to run the routine lab DB runbook check. Never execute DDL, DML, restarts, or changes.
---

# Routine Lab Database Runbook Check

Follow these steps strictly in order when asked to run a routine database health check in a **lab environment**.

## Hard Safety Rules (Non-Negotiable)

1. **Read-only only:** Never run `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `GRANT`, or service restarts.
2. **Lab targets only:** Confirm the target host or SQLite lab file is a designated lab environment (`<db_host>` or `northwind_lab.db`), never production.
3. **No secrets in output:** Never echo passwords, wallet contents, connection strings, or customer PII.

## Step 1: Pre-Checks

Verify the environment before inspecting metrics:
- Confirm you are using a read-only role (`<db_readonly_user>`) or read-only file mode (`mode=ro`).
- Confirm the database target name and engine (SQLite lab file, PostgreSQL, Oracle, MySQL, or SQL Server).
- If running the bundled lab helper script, verify `scripts/check_lab_db.py` exists and inspect its `--help` output first.

## Step 2: Read-Only Diagnostic Checks

Run only read-only checks covering three operational pillars:
1. **Storage / Tablespace Growth:** Check database file size or tablespace utilization (flag >= 80 percent as `WARN`, >= 90 percent as `HIGH`).
2. **Backup Freshness:** Check last recorded backup timestamp or archive status (flag > 24 hours stale in lab tests as `WARN`).
3. **Replication Lag / Table Activity:** Check replica delay (for replicated engines) or order-table row counts in the lab SQLite database using:

```bash
python3 scripts/check_lab_db.py --db <path_to_northwind_lab_db>
```

## Step 3: Expected Output Format

Present findings in this exact structure:
- **Target & Timestamp (UTC)**
- **Summary Status:** `OK` | `WARN` | `ESCALATE`
- **Metrics Table:** Check Name, Observed Value, Threshold, Status
- **First Safe Diagnostic Check** (read-only command for a human to confirm any warning)
- **Escalation Criteria:** Escalate to the on-call DBA lead if storage >= 90 percent, backup > 24h stale, or replication lag exceeds SLA.
- **Rollback Notes:** Because this runbook executes zero writes or configuration changes, rollback requires no database action; simply close the read-only session.
