# Reference: Lab Health Check Thresholds and Engine Equivalents

Loaded only on demand (progressive disclosure) when deeper context is requested.

## Lab Status Rules

- **OK:** `PRAGMA quick_check` returns `["ok"]`, all three approved tables (`customers`, `orders`, `order_lines`) exist, and each has at least 1 synthetic row.
- **WARN:** Integrity passes, yet one or more expected lab tables are empty or missing.
- **FAIL:** Database file missing, unreadable, or `PRAGMA quick_check` reports errors. Stop and escalate to a human DBA; never auto-repair.

## Read-Only Health Check Equivalents in Enterprise Engines (Lab Reference Only)

Always run under a least-privilege `<db_readonly_user>` account with statement timeouts enabled:

- **PostgreSQL:** Check database connectivity, `pg_stat_database` deadlocks/conflicts, and `pg_stat_activity` long-running idle-in-transaction sessions.
- **Oracle:** Check `v$instance` (`status = 'OPEN'`), `dba_tablespace_usage_metrics` free space, and `v$dataguard_stats` lag on standbys.
- **MySQL:** Check `SHOW GLOBAL STATUS LIKE 'Threads_connected'`, `SHOW REPLICA STATUS` (MySQL 8.0.22+ / 8.4+), and InnoDB buffer pool metrics.
- **Microsoft SQL Server:** Check `sys.databases` (`state_desc = 'ONLINE'`) and read-only DMV queries such as `sys.dm_exec_requests` with `VIEW SERVER STATE` only where approved.
