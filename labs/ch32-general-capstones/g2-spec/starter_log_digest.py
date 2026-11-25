#!/usr/bin/env python3
"""Starter CLI utility for Capstone G2 (Spec to Tool).

Read-only log digest tool using Python standard library only.
Readers can run this working baseline right away and extend it against SPEC.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

TS_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\s+")


def normalize_error_line(line: str) -> str:
    """Strip a leading ISO-style timestamp so identical errors group cleanly."""
    return TS_PREFIX_RE.sub("", line.strip())


def summarize_lines(lines: list[str], top_n: int = 5) -> dict[str, object]:
    """Count severity levels and return top recurring ERROR lines."""
    if top_n < 1:
        raise ValueError("--top must be at least 1")

    counts = {"ERROR": 0, "WARN": 0, "INFO": 0, "OTHER": 0}
    error_messages: Counter[str] = Counter()
    total = 0

    for raw in lines:
        text = raw.strip()
        if not text:
            continue
        total += 1
        upper = text.upper()
        if "[ERROR]" in upper:
            counts["ERROR"] += 1
            error_messages[normalize_error_line(text)] += 1
        elif "[WARN]" in upper:
            counts["WARN"] += 1
        elif "[INFO]" in upper:
            counts["INFO"] += 1
        else:
            counts["OTHER"] += 1

    top_errors = [
        {"message": msg, "count": cnt}
        for msg, cnt in error_messages.most_common(top_n)
    ]
    return {"total_lines": total, "counts": counts, "top_errors": top_errors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only severity digest for redacted lab log files.")
    parser.add_argument("--file", type=Path, required=True, help="Path to a redacted UTF-8 log file.")
    parser.add_argument("--top", type=int, default=5, help="Number of top error messages to show (>= 1).")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    args = parser.parse_args(argv)

    if args.top < 1:
        print("Error: --top must be >= 1", file=sys.stderr)
        return 2
    if not args.file.is_file():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 2

    lines = args.file.read_text(encoding="utf-8").splitlines()
    digest = summarize_lines(lines, top_n=args.top)

    if args.format == "json":
        print(json.dumps(digest, indent=2))
    else:
        counts = digest["counts"]
        print(f"Total non-empty lines: {digest['total_lines']}")
        print(
            f"ERROR: {counts['ERROR']} | WARN: {counts['WARN']} | "
            f"INFO: {counts['INFO']} | OTHER: {counts['OTHER']}"
        )
        print("Top errors:")
        for item in digest["top_errors"]:
            print(f"  ({item['count']}x) {item['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
