# Chapter 1 Prompt Toolkit: What AI Is and Isn't (in Plain English)

Copy-ready prompts from Chapter 1 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Cross-Department Plain-English Explainer

**Use it when:** You need to explain a technical concept, outage, or change to a smart colleague outside your specialty without sounding patronizing.

```text
Explain <technical_concept> to me as if I am a smart colleague from another IT
department (for example, <target_role>, not a specialist in <your_domain>).
Use:
1. A one-sentence plain-English definition.
2. One everyday non-IT analogy.
3. One concrete workplace example showing why it matters during an incident or project.
Keep the entire answer under 250 words and avoid unexplained acronyms.
```

**What good output looks like:** Three tight, jargon-free sections you could paste straight into a team chat or onboarding doc after a quick accuracy check.

---

## 2. Known Blind-Spot Check ("What Are You Likely to Get Wrong?")

**Use it when:** You are learning an unfamiliar tool, command, or technology and want the model to flag its own common failure modes before you trust its advice.

```text
I am researching <topic_or_tool> for a lab exercise. Before you give me step-by-step
instructions, list five things an LLM is most likely to get wrong, confuse across
versions, or hallucinate about <topic_or_tool>.
For each item, tell me the exact official documentation page or local command
(such as --help or a read-only check) I should use to verify it myself.
```

**What good output looks like:** A realistic warning list (version-specific flags, renamed defaults, platform differences) paired with concrete verification commands rather than generic disclaimers.

**Safety note:** Always run the verification check yourself against official docs or a lab host; the model can also miss blind spots it does not realize it has.

---

## 3. Messy Notes to Clear Summary

**Use it when:** You finished a hectic troubleshooting call or working session and have fragmented bullet points that need to become a readable summary.

```text
Turn the messy notes below into a clean, structured summary for <audience>.
Use ONLY the facts present in my notes. Do not invent causes, timestamps, owners,
or next steps. If an important detail is missing, list it under "Open Questions."

Output format:
- 2-sentence overview
- Key findings (bullets)
- Decisions made (bullets)
- Open questions (bullets)

Notes (sanitized, no confidential data):
<paste_sanitized_notes>
```

**What good output looks like:** A crisp, faithful rewrite that surfaces genuine gaps under "Open Questions" instead of filling them in with guesses.

**Safety note:** Strip credentials, IP addresses, hostnames, customer names, and ticket IDs before pasting notes into a consumer chat tool.

---

## 4. Five-Minute Compare Habit Review

**Use it when:** You have already sketched your own plan for a technical task and want a second pair of eyes without handing over the driver's seat.

```text
I am planning how to handle <task_description> in a LAB environment.
Here is my initial 5-minute draft approach:
<paste_your_short_draft>

Please act as a careful senior peer reviewer:
1. Propose one alternative approach or improvement I should consider.
2. Point out up to three risks, edge cases, or missing verification steps in my draft.
3. Ask me two clarifying questions about constraints you do not know yet.
Explain the risk of each step and how to verify it; do not assume any change will run
without review.
```

**What good output looks like:** Constructive trade-offs and concrete verification ideas that help you spot what the AI caught and what *it* missed about your environment.

**Safety note:** Use fictional or lab details only, and review every suggested command or configuration step before executing anything.
