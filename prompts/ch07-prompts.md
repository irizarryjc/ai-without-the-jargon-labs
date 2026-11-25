# Chapter 7 Prompt Toolkit: Research, Documents, and Your Own Files

Copy-ready prompts from Chapter 7 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Grounded Research Brief With Citations

**Use it when:** You have uploaded two or more public manuals, RFCs, or approved internal docs and want a structured brief strictly tied to those sources.

```text
Create a concise research brief answering: <your_research_question>
Use ONLY the uploaded or pasted sources below. Do not add facts from outside memory.

Rules:
- Cite the exact document name and section/heading in brackets after every claim,
  like [DocA, Section 3].
- If sources disagree, call out the conflict explicitly rather than picking a side.
- If a sub-question is unanswered in the sources, write "Not found in sources."

Output format:
1. Executive takeaway (3 sentences max)
2. Key findings (5 to 7 bullets, each with a source citation)
3. Conflicts, caveats, or footnotes to double-check
4. Gaps not covered by the sources
```

**What good output looks like:** Every bullet carries a real source tag, disagreements between documents stand out cleanly, and missing information is listed honestly under Gaps.

---

## 2. Exact Supporting-Quote Audit

**Use it when:** You want zero paraphrasing drift and need verbatim sentences you can verify in seconds inside the original PDF or runbook.

```text
Answer each question below using ONLY the provided source documents.
For every answer, provide:
1. Direct answer (1 to 2 sentences).
2. Verbatim quote copied word-for-word from the source, plus document name and
   section/page if visible.
3. Confidence check: "Explicitly stated" or "Not found in the provided sources."

Do NOT paraphrase quotes and do NOT fill gaps from outside knowledge.

Questions:
1. <question_1>
2. <question_2>
3. <question_3>
```

**What good output looks like:** Short answers paired with word-for-word quotes you can verify immediately with Ctrl+F in the original file.

---

## 3. Meeting Notes to Decisions, Owners, and Dates

**Use it when:** You finished a technical design review, incident call, or vendor meeting and need a crisp recap that does not confuse ideas with firm commitments.

```text
Turn the sanitized meeting notes below into a structured follow-up summary.
Use ONLY facts stated in the notes. Do NOT promote brainstorming ideas into
agreed decisions unless the notes explicitly indicate agreement.

Output format:
1. Meeting summary (2 sentences)
2. Confirmed decisions (bullets; write "None explicitly confirmed" if unclear)
3. Action items table: Action | Owner | Target Date | Dependency
   (Use "Unassigned" or "TBD" wherever missing; never guess.)
4. Open discussions and unresolved questions (bullets)

Sanitized meeting notes:
<paste_sanitized_notes>
```

**What good output looks like:** A disciplined recap that catches unassigned tasks and keeps tentative suggestions out of the Confirmed Decisions list.

**Safety note:** Strip real client names, employee contact details, internal hostnames, and confidential project codes before pasting into a non-enterprise assistant.

---

## 4. Two-Policy or Two-Version Document Comparison

**Use it when:** A vendor updated its terms, a policy changed between editions, or you need to compare two runbooks side by side.

```text
Compare Document 1 (<doc_1_label>) and Document 2 (<doc_2_label>) strictly on
the text provided. Ignore minor wording changes that do not alter meaning.

Output format:
1. Added requirements or capabilities in Document 2 (with short verbatim quotes)
2. Removed or tightened items compared to Document 1 (with short verbatim quotes)
3. Ambiguities or footnotes an IT practitioner should verify manually
4. Summary table: Topic | <doc_1_label> | <doc_2_label> | Operational Impact

Do not invent changes not visible in the text.
```

**What good output looks like:** A clean diff-style briefing focusing on real operational impact rather than cosmetic wording edits.
