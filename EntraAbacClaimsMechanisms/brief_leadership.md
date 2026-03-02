# Entra ID to IAM Identity Center ABAC Pipeline — Attribute Delivery, PrincipalTag Scope, and SSMSessionRunAs — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> SAML and SCIM are parallel attribute pipelines; SCIM silently wins on conflicts; SSMSessionRunAs is SAML-only; aws:PrincipalTag gates API access but cannot set OS identity

---

## So What

The Entra ID to IAM Identity Center ABAC pipeline has two distinct attribute delivery paths and two distinct enforcement layers. SAML carries custom attributes including SSMSessionRunAs at login time; SCIM continuously provisions a narrower attribute set from the identity store. When both paths carry the same key, SCIM overrides SAML — silently, with no console visibility. aws:PrincipalTag in permission set policies controls whether API calls (like StartSession) are permitted; SSMSessionRunAs controls which OS user the session runs as — these share the same STS session tag infrastructure but cannot substitute for each other. Architects must design explicitly for both layers.

---

## Key Points

- SCIM unconditionally overrides SAML on shared attribute keys — AWS-documented, not configurable, not surfaced in the IdC console
- SSMSessionRunAs must be delivered via the SAML claims path; SCIM cannot carry it because the AWS SCIM endpoint rejects schema extensions with HTTP 400
- aws:PrincipalTag in IAM policy Conditions gates StartSession API access; it does not and cannot influence which OS user SSM Agent assigns to the session
- SAML-delivered attributes have no visibility in the IdC console — the only audit surface is the Entra enterprise app Attributes and Claims configuration and CloudTrail AssumeRoleWithSAML events
- Stale SCIM values can override fresher SAML values when an Entra attribute changes between SCIM sync cycles — the winning path is also the lagging path
- Per-user OS identity at scale requires Linux usernames pre-provisioned on every managed instance — the tag flow is defined but the OS-side account provisioning is a separate operational requirement

---

## Action Required

> Architects must audit the full attribute key inventory: which keys are SAML-only (including SSMSessionRunAs), which are SCIM-sourced, and whether any key appears in both paths. Any overlap where SCIM is not the intended authoritative source must be resolved by removing the key from the IdC Attributes for Access Control console mapping.

---

*Full engineering investigation: [investigation.md](investigation.md)*
