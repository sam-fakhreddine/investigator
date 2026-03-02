# aws:PrincipalTag Condition Keys — Scope, Capabilities, and SSMSessionRunAs Influence — Product Brief

**Date:** 2026-03-02
**Risk Level:** MEDIUM

---

## What Is This?

> Entra ID user attributes can control both which servers a user can access and which Linux account they land as — but through two separate mechanisms

---

## What Does This Mean for Us?

The ABAC pipeline from Entra ID to AWS can enforce two distinct behaviors at the same time: (1) whether a user is allowed to start a session on a given server at all, and (2) which Linux OS user they become when they connect. Both flow from Entra ID attributes, but they work differently internally. PO/EM teams need to know that implementing per-user OS identity requires a specific attribute mapping step in IAM Identity Center — it is not automatic from having ABAC enabled.

---

## Key Points

- AWS engineers can configure Entra ID user attributes (like department or team) to control which EC2 instances each user is allowed to connect to via Session Manager
- A separate Entra ID attribute called SSMSessionRunAs can control which Linux username each user lands as when they connect — this is independent of the access permission check
- Both behaviors require specific setup: the Windows/infra team configures EC2 instance tags, and the IAM/Identity team configures attribute mappings in IAM Identity Center
- A user whose OS username does not exist on the target server will be denied a session — the Linux username must be pre-provisioned on every instance the user is permitted to access
- Users who legitimately need to operate as different OS users on different servers cannot be handled with this mechanism alone — that scenario requires a different architectural approach

---

## Next Steps

**PO/EM Decision:**

> PO/EM to confirm whether per-user OS identity (each engineer lands as their own Linux account) or shared OS identity (team or role lands as a shared Linux account) is the required model — this determines scope of infrastructure work.

**Engineering Work Items:**
- IAM/Identity team: map SSMSessionRunAs as an ABAC attribute in IAM Identity Center, sourced from the appropriate Entra ID user attribute
- Windows/infra team: tag all managed EC2 instances with department or team tags that match the ABAC attribute values used in permission set policies
- Linux/OS team: pre-provision named OS accounts on each managed instance for every user or role that will connect via Session Manager Run As
- IAM/Identity team: update permission set inline policies to gate ssm:StartSession via ssm:resourceTag conditions matching aws:PrincipalTag values

**Leadership Input Required:**

> Leadership to decide whether per-user OS identity is a compliance requirement (drives Linux account provisioning at scale) or a nice-to-have (shared OS account per team is simpler and may be sufficient).

---

## Open Questions

- Is IAM Identity Center ABAC already enabled for the accounts where Session Manager is used, or does that need to be turned on first?
- What Entra ID attribute currently holds the value we would use as the Linux username — is it the UPN, a custom attribute, or something else?
- How are Linux OS accounts currently provisioned on managed EC2 instances — is there an automated pipeline that could be extended to create per-user accounts?
- If a user's Entra ID attribute for SSMSessionRunAs changes (e.g., username change), how quickly does the change propagate to their next AWS session?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
