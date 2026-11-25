# Chapter 31 Prompt Toolkit: AI and Regulated or Sensitive Data

Copy-ready prompts from Chapter 31 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety Check:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Local PII Masking Script Generator

**Use it when:** You want a deterministic Python or Bash redaction script to scrub emails, IPs, tokens, and IDs locally *before* sending logs to an AI tool.

```text
Write a small Python 3 standard-library script (zero external packages) that reads a
UTF-8 text log from stdin and writes a redacted version to stdout.
Deterministically replace:
- Email addresses -> <email>
- IPv4 addresses -> <ip>
- Bearer tokens or key=value secrets (password=, token=, api_key=) -> <redacted_secret>
- 13-to-16 digit card-like sequences -> <redacted_card>
- Custom internal domain <fictional_domain> -> <internal_host>

Also print a redaction count summary to stderr so I can verify what was scrubbed.
Explain the risk of regex edge cases (what this script might miss) and how to verify it
on synthetic test text; do not assume it will run without review.
```

**What good output looks like:** Clean stdlib Python code plus an honest list of limitations (such as free-text personal names) and synthetic verification examples.

**Safety note:** Test the generated script on fictional data first, and never assume regex alone guarantees complete anonymization for regulated compliance.

---

## 2. Synthetic Lab Data Generator (Schema-Matched)

**Use it when:** You need realistic fake SQL `INSERT` statements or CSV rows matching a table structure for lab testing, SQL tuning, or evals with zero real customer data.

```text
Generate synthetic, 100 percent FICTIONAL SQL INSERT statements for a LAB <database_engine>
database matching this sanitized schema:
<paste_sanitized_ddl_only>

Requirements:
- Generate <row_count> rows with realistic skew (for example, 80% active, 20% archived).
- Use obviously fictional names, emails ending in @northwind-lab.invalid, and fake IDs.
- Preserve all primary-key, foreign-key, and NOT NULL constraints.
- Include zero real people, companies, or production values.

Explain how to verify row counts and constraints in a disposable lab database; do not
assume any SQL will run without review.
```

**What good output looks like:** Valid, constraint-safe synthetic inserts that mirror realistic query selectivity without touching production data.

**Safety note:** Run generated seed scripts strictly inside an isolated lab database, never in staging or production.

---

## 3. Pre-AI Data Sensitivity Classifier

**Use it when:** You want to double-check which columns of a sanitized table schema (column names and types only, zero row values!) require masking before cloning or AI analysis.

```text
Act as a data privacy engineer. Review the sanitized database schema below (column names
and data types ONLY, zero row data) and classify each column for AI handling:

Schema (fictional/sanitized):
<paste_column_names_and_types_only>

Return a Markdown table with:
1. Column name
2. Likely sensitivity (Public / Internal / Confidential / Restricted: PII, PHI, PCI, Secret)
3. Why (flag free-text notes/comments columns that often hide unexpected PII)
4. Recommended lab masking strategy (hash, synthetic replacement, nullify, or drop)

Include a clear reminder that this is technical triage only and not legal advice; confirm
classification with our privacy/compliance team.
```

**What good output looks like:** A thorough column-by-column masking plan that catches sneaky risk columns like `support_notes`, `raw_payload`, and `audit_ip`.

**Safety note:** Paste only sanitized column names and types, never sample rows or proprietary table comments containing real customer details.
