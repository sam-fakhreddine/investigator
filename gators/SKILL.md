---
name: gators
description: Full swarm investigation pipeline — scope gate, three-teammate agent team (investigator + validator + arbiter), evaluator-optimizer loop with arbiter voting on disputes, final synthesis. Requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1.
allowed-tools: Read Write Edit Bash WebSearch WebFetch Task
metadata:
  argument-hint: "[research topic or question]"
---

Runs a full investigation pipeline using a three-agent team. The investigator researches and writes findings. The validator fact-checks. If investigator and validator still disagree after the first correction cycle, the arbiter independently verifies the disputed items and casts a binding vote per claim. The lead orchestrates all three teammates and synthesizes the final output.

## Invocation

```
/gators <topic>
```

---

## Prerequisites

Requires the Claude Code experimental agent teams feature:

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

If not set, inform the user and do not proceed past the scope gate.

---

## Lead Session Responsibilities

The lead is **orchestrator and synthesizer only**. It must never:
- Do raw research itself
- Write `investigation.json`, `validation_report.md`, or `arbiter_verdict.md` directly
- Run scripts on behalf of a teammate that has not yet been spawned

---

## Step 1 — Scope Gate

Ask all four questions together. Do not proceed until all four are answered.

```
Before I start the investigation, I need to scope it precisely:

1. What is the single core question? State it in one sentence. If it cannot be stated in one sentence, we should split it into separate investigations.
2. What is explicitly out of scope? Name at least one related area this investigation will not cover.
3. Who is the intended consumer of the findings? (Engineer, Engineering Leadership, Product Owner / EM, or some combination)
4. Are there known sub-topics that each warrant a separate investigation? If yes, list them — each gets its own folder rather than being rolled into this one.
```

Once answered:
- Restate the scoped question as a single sentence
- Confirm what is out of scope
- Note the intended consumer(s) — determines whether `audience_briefs` is required
- If sub-topics were identified, note that each requires a separate `/gators` invocation; proceed with the one confirmed topic only

---

## Step 2 — Derive the Folder Name

Derive a **PascalCase** folder name (no hyphens, underscores, or spaces; 2–5 words).
Examples: `AwsIamPrivilegeEscalation`, `LlmContextWindows`, `RustAsyncPatterns`

Show the proposed name to the user. Adjust if they object.

```bash
mkdir /Users/samfakhreddine/repos/research/<PascalCaseName>
```

---

## Step 3 — Create the Task List

Create the following three tasks before spawning any teammate:

```json
[
  {
    "id": "investigate",
    "description": "Research the scoped question and write investigation.json. Run json_to_md.py and check_sync.py. Both must exit 0 before marking complete.",
    "status": "pending"
  },
  {
    "id": "validate",
    "description": "Fact-check investigation.json. Run check_sync.py first and paste its stdout into the report. Verify every source URL. Spot-check high-stakes factual claims. Write validation_report.md.",
    "status": "pending",
    "dependsOn": ["investigate"]
  },
  {
    "id": "arbitrate",
    "description": "Independently verify any disputed claims still outstanding after the first correction cycle. Read investigation.json and validation_report.md. For each disputed item, independently verify using live sources. Cast SUSTAINED or OVERTURNED per item. Write arbiter_verdict.md.",
    "status": "pending",
    "dependsOn": ["validate"]
  }
]
```

The `arbitrate` task only activates if disputes remain after cycle 1 (see Step 6).

---

## Step 4 — Spawn the Investigator Teammate

Claim the `investigate` task, then spawn the investigator teammate.

Include the full contents of `templates/agent_persona.md` verbatim as the system persona. Do not summarize or paraphrase it — pass it in full. Append this task context:

```
---

## Your Task

Investigation folder: /Users/samfakhreddine/repos/research/<PascalCaseName>

Scoped question: <the confirmed one-sentence question>

Out of scope: <what the user said is out of scope>

Intended consumer(s): <Engineer | Engineering Leadership | Product Owner/EM | combination>

Audience briefs required: <YES if technical (infra, security, config, operational risk). NO if non-technical (market, financial, historical, organizational).>

## What to do

1. Research the scoped question using live sources.
2. Write investigation.json to the investigation folder. The JSON is the only file you author.
3. Run: python3 /Users/samfakhreddine/repos/research/scripts/json_to_md.py <investigation_folder>
4. Run: python3 /Users/samfakhreddine/repos/research/scripts/check_sync.py <investigation_folder>
   - Exit 0 = IN_SYNC — done.
   - Exit 1 = OUT_OF_SYNC — re-run json_to_md.py then check_sync.py.
   - Exit 2 = error — fix the underlying issue before continuing.
5. Do not return until check_sync.py exits 0.

Trust boundary: no embedded newlines in single-value fields, no unescaped pipes in table cells, no non-http(s) source URLs, no concept names beginning with #.
```

