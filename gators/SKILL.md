# Skill: /gators

Runs a full investigation pipeline for a given topic using an agent team. The lead session scopes the question, creates the investigation folder, spawns an investigator teammate and a validator teammate, monitors remediation cycles, and synthesizes the final output.

## Invocation

```
/gators <topic>
```

`<topic>` may be a phrase, sentence, or rough area. The lead will narrow it through the scope gate before any agent is spawned.

---

## Prerequisites

This skill requires the Claude Code experimental agent teams feature:

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

If this environment variable is not set, the skill cannot spawn teammate agents. Inform the user before proceeding:

> Agent teams are required for this skill. Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your environment and re-invoke `/gators`.

Do not proceed past the scope gate if the variable is not set.

---

## Lead Session Responsibilities

The lead session is the **orchestrator and synthesizer only**. It must never:
- Do raw research itself
- Write `investigation.json` or `validation_report.md` directly
- Run scripts on behalf of a teammate that has not yet been spawned

The lead creates the task list, spawns teammates, monitors outputs, drives the remediation loop, and produces the final synthesis. All research and verification happens inside spawned teammates.

---

## Step 1 — Scope Gate

Before creating any folder or spawning any agent, the lead must ask the user the following four questions. Present them together as a single prompt. Do not proceed until all four are answered.

```
Before I start the investigation, I need to scope it precisely:

1. What is the single core question? State it in one sentence. If it cannot be stated in one sentence, we should split it into separate investigations.
2. What is explicitly out of scope? Name at least one related area this investigation will not cover.
3. Who is the intended consumer of the findings? (Engineer, Engineering Leadership, Product Owner / EM, or some combination)
4. Are there known sub-topics that each warrant a separate investigation? If yes, list them — each gets its own folder rather than being rolled into this one.
```

Once the user answers:
- Restate the scoped question as a single sentence
- Confirm what is out of scope
- Note the intended consumer(s) — this determines whether `audience_briefs` is required in the JSON
- If sub-topics were identified, note that each will require a separate `/gators` invocation; proceed with the one confirmed topic only

Do not proceed until the scoped question is confirmed by the user.

---

## Step 2 — Derive the Folder Name

From the confirmed scoped question, derive a **PascalCase** folder name. Rules:
- No hyphens, underscores, or spaces
- Concatenate meaningful words with the first letter of each word capitalized
- Keep it short (2–5 words is ideal)
- Examples: `AwsIamPrivilegeEscalation`, `LlmContextWindows`, `RustAsyncPatterns`

Show the proposed folder name to the user before creating it. If they object, adjust.

Create the folder:

```bash
mkdir /Users/samfakhreddine/repos/research/<PascalCaseName>
```

---

## Step 3 — Create the Task List

The lead creates the following task list at the start of the run. Both tasks must exist before either teammate is spawned.

```json
[
  {
    "id": "investigate",
    "description": "Research the scoped question and write investigation.json to the investigation folder. Run python3 scripts/json_to_md.py <folder> and python3 scripts/check_sync.py <folder>. Both must exit 0 before marking this task complete. Do not return partial findings.",
    "status": "pending"
  },
  {
    "id": "validate",
    "description": "Fact-check investigation.json. Run python3 scripts/check_sync.py <folder> first and paste its stdout into the report. Verify every source URL. Spot-check high-stakes factual claims. Write validation_report.md to the investigation folder. check_sync.py must pass before you begin any LLM-based verification.",
    "status": "pending",
    "dependsOn": ["investigate"]
  }
]
```

---

## Step 4 — Spawn the Investigator Teammate

Claim the `investigate` task, then spawn the investigator teammate.

The teammate's spawn prompt must include the full contents of `templates/agent_persona.md` verbatim as the system persona, followed by the task context below. Do not summarize or paraphrase the persona — pass it in full.

Append this task context after the persona:

