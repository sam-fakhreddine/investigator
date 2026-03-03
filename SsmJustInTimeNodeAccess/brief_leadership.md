# AWS SSM Just-in-Time Node Access (JITNA) — IAM Identity Center / Entra ID Federation and SSMSessionRunAs Compatibility — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> AWS JITNA delivers Entra ID-compatible JIT access with Slack/Teams approvals, but SSMSessionRunAs compatibility requires empirical validation before production cutover

---

## So What

JITNA can replace CyberArk and custom approval workflows for Linux prod access, but the team's per-user OS identity mechanism (SSMSessionRunAs) is not explicitly confirmed to work inside JITNA sessions. A proof-of-concept validation is required before the team removes Session Manager permissions in production accounts.

---

## Key Points

- JITNA explicitly supports IAM Identity Center / Entra ID federated users as an identity source — no additional identity infrastructure is needed
- Approval models cover the full range: auto-approve (break-glass), manual with Slack/Teams notification, and explicit deny — eliminating the need for a custom approval system or CyberArk
- JITNA is same-account, same-region only — cross-account prod access requests cannot use JITNA and would still require an alternative path
- Cost is ~$9.86/node/month (first tier) billed on enrolled nodes regardless of access frequency — fleet size drives cost, not usage
- SSMSessionRunAs session tag compatibility is architecturally plausible but undocumented — validation in a non-production account is required before committing to full migration

---

## Action Required

> Approve a proof-of-concept in a non-production account to validate SSMSessionRunAs + JITNA session establishment with Entra ID federated credentials before authorizing production migration.

---

*Full engineering investigation: [investigation.md](investigation.md)*
