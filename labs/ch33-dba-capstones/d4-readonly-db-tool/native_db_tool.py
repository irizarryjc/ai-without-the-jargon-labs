#!/usr/bin/env python3
"""Capstone D4 (Way 1): Native Tool-Calling Read-Only Database Handler.

Exposes JSON Schema tool definitions ready for native function calling in your
application code (OpenAI Responses API, Anthropic Messages API, Gemini API, or
local Ollama) and dispatches calls through the shared read-only `db_policy.py`
with deterministic validation and append-only audit logging.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from db_policy import TOOL_DEFINITIONS, execute_allowlisted_tool


def get_native_tool_schemas() -> list[dict[str, object]]:
    """Return compact JSON Schema definitions for native model API requests."""
    return [
        {
            "type": "function",
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["inputSchema"],
        }
        for tool in TOOL_DEFINITIONS
    ]


def handle_native_tool_call(
    db_path: Path,
    audit_log: Path,
    tool_name: str,
    arguments: dict[str, object],
) -> dict[str, object]:
    return execute_allowlisted_tool(
        db_path=db_path,
        audit_log=audit_log,
        caller_channel="native_tool",
        tool_name=tool_name,
        arguments=arguments,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Native read-only DB tool handler (Capstone D4).")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "d1-sql-tuning" / "northwind_lab.db",
        help="Path to northwind_lab.db.",
    )
    parser.add_argument(
        "--audit-log",
        type=Path,
        default=Path(__file__).resolve().parent / "audit_log.jsonl",
        help="Append-only JSONL audit log path.",
    )
    parser.add_argument("--print-schemas", action="store_true", help="Print native JSON Schema tool definitions.")
    parser.add_argument("--demo", action="store_true", help="Run one allowed read call and one blocked write attempt.")
    args = parser.parse_args()

    if args.print_schemas:
        print(json.dumps(get_native_tool_schemas(), indent=2))
        return 0

    if args.demo:
        allowed = handle_native_tool_call(
            args.db,
            args.audit_log,
            "get_order_summary_by_status",
            {"region": "NORTH", "limit": 5},
        )
        blocked = handle_native_tool_call(
            args.db,
            args.audit_log,
            "drop_orders_table",
            {"sql": "DROP TABLE orders;"},
        )
        print("1. Allowed read-only call:")
        print(json.dumps(allowed, indent=2))
        print("\n2. Blocked non-allowlisted call:")
        print(json.dumps(blocked, indent=2))
        print(f"\nAudit log appended to: {args.audit_log}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
