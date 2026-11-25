# Chapter 10 Lab: Input Validation and Unit Tests Starter

Starter files for the **Try It Now** exercise in Chapter 10 (*VS Code and GitHub Copilot, Step by Step*) of *AI Without the Jargon* by **Juan C. Irizarry, OCP**.

## What Is Here

- `backup_manifest.py`: A small Python script for a fictional lab environment (Northwind Parts) that builds backup-retention records without input validation yet.
- `test_backup_manifest.py`: Two starter `pytest` tests covering the happy path.

## How to Run Locally

```bash
python3 backup_manifest.py
pytest -v
```

If `pytest` is not installed yet in your lab virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -v
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest
pytest -v
```

## Safety Reminder

Use fictional host labels and local lab paths only. Review every proposed diff before accepting changes from any coding agent.
