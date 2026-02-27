# How We Built a Research Intelligence System in One Afternoon

*A behind-the-scenes look at building a verified AI research engine — through iteration, mistakes, and a few smart shortcuts.*

---

## The Problem That Started Everything

It started with a practical headache: Windows servers in AWS were burning CPU. The culprit was Microsoft Defender — the built-in security scanner — aggressively scanning log files being written by three agents we run on every server: Amazon CloudWatch, AWS Systems Manager, and Rapid7.

The fix was known in principle: add folder exclusions to tell Defender to leave those directories alone. But the details were scattered everywhere. AWS documentation. Rapid7 documentation. Microsoft's own guidance. Security advisories. No single source of truth.

The instinct was to just Google it and piece together an answer. But that raises an obvious question: how do you know what you find is accurate? How do you know the paths are right? How do you know you're not introducing a security risk by excluding the wrong things?

That's where this system came from.

---

## Step 1: The First Investigation

The first thing we did was ask an AI agent to go research the question properly. Not summarise from memory — actually go and read the live documentation, cross-reference sources, and come back with structured findings.

We gave the agent a clear brief:
- What are the documented exclusion paths for CloudWatch, SSM, and Rapid7?
- What does Microsoft say about the risks of adding exclusions?
- Are there known ways attackers exploit exclusion configurations?

About 15 minutes later, we had a rich research document — 36 findings, 23 cited sources, a full breakdown of tensions and tradeoffs, and a list of open questions the research couldn't answer.

It was genuinely impressive. Paths were documented. Security implications were explained. Attack vectors were named with MITRE ATT&CK technique IDs.

But here was the problem: **how much of it was actually right?**

---

## Step 2: We Discovered We Needed a Fact-Checker

Reading through the findings, most of it looked solid. But "looked solid" isn't the same as "is correct." The agent had done its best, but AI systems can confidently state things that turn out to be slightly wrong. Paths with one folder name swapped. Malware behaviour attributed to the wrong variant. A source URL that no longer exists.

Any of those errors, if acted on, could mean misconfigured servers or a false sense of security.

So we built a second agent: a **Validator**. Its only job was to go back and check the work. Not add new findings. Not rewrite anything. Just verify:

- Is every source URL real and accessible?
- Does the page actually say what the investigation claims?
- Are the file paths correct?
- Are the attack technique descriptions accurate?

The Validator ran through all 23 sources and spot-checked the key claims. It found two material errors:

