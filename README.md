# 🐊🔍 Investigator

> *The Sherlock Holmes Gator never misses a clue.*

A structured research engine that turns complex technical questions into verified, actionable findings — in minutes, not days.

---

## What is this?

Investigator is a three-agent AI research pipeline. You ask a question. A research agent investigates it deeply, a validation agent fact-checks every finding and source, and you get a clean document with the answer at the top and the evidence below.

It is not a chatbot. It produces a permanent, structured research document you can share with your team, link to from a Jira ticket, or use as the foundation for a decision.

---

## Why use it?

**Research that would take a senior engineer 2–3 days takes under an hour.**
The system searches live documentation, vendor sources, security advisories, and community references simultaneously. It doesn't summarise from memory — it goes and reads the actual sources.

**You get a verified answer, not just a generated one.**
Every investigation is automatically fact-checked by a second AI agent that verifies sources are real and accessible, and flags any finding that contradicts what the documentation actually says. You see exactly what was confirmed, what was partially confirmed, and what couldn't be verified.

**The answer is always at the top.**
Every investigation opens with a quick-reference table — the concrete takeaway, the list of paths, the decision, the config — before any explanation.

**It scales.**
Once an investigation is complete, it lives here permanently. The next person who asks the same question finds the answer already done, already verified, already formatted.

---

## What does an investigation produce?

Every investigation creates a folder with these documents:

| Document | Audience | What it is |
|----------|----------|-----------|
| `investigation.md` | Engineers | Full research document — actionable summary table first, then findings, concepts, tradeoffs, open questions, and sources |
| `brief_leadership.md` | Leadership (Architects, Senior ICs) | Risk and impact focused. What needs a decision before work can proceed. No implementation details. |
| `brief_po.md` | Product Owners / PMs / EMs | Plain English, zero jargon. Risk level badge. What to decide, what to assign, what to loop leadership in on. |
| `glossary.md` | Anyone | Definitions of every key term and concept referenced in the investigation |
| `investigation.json` | AI systems | The same content in structured format, suitable for feeding into other agents |
| `validation_report.md` | Anyone needing trust | The fact-check report — every source verified, every key claim checked against live documentation |

All markdown files are generated from `investigation.json` — they stay in sync automatically. Which brief you share depends on the audience.

---

## How to request an investigation

Just describe what you want to understand. You don't need to be technical. Examples:

> *"What folders should we exclude from Microsoft Defender on our Windows servers in AWS? We use CloudWatch, SSM, and Rapid7."*

> *"What are the security risks of giving developers broad S3 access in production?"*

> *"What do we need to know about SOC 2 Type II before we start the process?"*

Investigator will ask a few quick scoping questions to make sure the investigation is focused — then it runs on its own and comes back with findings.

---

## How to read an investigation

**Which brief should you read?**

- **Engineers** — full depth, all tradeoffs, all sources, all open questions → `investigation.md`
- **Leadership (Architects, VPs)** — risk, required decisions, technical implications → `brief_leadership.md`
- **Product / Program Manager** — whether to schedule work, what to assign, what needs leadership input → `brief_po.md`

**Reading the full investigation:**

1. **Quick reference table** — the answer. Paths, configs, decisions. Start here.
2. **Key Findings** — the evidence behind the table.
3. **Concepts & Entities** — definitions of key terms. See also `glossary.md`.
4. **Tensions & Tradeoffs** — where there is no clean answer.
5. **Open Questions** — what the investigation couldn't answer.
6. **Sources** — every claim is cited.

**Verifying the facts:**

Check `validation_report.md` to see what was independently verified. Verdicts:
- `VERIFIED` — checked against live documentation
- `PARTIALLY CONFIRMED` — claim narrowed to only what documentation confirms
- `UNVERIFIED` — credible but couldn't be independently confirmed
- `CONTRADICTED` — conflicts with source documentation (corrected before completion)

---

## Investigations

| Investigation | Question | Status |
|---------------|----------|--------|
| [MS Defender AWS Exclusions](./ms-defender-aws-exclusions/investigation.md) | What Defender exclusions should we configure for CloudWatch, SSM, and Rapid7 on Windows Server EC2? | ✅ Complete + Validated |
| [RXT Short Squeeze](./RxtShortSqueeze/investigation.md) | What drove the RXT short squeeze? | ✅ Complete + Validated |

---

## FAQ

**How long does an investigation take?**
Typically 10–20 minutes from question to verified findings.

**Can I trust the findings?**
Every investigation is validated by a second independent agent. The validation report tells you exactly what was confirmed and what wasn't. Nothing in the quick-reference table has been placed there without being verified against live documentation.

**What if the investigation gets something wrong?**
The validation step catches this. If a finding is contradicted by source documentation, it is corrected before the investigation is considered complete.

**Can I ask follow-up questions?**
Yes. Completed investigations include open questions. If something needs deeper research, a new investigation can be requested on that specific sub-question.

---

## How it works

Three-layer agent pattern:

1. **Investigator agent** — researches the question, writes `investigation.json`
2. **Script** — generates all markdown from JSON (`python3 _scripts/json_to_md.py <dir>`)
3. **Validation agent** — fact-checks findings and sources, writes `validation_report.md`

Investigations cannot be marked complete until the validation agent has run and all material findings have been confirmed or corrected.

See [BUILD-STORY.md](./BUILD-STORY.md) for how the system evolved and why each piece exists.
