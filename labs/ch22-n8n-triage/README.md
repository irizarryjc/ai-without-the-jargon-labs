# Chapter 22 Lab: n8n Alert Triage with Human Approval

Lab assets for Chapter 22 (*No-Code and Low-Code Automation with n8n*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

Verified as of late 2026 (November). Check current n8n docs if node versions change.

## Files in This Folder

- `docker-compose.yml`: Local n8n Community Edition stack bound strictly to `127.0.0.1:5678`.
- `alert-triage-workflow.json`: Importable n8n workflow featuring deterministic sanitization, an AI Agent node with Structured Output Parser, a `Wait for Human Approval` webhook gate, and an `IF` approval branch.
- `sample-alert.json`: Synthetic lab alert payload for Northwind Parts (`lab-pg-replica-01.example.test`).

## Quick Start (Disposable Lab Only)

1. Start n8n locally:

```bash
$ docker compose up -d
```

2. Open `http://localhost:5678` in your browser and finish the local owner setup.
3. Create a new workflow, choose **Import from File**, and import `alert-triage-workflow.json`.
4. Open **Chat Model (Connect Your Lab Credential)**, select your lab API credential (or swap the sub-node for an Ollama Chat Model), replace `<model_name>` with your chosen model, and save.
5. Click **Execute workflow**, then send the synthetic test alert:

```bash
$ curl -X POST http://localhost:5678/webhook-test/lab-alert-triage \
  -H "Content-Type: application/json" \
  -d @sample-alert.json
```

6. Open **Build Approval Packet** in the n8n UI to review the draft ticket and copy `approve_url` or `reject_url`.
7. Resume the paused execution with `curl "<copied_approve_or_reject_url>"`.

## Safety Reminder

- Never expose port `5678` directly to the public internet without HTTPS and authentication.
- Never paste production credentials, customer data, or live hostnames into lab payloads or exported JSON files.
