#!/usr/bin/env bash
# Format as of November 2026; thin Bash wrapper for guard_pre_tool.py.
# Fail-closed: if python3 is missing or exits non-zero unexpectedly, exit 2 (block).

set -euo pipefail

HOST_MODE="${1:-claude}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Blocked: python3 is required for guard_pre_tool.py (fail-closed)." >&2
  exit 2
fi

exec python3 "${SCRIPT_DIR}/guard_pre_tool.py" --host "${HOST_MODE}"
