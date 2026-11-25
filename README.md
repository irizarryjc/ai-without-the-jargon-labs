# AI Without the Jargon: Companion Prompts, Labs, Skills, and Configs

Official companion repository for *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP** (First Edition, November 2026).

Public repository URL: `https://github.com/irizarryjc/ai-without-the-jargon-labs`

## Safety First

Every prompt, script, SQL schema, skill, configuration file, and workflow in this repository is built strictly for **disposable lab environments and synthetic sample data** (such as the fictional company Northwind Parts and synthetic `customers`, `orders`, and `order_lines` tables).

- Never paste real credentials, API keys, database connection strings, production IP addresses, internal hostnames, or regulated customer data into prompts, scripts, or Git commits.
- Replace all `<angle_bracket>` placeholders with your own lab values and load API keys exclusively from environment variables or a secrets vault.
- Review every generated SQL statement, shell command, hook script, or configuration file before executing it in a lab.
- Keep local model endpoints (`localhost:11434`, `localhost:1234`) bound to loopback (`127.0.0.1`), and keep database lab tools strictly read-only.

## Repository Structure at a Glance

```text
companion-repo/
├── .gitignore
├── LICENSE
├── README.md
├── configs/
│   ├── ch10-copilot-instructions.md
│   ├── ch14-AGENTS.md
│   ├── ch14-antigravity-rule.md
│   ├── ch14-cursor-rule.mdc
│   ├── hooks/
│   │   ├── README.md
│   │   ├── antigravity.hooks.json
│   │   ├── claude-code.settings.json
│   │   ├── copilot-cli.hooks.json
│   │   ├── guard_pre_tool.py
│   │   └── guard_pre_tool.sh
│   └── mcp/
│       ├── README.md
│       ├── antigravity.mcp_config.json
│       ├── claude-code.mcp.json
│       ├── codex.config.toml
│       └── vscode.mcp.json
├── labs/
│   ├── ch08-api-calls/
│   │   ├── README.md
│   │   ├── call_local_ollama.py
│   │   ├── call_local_ollama.sh
│   │   ├── call_openai_responses.py
│   │   └── call_openai_responses.sh
│   ├── ch10-validation-demo/
│   │   ├── README.md
│   │   ├── backup_manifest.py
│   │   └── test_backup_manifest.py
│   ├── ch17-tool-calling/
│   │   ├── README.md
│   │   ├── init_lab_db.py
│   │   └── tool_calling_lab.py
│   ├── ch18-mcp-server/
│   │   ├── README.md
│   │   ├── init_lab_db.py
│   │   ├── requirements.txt
│   │   └── server.py
│   ├── ch19-mcp-vs-native/
│   │   ├── README.md
│   │   ├── init_repl_lab_db.py
│   │   ├── mcp_repl_lag_server.py
│   │   └── native_repl_lag.py
│   ├── ch22-n8n-triage/
│   │   ├── README.md
│   │   ├── alert-triage-workflow.json
│   │   ├── docker-compose.yml
│   │   └── sample-alert.json
│   ├── ch24-agent-sdks/
│   │   ├── README.md
│   │   ├── ops_agent_adk.py
│   │   ├── ops_agent_openai.py
│   │   ├── ops_tools.py
│   │   ├── requirements.txt
│   │   └── test_ops_tools.py
│   ├── ch29-evals/
│   │   ├── README.md
│   │   ├── eval_cases.jsonl
│   │   └── eval_runner.py
│   ├── ch32-general-capstones/
│   │   ├── README.md
│   │   ├── g1-docs/
│   │   │   ├── northwind_backup_policy.md
│   │   │   ├── northwind_change_window.md
│   │   │   └── northwind_oncall_escalation.md
│   │   ├── g2-spec/
│   │   │   ├── SPEC.md
│   │   │   ├── starter_log_digest.py
│   │   │   └── test_log_digest.py
│   │   └── g3-n8n-triage/
│   │       ├── sample_inbox.json
│   │       └── workflow-blueprint.json
│   └── ch33-dba-capstones/
│       ├── README.md
│       ├── d1-sql-tuning/
│       │   ├── engine_explain_notes.sql
│       │   ├── lab_schema.sql
│       │   └── seed_lab_db.py
│       ├── d3-log-triage/
│       │   ├── sample_alert_log_redacted.log
│       │   └── triage_pipeline.py
│       ├── d4-readonly-db-tool/
│       │   ├── db_policy.py
│       │   ├── mcp_db_server.py
│       │   ├── native_db_tool.py
│       │   └── requirements.txt
│       └── d5-change-review/
│           ├── change_review_preflight.py
│           └── sample_migration.sql
├── prompts/
│   ├── appendix-a-prompt-patterns.md
│   └── ch01-prompts.md through ch33-prompts.md (33 chapter prompt files)
└── skills/
    ├── db-health-check/
    │   ├── SKILL.md
    │   ├── references/
    │   │   └── thresholds.md
    │   └── scripts/
    │       └── check_lab_db.py
    └── db-runbook-check/
        ├── SKILL.md
        └── scripts/
            └── check_lab_db.py
```

## Detailed Inventory by Folder

### 1. Copy-Ready Prompts (`prompts/`, 34 files)

Every chapter's Prompt Toolkit is mirrored verbatim alongside the 21 named prompt pattern templates from Appendix A (**141 total copy-ready templates**):

