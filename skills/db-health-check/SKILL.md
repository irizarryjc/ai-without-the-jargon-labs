---
name: db-health-check
description: >-
  Run a strictly read-only health check on a disposable LAB SQLite database
  (integrity check, approved table row counts, and order-status summary) with
  pre-checks and a fixed Markdown report format. Use when asked to check lab
  database health, run a read-only database smoke test, or verify lab tables.
compatibility: Requires python3 (standard library only). Lab databases only.
metadata:
  author: Juan C. Irizarry, OCP
  version: "1.0"
  format_verified: "2026-11"
---

# Read-Only Lab Database Health Check

# Format as of November 2026; check https://agentskills.io and host docs.

## Hard Safety Rules (Never Override)

1. **Lab data only:** Confirm the target file is a disposable lab database inside `<project_root>` (for example, `northwind_lab.db`). Refuse immediately if the request names a production host, real customer database, or live connection string.
2. **Never run DDL or DML:** Do **not** generate or execute `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, or `VACUUM`. Every check must remain strictly read-only.
3. **Never echo secrets:** Never print credentials, tokens, or connection passwords into output or logs.
4. **No auto-remediation:** If a check flags corruption, missing tables, or unexpected counts, report the finding and stop for human review.

## Step 1: Pre-Checks

Before running the helper script, verify:
- The user supplied a local lab database path (or confirm `<project_root>/northwind_lab.db`).
- `python3` is available in the lab environment.
- The target database file exists and is readable.

## Step 2: Execute the Read-Only Helper Script

Run the bundled read-only helper script instead of writing ad-hoc SQL from scratch:

```bash
python3 scripts/check_lab_db.py --db "<lab_db_path>"
```

The script opens SQLite with `?mode=ro` and `PRAGMA query_only = ON`, runs `PRAGMA quick_check`, counts rows across the approved lab tables (`customers`, `orders`, `order_lines`), and prints structured JSON to stdout.

## Step 3: Load Engine Thresholds Only If Needed

If the user asks how a finding compares against warning thresholds or what the read-only SQL equivalent looks like in PostgreSQL, Oracle, MySQL, or SQL Server, read `references/thresholds.md`. Do not load it for a routine healthy check.

## Step 4: Expected Output Format

Present the findings using this exact Markdown structure:

```markdown
## Lab Database Health Check Summary
- **Target:** `<db_filename>` (read-only)
- **Overall Status:** `OK` | `WARN` | `FAIL`
- **SQLite Quick Check:** `ok` (or exact finding)
- **Approved Table Row Counts:** `customers=N`, `orders=N`, `order_lines=N`
- **Warnings / Notes:** (bullets, or "None")
- **Recommended Next Human Action:** (one line; never auto-apply changes)
```
