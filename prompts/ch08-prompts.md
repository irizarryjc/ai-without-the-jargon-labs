# Chapter 8 Prompt Toolkit: Talking to Models Directly: API Calls Explained

Copy-ready prompts from Chapter 8 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Safe `curl` API Request Generator

**Use it when:** You want a clean `curl` test command for a specific model vendor without accidentally hardcoding secrets or using deprecated endpoints.

```text
Role: Act as a senior backend engineer.
Goal: Write a single copy-ready curl command to call the <vendor_name> text API
using its current documented endpoint.
Context:
- Target OS shell: <bash_or_powershell>
- Model placeholder: <model_name>
- System instruction: <short_system_rule>
- User prompt: <short_test_prompt>

Constraints:
- Read the API key strictly from an environment variable (never hardcode a key).
- Include a dated comment reminding me to verify headers and endpoint paths
  against the vendor's current API reference.
- Include a second command showing how to pretty-print the JSON response and
  inspect token usage and finish_reason.
- Explain the risk of each step and how to verify it; do not assume it will run without review.
```

**What good output looks like:** A clean, environment-variable-backed `curl` snippet using current headers plus a safe inspection pipe.

**Safety note:** Confirm the endpoint URL belongs to the official vendor domain (or `localhost`) before running with any live API key.

---

## 2. Free Text to Strict JSON Schema Converter

**Use it when:** You want to design a clean JSON Schema for structured API outputs and test it on a sample redacted input.

```text
Help me design a strict JSON Schema for extracting structured fields from
<input_type_for_example_redacted_alert_summaries>.

Required fields:
- <field_1_and_type>
- <field_2_and_allowed_values>
- <field_3_nullable_if_missing>

Output format:
1. A valid JSON Schema object with "additionalProperties": false and required fields.
2. One short system prompt instructing the model to return ONLY matching JSON
   and never invent missing values.
3. One valid example JSON output and one edge-case example where optional fields are null.
```

**What good output looks like:** A tight schema with explicit enums, `additionalProperties: false`, and clear `null` handling for missing data.

---

## 3. API Error Decoder and Safe Retry Helper

**Use it when:** An API call returns an HTTP `400`, `401`, `403`, `429`, or `5xx` error and you want a fast diagnosis without pasting your API key.

```text
Diagnose the redacted model API error below.
Provider / endpoint: <vendor_and_endpoint_path>
HTTP status code: <status_code>
Redacted error JSON (zero API keys or sensitive payload data):
<paste_redacted_error_message>

1. Explain in plain English the most likely root cause.
2. List 3 concrete checks I can run locally (headers, env vars, parameter names,
   rate limits, or API version headers).
3. Tell me whether this error should be retried with exponential backoff
   (transient) or fixed in code first (client error).
Explain the risk of each step and how to verify it; do not assume any code change
will run without review.
```

**What good output looks like:** Accurate distinction between client errors you must fix (`400`/`401`) and transient errors safe to retry with backoff (`429`/`503`).

**Safety note:** Never paste `Authorization`, `x-api-key`, or full request dumps containing secrets when asking for error help.

---

## 4. Minimal Python API Wrapper With Safe Guardrails

**Use it when:** You want a tiny, maintainable Python starter script that respects timeouts, retries, token logging, and environment-variable keys.

```text
Write a minimal, clean Python 3 script (under 50 lines) that calls an
OpenAI-compatible endpoint (<base_url_placeholder_or_localhost>) using the
official openai Python SDK.

Constraints:
- Load API key and base URL from environment variables; exit cleanly if missing.
- Set an explicit request timeout (30 seconds) and max_tokens cap.
- Print the response text, finish_reason, and token usage clearly.
- Include brief comments noting how to run python3 -m py_compile to syntax-check it.
- Explain the risk of each step and how to verify it; do not assume it will run without review.
```

**What good output looks like:** A concise, readable script with zero hardcoded secrets, explicit timeouts, and clear token-usage logging.

**Safety note:** Review every dependency and endpoint URL before running, and test against a local server or low-cap lab key first.
