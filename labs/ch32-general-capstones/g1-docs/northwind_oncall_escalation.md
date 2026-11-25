# Northwind Parts (Fictional) On-Call Escalation Matrix

Document ID: NW-POL-031
Effective Date: November 1, 2026
Owner: Service Desk and Platform Ops

## Severity Definitions

- **Severity 1 (Critical):** Customer-facing checkout or core order database unavailable. Initial response SLA: 15 minutes. Escalate to Infrastructure Lead after 30 minutes if unresolved.
- **Severity 2 (High):** Degraded performance, failed scheduled backup, or single redundant node offline. Initial response SLA: 60 minutes.
- **Severity 3 (Normal):** Non-urgent lab errors, disk usage above 75 percent warning threshold, or access requests. Response SLA: Next business day.

## Communication Rules

- Never post database passwords, API keys, or customer PII in incident chat channels.
- All Severity 1 and Severity 2 incidents require a brief blameless postmortem within 3 business days.