Wait for the investigator to complete before proceeding.

---

## Step 5 — Spawn the Validator Teammate

Once `investigation.json` exists, claim the `validate` task and spawn the validator teammate.

Include the full contents of `templates/validator_persona.md` verbatim. Append this task context:

```
---

## Your Task

Investigation folder: /Users/samfakhreddine/repos/research/<PascalCaseName>

investigation.json path: /Users/samfakhreddine/repos/research/<PascalCaseName>/investigation.json

## What to do

1. Run check_sync.py first:
   python3 /Users/samfakhreddine/repos/research/scripts/check_sync.py <investigation_folder>
   Paste full stdout into the JSON/MD Sync Check section of your report.
   If check_sync.py exits non-zero, note it and do not proceed to LLM verification.

2. Read investigation.json (authoritative — not investigation.md).

3. Verify every URL in the sources array: VERIFIED | REDIRECT | DEAD | UNVERIFIABLE.

4. Spot-check high-stakes factual claims against live documentation or web search.
   Assign: CONFIRMED | PARTIALLY CONFIRMED | UNVERIFIED | CONTRADICTED.
   Record evidence and the source used for each verdict.

5. Write validation_report.md to the investigation folder.

6. Do not add findings, expand scope, or suggest further research — only verify what was claimed.
```

Wait for the validator to complete before proceeding.

---

## Step 6 — Evaluator-Optimizer Loop with Arbiter Voting

After the validator completes, the lead reads `validation_report.md` and applies the following decision tree.

### Remediation rules (cycle 1)

| Verdict | Action |
|---------|--------|
| `CONTRADICTED` | Re-spawn investigator with the specific claim and contradicting evidence |
| `UNVERIFIED` (material claim) | Re-spawn investigator to correct or move to `open_questions` |
| `UNVERIFIED` (peripheral claim) | No re-spawn — add a note in `open_questions` |
| `PARTIALLY CONFIRMED` | Re-spawn investigator to narrow the claim to only what was confirmed |
| `DEAD` source | Re-spawn investigator to replace or remove the source |
| `REDIRECT` source | Re-spawn investigator to update the URL in `investigation.json` |
| `OUT_OF_SYNC` | Re-spawn investigator to re-run `json_to_md.py` and `check_sync.py` |

Re-spawn the investigator with the full persona plus corrective context. Then re-spawn the validator. This is **cycle 1**.

### After cycle 1 — arbiter vote

If any `CONTRADICTED` or material `UNVERIFIED` verdicts **still remain** after the investigator's correction and validator's re-check, activate the `arbitrate` task and spawn the Arbiter teammate.

The Arbiter spawn prompt:

```
You are an independent research arbiter. Your role is to break a factual dispute between an investigator and a validator. You have no prior position — you verify each disputed claim from scratch using live sources.

---

## Your Task

Investigation folder: /Users/samfakhreddine/repos/research/<PascalCaseName>

Disputed items (from validation_report.md):
<paste the full list of remaining CONTRADICTED and material UNVERIFIED items here>

## What to do

1. Read investigation.json to understand the investigator's current claim for each disputed item.
2. Read validation_report.md to understand the validator's objection and the evidence they cited.
3. For each disputed item, independently search for evidence using web search and live documentation. Do not rely on either agent's sources — find your own.
4. Cast a binding vote for each item:
   - SUSTAINED — the validator was correct; the investigator's claim is wrong or unsupported
   - OVERTURNED — the investigator was correct; the validator's objection is wrong or the claim is supported

5. For each vote, record:
   - The claim as stated in investigation.json
   - The validator's objection
   - Your independent evidence
   - Your vote: SUSTAINED or OVERTURNED
   - One-sentence rationale

6. Write arbiter_verdict.md to the investigation folder using this format:

   # Arbiter Verdict

   ## Disputed Items

   ### [Finding or source title]
   **Investigator's claim:** <quote from investigation.json>
   **Validator's objection:** <quote from validation_report.md>
   **Arbiter's evidence:** <source title and URL>
   **Vote:** SUSTAINED | OVERTURNED
   **Rationale:** <one sentence>

   ## Summary
   - Sustained: <N>
   - Overturned: <N>

7. Do not add new findings or expand scope. Only rule on the items listed above.
```

