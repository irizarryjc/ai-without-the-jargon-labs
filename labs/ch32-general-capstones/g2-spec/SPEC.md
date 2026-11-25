# Specification: `log_digest` CLI Utility (Capstone G2)

## 1. Problem Statement
Operations staff receive redacted plain-text log files from lab servers and need a fast, offline, zero-dependency Python 3 CLI utility that counts lines by severity level (`ERROR`, `WARN`, `INFO`), extracts the top N recurring error messages, and outputs either plain text or valid JSON.

## 2. Functional Requirements & Acceptance Criteria
- **AC-1 (Read-Only Input):** Accepts `--file <path>` (a UTF-8 text log file) and never modifies the input file.
- **AC-2 (Severity Counting):** Counts lines containing `[ERROR]`, `[WARN]`, and `[INFO]` (case-insensitive) plus `OTHER` for unmatched non-empty lines.
- **AC-3 (Top Errors):** Supports `--top <int>` (default `5`, must be `>= 1`) returning the most frequent normalized error messages (stripping leading ISO timestamps before grouping).
- **AC-4 (Output Format):** Supports `--format text` (default) and `--format json` (valid JSON object with keys `total_lines`, `counts`, and `top_errors`).
- **AC-5 (Error Handling):** Exits with non-zero status and a clear message on stderr if the file does not exist or `--top` is less than 1.

## 3. Non-Functional & Safety Constraints
- Python 3 standard library only (no third-party packages; zero slopsquatting risk).
- No network calls, no subprocess shell calls, no writes to disk unless explicitly redirected by the user.

## 4. Implementation Tasks
1. Review `starter_log_digest.py` and `test_log_digest.py`.
2. Ask your coding agent (in Plan Mode first) to implement timestamp normalization in `normalize_error_line` and add `--format json` plus `--top` validation.
3. Expand `test_log_digest.py` with edge-case tests (empty file, missing file, `--top 0`, mixed case).
4. Review the full Git diff and run `python3 -m unittest discover -s g2-spec -v`.
