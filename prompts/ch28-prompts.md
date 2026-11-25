# Chapter 28 Prompt Toolkit: The Frameworks Map: OWASP, NIST, MITRE, ISO, EU, and Vendor Frameworks

Copy-ready prompts from Chapter 28 of *AI Without the Jargon: A Hands-On Bootcamp for IT Professionals, DBAs, and Sysadmins* by **Juan C. Irizarry, OCP**.

> **Safety Check:** Never paste real credentials, API keys, hostnames, IP addresses, or customer data into any prompt. Replace `<placeholders>` with sanitized or lab values.

---

## 1. NIST AI RMF Four-Function Mapper

**Use it when:** You want to structure an AI pilot proposal using NIST AI RMF's Govern, Map, Measure, and Manage functions.

```text
Act as an IT risk analyst helping me draft a 1-page pre-pilot briefing for a fictional
or LAB AI workflow (no confidential data):
- Workflow: <use_case_summary>
- Intended users: <intended_users>
- Sanitized data types: <data_types>
- Permitted actions: <read_only_or_draft_actions>

Organize the briefing under the four NIST AI RMF 1.0 functions (Govern, Map, Measure,
Manage) and cite relevant generative AI risks from NIST AI 600-1. Include 3 concrete
checks per function and end with a reminder that this is technical planning only and
not legal advice.
```

**What good output looks like:** Four crisp sections with concrete owners, eval checks, and stop controls that a manager or security reviewer can skim in two minutes.

**Safety note:** Describe systems with sanitized placeholders only; never paste real internal architectures or customer details.

---

## 2. EU AI Act & State Law Intake Questions (Not Legal Advice)

**Use it when:** You want a sharp list of questions before meeting legal or compliance about a new AI workflow.

```text
I am preparing an intake note for our legal and compliance team about a proposed AI
workflow: <sanitized_workflow_description>.

Do NOT give legal advice or declare compliance. Instead:
1. Start with a bold "Not legal advice - confirm with qualified counsel" notice.
2. List 10 clarifying questions our team should answer before meeting legal counsel,
   covering EU AI Act risk tiers (prohibited uses, Annex III/Annex I high-risk areas,
   AI literacy, transparency) and US state automated-decision triggers (such as
   Colorado SB 26-189 consequential decisions).
3. List the technical artifacts IT must bring (data inventory, human review gates,
   audit logs, vendor vs deployer role).
```

**What good output looks like:** A focused pre-meeting intake list so legal counsel gets exact engineering facts on the first call.

**Safety note:** Never treat an AI summary as a legal determination; always obtain formal compliance sign-off.

---

## 3. Framework Section to 10-Item Engineering Checklist

**Use it when:** You want to turn a section of CISA/NCSC, Google SAIF 2.0, CSA MAESTRO, or OWASP into a practical team checklist.

```text
Convert the public framework reference below into a plain-English 10-item engineering
checklist for a <team_role> team:
<framework_name_and_public_excerpt>

Rules:
- Each item must map to a verifiable artifact (config, test, log, or human review).
- Group into "Before Launch" and "Ongoing Operations."
- Keep under 350 words with zero buzzwords.
Explain the risk of each check and how to verify it; do not assume any change will run
without review.
```

**What good output looks like:** Ten concrete, auditable checks rather than vague policy slogans.

**Safety note:** Cross-check generated items against the official source document so nothing required is omitted or invented.
