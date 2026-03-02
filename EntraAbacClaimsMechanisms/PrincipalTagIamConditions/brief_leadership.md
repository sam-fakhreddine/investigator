# aws:PrincipalTag Condition Keys — Scope, Capabilities, and SSMSessionRunAs Influence — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> aws:PrincipalTag gates API access; SSMSessionRunAs sets OS identity — they share infrastructure but are not interchangeable

---

## So What

The Entra ID → IAM Identity Center ABAC pipeline can deliver both API-layer access control and per-user OS identity mapping through the same session tag mechanism. These are two distinct effects of the same infrastructure, not a single unified control. Architects must design for both layers explicitly: permission set policies for API gating, and the SSMSessionRunAs attribute mapping for OS identity.

---

## Key Points

- aws:PrincipalTag in an IAM policy Condition can restrict which EC2/managed instances a user's StartSession call is permitted against, scoped by matching instance resource tags to the principal's session tags
- SSMSessionRunAs OS user selection is driven by SSM Agent reading the principal's tag context directly — it is not an IAM policy Condition effect and cannot be configured via a permission set inline policy Condition block
- End-to-end per-user OS identity mapping is feasible: Entra ID attribute → IAM Identity Center ABAC attribute mapping → STS session tag → SSM Agent reads SSMSessionRunAs tag → session starts as named Linux user
- IAM Identity Center automatically permits sts:TagSession in provisioned role trust policies, so session tag passthrough requires no manual trust policy changes for standard ABAC attribute mappings
- Multi-valued OS user assignments (one user, multiple possible OS identities) are not expressible in a single session tag — STS does not support multi-valued tags; this is a hard architectural constraint

---

## Action Required

> Architects designing per-user OS identity must configure SSMSessionRunAs as a mapped ABAC attribute in IAM Identity Center — not rely on aws:PrincipalTag Conditions in permission set policies, which cannot produce that effect.

---

*Full engineering investigation: [investigation.md](investigation.md)*
