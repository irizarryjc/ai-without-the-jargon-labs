# Chapter 13 Prompt Toolkit: Vibe Coding vs Spec-Driven Development

Copy-ready prompts from Chapter 13 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Idea to Three-Part Spec

**Use it when:** You want to turn a rough utility or feature idea into a crisp, agent-ready `SPEC.md` before writing any code.

```text
Turn the lab project idea below into a concise Markdown specification (under 500
words) with three sections: Requirements, Design, and Tasks.

Idea: <short_project_idea>
Runtime and OS: <language_version> on <target_os>
Constraints: <constraints_or_stdlib_only>

Rules:
- Include explicit Non-Goals so the agent does not expand scope.
- Write 5 testable acceptance criteria using `WHEN <condition>, THE system SHALL
  <expected_behavior>`.
- Specify input validation, exit codes, and lab-only data boundaries.
- Break Tasks into 3 to 5 small steps, each ending with a verification command.
Do not write implementation code yet.
```

**What good output looks like:** A clean one-page `SPEC.md` with unambiguous acceptance criteria, explicit non-goals, and concrete verification steps.

**Safety note:** Check that the Design section forbids hardcoded secrets, live production endpoints, and unapproved third-party packages.

---

## 2. Acceptance-Criteria Writer

**Use it when:** A ticket or change request is vague ("make backup alerts cleaner") and you need concrete, testable criteria before prompting an agent.

```text
Convert this vague request into 6 concrete, testable acceptance criteria for a
LAB implementation:
<paste_sanitized_request>

For each criterion:
- Use `WHEN <condition>, THE system SHALL <observable_outcome>`.
- Cover at least 2 happy paths, 2 invalid-input or missing-resource failures,
  1 boundary condition, and 1 safety/read-only guardrail.
- State the exact test or check that proves each criterion passed.
```

**What good output looks like:** Six crisp, verifiable statements that map 1-to-1 to unit tests with zero fuzzy adjectives like "fast" or "clean."

**Safety note:** Keep all tickets and examples sanitized; remove internal ticket numbers, hostnames, and customer names.

---

## 3. "What's Missing From This Spec?" (Critical Spec Review)

**Use it when:** You finished drafting a spec and want an adversarial peer review to surface hidden failure modes before implementation starts.

```text
Review the draft specification below as a skeptical senior SRE and DBA. Do NOT
rewrite it into code yet.

Draft spec:
<paste_sanitized_spec>

Identify:
1. Up to 5 missing edge cases, failure modes, or ambiguous requirements.
2. Any security, input-validation, locking, or rollback risks left unaddressed.
3. Up to 3 clarifying questions I must answer before an agent writes a single
   line of code.
Explain the risk of each gap and how to verify the fix once added; do not assume
anything will run without review.
```

**What good output looks like:** Concrete operational catches (missing exit codes, empty files, permissions errors, rollback omissions) rather than generic praise.

**Safety note:** Use lab specs only; treat the reviewer's findings as prompts for *your* judgment rather than automatic mandates.

---

## 4. Test-First Prompt From a Spec

**Use it when:** Your `SPEC.md` is finalized and you want your coding agent to generate failing unit tests *before* implementing the solution.

```text
Read <spec_file> in this LAB repository and write unit tests in <test_file>
using <test_framework> BEFORE modifying or creating implementation code.

Requirements:
- Map each test function explicitly to a numbered acceptance criterion in <spec_file>.
- Use synthetic, deterministic lab fixtures only.
- Include negative tests for invalid inputs, missing files, and boundary values.
- Do not weaken assertions or mock away the core validation logic.
Explain how to run the tests now to confirm they fail before implementation.
Explain the risk of each step and how to verify it; do not assume it will run
without review.
```

**What good output looks like:** A clean test file whose tests trace straight back to `SPEC.md` and fail cleanly until the real implementation is written.

**Safety note:** Inspect every test assertion yourself before running or moving to implementation; AI-generated tests can accidentally assert the wrong expected value.
