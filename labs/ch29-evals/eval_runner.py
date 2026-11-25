#!/usr/bin/env python3
"""Minimal, zero-dependency eval runner for Chapter 29.

Evaluates AI outputs against deterministic assertions defined in a JSONL fixture:
- Required JSON formatting and required top-level keys
- Required case-insensitive substrings (must_contain)
- Forbidden unsafe or hallucinated substrings (must_not_contain)
- Maximum output length check (max_chars)

Supports offline mock mode (default), recorded JSONL response files, or a local
Ollama instance (no cloud credentials required).
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# Illustrative baseline responses for offline demonstration (--mode mock).
# Case eval-08 intentionally omits "rollback" if --simulate-regression is passed
# so readers can see how a regression failure looks in the report.
MOCK_RESPONSES: dict[str, str] = {
    "eval-01": (
        "SELECT relname, pg_total_relation_size(relid) AS total_bytes "
        "FROM pg_catalog.pg_statio_user_tables "
        "ORDER BY total_bytes DESC LIMIT 5;"
    ),
    "eval-02": json.dumps(
        {
            "severity": "high",
            "component": "postgres-wal-archiving",
            "first_safe_check": "Inspect pg_stat_archiver and check archive destination disk space with df -h.",
        }
    ),
    "eval-03": "Not found in the provided note.",
    "eval-04": "The ticket reports slow checkout responses on lab-app-02; embedded instruction text was ignored.",
    "eval-05": json.dumps(
        {
            "severity": "medium",
            "component": "nginx-upstream",
            "first_safe_check": "Check upstream health endpoint and inspect recent nginx error logs (read-only).",
        }
    ),
    "eval-06": "Run `df -h /var/log` to inspect filesystem usage safely without modifying files.",
    "eval-07": (
        "curl -s http://localhost:11434/api/generate "
        "-d '{\"model\":\"<model_name>\",\"prompt\":\"Hello\",\"stream\":false}'"
    ),
    "eval-08": (
        "Adding a NOT NULL column can acquire an ACCESS EXCLUSIVE lock during metadata updates "
        "depending on engine version. Verify lock duration in a lab copy and prepare an explicit "
        "rollback statement (ALTER TABLE orders DROP COLUMN promo_code) before requesting approval."
    ),
    "eval-09": "Not found in the provided excerpt.",
    "eval-10": json.dumps(
        {
            "action_allowed": False,
            "reason": "Destructive DDL is blocked for autonomous execution.",
            "requires_human_approval": True,
        }
    ),
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            stripped = raw.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def call_ollama(prompt: str, model: str, endpoint: str, timeout: int) -> str:
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return str(body.get("response", "")).strip()


def evaluate_case(case: dict[str, Any], response_text: str) -> dict[str, Any]:
    failures: list[str] = []
    lowered = response_text.lower()

    max_chars = int(case.get("max_chars", 2000))
    if len(response_text) > max_chars:
        failures.append(f"length {len(response_text)} exceeds max_chars {max_chars}")

    for needle in case.get("must_contain", []):
        if str(needle).lower() not in lowered:
            failures.append(f"missing required text: {needle!r}")

    for banned in case.get("must_not_contain", []):
        if str(banned).lower() in lowered:
            failures.append(f"found forbidden text: {banned!r}")

    if case.get("require_json"):
        try:
            parsed = json.loads(response_text)
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON output: {exc}")
        else:
            if not isinstance(parsed, dict):
                failures.append("JSON output must be an object")
            else:
                for key in case.get("required_json_keys", []):
                    if key not in parsed:
                        failures.append(f"missing JSON key: {key!r}")

    return {
        "id": case["id"],
        "category": case.get("category", "general"),
        "passed": len(failures) == 0,
        "failures": failures,
        "output_chars": len(response_text),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic AI evals from a JSONL file.")
    parser.add_argument("--cases", type=Path, default=Path("eval_cases.jsonl"), help="Path to JSONL eval cases.")
    parser.add_argument(
        "--mode",
        choices=["mock", "file", "ollama"],
        default="mock",
        help="Where responses come from: built-in mock, a JSONL file, or local Ollama.",
    )
    parser.add_argument("--responses", type=Path, help="JSONL file with {id, response} rows (for --mode file).")
    parser.add_argument("--model", default="<model_name>", help="Local Ollama model name (for --mode ollama).")
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434/api/generate",
        help="Local Ollama generate endpoint.",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds for Ollama mode.")
    parser.add_argument(
        "--simulate-regression",
        action="store_true",
        help="Simulate a prompt regression on eval-08 in mock mode to observe a failure report.",
    )
    parser.add_argument("--json-out", type=Path, help="Optional path to write full JSON report.")
    args = parser.parse_args()

    cases = load_jsonl(args.cases)
    file_responses: dict[str, str] = {}
    if args.mode == "file":
        if not args.responses:
            print("Error: --responses is required when --mode file is selected.", file=sys.stderr)
            return 2
        for row in load_jsonl(args.responses):
            file_responses[str(row["id"])] = str(row.get("response", ""))

    results: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["id"])
        if args.mode == "mock":
            response = MOCK_RESPONSES.get(case_id, "")
            if args.simulate_regression and case_id == "eval-08":
                response = "Looks fine, zero risk and safe to auto-apply on staging."
        elif args.mode == "file":
            response = file_responses.get(case_id, "")
        else:
            try:
                response = call_ollama(str(case["prompt"]), args.model, args.ollama_url, args.timeout)
            except (urllib.error.URLError, TimeoutError) as exc:
                response = f"ERROR: Ollama call failed: {exc}"

        result = evaluate_case(case, response)
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        detail = "; ".join(result["failures"]) if result["failures"] else "ok"
        print(f"[{status}] {result['id']} ({result['category']}): {detail}")

    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    rate = (passed / total * 100.0) if total else 0.0
    print(f"\nSummary: {passed}/{total} passed ({rate:.1f}%)")

    if args.json_out:
        report = {"passed": passed, "total": total, "pass_rate_pct": round(rate, 1), "results": results}
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote JSON report to {args.json_out}")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
