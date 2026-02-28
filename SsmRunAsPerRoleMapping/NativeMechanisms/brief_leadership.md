# Native AWS Mechanisms for Per-Role Linux Identity Mapping in SSM Session Manager — Engineering Leadership Brief

**Date:** 2026-02-28

---

## Headline

> No native AWS mechanism exists to vary the SSM Session Manager RunAs Linux user based on which IAM Identity Center permission set is assumed; custom infrastructure (e.g., Lambda session broker) is required for per-role identity mapping.

---

## So What

The per-user ABAC model in IAM Identity Center means that a user's Linux session identity is fixed regardless of which permission set they select. Achieving per-role mapping requires either custom infrastructure (Lambda broker) or a fragile workaround (per-document RunAs without ABAC tags, enforced via IAM policy on each permission set).

---

## Key Points

- IdC ABAC attributes are per-user, not per-permission-set: the SSMSessionRunAs session tag sent to AWS is always the same value for a given user, regardless of which permission set they assume.
- AWSReservedSSO_ roles are protected by AWS and cannot be tagged directly, blocking the most obvious native approach of tagging each permission set's role with a different SSMSessionRunAs value.
- A per-document workaround exists (separate SSM documents per role, restricted via IAM policy on each permission set) but only works if the SSMSessionRunAs ABAC attribute is removed entirely, and it requires users to specify --document-name on every session start.
- Permission set inline policies can provide defense-in-depth by denying sessions where the SSMSessionRunAs tag does not match an expected value, but they cannot set or override the tag.
- The gap is architectural: SSM resolves RunAs from the calling principal's identity, and IdC provides the same identity attributes regardless of permission set. A Lambda broker is the only proven approach to inject permission-set-awareness into the RunAs resolution.

---

## Action Required

> Proceed with Lambda session broker design (separate investigation) as the primary path for per-role RunAs mapping. Consider the per-document workaround only if Lambda complexity is unacceptable and per-user RunAs override is not needed.

---

*Full engineering investigation: [investigation.md](investigation.md)*
