# Lambda-Based Session Broker for SSM Per-Role Linux Identity — Engineering Leadership Brief

**Date:** 2026-02-28

---

## Headline

> A Lambda session broker can achieve per-role Linux identity mapping in SSM by intercepting session creation and selecting the RunAs user based on the caller's permission set, but it introduces audit attribution gaps and client-side workflow changes.

---

## So What

This architecture fills a gap that native AWS mechanisms cannot address: mapping IAM Identity Center permission sets to different Linux OS users on the same target instance. The trade-off is added operational complexity (Lambda broker, per-role session documents, compensating audit logs) and a changed user workflow requiring a wrapper script instead of direct SSM CLI usage.

---

## Key Points

- The broker only handles session creation (control plane); terminal I/O flows directly between the user's machine and the SSM agent, so there is no data-plane latency or throughput impact.
- CloudTrail will attribute SSM sessions to the Lambda execution role, not the original user. Compensating logs in the Lambda are required to maintain audit traceability for compliance.
- Per-role SSM session documents (e.g., SSMRunAs-Admin-Session, SSMRunAs-Developer-Session) must be deployed to every member account, adding to the StackSet footprint.
- IAM policy conditions on session document access provide defense-in-depth: even bypassing the broker, a role cannot use a document mapped to a different OS user.
- The Lambda broker becomes a new availability dependency for session initiation -- if it is down, per-role mapping is unavailable, though fallback to native SSM remains possible.

---

## Action Required

> Decide whether the audit attribution gap and client workflow change are acceptable trade-offs for per-role Linux identity mapping, and whether to proceed with a proof-of-concept implementation.

---

*Full engineering investigation: [investigation.md](investigation.md)*
