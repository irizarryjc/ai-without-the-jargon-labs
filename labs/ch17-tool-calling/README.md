# Chapter 17 Lab: Read-Only Tool Calling (`get_table_row_count`)

Verified as of late 2026 (November). Check your vendor's API reference for any field updates.

This lab accompanies Chapter 17 (*Tool Calling (Function Calling) Explained*) of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

## What It Demonstrates

1. Creating a tiny synthetic SQLite lab database (`customers`, `orders`, `order_lines`) for the fictional distributor Northwind Parts.
2. Defining a strict JSON Schema tool (`get_table_row_count`) with `enum` and `additionalProperties: false`.
3. Validating model-supplied arguments against a hard-coded Python allowlist (`ALLOWED_TABLES`) so dynamic SQL is never constructed from model text.
4. Opening SQLite strictly read-only (`?mode=ro` plus `PRAGMA query_only = ON`).
5. Returning a structured `function_call_output` payload matching each `call_id`.

## Run Locally (No API Key Needed)

macOS / Linux:

```bash
python3 init_lab_db.py --db northwind_lab.db
python3 tool_calling_lab.py --db northwind_lab.db --dry-run
```

Windows PowerShell:

```powershell
py init_lab_db.py --db northwind_lab.db
py tool_calling_lab.py --db northwind_lab.db --dry-run
```

## Optional Live API Mode

Export your API key in your shell (never commit keys to files) and replace `<model_name>` with a current OpenAI model identifier:

```bash
export OPENAI_API_KEY="<your_api_key>"
python3 tool_calling_lab.py --db northwind_lab.db --live --model "<model_name>"
```

## Cleanup

Delete the disposable lab database file when finished:

```bash
rm -f northwind_lab.db
```