### Acting on the arbiter's verdict

After `arbiter_verdict.md` is written:

| Arbiter vote | Action |
|--------------|--------|
| `SUSTAINED` | Investigator's claim is wrong — re-spawn investigator one final time to correct only the sustained items |
| `OVERTURNED` | Investigator's claim stands — no correction needed; validator's objection is dismissed |

After any final corrections from sustained items, re-run `json_to_md.py` and `check_sync.py`. No further validator re-check is required after arbiter ruling.

### Maximum cycles

- Cycle 1: investigator corrects → validator re-checks
- Cycle 2 (if still disputed): arbiter votes → investigator corrects sustained items only
- After cycle 2, the investigation is final. Note any remaining open issues in the synthesis.

---

## Step 7 — Lead Synthesis

Once the loop exits, produce this synthesis in chat:

```
## Investigation Complete: <Topic>

**Folder:** /Users/samfakhreddine/repos/research/<PascalCaseName>

**Files produced:**
- investigation.json (authoritative)
- investigation.md (generated)
- glossary.md (generated, if concepts were populated)
- brief_leadership.md (generated, if technical investigation)
- brief_po.md (generated, if technical investigation)
- validation_report.md
- arbiter_verdict.md (if disputes required arbitration)

**Validation summary:**
- Sources: <N verified> / <N total>, <N dead>, <N unverifiable>
- Findings: <N confirmed>, <N partially confirmed>, <N unverified>, <N contradicted>
- Correction cycles: <N>
- Arbiter invoked: YES (<N sustained>, <N overturned>) | NO
- Final sync status: IN_SYNC | OUT_OF_SYNC (note if unresolved)

**Key findings (top 3–5):**
<quote directly from key_findings in investigation.json>

**Open questions:**
<quote directly from open_questions in investigation.json>

**Unresolved issues (if any):**
<list anything remaining after all cycles>
```

The lead does not add new analysis or editorial commentary. All content quoted directly from `investigation.json`, `validation_report.md`, and `arbiter_verdict.md`.

---

## Agent Roles Summary

| Teammate | Produces | Triggers |
|----------|----------|---------|
| Investigator | `investigation.json` + generated markdown | Always — first |
| Validator | `validation_report.md` | Always — after investigator |
| Arbiter | `arbiter_verdict.md` | Only if disputes remain after cycle 1 |

---

## Quick-Reference: Script Exit Codes

| Script | Exit | Meaning | Recovery |
|--------|------|---------|----------|
| `json_to_md.py` | 0 | Success | — |
| `json_to_md.py` | 2 | Invalid JSON, missing required field, or I/O error | Fix `investigation.json`, re-run |
| `check_sync.py` | 0 | IN_SYNC | — |
| `check_sync.py` | 1 | OUT_OF_SYNC | Re-run `json_to_md.py`, then `check_sync.py` |
| `check_sync.py` | 2 | Error (bad JSON or missing file) | Fix the underlying issue |

---

## Quick-Reference: Verdict Taxonomy

| Verdict | Who assigns | Meaning |
|---------|------------|---------|
| `VERIFIED` | Validator | URL resolves, content matches the claim |
| `REDIRECT` | Validator | URL resolves at a different address |
| `DEAD` | Validator | 404 or unreachable |
| `UNVERIFIABLE` | Validator | Blocked, paywalled, or login required |
| `CONFIRMED` | Validator | Claim supported by live source |
| `PARTIALLY CONFIRMED` | Validator | Part of claim supported; part not |
| `UNVERIFIED` | Validator | Could not confirm or deny |
| `CONTRADICTED` | Validator | Claim contradicted by available evidence |
| `SUSTAINED` | Arbiter | Validator was correct — investigator must correct |
| `OVERTURNED` | Arbiter | Investigator was correct — validator's objection dismissed |