```
---

## Your Task

Investigation folder: /Users/samfakhreddine/repos/research/<PascalCaseName>

Scoped question: <the confirmed one-sentence question>

Out of scope: <what the user said is out of scope>

Intended consumer(s): <Engineer | Engineering Leadership | Product Owner/EM | combination>

Audience briefs required: <YES if the investigation is technical (infra, security, config, operational risk) — include audience_briefs in investigation.json. NO if non-technical (market, financial, historical, organizational) — omit audience_briefs entirely.>

## What to do

1. Research the scoped question using live sources.
2. Write investigation.json to the investigation folder listed above. The JSON is the only file you author — never write investigation.md directly.
3. Run: python3 /Users/samfakhreddine/repos/research/scripts/json_to_md.py <investigation_folder>
   - If this exits non-zero, fix the error in investigation.json and re-run.
4. Run: python3 /Users/samfakhreddine/repos/research/scripts/check_sync.py <investigation_folder>
   - Exit 0 = IN_SYNC — you are done.
   - Exit 1 = OUT_OF_SYNC — re-run json_to_md.py then check_sync.py again.
   - Exit 2 = error — fix the underlying issue (invalid JSON or missing file) before continuing.
5. Do not mark this task complete and do not return until check_sync.py exits 0.

Adhere strictly to the trust boundary rules in your persona: no embedded newlines in single-value fields, no pipe characters unescaped in table cells, no non-http(s) source URLs, no concept names beginning with #.
```

---

## Step 5 — Spawn the Validator Teammate

Once the `investigate` task is marked complete and `investigation.json` exists, claim the `validate` task and spawn the validator teammate.

The teammate's spawn prompt must include the full contents of `templates/validator_persona.md` verbatim as the system persona, followed by the task context below. Do not summarize or paraphrase the persona — pass it in full.

Append this task context after the persona:

```
---

## Your Task

Investigation folder: /Users/samfakhreddine/repos/research/<PascalCaseName>

investigation.json path: /Users/samfakhreddine/repos/research/<PascalCaseName>/investigation.json

## What to do

1. Run check_sync.py first — zero LLM tokens before sync is confirmed:
   python3 /Users/samfakhreddine/repos/research/scripts/check_sync.py <investigation_folder>
   Paste the full stdout into the JSON/MD Sync Check section of your report.
   If check_sync.py exits non-zero, note it in the report and do not proceed to LLM verification.

2. Read investigation.json (the authoritative input — not investigation.md).

3. Verify every URL in the sources array: VERIFIED | REDIRECT | DEAD | UNVERIFIABLE.
   If a source is inaccessible, attempt an alternative route (search by title, search for the claim) before marking it UNVERIFIABLE.

4. Spot-check high-stakes factual claims (file paths, binary names, version numbers, technique identifiers, attributed behaviors) against live documentation or web search.
   Assign: CONFIRMED | PARTIALLY CONFIRMED | UNVERIFIED | CONTRADICTED.
   Record evidence and the source used for each verdict.

5. Write validation_report.md to the investigation folder. Use the report format defined in your persona exactly.

6. Do not add new findings, expand scope, or suggest further research — only verify what was claimed.
```

---

## Step 6 — Evaluator-Optimizer Loop

After the validator teammate completes, the lead reads `validation_report.md` and evaluates the remediation table.

### Remediation rules

| Verdict | Action |
|---------|--------|
| `CONTRADICTED` | Must be corrected — re-open the `investigate` task (see below) |
| `UNVERIFIED` (material claim) | Must be corrected or downgraded to `open_questions` — re-open the `investigate` task |
| `UNVERIFIED` (peripheral claim) | May remain — add a note in `open_questions`; no re-spawn required |
| `PARTIALLY CONFIRMED` | Investigator must narrow the claim to only what was confirmed — re-open the `investigate` task |
| `DEAD` source | Must be replaced with an accessible equivalent or removed — re-open the `investigate` task |
| `REDIRECT` source | Update URL in `investigation.json`, re-run `json_to_md.py` — re-open the `investigate` task for this targeted fix |
| `OUT_OF_SYNC` | Re-run `json_to_md.py` — re-open the `investigate` task for this targeted fix |

### If remediation is required

Re-open the `investigate` task with status `pending` and spawn the investigator teammate again. The corrective spawn prompt must:

1. Include the full `templates/agent_persona.md` persona verbatim (as before)
2. Append the following corrective task context:

```
---

## Corrective Task — Cycle <N>

Investigation folder: /Users/samfakhreddine/repos/research/<PascalCaseName>

The validator found the following issues that require correction. Address only the listed items — do not re-research sections that are not listed.

Issues to correct:
<paste the full Remediation Required table from validation_report.md here>

For each issue:
- CONTRADICTED: locate the claim in investigation.json, correct it to match the evidence cited by the validator, cite a corrected source if needed.
- UNVERIFIED (material): correct the claim with a source or move it to open_questions.
- PARTIALLY CONFIRMED: narrow the claim in investigation.json to only the scope that was confirmed.
- DEAD source: find an accessible equivalent and update the url in investigation.json, or remove the source entry.
- REDIRECT source: update the url field in investigation.json to the redirect target.
- OUT_OF_SYNC: this is resolved by re-running the scripts — no change to investigation.json content needed unless a field is actually wrong.

After making corrections:
1. Run: python3 /Users/samfakhreddine/repos/research/scripts/json_to_md.py <investigation_folder>
2. Run: python3 /Users/samfakhreddine/repos/research/scripts/check_sync.py <investigation_folder>
   Must exit 0. If it exits 1, re-run json_to_md.py. If it exits 2, fix the underlying error.
3. Do not mark complete until check_sync.py exits 0.
```

