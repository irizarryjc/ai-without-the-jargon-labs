# Chapter 19 Prompt Toolkit: MCP vs Native Tool Calls: Choosing Wisely

Copy-ready prompts from Chapter 19 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Recommend MCP or Native Tools and Justify

**Use it when:** You are scoping a new AI tool integration and want a structured recommendation weighing control, portability, maintenance, security, and context cost.

```text
Act as a pragmatic systems architect helping me decide between native tool calling
and an MCP server for a LAB or internal IT capability.

Requirements (sanitized, no real hostnames or company data):
- Capability description: <what_the_tool_does>
- Do I control the calling app? <yes_or_no>
- AI hosts that need it: <list_of_hosts_or_single_app>
- Read-only or write actions? <read_only_or_write>
- Sensitive or regulated data involved? <yes_or_no>
- Official vendor MCP server available? <yes_no_or_unknown>

Evaluate all seven decision criteria (app control, host count, write impact,
maintenance, context cost, data sensitivity, official server availability), then:
1. Recommend Native Tool Calls, MCP, or Shared Core + Thin MCP Wrapper.
2. Explain the top two trade-offs driving that recommendation.
3. List the minimum security controls required before lab testing.
```

**What good output looks like:** A clear, decisive recommendation grounded in your actual host count and risk profile rather than generic "MCP is modern" advice.

---

## 2. Convert an MCP Tool Into a Native Tool Definition

**Use it when:** You tried a prototype MCP server, realized only your own Python app needs one read-only tool from it, and want to shrink it down into a clean native tool call.

```text
Convert this single read-only MCP tool specification into a compact native tool
definition and Python handler stub for <OpenAI Responses API | Anthropic Messages API | Google Gemini API>.

MCP tool description and schema (sanitized, LAB only):
<paste_single_mcp_tool_schema>

Requirements:
1. Keep only the minimum required parameters with strict enums and
   additionalProperties: false.
2. Add explicit Python allowlist validation, read-only guards, a short timeout,
   and structured stderr audit logging with zero secrets.
3. Estimate the approximate schema token footprint so I can compare it against
   loading the full MCP server.

Explain the risk of each parameter and how to verify invalid inputs are rejected;
do not assume the code will run without review.
```

**What good output looks like:** A lean, self-contained JSON Schema and validated Python handler with far fewer moving parts and lower context overhead than a multi-tool server.

**Safety note:** Test the generated handler strictly against disposable lab data and review every validation check manually before connecting any real endpoint.

---

## 3. Threat-Model a Tool Before Shipping (Native or MCP)

**Use it when:** You are about to expose a new read-only diagnostic tool (either natively or over MCP) and want a quick security review covering auth, scope creep, prompt injection, and telemetry.

```text
Threat-model this proposed LAB diagnostic tool for <fictional_org> against both
OWASP LLM Top 10 (2026) and OWASP MCP Top 10 (beta) risks.

Architecture choice: <Native Tool Call | Local stdio MCP | Remote Streamable HTTP MCP>
Tool summary and parameters (sanitized):
<paste_sanitized_tool_summary>

Return a concise table covering:
- Auth and credential exposure risk
- Permission / scope-creep risk
- Indirect prompt injection or tool-poisoning risk
- Supply-chain / update ("rug pull") risk
- Missing audit / telemetry risk

For each row, list one concrete technical control and how to test it safely in a
lab. Explain the risk of each gap; do not assume any config will run without review.
```

**What good output looks like:** A targeted five-row threat table that distinguishes native-specific risks from MCP-specific risks and gives testable controls for each.

**Safety note:** Never paste live credentials, internal IP addresses, or production schema details when running a threat model in an external chat tool.
