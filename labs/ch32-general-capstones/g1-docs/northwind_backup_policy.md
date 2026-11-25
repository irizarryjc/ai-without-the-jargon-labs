# Northwind Parts (Fictional) Lab Backup Policy

Document ID: NW-POL-014
Effective Date: October 1, 2026
Owner: Infrastructure Operations Team

## Standard Backup Schedule

1. Lab database instances (`lab-db-01`, `lab-db-02`) run full logical backups every Sunday at 02:00 UTC.
2. Incremental transaction-log archives run every 4 hours during business days (Monday through Friday).
3. Backup verification restore tests must run on the first Tuesday of each month in an isolated sandbox container.

## Storage and Retention

- Primary encrypted backups remain in the local backup vault for 30 days.
- Monthly archival snapshots are stored in immutable object storage for 180 days.
- Restoration requests require a ticket approved by the Infrastructure Operations Lead.

Note: This document intentionally omits disaster-recovery RTO/RPO targets for external SaaS vendors (those live in a separate vendor-risk appendix not included in this lab folder).