After the investigator completes the correction, re-spawn the validator (full persona + task context) to re-check the affected items. The validator writes an updated `validation_report.md`, overwriting the previous one.

### Maximum correction cycles

The loop runs a maximum of **3 correction cycles**. After 3 cycles:
- If material issues remain, the lead notes them in the final synthesis as unresolved and flags them clearly to the user
- The investigation is marked `status: "in_progress"` in `investigation.json` (the lead re-opens the investigate task one final time to update this field only, then re-runs the scripts)

### Loop exit condition

Exit the loop when:
- The validator's remediation table is empty (no items requiring action), OR
- The only remaining items are peripheral `UNVERIFIED` findings that the validator has confirmed may remain in `open_questions`, OR
- 3 correction cycles have been exhausted

---

## Step 7 — Lead Synthesis

Once the loop exits cleanly (or is exhausted), the lead reads all final output files and produces a synthesis in the chat:

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

**Validation summary:**
- Sources: <N verified> / <N total> verified, <N dead>, <N unverifiable>
- Findings spot-checked: <N confirmed>, <N partially confirmed>, <N unverified>, <N contradicted>
- Correction cycles: <N>
- Final sync status: IN_SYNC / OUT_OF_SYNC (note if unresolved)

**Key findings (top 3–5):**
<bullet list drawn from key_findings in investigation.json — do not paraphrase, quote directly>

**Open questions:**
<bullet list drawn from open_questions in investigation.json>

**Unresolved validation issues (if any):**
<list any items that remain after exhausting correction cycles>
```

The lead does not add new analysis, new findings, or editorial commentary. The synthesis quotes directly from `investigation.json` and reports verdicts from `validation_report.md`.

---

## File Layout Reference

```
/Users/samfakhreddine/repos/research/
  scripts/
    json_to_md.py          # Generates all markdown from investigation.json
    check_sync.py          # Verifies JSON and markdown are in sync
  templates/
    agent_persona.md       # Full system prompt for the investigator teammate
    validator_persona.md   # Full system prompt for the validator teammate

  <PascalCaseName>/        # Created by lead at Step 2
    investigation.json     # Written by investigator teammate
    investigation.md       # Generated by json_to_md.py
    glossary.md            # Generated (when concepts list is non-empty)
    brief_leadership.md    # Generated (technical investigations only)
    brief_po.md            # Generated (technical investigations only)
    validation_report.md   # Written by validator teammate
```

---

## Quick-Reference: Script Exit Codes

| Script | Exit | Meaning | Recovery |
|--------|------|---------|----------|
| `json_to_md.py` | 0 | Success | — |
| `json_to_md.py` | 2 | Invalid JSON, missing required field, or I/O error | Fix `investigation.json`, re-run |
| `check_sync.py` | 0 | IN_SYNC | — |
| `check_sync.py` | 1 | OUT_OF_SYNC (content drifted or brief file missing) | Re-run `json_to_md.py`, then `check_sync.py` |
| `check_sync.py` | 2 | Error (bad JSON or missing file) | Fix the underlying issue before checking sync |

---

## Quick-Reference: Verdict Taxonomy

### Source verdicts (validator)
| Verdict | Meaning |
|---------|---------|
| `VERIFIED` | URL resolves, title and content match the claim |
| `REDIRECT` | URL resolves but at a different address |
| `DEAD` | 404 or unreachable |
| `UNVERIFIABLE` | Blocked, paywalled, or login required |

### Finding verdicts (validator)
| Verdict | Meaning |
|---------|---------|
| `CONFIRMED` | Claim is supported by live documentation or a reliable source |
| `PARTIALLY CONFIRMED` | Part of the claim is supported; part is not |
| `UNVERIFIED` | Could not be confirmed or denied — no source found |
| `CONTRADICTED` | Claim is contradicted by available evidence |
