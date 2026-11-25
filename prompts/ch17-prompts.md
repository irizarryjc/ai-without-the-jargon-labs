# Chapter 17 Prompt Toolkit: Tool Calling (Function Calling) Explained

Copy-ready prompts from Chapter 17 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Write a Strict JSON Schema Tool Definition

**Use it when:** You want to turn an existing read-only check or helper function into a clean JSON Schema tool definition for OpenAI, Anthropic, or Gemini APIs.

```text
Write a strict JSON Schema tool definition for a READ-ONLY LAB function named
<function_name> that does the following:
<describe_what_the_function_checks_and_its_allowed_inputs>

Target API format: <OpenAI Responses API | Anthropic Messages API | Google Gemini API>
Requirements:
1. Write a clear description stating what it returns, when to use it, and that it
   cannot modify state.
2. Use explicit parameter names, strict types, enums where possible, required
   fields, and additionalProperties: false.
3. Also provide a 15-line Python validation stub that rejects invalid arguments
   using an explicit allowlist before running any command or query.

Explain the risk of each parameter and how to verify the validation rejects
malformed inputs; do not assume it will run without review.
```

**What good output looks like:** A tight, copy-ready JSON Schema object plus a defensive Python validation stub that blocks unexpected keys and unapproved values.

**Safety note:** Review every allowed value and parameter bound yourself, and test against a disposable lab database or directory only.

---

## 2. Fix Overlapping or Ambiguous Tool Descriptions

**Use it when:** An agent keeps calling the wrong tool or passing incorrect units/arguments because two or more tool descriptions sound too similar.

```text
Act as an AI tooling reviewer. My LAB agent keeps confusing these tool definitions:
<paste_sanitized_tool_definitions_json>

Observed mistakes:
<describe_1_or_2_wrong_calls_without_real_data>

1. Identify every overlap or ambiguity in the tool names, descriptions, and
   parameter descriptions.
2. Rewrite each description in 2 to 3 crisp sentences stating exact scope, units,
   when to choose this tool, and when NOT to choose it.
3. Suggest any enum or parameter-naming improvements that remove guesswork.
```

**What good output looks like:** Side-by-side diagnosis of why the model got confused, followed by sharp, mutually exclusive descriptions and cleaner parameter names.

---

## 3. Generate Edge-Case and Defensive Tool Tests

**Use it when:** You wrote a Python tool handler and want repeatable unit tests covering valid inputs, missing keys, bad types, oversized results, and injection-style strings.

```text
Write pytest unit tests for this READ-ONLY LAB tool handler (no production data or
network access):

<paste_sanitized_python_tool_function>

Include test cases for:
1. Valid happy-path inputs.
2. Missing required fields and unexpected extra keys.
3. Wrong data types (None, integers instead of strings, empty strings).
4. Harmless lab fixture strings resembling SQL injection or path traversal (verify
   they are rejected cleanly without raising unhandled exceptions).
5. Missing file or timeout behavior returning a structured {"ok": false, "error": ...}
   object without leaking secrets or stack traces.

Explain the risk each test covers and how to run pytest safely in a lab; do not
assume the code will run without review.
```

**What good output looks like:** Clean, isolated `pytest` tests using temporary lab fixtures that confirm your validation layer fails safely on every malformed argument.

**Safety note:** Run tests strictly against disposable temp files or in-memory SQLite databases, never against shared or production hosts.
