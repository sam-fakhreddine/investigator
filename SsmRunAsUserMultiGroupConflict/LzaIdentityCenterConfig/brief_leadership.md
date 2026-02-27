# LZA identityCenter Config Block — Declarative Surface, Limits, and ABAC Gap — Engineering Leadership Brief

**Date:** 2026-02-27

---

## Headline

> LZA declaratively manages permission sets and assignments but has a confirmed gap: the ABAC attribute configuration that enables the SSMSessionRunAs session-tag pipeline is entirely outside LZA's scope and has no IaC owner today.

---

## So What

LZA provides solid coverage of permission set policy content and account assignment topology, but the 'Attributes for Access Control' setting — the IdC instance-level config that maps user attributes to session tags — is not managed by LZA in any version. If no supplemental IaC (Terraform, CloudFormation) owns this resource, it exists only in the IdC control plane with no version history, no code review, and no drift detection. For any organization using ABAC to drive SSM RunAs access, this is a config drift risk.

---

## Key Points

- LZA manages permission sets (policies, session duration, permissions boundaries) and assignments (group/user to permission set to account/OU) — these are well-covered and idempotent on every pipeline run.
- relay state per permission set is not a supported LZA field — must be set via console or aws ssoadmin CLI if required.
- ABAC (Attributes for Access Control) — the instance-level configuration mapping Entra user attributes to IAM session tags — is a confirmed LZA gap and must be managed via a separate IaC resource or manually via the IdC console.
- OU-scoped assignments cover direct child accounts only; nested OUs must be explicitly listed — a silent correctness gap if account hierarchy is not flat.
- Permission set updates do not immediately revoke active user sessions; credentials issued before a policy change remain valid until session duration expires (up to 12 hours).

---

## Action Required

> Engineering Leadership must decide: (1) whether a supplemental IaC tool (Terraform or CloudFormation) will own the IdC ABAC attribute configuration alongside the LZA config repo, and (2) whether the current OU-scoping behavior for assignments has been verified against the actual account hierarchy. The ABAC gap is the highest-priority item given its role in the SSMSessionRunAs pipeline.

---

*Full engineering investigation: [investigation.md](investigation.md)*
