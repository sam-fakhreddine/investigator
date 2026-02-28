# Native AWS Mechanisms for Per-Role Linux Identity Mapping in SSM Session Manager — Product Brief

**Date:** 2026-02-28
**Risk Level:** MEDIUM

---

## What Is This?

> AWS does not natively support giving the same person different Linux identities based on which access level they select; a custom component is needed.

---

## What Does This Mean for Us?

When a user picks between 'Admin' and 'Developer' access in the AWS portal, they currently always land as the same Linux user on servers. Making the Linux user change based on the access level selected requires building a custom intermediary, because AWS does not offer this feature out of the box.

---

## Key Points

- The current setup ties the Linux username to the person, not the access level they select -- Alice is always 'alice' whether she picks Admin or Developer access.
- AWS protects the roles it creates for access levels and does not allow changing their configuration to set different Linux usernames.
- A partial workaround exists but degrades user experience: users would need to type extra commands every time they connect to a server.
- The recommended path is a custom 'session broker' component that automatically selects the correct Linux user based on the access level chosen.
- This is not a bug or misconfiguration -- it is a design limitation in how AWS Identity Center passes user attributes to downstream services.

---

## Next Steps

**PO/EM Decision:**

> Decide whether to invest in building the Lambda session broker (custom infrastructure) or accept the limitation of per-user-only Linux identity mapping.

**Engineering Work Items:**
- Prototype the Lambda session broker architecture (see companion investigation: LambdaSessionBroker).
- Evaluate the per-document workaround to determine if the user experience trade-off is acceptable for the team's use case.
- Document the current per-user RunAs behavior as a known limitation for stakeholders.

**Leadership Input Required:**

> Architects should weigh the operational complexity of a Lambda session broker against the security value of per-role Linux identity mapping. If per-user mapping is sufficient for compliance, the custom component may not be needed.

---

## Open Questions

- How much operational overhead does the Lambda session broker add compared to the current per-user setup?
- Is per-user Linux identity mapping sufficient for our compliance requirements, or is per-role mapping strictly necessary?
- Can the per-document workaround be wrapped in a CLI alias to reduce user friction?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
