# IAM Identity Center InstanceAccessControlAttributeConfiguration — Drift, Idempotency, and Update Behavior — Product Brief

**Date:** 2026-02-27
**Risk Level:** HIGH

---

## What Is This?

> The AWS setting that lets user attributes control server session routing is a single shared control — deleting the stack that manages it breaks access routing for everyone immediately, with no warning or automatic recovery

---

## What Does This Mean for Us?

This is not a setting that can be safely managed in a deployment stack without explicit protection enabled. By default, deleting the stack deletes the setting. AWS has no built-in alarm if someone changes this setting outside the deployment pipeline — console changes are invisible to the pipeline.

---

## Key Points

- One setting, shared across all users — there is no per-user or per-team copy.
- Deleting the owning stack disables server session routing for every engineer instantly.
- AWS does not alert when this setting is changed outside the automated pipeline.
- Explicit safeguards (deletion protection on the stack) are off by default and must be requested from the infra team.
- No product feature work is required — this is a pure infrastructure guardrail task.

---

## Next Steps

**PO/EM Decision:**

> PO/EM to confirm with the infra team that deletion protection is enabled on the stack managing this setting before it goes to production.

**Engineering Work Items:**
- Infra/architecture team: add DeletionPolicy: Retain to the InstanceAccessControlAttributeConfiguration resource.
- Infra/architecture team: enable stack termination protection on the owning stack.
- Infra team: document which stack owns the ABAC resource and confirm no other pipeline deploys this resource to the same Identity Center instance.

**Leadership Input Required:**

> Engineering leadership to approve the guardrail policy requiring termination protection on stacks containing identity infrastructure.

---

## Open Questions

- Is deletion protection already enabled on the stack that manages this setting?
- Which team owns this stack, and is there a risk another pipeline could deploy to the same Identity Center instance?
- What is the recovery procedure if ABAC is accidentally disabled in production?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
