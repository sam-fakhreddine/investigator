# Entra ID to IAM Identity Center ABAC Pipeline — Attribute Delivery, PrincipalTag Scope, and SSMSessionRunAs — Product Brief

**Date:** 2026-03-02
**Risk Level:** HIGH

---

## What Is This?

> Two Entra ID attribute pipelines feed AWS access control; silent SCIM precedence and SAML-only OS identity require explicit engineering design choices

---

## What Does This Mean for Us?

When Entra ID is federated to AWS, user attributes flow through two channels: SAML (sent at each login) and SCIM (background sync). Both affect which AWS resources each user can access and which Linux account they land as on servers. When both channels carry the same attribute, SCIM always wins — with no warning to anyone. The attribute that sets a developer's OS username on managed servers (SSMSessionRunAs) can only travel through the SAML channel. If it is misconfigured or overridden, developers either get the wrong OS user or their session fails entirely. Separately, the Entra attribute pipeline can also restrict which servers a user is allowed to connect to — but this is a different control from the OS identity mechanism and requires server-side tagging work.

---

## Key Points

- If SCIM and SAML both carry the same user attribute, SCIM always wins — this is fixed AWS behavior with no opt-out and no alert when it happens
- The attribute that controls which Linux account a developer gets on a server (SSMSessionRunAs) can only be delivered through SAML — SCIM cannot carry it
- SAML attributes are invisible in the AWS console — neither engineers nor operators can see them from the AWS side without reading CloudTrail logs
- A mismatch between the Entra attribute value and the Linux account name pre-provisioned on the server causes the session to fail — both the IAM/IdC configuration and the OS-level account must be aligned
- Restricting which servers a user can access via Entra attributes and controlling which OS user they become are separate mechanisms that both require explicit configuration

---

## Next Steps

**PO/EM Decision:**

> PO/EM should confirm with the IAM/IdC architects that the full attribute key inventory has been audited — specifically which keys appear in both SAML claims and the IdC Attributes for Access Control console, and that no unintended SCIM precedence overrides exist for SSMSessionRunAs or other access-critical attributes.

**Engineering Work Items:**
- IAM/IdC architects: produce a full attribute key inventory listing each ABAC key, its delivery path (SAML-only, SCIM-only, or both), and the expected authoritative source — document any keys that appear in both paths
- IAM/IdC architects: verify SSMSessionRunAs is configured as a SAML claim in the Entra enterprise app using the AccessControl:SSMSessionRunAs attribute name, confirm no Attributes for Access Control mapping exists for the same key in the IdC console
- Windows/infra team: validate end-to-end — confirm CloudTrail AssumeRoleWithSAML events show the expected SSMSessionRunAs principal tag value for test users, and confirm Session Manager sessions start under the correct Linux OS user
- Linux/OS team: audit whether named OS accounts are pre-provisioned on all managed instances for each user or role expected to use SSMSessionRunAs — this is a prerequisite for the tag-based OS identity to work
- IAM/IdC architects: if ABAC enforcement on StartSession is required, ensure managed EC2 instances are tagged with department or team tags that match the ABAC session tag values used in permission set inline policies

**Leadership Input Required:**

> Leadership should confirm whether per-user OS identity (each engineer lands as their own named Linux account) is a compliance or security requirement. If yes, the Linux account provisioning at scale is a material infrastructure commitment that needs resourcing separate from the IAM/IdC configuration work.

---

## Open Questions

- Has the full ABAC attribute key inventory been documented — which keys are SAML-only, which are SCIM-sourced, and are any keys present in both paths where SCIM overriding SAML would be unintended?
- Has SSMSessionRunAs been tested end-to-end from the Entra attribute through STS principal tag to an actual Session Manager session — does CloudTrail confirm the expected OS username appears in principalTags on the AssumeRoleWithSAML event?
- What is the SCIM sync frequency, and how long can a stale SCIM attribute value persist before it reflects an Entra change — is that lag window acceptable for access control decisions?
- Are Linux OS accounts currently pre-provisioned on managed EC2 instances for each user who will connect via Session Manager Run As, and is there an automated pipeline to keep them current as team membership changes?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
