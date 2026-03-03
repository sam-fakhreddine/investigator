# AWS SSM Just-in-Time Node Access (JITNA) — IAM Identity Center / Entra ID Federation and SSMSessionRunAs Compatibility — Product Brief

**Date:** 2026-03-02
**Risk Level:** LOW

---

## What Is This?

> AWS has a built-in JIT access approval workflow for Linux servers that works with Entra ID — no CyberArk needed — but one technical compatibility point needs a lab test before POs and EMs can commit a delivery timeline

---

## What Does This Mean for Us?

A developer who needs emergency prod access today must go through a manual process or rely on standing access. JITNA would let Architects configure an approval workflow where a developer requests access, an approver clicks approve in Slack or Teams, and the developer connects — all within the AWS console, no new tools. POs and EMs do not need to decide on CyberArk or build a custom approval system. The one open item is whether the team's existing per-user Linux account mapping (SSMSessionRunAs) continues to work inside JITNA sessions, which requires a lab test by the Windows/infra team before a timeline can be set.

---

## Key Points

- JITNA supports the team's existing Entra ID identity — no new SSO or directory work is needed for POs/EMs to understand
- Three approval modes are available out of the box: automatic (no approver needed), manual via Slack/Teams, or hard block — the right mode per environment can be decided by PO/EM with Architects
- Access is time-bound and logged for one year — audit and compliance requirements are addressed by the feature itself
- JITNA does not work across AWS accounts — if developers need access to nodes in a different account, JITNA alone cannot cover that path
- Cost is roughly $10/server/month for any server enrolled in JITNA — PO/EM should confirm which servers are in scope before budgeting
- No CyberArk license, no custom approval Lambda, no webhook plumbing — this is a managed AWS feature

---

## Next Steps

**PO/EM Decision:**

> PO/EM to decide which environments (dev, staging, prod) should require manual approval vs auto-approval, and confirm which server fleet should be enrolled in JITNA for cost estimation.

**Engineering Work Items:**
- Windows/infra team: run a proof-of-concept in a non-production account to confirm SSMSessionRunAs session tag functions correctly inside a JITNA-approved session with Entra ID federated credentials
- Architects: define approval policy structure per environment — which node tags map to auto-approve vs manual, and who the designated approvers are per team
- Architects: assess cross-account access gaps — identify any prod nodes in accounts other than the JITNA-enrolled account that would require an alternative access path

**Leadership Input Required:**

> Leadership to confirm whether the ~$10/node/month JITNA cost is acceptable across the target prod fleet, or whether a tiered rollout (only high-risk nodes enrolled) is preferred.

---

## Open Questions

- How many prod nodes would be enrolled in JITNA from day one, and how does that translate to monthly cost?
- Did the lab test confirm that SSMSessionRunAs works inside a JITNA session — or is the per-user Linux account mapping a blocker?
- Are any prod nodes in a different AWS account than the account where JITNA would be configured? If yes, what is the alternative access path?
- Which team members will be designated as JITNA approvers in Slack/Teams, and do they have the necessary IAM permissions to approve requests?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
