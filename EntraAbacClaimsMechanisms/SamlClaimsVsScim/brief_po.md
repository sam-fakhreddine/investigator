# SAML Claims vs SCIM Sync: ABAC Attribute Delivery Paths in Entra ID to IAM Identity Center — Product Brief

**Date:** 2026-03-02
**Risk Level:** HIGH

---

## What Is This?

> Two delivery paths for user attributes in AWS federation; SCIM wins conflicts silently; one attribute critical to OS-level session identity cannot use SCIM

---

## What Does This Mean for Us?

When Entra ID is federated to AWS, user attributes that control access decisions can flow via two channels: SAML (at login) or SCIM (background sync). These channels can conflict on the same attribute, and when they do, SCIM always wins — silently, with no alert to operators. One attribute in particular, SSMSessionRunAs, controls which OS user account a developer gets when connecting to a Linux server via AWS Session Manager. This attribute cannot be delivered through SCIM at all — AWS's sync endpoint does not support it. If it is not correctly wired through the SAML path, developers will not get the expected OS user on server connections.

---

## Key Points

- If SCIM and SAML both send the same attribute, SCIM always wins — no alert, no override visibility
- SSMSessionRunAs (the attribute that sets OS username for server sessions) is SAML-only; SCIM cannot deliver it
- SAML attributes are invisible in the AWS console — troubleshooting requires knowledge of what was configured in Entra
- SCIM sync can be stale — an attribute change in Entra may not reach AWS until the next sync cycle, while SAML always reflects current values

---

## Next Steps

**PO/EM Decision:**

> PO/EM should confirm with the Windows/infra team and IAM architects that SSMSessionRunAs is wired via the Entra SAML claims path and is not being inadvertently overridden by an identity store configuration for the same key.

**Engineering Work Items:**
- IAM/IdC architects: audit all Attributes for Access Control console mappings against the Entra SAML claims list; identify any key that appears in both and confirm the SCIM value is intentionally correct
- Windows/infra team: verify SSMSessionRunAs is configured as a SAML claim in the Entra enterprise app using the AccessControl:SSMSessionRunAs attribute name, and test that STS session tags reflect the expected OS username in CloudTrail
- IAM/IdC architects: document the attribute key inventory for ABAC — which keys are SAML-only, which are SCIM-sourced, and the expected value for each — so operators can audit without reverse-engineering Entra config

**Leadership Input Required:**

> Leadership should confirm whether the SCIM-wins-over-SAML precedence creates an acceptable operational risk for any attributes currently in both paths, or whether the architecture should be restructured to use a single delivery path per attribute key.

---

## Open Questions

- Which ABAC attribute keys are currently configured in both Entra SAML claims and the IdC Attributes for Access Control console, and are we aware that SCIM values win on those keys?
- Has SSMSessionRunAs been tested end-to-end from Entra attribute through STS principal tag to an actual Session Manager session — and does CloudTrail confirm the expected OS username appears in principalTags?
- What is the SCIM sync frequency, and how long does a stale SCIM attribute value persist before it reflects an Entra change — is this lag acceptable for access control decisions?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
