# IAM Session Policy Mechanics — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> Session policies narrow permissions at credential issuance time but are blocked from IAM Identity Center login flows and capped at 2,048 characters

---

## So What

Session policies are a real STS capability but carry hard constraints that limit their viability as a role-consolidation strategy, particularly for Identity Center environments. The mechanism works cleanly for programmatic callers; it is not available through Identity Center's login-time credential flow.

---

## Key Points

- Session policies only restrict — they cannot expand what the target role already allows; a caller cannot use them to gain access they don't already have via the role's attached policies.
- The 2,048-character combined limit on inline policy and managed policy ARN strings, together with a separate packed binary limit shared with session tags, constrains policy complexity in ways that prevent non-trivial scoping.
- IAM Identity Center's credential issuance flow (OIDC device-code) does not accept caller-supplied session policies — permission set definition at the infrastructure level is the only control point available to Identity Center users.
- Role chaining caps all chained sessions at one hour; any architecture that uses assumed-role-then-assume-role to inject session policies hits this limit unconditionally.
- When a resource-based policy names the session ARN (not the role ARN) as principal, those permissions bypass the session policy filter entirely — a behavioral nuance with security implications.

---

*Full engineering investigation: [investigation.md](investigation.md)*
