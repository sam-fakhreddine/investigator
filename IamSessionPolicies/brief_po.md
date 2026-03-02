# IAM Session Policies and Role Sprawl Reduction in AWS with IAM Identity Center — Product Brief

**Date:** 2026-03-02
**Risk Level:** HIGH

---

## What Is This?

> The AWS feature that could reduce IAM role count does not work through the standard enterprise login system — two alternatives exist but each comes with hard limits that affect platform engineering scope and compliance posture

---

## What Does This Mean for Us?

IAM role sprawl is a real maintenance and audit burden in multi-account AWS environments. Session policies appear to offer a consolidation path, but the enterprise login platform (IAM Identity Center) does not support them at login time — a structural API constraint, not a configuration gap. PO/EMs commissioning access simplification work need to understand which alternatives are actually on the table and what prerequisites each requires, to set accurate scope and avoid approving an architecture that cannot be delivered through the current identity stack.

---

## Key Points

- If the organization logs in through IAM Identity Center (the AWS default for multi-account setups), the session policy consolidation pattern is not available through the standard login path — engineering teams proposing it need an explicit alternative design.
- Option A — ABAC: Engineers configure user attributes in Identity Center; shared roles grant access based on whether the user's attributes match resource tags. Fewer permission sets are needed, but every resource across every account must be tagged consistently. Missing or wrong tags silently over-permit access on a broad role.
- Option B — Role chaining: Users log in through Identity Center, then applications perform a second role assumption with a scoped-down policy. Works technically but caps every session at 1 hour — even for users or workloads that currently run longer sessions under the permission set's configured duration.
- Security and compliance teams cannot reconstruct what permissions were in effect for a session-policy session from CloudTrail alone; a separate logging mechanism is required and must be scoped and costed before the architecture is approved for regulated workloads.
- The AWS Policy Simulator — the standard pre-deployment validation tool for IAM changes — does not support session policy simulation; testing requires a live environment, adding deployment risk that does not exist for standard role policies.
- Reducing IAM role count via session policies shifts complexity to the calling application (policy generation, minification, character budget monitoring, PackedPolicySize alerting); total system complexity may not decrease, only its location.

---

## Next Steps

**PO/EM Decision:**

> PO/EM should confirm with the IAM platform team which credential issuance path is in use for the roles targeted for consolidation, and which of the two viable alternatives — ABAC or role chaining — the team proposes. Neither should be approved without the prerequisite assessments listed below.

**Engineering Work Items:**
- IAM platform engineers: confirm whether IAM Identity Center GetRoleCredentials is in the credential issuance path for all roles targeted for consolidation.
- IAM platform engineers: assess current resource tag coverage across accounts to determine ABAC viability and estimate tag remediation effort.
- Architects: evaluate whether any targeted workloads or interactive users require sessions longer than 1 hour; if yes, role chaining is off the table for those workloads.
- Security engineering: assess the CloudTrail audit gap for session policy content and define the out-of-band logging mechanism required to meet compliance requirements.
- Platform engineering: prototype the policy generation pipeline and character budget monitoring tooling and report back on implementation cost before the architecture is approved.

**Leadership Input Required:**

> Leadership should clarify acceptable risk tolerance for the CloudTrail audit gap before approving this architecture for workloads in regulated environments. Leadership should also decide whether to invest in ABAC infrastructure (tagging policy, tag compliance tooling) as a prerequisite to role consolidation, or to accept the current permission-set-per-use-case model as the operational baseline.

---

## Open Questions

- Do users and workloads in scope access AWS through IAM Identity Center? If yes, which consolidation alternative — ABAC or role chaining — is being proposed, and has its specific constraint been evaluated against the workload requirements?
- What is the current resource tag coverage across accounts, and is a tagging enforcement policy already in place?
- Do any targeted workloads or interactive users require sessions longer than 1 hour? If yes, role chaining is not viable for those.
- What is the engineering estimate to build and maintain the policy generation pipeline, character budget monitoring, and PackedPolicySize alerting required if session policies are adopted for direct STS callers?
- What out-of-band audit log mechanism replaces the CloudTrail gap for session policy content, and has this been scoped and costed for compliance review?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
