# IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema and Configuration Surface — Product Brief

**Date:** 2026-02-27
**Risk Level:** LOW

---

## What Is This?

> This configuration makes SSM sessions automatically use each engineer's correct server OS account, without any per-user manual setup

---

## What Does This Mean for Us?

When engineers start an SSM session on a managed server, the session needs to use their personal OS account. This AWS setting looks up the user's directory username at sign-in and passes it automatically to the server — no manual mapping, no shared credentials. It is a required building block for the SSMSessionRunAs fix identified in the prior investigation. One open dependency remains before the configuration can be written.

---

## Key Points

- Each engineer's server session uses their own OS account automatically — no admin needs to configure per-user mappings.
- This is a shared, singleton setting — it cannot be managed by multiple deployment pipelines simultaneously.
- One open dependency: the Identity team must confirm which directory attribute field carries the per-user OS username in the Entra SCIM setup.
- If this feature was previously enabled manually in the AWS console, an extra import step is required before automated deployment can proceed.
- Once the dependency is resolved, this is a pure infrastructure change — no product feature work is required.

---

## Next Steps

**PO/EM Decision:**

> No product decision required from PO/EM. Confirm with the identity team that the SCIM attribute path dependency is being resolved.

**Engineering Work Items:**
- Identity team: confirm which SCIM attribute field carries the per-user OS username (sAMAccountName) in the Entra provisioning configuration — this is the only remaining dependency before the IaC change can be written.
- Platform team: assess whether IdC ABAC is already enabled in the target instance and determine if a CloudFormation import step is required before first deployment.

---

## Open Questions

- Has the Entra SCIM attribute path for the per-user OS username been confirmed — and if so, what is it?
- Is ABAC already enabled in the Identity Center instance, and do we need an import step before deploying via CloudFormation?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
