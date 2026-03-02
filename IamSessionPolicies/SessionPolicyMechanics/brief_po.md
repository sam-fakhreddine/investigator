# IAM Session Policy Mechanics — Product Brief

**Date:** 2026-03-02
**Risk Level:** LOW

---

## What Is This?

> AWS session policies let engineers narrow permissions at login time, but are not available through IAM Identity Center and have strict size constraints

---

## What Does This Mean for Us?

Engineering teams exploring session policies as a way to reduce the number of IAM roles in AWS environments will find the mechanism is real but narrowly applicable. Organizations that use IAM Identity Center (SSO) as their primary login layer cannot use this mechanism at login time — permission changes must go through the permission set provisioning process instead.

---

## Key Points

- Session policies work only when engineers call the AWS API or CLI directly to assume a role — they are not triggered by the normal SSO login flow that most teams use.
- The size cap (roughly a short JSON policy document) means session policies can only express simple access rules — not the complex permission sets most teams need.
- For Identity Center environments, the only way to change what a user can do is to update the permission set — a change that goes through infrastructure provisioning, not a runtime parameter.
- This investigation is about understanding the mechanics — not a recommendation to adopt or reject session policies. Implementation decisions and role-consolidation designs are separate work.

---

## Next Steps

**PO/EM Decision:**

> No product decision required from this investigation. Findings are input to Architects and the platform team evaluating IAM role consolidation strategies.

**Engineering Work Items:**
- Architects to assess whether session policy constraints rule out role consolidation for Identity Center environments or only for non-SSO programmatic callers.
- Platform/infra team to evaluate the packed policy size budget under current ABAC attribute volume (session tags) to determine remaining headroom for any session policy payload.

**Leadership Input Required:**

> If the platform team's assessment concludes that session policies cannot address role sprawl in Identity Center environments, leadership should decide whether to prioritize an alternative investigation (e.g., permission set consolidation patterns or ABAC-only architectures).

---

## Open Questions

- Do our workloads primarily access AWS through IAM Identity Center (SSO), or do some services call AssumeRole directly via the API?
- How many ABAC session tag attributes is Identity Center currently passing, and does that leave meaningful packed policy budget for session policies?
- Are there any workloads today that already use session policies, and if so, what is the observed PackedPolicySize percentage?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
