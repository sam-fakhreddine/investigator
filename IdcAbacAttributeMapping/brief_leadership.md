# IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema, Configuration Surface, Drift, and Idempotency — Engineering Leadership Brief

**Date:** 2026-02-27

---

## Headline

> IAM Identity Center ABAC configuration is a singleton IaC resource with no drift detection, a destructive default deletion behavior, and a create/update API split that blocks deployment against pre-existing console-configured instances

---

## So What

Once deployed, this resource is production-critical — it is the only control plane object wiring SCIM-synced user attributes to OS login in SSM sessions. Default CloudFormation behavior makes accidental ABAC deletion a realistic operational risk: stack deletion calls the Delete API immediately with no grace period, and drift detection is unsupported, meaning out-of-band changes accumulate silently.

---

## Key Points

- Singleton per IdC instance — one resource object, one owning stack. Multiple pipelines writing to the same instance will conflict.
- Stack deletion immediately disables ABAC for all users with no recovery grace period. DeletionPolicy: Retain and stack termination protection are off by default and must be explicitly set.
- CloudFormation drift detection returns NOT_CHECKED — console or CLI changes after deployment are invisible to IaC tooling.
- Deploying IaC against an instance where ABAC was manually configured will fail with ConflictException until the existing resource is imported into the stack.
- Every attribute list update is a full replacement — any team that omits an existing attribute in an update call silently deletes it.

---

## Action Required

> Authorize IdC ABAC configuration as a standalone IaC change outside the LZA customizations pipeline. Approve a policy requiring DeletionPolicy: Retain and stack termination protection on all stacks containing this resource. Confirm whether multiple teams share the same IdC instance — if yes, a coordination gate is required.

---

*Full engineering investigation: [investigation.md](investigation.md)*
