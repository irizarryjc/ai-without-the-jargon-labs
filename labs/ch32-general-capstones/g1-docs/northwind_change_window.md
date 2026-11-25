# Northwind Parts (Fictional) Maintenance & Change Window Guide

Document ID: NW-POL-022
Effective Date: October 15, 2026
Owner: Change Advisory Board (CAB)

## Approved Maintenance Windows

- Standard low-risk patching: Tuesdays and Thursdays, 01:00 to 03:00 UTC.
- Database schema migrations requiring table locks: Sundays, 04:00 to 06:00 UTC, with at least 48 hours advance notice to application owners.
- Emergency security patches may bypass the 48-hour notice only with written approval from the VP of Infrastructure and the On-Call Lead.

## Mandatory Change Ticket Checklist

Every change request must include:
1. Plain-English summary of scope and affected lab or staging hosts.
2. Pre-change verification check (read-only).
3. Step-by-step rollback plan tested in a lab environment.
4. Post-change health check confirming service recovery.