- `prompts/ch01-prompts.md` through `prompts/ch05-prompts.md`: Part I (Welcome to AI, 21 prompts)
- `prompts/ch06-prompts.md` through `prompts/ch09-prompts.md`: Part II (AI at Your Desk, 14 prompts)
- `prompts/ch10-prompts.md` through `prompts/ch15-prompts.md`: Part III (AI-Assisted Coding, 23 prompts)
- `prompts/ch16-prompts.md` through `prompts/ch26-prompts.md`: Part IV (Agents, Tools, and Workflows, 38 prompts)
- `prompts/ch27-prompts.md` through `prompts/ch31-prompts.md`: Part V (Running AI Safely and Well at Work, 16 prompts)
- `prompts/ch32-prompts.md` and `prompts/ch33-prompts.md`: Part VI (Hands-On Capstone Projects, 8 prompts)
- `prompts/appendix-a-prompt-patterns.md`: Appendix A (all 21 named prompt pattern templates)

### 2. Hands-On Labs (`labs/`, 10 lab suites)

| Folder | Book Chapter | Contents and Purpose |
| :--- | :--- | :--- |
| `labs/ch08-api-calls/` | Chapter 8 | `call_local_ollama.{sh,py}` and `call_openai_responses.{sh,py}`: environment-variable-safe `curl` and Python API calls (local Ollama with zero cloud key + OpenAI Responses API) |
| `labs/ch10-validation-demo/` | Chapter 10 | `backup_manifest.py` and `test_backup_manifest.py`: input validation and unit-test lab for VS Code and GitHub Copilot Agent mode |
| `labs/ch17-tool-calling/` | Chapter 17 | `init_lab_db.py` and `tool_calling_lab.py`: parameterized, allowlisted native tool calling (`get_table_row_count`) against a local SQLite lab database |
| `labs/ch18-mcp-server/` | Chapter 18 | `init_lab_db.py`, `server.py`, `requirements.txt`: minimal read-only Python MCP server (`MCPServer`/`FastMCP`) exposing scoped lab resources and tools |
| `labs/ch19-mcp-vs-native/` | Chapter 19 | `init_repl_lab_db.py`, `native_repl_lag.py`, `mcp_repl_lag_server.py`: side-by-side native vs. MCP implementation of read-only `check_replication_lag` |
| `labs/ch22-n8n-triage/` | Chapter 22 | `docker-compose.yml`, `alert-triage-workflow.json`, `sample-alert.json`: self-hosted n8n Community Edition alert-triage workflow with deterministic redaction and HITL approval gate |
| `labs/ch24-agent-sdks/` | Chapter 24 | `ops_tools.py`, `test_ops_tools.py`, `ops_agent_openai.py`, `ops_agent_adk.py`, `requirements.txt`: the same bounded read-only ops agent built in OpenAI Agents SDK and Google ADK |
| `labs/ch29-evals/` | Chapter 29 | `eval_cases.jsonl` and `eval_runner.py`: 10-case repeatable offline eval harness with simulated regression detection |
| `labs/ch32-general-capstones/` | Chapter 32 | `g1-docs/` (3 fictional Northwind Parts policy docs), `g2-spec/` (`SPEC.md`, `starter_log_digest.py`, `test_log_digest.py`), `g3-n8n-triage/` (`sample_inbox.json`, `workflow-blueprint.json`) |
| `labs/ch33-dba-capstones/` | Chapter 33 | `d1-sql-tuning/` (`lab_schema.sql`, `seed_lab_db.py`, `engine_explain_notes.sql`), `d3-log-triage/` (`sample_alert_log_redacted.log`, `triage_pipeline.py`), `d4-readonly-db-tool/` (`db_policy.py`, `native_db_tool.py`, `mcp_db_server.py`, `requirements.txt`), `d5-change-review/` (`sample_migration.sql`, `change_review_preflight.py`) |

### 3. Portable Agent Skills (`skills/`, 2 skill packages)

- `skills/db-health-check/` (Chapter 20): portable `SKILL.md` plus `references/thresholds.md` and read-only `scripts/check_lab_db.py` designed to run across Claude Code, GitHub Copilot, Cursor, Antigravity, Codex, and Cline.
- `skills/db-runbook-check/` (Chapter 33, Capstone D2): portable database operations runbook `SKILL.md` paired with read-only `scripts/check_lab_db.py`.

### 4. Rules, MCP, and Hook Configurations (`configs/`, 15 files)

- **Rules and instructions files:** `configs/ch10-copilot-instructions.md` (Chapter 10), `configs/ch14-AGENTS.md`, `configs/ch14-antigravity-rule.md`, and `configs/ch14-cursor-rule.mdc` (Chapter 14).
- **Read-only MCP host configurations (`configs/mcp/`):** `README.md`, `antigravity.mcp_config.json`, `claude-code.mcp.json`, `codex.config.toml`, and `vscode.mcp.json` (Chapter 18).
- **Fail-closed pre-tool safety hooks (`configs/hooks/`):** `README.md`, `antigravity.hooks.json`, `claude-code.settings.json`, `copilot-cli.hooks.json`, `guard_pre_tool.py`, and `guard_pre_tool.sh` (Chapter 21).

## Quick Verification Commands (Safe, Offline)

Every script in this repository includes an offline or dry-run verification path that requires no cloud API keys or production databases. Inspect any lab folder's `README.md` before running, or run quick syntax checks from the repository root:

```bash
bash -n labs/ch08-api-calls/*.sh configs/hooks/guard_pre_tool.sh
python3 -m unittest discover -s labs/ch24-agent-sdks -v
python3 -m unittest discover -s labs/ch32-general-capstones/g2-spec -v
python3 labs/ch10-validation-demo/backup_manifest.py
python3 labs/ch29-evals/eval_runner.py --cases labs/ch29-evals/eval_cases.jsonl
# Optional (with pytest installed):
# (cd labs/ch10-validation-demo && pytest -v)
```

## License

MIT License. See [LICENSE](LICENSE).
