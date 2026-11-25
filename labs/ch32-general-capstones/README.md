# Chapter 32 Labs: General Track Capstones (G1, G2, G3)

Companion lab materials for Chapter 32 (*Capstones, General Track*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

## Folder Layout

- `g1-docs/`: Three fictional policy documents for **Northwind Parts** (fictional industrial distributor) used to build and test Capstone G1 (Grounded Research Assistant), including intentional information gaps to verify the `"not found"` rule.
- `g2-spec/`: Written specification (`SPEC.md`), starter CLI script (`starter_log_digest.py`), and starter unit tests (`test_log_digest.py`) for Capstone G2 (Spec to Tool).
- `g3-n8n-triage/`: Synthetic shared-inbox ticket queue (`sample_inbox.json`, including one harmless indirect prompt-injection test ticket) and a sanitized n8n workflow blueprint (`workflow-blueprint.json`) with a human approval gate for Capstone G3.

## Quick Verification

```bash
python3 -m unittest discover -s g2-spec -v
python3 g2-spec/starter_log_digest.py --help
python3 -m json.tool g3-n8n-triage/sample_inbox.json > /dev/null
python3 -m json.tool g3-n8n-triage/workflow-blueprint.json > /dev/null
```

All files contain strictly fictional lab data with zero real credentials, hostnames, or customer records.
