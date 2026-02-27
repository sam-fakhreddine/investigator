# IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema, Configuration Surface, Drift, and Idempotency — Product Brief

**Date:** 2026-02-27
**Risk Level:** HIGH

---

## What Is This?

> The setting that routes each engineer to their own server OS account is a single shared control — deleting the stack that manages it breaks server access routing for everyone instantly, with no warning

---

## What Does This Mean for Us?

When engineers start an SSM session on a managed server, the session needs to use their personal OS account. This AWS setting looks up the user's directory username at sign-in and passes it automatically to the server. It is a required building block for the SSMSessionRunAs fix. If the owning infrastructure stack is accidentally deleted, per-user session routing stops immediately for all engineers — there is no automatic recovery and no built-in alarm.

---

## Key Points

- This is a shared, singleton setting — it cannot be owned by multiple deployment pipelines at the same time.
- Deleting the infrastructure stack that manages this setting disables per-user session routing with no grace period or rollback warning.
- AWS does not automatically detect or alert when this setting is changed outside the deployment pipeline.
- One open technical dependency remains before the configuration can be written: the Identity (Entra) team must confirm which directory attribute field carries the per-user OS username in the SCIM provisioning setup.
- Once the dependency is resolved, this is a pure infrastructure change — no product feature work is required.

---

## Next Steps

**PO/EM Decision:**

> PO/EM to confirm with the infra team that deletion protection is enabled on the stack managing this setting before it goes to production.

**Engineering Work Items:**
- Identity team: confirm the Entra SCIM attribute path for the per-user OS username (sAMAccountName) — this is the only remaining dependency before the IaC change can be written.
- Infra/architecture team: add DeletionPolicy: Retain to the resource and enable stack termination protection on the owning stack.
- Platform team: assess whether IdC ABAC is already enabled in the target instance and determine if a CloudFormation import step is required before first deployment.

**Leadership Input Required:**

> Engineering leadership to approve the guardrail policy requiring termination protection on stacks containing identity infrastructure.

---

## Open Questions

- Has the Entra SCIM attribute path for the per-user OS username been confirmed — and if so, what is it?
- Is ABAC already enabled in the Identity Center instance, and do we need an import step before deploying via CloudFormation?
- Which team owns the stack that will manage this resource, and is deletion protection already in place?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