**Error 1 — CloudWatch log path was wrong.** The investigation said the log file lived in `C:\Program Files\Amazon\AmazonCloudWatchAgent\Logs\`. The actual path is `C:\ProgramData\Amazon\AmazonCloudWatchAgent\Logs\`. One folder name different. If you had configured your exclusion based on the original, it wouldn't have applied to the log file at all. The CPU problem would have persisted.

**Error 2 — WhisperGate malware detail was inaccurate.** The investigation described a specific folder path that WhisperGate (a destructive piece of malware) used to evade antivirus scanning. When the Validator checked the primary sources — CISA's official advisory, MITRE ATT&CK, independent security research — they all documented a different path. The original claim couldn't be verified.

Both errors were corrected. The investigation was updated. The Validator ran again. Clean.

This was the moment we knew: **every investigation needs a Validator, every time, no exceptions.**

---

## Step 3: Turning a One-Off into a System

At this point we had done one investigation well. But we'd done it somewhat ad-hoc — decisions made on the fly, no consistent structure, no guarantee the next investigation would follow the same quality bar.

So we started writing down the rules.

We created a file called `CLAUDE.md` that lives at the root of the project. Think of it as the operating manual — it tells the AI exactly how this system works and what the standards are. Every investigation follows the same structure. Every investigation gets validated. Validation is not optional.

We also created **persona templates** — detailed briefs that define how each type of agent should behave:

- The **Investigator** persona: research only, no problem-solving, no code, no recommendations — pure analysis
- The **Validator** persona: verify only, no new findings, every verdict backed by a source

Having these written down meant any future investigation would follow the same rules automatically. The system could run consistently without someone manually supervising each step.

---

## Step 4: The Naming Convention Argument

Small things matter when you're building something you'll use for a long time.

We needed a convention for naming investigation folders. This sounds trivial but if you've ever worked in a shared repository where half the folders are named `my-thing`, `MyThing`, `my_thing_v2`, and `Untitled`, you know it becomes a mess fast.

We looked at four options:

- `kebab-case` — all lowercase, hyphens
- `snake_case` — all lowercase, underscores
- `dot.notation` — dots as separators
- `PascalCase` — capitalised words, no separators

**PascalCase** was chosen. `MsDefenderAwsExclusions`. `AwsIamPrivilegeEscalation`. Clean, readable, consistent.

One rule, decided once, written down. Every investigation from here will use it.

---

## Step 5: The Scope Problem

We noticed a pattern: vague questions produce vague investigations. If you ask "tell me about cloud security" you'll get a document that's a mile wide and an inch deep. Not useful.

So we added a **scope gate** — a mandatory set of questions that get asked before any investigation starts:

1. What is the single core question? Can it be stated in one sentence?
2. What is explicitly out of scope?
3. Who is going to use the findings?
4. Are there sub-topics that should be separate investigations?

This forces precision upfront. A narrowly defined question produces deep, trustworthy findings. A broad question gets split into focused sub-investigations.

---

## Step 6: The Token Problem (and the Smart Fix)

Here's where things got interesting from a systems design perspective — and where a non-technical reader can learn something genuinely useful about how AI systems work.

Every AI conversation costs something. Not in the traditional sense — but in terms of what the AI can hold in its head at once. Think of it like working memory. The more you ask it to juggle simultaneously, the more chance something gets dropped or done sloppily.

We had a quality check built into the Validator: compare the research document (a nicely formatted human-readable file) against the structured data file (a machine-readable version of the same content) to make sure they matched. If someone updated one and forgot to update the other, the Validator would catch it.

The problem: we were asking the AI to do this comparison manually. Read both files, compare every field, report differences. That's a lot of working memory spent on a task that is — at its core — just checking whether two pieces of text are the same.

A human pointed this out: *"comparing can be done by a script, not tokens."*

That was the right call. We wrote a small Python script — about 100 lines of code — that does the comparison automatically. It reads both files, normalises the text (removes formatting differences that don't affect meaning), hashes the content, and compares. It reports exactly which fields match and which don't. Takes a fraction of a second. Zero AI working memory used.

The principle here is important: **use AI for things that require reasoning. Use scripts for things that are deterministic.** Blending the two is where the real efficiency comes from.

---

## Step 7: One Source of Truth

The normalisation script led us to an even cleaner solution.

We were maintaining two versions of every investigation: the human-readable markdown document and the machine-readable structured file. Both had to stay in sync. Any time the AI updated one, it had to remember to update the other.

The better approach: **the AI writes the structured file only. The markdown is generated by a script.**

Now there's only one thing to write and only one thing that can contain errors. The readable document is always derived from the structured data. Drift is impossible.

This is a well-established principle in software engineering — have one source of truth, generate everything else from it. We applied it here.

---

## Step 8: The Answer Should Come First

We noticed something when we looked at the generated documents: the answer was buried.

The document started with metadata, then a question statement, then context, then dozens of findings. By the time you got to "here are the actual folders to exclude," you'd read several pages.

That's backwards. The person opening this document probably wants to know: *what do I actually do?*

So we added a rule: every investigation that has a concrete actionable output — a list of folders, a set of decisions, a configuration table — must put that at the very top. Before the question, before the context, before the findings. The rest of the document is the evidence. The table is the answer.

Open any completed investigation now and the first thing you see is a table that tells you exactly what to do. Everything below it explains why.

---

## Step 9: Making the Hard Work Usable

Research findings are only useful if someone acts on them. We had a rich investigation. We had a validated fact-check. What we also had was a list of things the research couldn't answer — questions that require either hands-on testing or further deep-diving.

The key was not to let those sit as vague notes at the bottom of a document. We structured them as explicit handoffs — precise enough that an engineer or a follow-on investigation can pick one up without needing to re-read the full investigation to understand why it matters.

Some open questions become follow-on investigations in their own right, scoped tightly and run through the same pipeline. Others are empirical questions that only a human with access to the actual environment can answer — a test server, a live process, a real patch window. Those get captured clearly enough that when the right person sits down, they know exactly what to do and why.

---

## Step 10: Audience-Specific Briefs

We had a working system — but we noticed the research document itself wasn't well-suited to all the people who needed to act on it.

A Platform Engineering PO received a deep investigation and panicked. It was too technical, too detailed, too risk-heavy for someone who just needed to know: *should we do this work, or not?*

So we added a new layer: **audience-specific briefs**, generated from the same structured research data:

- **Engineering brief** — the full investigation, unchanged. Dense, technical, complete.
- **Leadership brief** — impact, risk, and decisions. What architects and senior ICs need to weigh in on. No mechanics.
- **Product brief** — plain English. Risk level badge. What the PO/EM needs to decide and assign. Zero jargon.

Each brief is generated from the same JSON source, but tailored to a different reader. A PO now gets a 2-page document with "Your Call", "Work to Assign", and "Leadership Input Required" sections. Leadership gets the risk and architectural implications without implementation details.

The insights are identical. The presentation matches the role.

---

## Step 11: Making Briefs Actually Usable

After iteration with the PO team, we found that even the tailored briefs had problems:

- Generic pronouns ("they", "your team", "you") made it unclear who actually had to do something
- Language like "the fix is ready" violated the core principle — investigations surface findings, they never claim solutions are done
- "Questions to ask engineering" implied the PO was external, not embedded in the team

So we added explicit rules:

- **Name every actor.** Write "Windows/infra team", "Architects", "PO/EM" — never "they" or "you"
- **Never claim work is complete.** Investigations scope what needs to happen. Implementation is always separate and always still ahead.
- **Match the org structure.** The brief reflects how work actually flows: PO decides and assigns, Leadership advises on hard tradeoffs, specific teams execute.

A brief now shows exactly who does what, in explicit order, with no ambiguity.

---

## Step 12: Writing It Up for Everyone Else

By this point the system was genuinely mature — but it only made sense to someone who had been in the room for the iterations.

We wrote two final documents:

**A README** — for anyone who might use this system. Non-technical, benefits-forward, explaining what investigations produce and how to read one.

**This document** — the build story. Because the process of getting here is as valuable as the system itself. Every iteration happened because something wasn't good enough yet. The fact-checker was added because we couldn't trust the first pass. The script was added because we were wasting AI working memory on something a computer can do faster and cheaper. The answer-first principle was added because the documents were useful but not immediately usable. The briefs were added because different readers needed different outputs. The explicit naming was added because ambiguity meant mistakes.

---

## What We Actually Built

Standing back, what exists now is a small but rigorous research pipeline:

1. A question comes in
2. Scoping questions narrow it to something answerable
3. A research agent investigates from live sources (using a detailed persona that defines what good research means)
4. A sync script verifies the investigation's two output formats match (JSON is authoritative, markdown is derived)
5. A validation agent fact-checks every source and key claim against live documentation
6. Errors are corrected using a clear remediation table (no vague "fix it" — specific discrepancies named)
7. The final documents lead with actionable outputs: a quick reference table, then findings, then concepts and tensions
8. Three audience-specific briefs are generated from the same JSON: technical (engineers), strategic (leadership), and tactical (PO/EM)
9. Each brief names explicit actors and roles (Windows/infra team, Architects, PO/EM) — no ambiguous pronouns
10. Open questions become explicit handoffs — precise enough to pick up without re-reading the investigation
11. Everything is permanently stored and findable

The total build time was one afternoon. The system will run every future investigation at the same quality bar, automatically, without needing to re-establish any of these rules. Most importantly, the system evolves — each iteration adds exactly what was missing and reflects how the org actually works.

---

## The Bigger Lesson

The system we built is genuinely useful. But the more transferable insight is the **process** we used to build it.

We didn't design the perfect system upfront. We ran it once, found the problems, and fixed them. Then ran it again. Each iteration added exactly what was missing and nothing more.

The fact-checker wasn't planned — it was added because we realised we couldn't trust unverified findings. 

The script wasn't planned — it was added because we noticed we were using AI for something a computer does better. 

The answer-first principle wasn't planned — it was added because the documents were hard to use.

Every good system looks inevitable in hindsight. In practice, it's iteration all the way down.

---

*This system was built in a single session using Claude Code. The investigation, validation, scripts, templates, and all documentation in this repository were produced collaboratively through conversation — no pre-existing framework, no imported libraries beyond Python's standard library, no external dependencies.*
