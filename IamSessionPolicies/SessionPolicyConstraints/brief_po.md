# IAM Session Policy Real-World Constraints — Policy Size Limits, Tooling Gaps, Audit and Visibility — Product Brief

**Date:** 2026-03-02
**Risk Level:** HIGH

---

## What Is This?

> AWS session policies cannot be used with IAM Identity Center and create audit gaps that security and compliance teams must plan for

---

## What Does This Mean for Us?

Session policies are an AWS mechanism that restricts what a user or service can do during a temporary credential session. They are being evaluated as a way to reduce the number of IAM roles the platform maintains. However, they come with hard technical constraints — a small size ceiling, no console tooling, no standard audit trail, and incompatibility with the current identity platform (IAM Identity Center) — that affect platform engineering timelines and compliance posture.

---

## Key Points

- If the organization uses IAM Identity Center for login and credential issuance (the AWS default for multi-account setups), session policies cannot be used at all without building a parallel, non-standard auth path.
- Security and compliance teams cannot use CloudTrail to reconstruct what permissions were in effect during a session that used a session policy; a separate logging mechanism would need to be built.
- The AWS Policy Simulator — the standard pre-deployment validation tool for IAM changes — does not support session policies; testing requires deploying to a live environment.
- Using session policies at scale requires an engineering pipeline to generate, minify, and monitor policy size at call time; this is new infrastructure that does not exist in a standard IAM role model.
- The pattern reduces IAM role count but shifts complexity to the calling application; total system complexity may not decrease, only its location.

---

## Next Steps

**PO/EM Decision:**

> PO/EM should confirm with the platform or security engineering team whether IAM Identity Center is the active credential issuance path for the workloads in scope. If it is, the session policy architecture decision should be paused until a viable alternative is identified.

**Engineering Work Items:**
- Platform engineering: confirm whether IAM Identity Center GetRoleCredentials is in the credential issuance path for the roles targeted for consolidation.
- Security engineering: assess the CloudTrail audit gap and define the out-of-band logging mechanism required to meet compliance requirements if session policies are adopted.
- Platform engineering: prototype the policy generation pipeline and character budget monitoring tooling and report back on implementation cost before architecture is approved.
- Security engineering: run a live environment test of session policy intersection behavior, since the Policy Simulator does not support it.

**Leadership Input Required:**

> Leadership should clarify acceptable risk tolerance for the CloudTrail audit gap before this architecture is approved for workloads in regulated environments or covered by compliance frameworks requiring full audit trails of effective permissions.

---

## Open Questions

- Are the roles being consolidated accessed through IAM Identity Center? If yes, session policies are not applicable as designed.
- What is the character size of the smallest meaningful session policy for the target use case after minification? Does it fit within 2,048 characters with margin for session tags?
- What is the engineering estimate to build and maintain the policy generation pipeline, character budget monitoring, and PackedPolicySize alerting?
- What out-of-band audit log mechanism will replace the CloudTrail gap for session policy content? Has this been scoped and costed?
- Has the team tested the effective permission behavior in a live environment, given the Policy Simulator does not support session policy simulation?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
