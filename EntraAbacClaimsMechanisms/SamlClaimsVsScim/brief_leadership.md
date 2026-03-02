# SAML Claims vs SCIM Sync: ABAC Attribute Delivery Paths in Entra ID to IAM Identity Center — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> SCIM and SAML deliver ABAC attributes via separate paths; SCIM silently wins on conflicts; SSMSessionRunAs can only travel via SAML

---

## So What

Two independent pipelines deliver attributes to IAM Identity Center ABAC. When both pipelines carry the same attribute key, the SCIM/identity store value silently overrides the SAML assertion value — AWS-documented behavior that is non-obvious and not visible in the IdC console. SSMSessionRunAs, the session tag that drives OS-user identity for SSM sessions, cannot be delivered via SCIM at all because the AWS SCIM endpoint rejects schema extensions. Any design that routes SSMSessionRunAs through SCIM will silently fail to tag sessions.

---

## Key Points

- SCIM wins over SAML on attribute key conflicts — AWS-documented precedence rule, not configurable
- SAML-delivered attributes have no visibility in the IdC console — operators cannot inspect or audit them from the AWS side
- SSMSessionRunAs is SAML-only: SCIM cannot carry it; the AWS SCIM endpoint rejects custom schema extensions with HTTP 400
- SCIM lag means the winning (SCIM) value may be stale relative to what Entra would emit at login time
- Entra SCIM connector does not remove attribute values cleared in Entra — stale identity store values can persist and continue winning

---

## Action Required

> Architects designing the SSMSessionRunAs delivery path must use the Entra SAML claims path exclusively. Any team that has configured the same attribute key in both Entra SAML claims and IdC Attributes for Access Control must audit for unexpected SCIM precedence suppression.

---

*Full engineering investigation: [investigation.md](investigation.md)*
