# IAM Role Consolidation Patterns Using Session Policies and IAM Identity Center — Product Brief

**Date:** 2026-03-02
**Risk Level:** MEDIUM

---

## What Is This?

> A popular AWS simplification pattern cannot be used through the standard enterprise login path — teams that want fewer IAM roles have two real options, both with documented limitations.

---

## What Does This Mean for Us?

Many AWS environments accumulate hundreds of IAM roles — one per team, application, or environment. The idea of consolidating to a few broad roles that restrict dynamically sounds appealing, but the enterprise login system (IAM Identity Center) does not expose the required lever at login time. PO/EMs commissioning access simplification work need to know which paths are actually viable so scope is set accurately.

---

## Key Points

- The dynamic session policy mechanism that enables broad-role consolidation works at the STS API level — but IAM Identity Center (the system employees use to log in) does not pass this parameter through to AWS.
- Option A — ABAC: Engineers configure user attributes (team, department, project) in Identity Center; policies on shared roles grant or deny access based on whether the user's attributes match the resource's tags. Fewer roles needed, but resource tagging must be consistent across accounts.
- Option B — Role chaining: Employees log in via Identity Center, then applications do a second role assumption with a scoped-down policy. Works technically but limits session length to 1 hour hard — even if the permission set allows up to 12 hours.
- Neither option restores the full dynamism of the raw STS pattern. Engineers requesting 'broad base role + dynamic scoping via Identity Center' should be informed that this combination is not natively supported.
- The current alternative that does work — separate permission sets per use case — restores simplicity at the IAM level but moves the management burden to permission set administration.

---

## Next Steps

**PO/EM Decision:**

> If an IAM consolidation initiative is in scope, PO/EM should confirm with the IAM platform team which mechanism — ABAC, role chaining, or separate permission sets — is being targeted, and verify that the chosen path's constraints (resource tagging discipline for ABAC, 1-hour session cap for chaining) are acceptable before the work is prioritized.

**Engineering Work Items:**
- IAM platform engineers: assess current resource tag coverage across accounts to determine ABAC viability
- IAM platform engineers: document which existing permission sets could be merged under an ABAC model and estimate tag remediation effort
- Architects: evaluate whether any workloads have session duration requirements exceeding 1 hour that would be broken by role chaining

**Leadership Input Required:**

> Decision required on whether to invest in ABAC infrastructure (tagging policy, tag compliance tooling) as a prerequisite to role consolidation, or to accept the current permission-set-per-use-case model as the operational baseline.

---

## Open Questions

- Which of the three consolidation approaches — ABAC, role chaining, or keeping separate permission sets — is being proposed, and why?
- What is the current resource tag coverage across accounts, and is there a tagging enforcement policy in place?
- Do any user-facing workloads or interactive sessions require sessions longer than 1 hour? If so, role chaining is off the table for those.
- What is the total number of permission sets today, and how many could realistically be collapsed under an ABAC model?
- Is there a plan to assess the blast radius if an ABAC condition is misconfigured on a broad permission set?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
