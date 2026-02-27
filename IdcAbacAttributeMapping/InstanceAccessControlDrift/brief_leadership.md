# IAM Identity Center InstanceAccessControlAttributeConfiguration — Drift, Idempotency, and Update Behavior — Engineering Leadership Brief

**Date:** 2026-02-27

---

## Headline

> IAM Identity Center ABAC configuration, when managed via CloudFormation or CDK, has no drift detection support and a destructive default deletion behavior — a stack delete or a pre-existing console-configured ABAC state can silently break or block ABAC-dependent access with no automatic recovery path.

---

## So What

If the team deploys ABAC configuration via IaC and that stack is ever deleted (intentionally or accidentally), ABAC is disabled immediately and all permission policies depending on principal tag matching stop working. There is no native CloudFormation mechanism to detect out-of-band changes. Leadership should understand that owning this resource in IaC requires explicit guardrails (DeletionPolicy: Retain, stack deletion protection) that are not set by default.

---

*Full engineering investigation: [investigation.md](investigation.md)*
