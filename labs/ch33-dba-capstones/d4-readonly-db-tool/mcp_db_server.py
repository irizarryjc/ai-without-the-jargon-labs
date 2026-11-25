#!/usr/bin/env python3
"""Capstone D4 (Way 2): Read-Only Database MCP Server over stdio (JSON-RPC 2.0).

# Format as of November 2026; check current docs (MCP specification 2026-07-28)

Uses Python 3 standard library only so readers can run and test the exact MCP
wire protocol (`initialize`, `tools/list`, `tools/call`) immediately with zero
third-party installs. In team deployments, you can wrap the exact same
`db_policy.py` module with an official MCP SDK (such as the Python `mcp` SDK:
`MCPServer` in v2+ / `FastMCP` in v1.x, or TypeScript `@modelcontextprotocol/sdk`).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from db_policy import TOOL_DEFINITIONS, execute_allowlisted_tool

PROTOCOL_VERSION = "2026-07-28"


def handle_rpc_message(msg: dict[str, Any], db_path: Path, audit_log: Path) -> dict[str, Any] | None:
    req_id = msg.get("id")
    method = msg.get("method", "")
    params = msg.get("params") or {}

    # Notifications carry no id and expect no reply.
    if req_id is None:
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "northwind-lab-readonly-db", "version": "1.0.0"},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOL_DEFINITIONS},
        }

    if method == "tools/call":
        tool_name = str(params.get("name", ""))
        arguments = params.get("arguments") or {}
        outcome = execute_allowlisted_tool(
            db_path=db_path,
            audit_log=audit_log,
            caller_channel="mcp_stdio",
            tool_name=tool_name,
            arguments=arguments,
        )
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "isError": not bool(outcome.get("ok")),
                "content": [{"type": "text", "text": json.dumps(outcome, indent=2)}],
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only lab DB MCP stdio server (Capstone D4).")
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
    args = parser.parse_args()

    for raw_line in sys.stdin:
        stripped = raw_line.strip()
        if not stripped:
            continue
        try:
            message = json.loads(stripped)
        except json.JSONDecodeError as exc:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()
            continue

        response = handle_rpc_message(message, args.db, args.audit_log)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
