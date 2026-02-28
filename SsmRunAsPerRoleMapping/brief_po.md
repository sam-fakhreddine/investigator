# Per-Role Linux Identity Mapping via SSM Session Manager and IAM Identity Center — Product Brief

**Date:** 2026-02-28
**Risk Level:** MEDIUM

---

## What Is This?

> AWS does not natively support giving the same person different Linux usernames based on which access level they select; a custom component can solve this but adds complexity.

---

## What Does This Mean for Us?

When a user picks between 'Admin' and 'Developer' access in the AWS portal, they currently always land as the same Linux user on servers. Making the Linux username change based on the access level requires building a custom session broker component. Without it, audit logs show user identity but not which access level was active during the session.

---

## Key Points

- The current setup ties the Linux username to the person, not the access level -- Alice is always 'alice' whether she picks Admin or Developer access.
- AWS protects the roles it creates for access levels and does not allow changing their configuration to set different Linux usernames.
- A custom Lambda session broker can automatically select the correct Linux user based on the access level chosen, but it changes how users connect to servers (wrapper script instead of standard AWS command).
- The broker creates an audit gap: AWS logs will show the broker initiated the session, not the actual user. Extra logging in the broker is needed to maintain traceability.
- A simpler workaround exists but is less user-friendly: users must type extra flags every time they connect, and the per-person username feature must be turned off entirely.

---

## Next Steps

**PO/EM Decision:**

> Decide whether per-role Linux identity mapping justifies the added infrastructure complexity, or whether per-user mapping meets current compliance and operational needs.

**Engineering Work Items:**
- If proceeding: build a Lambda session broker proof-of-concept covering session creation, role-to-document mapping, and compensating audit logging.
- Evaluate whether the per-document workaround (no broker, but degraded UX) is acceptable as an interim solution.
- Document the per-user RunAs behavior as a known limitation for stakeholders who expect per-role mapping.

**Leadership Input Required:**

> Architects should assess whether the CloudTrail attribution gap in the broker model is acceptable for the organization's audit requirements, and whether the operational cost of maintaining per-role session documents across member accounts is justified.

---

## Open Questions

- How much operational overhead does the Lambda broker add compared to the current per-user setup, including deployment, monitoring, and incident response?
- Is the CloudTrail attribution gap addressable in a way that satisfies audit and compliance requirements?
- Could AWS release a native feature for per-permission-set ABAC attributes, and should the team wait or build now?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
