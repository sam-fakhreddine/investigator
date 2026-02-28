# Per-Role Linux Identity Mapping via SSM Session Manager and IAM Identity Center — Engineering Leadership Brief

**Date:** 2026-02-28

---

## Headline

> Per-role Linux identity mapping in SSM Session Manager is not achievable with native AWS mechanisms; a Lambda session broker is the only viable architecture, introducing audit attribution gaps and client workflow changes.

---

## So What

The current per-user ABAC model in IAM Identity Center cannot differentiate Linux session identity by permission set. Achieving per-role mapping requires custom infrastructure (Lambda broker with per-role session documents) that adds operational complexity, changes the user workflow, and creates a CloudTrail attribution gap requiring compensating controls. The alternative is accepting per-user-only mapping.

---

## Key Points

- IdC ABAC attributes are per-user: the SSMSessionRunAs tag is identical regardless of which permission set is assumed, and AWSReservedSSO_ roles cannot be tagged to override this.
- A Lambda broker intercepts session creation, parses the permission set name from the caller's role ARN, and calls StartSession with the correct per-role session document -- the data channel flows directly to the instance with no broker latency.
- CloudTrail will attribute SSM sessions to the Lambda execution role, not the original user; compensating logs in the Lambda are mandatory for audit compliance.
- Per-role session documents and corresponding IAM policy restrictions must be deployed to every member account via StackSets, expanding the infrastructure footprint.
- A fragile native workaround exists (per-document RunAs without the ABAC tag, enforced via IAM policy) but requires removing per-user ABAC entirely and degrades UX by mandating --document-name on every session start.

---

## Action Required

> Decide whether to invest in a Lambda session broker PoC (accepting audit and UX trade-offs) or accept per-user-only Linux identity mapping as sufficient for the current compliance requirements.

---

*Full engineering investigation: [investigation.md](investigation.md)*
