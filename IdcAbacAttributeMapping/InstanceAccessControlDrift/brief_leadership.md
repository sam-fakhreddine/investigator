# IAM Identity Center InstanceAccessControlAttributeConfiguration — Drift, Idempotency, and Update Behavior — Engineering Leadership Brief

**Date:** 2026-02-27

---

## Headline

> IAM Identity Center ABAC configuration managed via CloudFormation or CDK has no drift detection and a destructive default deletion behavior — a stack delete or pre-existing console-configured ABAC can silently break or block ABAC-dependent access with no automatic recovery path

---

## So What

If the team deploys ABAC configuration via IaC and that stack is ever deleted, ABAC is disabled immediately and all permission policies depending on principal tag matching stop working. There is no native CloudFormation mechanism to detect out-of-band changes — leadership must understand that owning this resource in IaC requires explicit guardrails that are off by default.

---

## Key Points

- Stack deletion calls the Delete API immediately — ABAC is disabled with no grace period and no automatic recovery.
- CloudFormation drift detection returns NOT_CHECKED for this resource — console or CLI changes after deployment are invisible to the pipeline.
- DeletionPolicy: Retain and stack termination protection are both off by default and must be explicitly set.
- If ABAC was previously enabled in the console before IaC deployment, the stack create will fail with ConflictException until the resource is imported.
- Changing the InstanceArn property causes resource replacement — the Delete API is called first, disabling ABAC before the new configuration is created.

---

## Action Required

> Approve a policy requiring DeletionPolicy: Retain and stack termination protection on all stacks containing this resource. Confirm which team owns the ABAC configuration stack and ensure no other pipeline deploys this resource against the same IdC instance.

---

*Full engineering investigation: [investigation.md](investigation.md)*
