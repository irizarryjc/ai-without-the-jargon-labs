# Chapter 6 Prompt Toolkit: The AI Vendor Map

Copy-ready prompts from Chapter 6 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety reminder:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. Strict Three-Plan Pricing Page Comparator

**Use it when:** You are choosing between personal or team subscriptions and want an apples-to-apples table using zero outdated memory.

```text
Build a clean comparison table of the three AI plans below using ONLY the
pasted pricing-page text I supply. Do not add prices, limits, or features
from memory. If a detail is missing from the pasted text, write "VERIFY ON PAGE."

Rows to include:
- Plan name and target audience
- Price and billing cycle (monthly vs. annual)
- Billing meter (seats, rolling limits, tokens, or credits)
- Included tools (chat, IDE, CLI, cloud agents)
- Data privacy / training note (if stated)
- Overage or limit-reached behavior

Plan A text:
<paste_plan_a_pricing_text>

Plan B text:
<paste_plan_b_pricing_text>

Plan C text:
<paste_plan_c_pricing_text>
```

**What good output looks like:** A crisp Markdown table where every number comes straight from your pasted vendor text and missing footnotes are flagged `"VERIFY ON PAGE"`.

---

## 2. 90-Day Tool Changelog Summarizer

**Use it when:** You have not checked a tool in a few months and want to know what was renamed, retired, or changed without reading fifty blog posts.

```text
Using ONLY the official changelog excerpts pasted below for <tool_name>
(covering approximately the last three months):

1. List any renamed, deprecated, or retired features (with exact dates if stated).
2. List breaking changes to CLI flags, config file paths, or pricing/credit meters.
3. List up to 4 genuinely practical new capabilities for an IT practitioner.
4. Cite the exact release date or changelog entry heading for every bullet.
Do not guess or pull unverified rumors.

Official changelog excerpts:
<paste_changelog_text>
```

**What good output looks like:** A date-stamped briefing separating real breaking changes and renames from minor UI tweaks.

---

## 3. Vendor Lock-In and Portability Check

**Use it when:** You or your team are about to invest time building prompts, rules, or workflows in a specific AI platform and want to check how easily you could move later.

```text
Act as a pragmatic enterprise architect reviewing a proposed AI tool setup.
Tool or platform: <tool_name>
Planned workflow: <short_sanitized_description>

1. Identify which parts of this workflow can stay in open, portable formats
   (plain Markdown prompts, AGENTS.md, SKILL.md, MCP servers, standard JSON/Python).
2. Identify which parts would be proprietary lock-in (vendor-only UI logic,
   proprietary agent state, non-portable connectors).
3. Recommend 3 lightweight habits to keep migration cost low if the vendor
   renames or reprices this product next year.
```

**What good output looks like:** Practical separation between portable assets you keep in Git and vendor-specific glue you keep thin.
