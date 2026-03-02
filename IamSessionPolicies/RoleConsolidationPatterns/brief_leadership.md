# IAM Role Consolidation Patterns Using Session Policies and IAM Identity Center — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> IAM Identity Center blocks the broad-base-role consolidation pattern at the credential API level — ABAC and role chaining are the only viable workarounds, each with documented tradeoffs.

---

## So What

A commonly proposed IAM simplification — maintain a few broad roles and scope them down dynamically at assume-role time — cannot be executed through the standard IAM Identity Center credential path. The GetRoleCredentials API (used by the portal and CLI) has no session policy parameter. Architects proposing this pattern in Identity Center environments need to understand which alternatives are actually available before committing to a consolidation design.

---

## Key Points

- STS AssumeRole natively supports dynamic session policies (inline JSON or up to 10 managed policy ARNs); this is documented and functional for direct callers of STS.
- Identity Center's GetRoleCredentials API has no Policy parameter — permissions are determined entirely by the permission set at assignment time, not at credential issuance time.
- Post-issuance role chaining (Identity Center credentials used to call AssumeRole with a session policy) is viable but imposes a hard 1-hour session cap — overriding the permission set's configurable duration of up to 12 hours.
- ABAC via session tags is the Identity Center-native path toward fewer permission sets: one permission set can differentiate access for multiple users based on organizational attributes (team, cost center, environment) matched against resource tags.
- ABAC does not replicate session policy behavior — it enforces resource-level access based on tag matching, not action-level restriction across the session. The two mechanisms address different control surfaces.
- GetFederationToken is the only STS mechanism that directly supports the broker pattern (caller injects session policy on behalf of another identity), but it requires IAM user credentials as the base principal and is architecturally incompatible with Identity Center.
- Role proliferation under Identity Center shifts from IAM roles to permission sets — ABAC reduces permission set count; without it, each distinct permission profile requires a distinct permission set assignment.

---

## Action Required

> Architects and IAM platform engineers should validate any proposed role consolidation design against the GetRoleCredentials constraint before endorsing the pattern for Identity Center environments. ABAC viability depends on resource tagging discipline — that coverage gap should be assessed before ABAC is selected as the consolidation strategy.

---

*Full engineering investigation: [investigation.md](investigation.md)*
