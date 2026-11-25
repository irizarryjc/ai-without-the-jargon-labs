#!/usr/bin/env python3
"""Deterministic DDL change-review pre-check for Capstone D5.

Scans a lab SQL migration file for locking, data-loss, bulk-write, and missing
rollback risks BEFORE passing the diff to an AI reviewer, and always marks
`human_signoff_required: true`. Never executes the SQL file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RISK_RULES: list[tuple[str, str, str, str]] = [
    (
        "HIGH",
        "destructive_drop",
        r"\bDROP\s+(?:TABLE|COLUMN|DATABASE|SCHEMA|INDEX)\b",
        "Destructive DROP statement causes irreversible data or object loss; require backup verification and explicit approval.",
    ),
    (
        "HIGH",
        "truncate_table",
        r"\bTRUNCATE\s+TABLE\b",
        "TRUNCATE removes all rows immediately and often cannot roll back cleanly across engines.",
    ),
    (
        "MEDIUM",
        "locking_alter",
        r"\bALTER\s+TABLE\b",
        "ALTER TABLE can acquire metadata or table locks depending on engine/version; test lock duration in a lab clone.",
    ),
    (
        "MEDIUM",
        "bulk_dml_update",
        r"\b(?:UPDATE|DELETE)\s+\w+",
        "Unbatched bulk UPDATE/DELETE can cause long row locks, replication lag, and transaction-log bloat.",
    ),
]


def inspect_migration(sql_path: Path) -> dict[str, object]:
    text = sql_path.read_text(encoding="utf-8")
    # Strip SQL line comments so fixture header comments do not trigger false positives.
    code_only = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("--")
    )
    findings = []

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        for severity, rule_id, pattern, message in RISK_RULES:
            if re.search(pattern, stripped, flags=re.IGNORECASE):
                findings.append(
                    {
                        "line": line_no,
                        "severity": severity,
                        "rule": rule_id,
                        "statement": stripped,
                        "detail": message,
                    }
                )

    has_rollback_section = bool(re.search(r"rollback", code_only, flags=re.IGNORECASE))
    if not has_rollback_section:
        findings.append(
            {
                "line": 0,
                "severity": "HIGH",
                "rule": "missing_rollback_plan",
                "statement": "",
                "detail": "No executable rollback commands detected in migration script.",
            }
        )

    high_count = sum(1 for f in findings if f["severity"] == "HIGH")
    return {
        "file": sql_path.name,
        "executed": False,
        "high_risk_findings": high_count,
        "total_findings": len(findings),
        "recommended_gate": "BLOCK_UNTIL_HUMAN_SIGNOFF" if findings else "HUMAN_REVIEW_REQUIRED",
        "human_signoff_required": True,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Static pre-flight risk scanner for SQL migration diffs (Capstone D5).")
    parser.add_argument(
        "--sql-file",
        type=Path,
        default=Path(__file__).parent / "sample_migration.sql",
        help="Path to lab SQL migration file.",
    )
    args = parser.parse_args()

    if not args.sql_file.is_file():
        print(f"Error: SQL file not found: {args.sql_file}", file=sys.stderr)
        return 2

    report = inspect_migration(args.sql_file)
    print(json.dumps(report, indent=2))
    return 1 if report["high_risk_findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
