#!/usr/bin/env python3
"""Read-only log triage pre-filter and ticket-draft builder for Capstone D3.

Reads a redacted lab alert log, groups recurring ERROR/WARN lines locally,
suggests a read-only first diagnostic check, and writes a JSON ticket DRAFT to
stdout (never auto-remediates, never restarts services, never edits configs).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

LINE_RE = re.compile(
    r"^(?P<ts>\S+)\s+(?P<host>\S+)\s+(?P<svc>[^:]+):\s+\[(?P<lvl>ERROR|WARN|INFO)\]\s+(?P<msg>.+)$"
)

SAFE_CHECKS: list[tuple[str, str]] = [
    ("archive_command", "Run read-only `df -h /mnt/lab-wal-archive` and inspect `pg_stat_archiver`."),
    ("usage at", "Run read-only `df -h` and `du -sh /mnt/lab-wal-archive/*` to locate space consumers."),
    ("upstream timed out", "Check read-only upstream health metrics and recent app logs; do not restart yet."),
    ("pool exhausted", "Inspect read-only active connection states in `pg_stat_activity`."),
]


def suggest_safe_check(message: str) -> str:
    lowered = message.lower()
    for needle, advice in SAFE_CHECKS:
        if needle in lowered:
            return advice
    return "Inspect surrounding redacted log context (read-only); escalate to on-call engineer."


def build_draft_ticket(log_path: Path) -> dict[str, object]:
    error_groups: Counter[tuple[str, str, str]] = Counter()
    warn_groups: Counter[tuple[str, str, str]] = Counter()

    for raw in log_path.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(raw.strip())
        if not m:
            continue
        lvl = m.group("lvl")
        key = (m.group("host"), m.group("svc"), m.group("msg"))
        if lvl == "ERROR":
            error_groups[key] += 1
        elif lvl == "WARN":
            warn_groups[key] += 1

    grouped_findings = []
    for (host, svc, msg), count in error_groups.most_common(10):
        grouped_findings.append(
            {
                "severity": "ERROR",
                "host": host,
                "service": svc,
                "count": count,
                "message": msg,
                "first_safe_check": suggest_safe_check(msg),
            }
        )
    for (host, svc, msg), count in warn_groups.most_common(10):
        grouped_findings.append(
            {
                "severity": "WARN",
                "host": host,
                "service": svc,
                "count": count,
                "message": msg,
                "first_safe_check": suggest_safe_check(msg),
            }
        )

    return {
        "draft_created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_file": log_path.name,
        "auto_remediation_performed": False,
        "requires_human_review": True,
        "proposed_ticket_title": f"[DRAFT] Lab Alert Triage Summary ({len(error_groups)} error groups, {len(warn_groups)} warnings)",
        "findings": grouped_findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only log triage pipeline (draft ticket only).")
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path(__file__).parent / "sample_alert_log_redacted.log",
        help="Path to redacted lab log file.",
    )
    args = parser.parse_args()

    if not args.log_file.is_file():
        print(f"Error: log file not found: {args.log_file}", file=sys.stderr)
        return 2

    draft = build_draft_ticket(args.log_file)
    print(json.dumps(draft, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
