# IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema and Configuration Surface — Engineering Leadership Brief

**Date:** 2026-02-27

---

## Headline

> IAM Identity Center's ABAC attribute configuration is the single IaC control plane object that wires a SCIM-synced per-user AD attribute to the OS login used in SSM sessions

---

## So What

InstanceAccessControlAttributeConfiguration is a singleton per IdC instance that maps identity store attributes to session tags. Configured with Key = SSMSessionRunAs pointing at a SCIM-synced user attribute, every IdC session carries the correct OS username as a principal tag — enabling SSM RunAs per-user routing without any per-user IAM configuration. The create/update API split means IaC deployments against instances with existing console-configured ABAC will fail with ConflictException until the resource is imported.

---

## Key Points

- Singleton per IdC instance — one resource, one owning stack. Multiple pipelines writing to the same instance will conflict.
- Key must be exactly SSMSessionRunAs (casing is significant) — any variation silently breaks SSM RunAs routing.
- Source path syntax differs by identity source type — ${path:...} for Entra SCIM, ${samaccountname} for AWS Managed AD. Mixing these produces silent mismatch.
- Update replaces the full attribute list — omitting an existing attribute in a redeployment silently deletes it.
- Only an L1 CDK construct exists — no higher-level abstraction is available as of 2026.

---

## Action Required

> Authorize IdC ABAC configuration as a standalone IaC change outside the LZA customizations pipeline. Confirm whether multiple teams share the same IdC instance — if yes, a coordination gate is required before any attribute list update. Confirm SCIM attribute path for sAMAccountName with the identity team before the IaC change is written.

---

*Full engineering investigation: [investigation.md](investigation.md)*
