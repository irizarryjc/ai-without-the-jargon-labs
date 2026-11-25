# Chapter 3 Prompt Toolkit: Prompting Basics That Actually Work

Copy-ready prompts from Chapter 3 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. RGCCF Universal Prompt Template

**Use it when:** You want a dependable, repeatable structure for almost any technical, writing, or planning task.

```text
Role: Act as a <senior_role_for_example_Linux_sysadmin_or_DBA>.
Goal: <single_clear_verb_and_deliverable>.
Context:
- Environment: <os_or_platform_version_LAB_only>
- Audience: <who_will_read_this>
- Background: <paste_sanitized_background>

Constraints:
- Use ONLY verified facts from my context; label any assumptions clearly.
- Keep the answer under <word_or_bullet_limit>.
- <safety_or_scope_rule_for_example_read_only_checks_only>

Format:
<exact_structure_table_columns_json_keys_or_sections>
```

**What good output looks like:** A focused, audience-appropriate deliverable that stays within your length and safety limits on the first try.

**Safety note:** Replace every `<placeholder>` with sanitized or fictional lab values; never paste production secrets or customer records.

---

## 2. Ask-Me-First Clarifier

**Use it when:** You are tackling a multi-step technical plan, migration, or script and want to surface missing constraints before the AI writes a single line.

```text
I want your help planning <task_description> in a LAB environment.
Here is what I know so far:
<paste_short_sanitized_summary>

Do NOT generate the full solution yet.
First, ask me up to 5 high-impact clarifying questions whose answers would
change your design, safety checks, or tool choices. Keep each question to
one sentence and wait for my replies.
```

**What good output looks like:** Three to five sharp operational questions (platform version, downtime window, rollback needs, data volume) rather than generic trivia.

---

## 3. Prompt Critic and Improver

**Use it when:** A prompt keeps giving you mediocre or overly wordy replies and you want a sharper rewrite fast.

```text
Critique the draft prompt below using the RGCCF framework
(Role, Goal, Context, Constraints, Format).

1. List up to 4 specific weaknesses or ambiguities in my draft.
2. Rewrite the prompt into a clean, copy-ready RGCCF version using
   <angle_bracket_placeholders> for any missing details I need to fill in.
3. Explain in two sentences why the rewrite will produce more reliable output.

Draft prompt:
<paste_your_weak_prompt>
```

**What good output looks like:** Honest critique of missing constraints or formats paired with a crisp template you can drop straight into a fresh chat.

---

## 4. Few-Shot Output Formatter

**Use it when:** You need messy tickets, log summaries, or notes converted into a strict house style without writing pages of formatting rules.

```text
Convert each new input below into the exact format shown in the examples.
Do not add commentary before or after the results. If a field is missing,
write "UNKNOWN" rather than guessing.

Example 1:
Input:  <example_input_1>
Output: <example_output_1>

Example 2:
Input:  <example_input_2>
Output: <example_output_2>

Example 3:
Input:  <example_input_3>
Output: <example_output_3>

Now convert these inputs:
<paste_sanitized_inputs>
```

**What good output looks like:** Every converted line mirrors your capitalization, separators, and `"UNKNOWN"` fallback consistently.

**Safety note:** Verify that your examples and inputs contain zero real hostnames, user emails, or confidential data.

---

## 5. Safe Lab Command or SQL Draft

**Use it when:** You need a starter shell command, config snippet, or SQL query for a lab environment with built-in risk and verification notes.

```text
Role: Act as a careful <database_engine_or_OS> specialist.
Goal: Draft a <read_only_check_or_lab_script> for <specific_lab_task> on <version>.
Context: <sanitized_schema_or_lab_environment_details>.

Constraints:
- Use <placeholders> for hosts, users, and paths; never hardcode credentials.
- Prefer read-only commands first; clearly separate any step that modifies state.
- Explain the risk of each step and how to verify it; do not assume it will run without review.

Format:
1. Command or script in a fenced code block.
2. Risk and blast-radius note for each step.
3. How to verify it worked and how to roll back in the lab.
```

**What good output looks like:** A clean, parameterized starter snippet paired with explicit verification commands and rollback notes you can inspect before touching a terminal.

**Safety note:** Run only in a disposable lab environment after reading every line and checking flags against `--help` or official docs.
