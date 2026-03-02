# Validation Report: IAM Role Consolidation Patterns
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 13
- Verified: 13 | Redirected: 0 | Dead: 0 | Unverifiable: 0
- Findings checked: 6
- Confirmed: 6 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/IamSessionPolicies/RoleConsolidationPatterns
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        6            6            fdc645db6672   fdc645db6672
tensions             IN_SYNC        5            5            ee864404c637   ee864404c637
open_questions       IN_SYNC        4            4            c039184bd696   c039184bd696
sources              IN_SYNC        13           13           51c4c5c8fe49   51c4c5c8fe49
concepts             IN_SYNC        7            7            2529fd723b2e   2529fd723b2e
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | AssumeRole API Reference — AWS Security Token Service | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html | VERIFIED | Page resolves. Confirms Policy parameter (inline JSON, max 2,048 chars combined), PolicyArns parameter (up to 10 ARNs), and explicit 1-hour role chaining cap. |
| 2 | Permissions for AssumeRole, AssumeRoleWithSAML, and AssumeRoleWithWebIdentity — AWS IAM User Guide | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_assumerole.html | VERIFIED | Page resolves. Confirms intersection model: session policy limits role permissions; cannot grant beyond role's identity-based policy. |
| 3 | GetRoleCredentials API Reference — AWS IAM Identity Center Portal API | https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html | VERIFIED | Page resolves. Confirms exactly three parameters: accessToken, accountId, roleName. No Policy parameter exists. |
| 4 | Manage AWS accounts with permission sets — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html | VERIFIED | Page resolves. Confirms permission set definition, IAM role provisioning per account, and policy attachment model. |
| 5 | Attribute-based access control — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html | VERIFIED | Page resolves. Confirms session tag propagation and tag-based access matching. Page does not itself enumerate aws:PrincipalTag syntax; that is covered in source 6. |
| 6 | Create permission policies for ABAC in IAM Identity Center — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html | VERIFIED | Page resolves. Confirms aws:PrincipalTag condition key usage with a concrete JSON policy example (CostCenter tag matching EC2 instances). |
| 7 | IAM and AWS STS quotas — AWS Identity and Access Management | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html | VERIFIED | Page resolves. Confirms 2,048-character combined plaintext limit for session policies, 10 managed policy ARN cap, and PackedPolicySize binary limit. |
| 8 | Methods to assume a role — AWS Identity and Access Management | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage-assume.html | VERIFIED | Page resolves. Explicitly states: "When you use role chaining, the role's session duration is limited to one hour." |
| 9 | Create fine-grained session permissions using IAM managed policies — AWS Security Blog | https://aws.amazon.com/blogs/security/create-fine-grained-session-permissions-using-iam-managed-policies/ | VERIFIED | Page resolves. Web search confirms EC2Admin is the explicit example role used in the post. Post demonstrates broad base role + managed policy session policy pattern. |
| 10 | Build an end-to-end attribute-based access control strategy with AWS IAM Identity Center and Okta — AWS Security Blog | https://aws.amazon.com/blogs/security/build-an-end-to-end-attribute-based-access-control-strategy-with-aws-sso-and-okta/ | VERIFIED | Page resolves. Web search confirms content covers ABAC with IAM Identity Center and Okta using session tags and attribute-to-resource-tag matching. |
| 11 | AssumeRoleWithWebIdentity API Reference — AWS Security Token Service | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html | VERIFIED | Page resolves. Confirms Policy parameter (inline JSON, max 2,048 chars) and PolicyArns parameter are accepted. |
| 12 | GetFederationToken API Reference — AWS Security Token Service | https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html | VERIFIED | Page resolves. Confirms API requires IAM user long-term credentials as the calling principal. Accepts Policy and PolicyArns parameters. |
| 13 | Set session duration for AWS accounts — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html | VERIFIED | Page resolves. Confirms configurable range of 1–12 hours for permission set session duration. |

---

## Finding Verification

### Finding 1: STS AssumeRole session policy mechanism and intersection model

- **Claim:** The STS AssumeRole API accepts an optional Policy parameter (inline JSON, max 2,048 chars combined with PolicyArns) and up to 10 managed policy ARN references, enabling a broad base role to be scoped down dynamically at assumption time. The effective session permissions are the strict intersection of the role's identity-based policies and the session policy — session policies cannot expand beyond what the role itself allows.
- **Verdict:** CONFIRMED
- **Evidence:** AssumeRole API reference explicitly documents the Policy parameter (string, JSON format) and PolicyArns parameter (up to 10 ARNs), with a combined plaintext limit of 2,048 characters. The Permissions for AssumeRole page states: "The resulting session's permissions are the intersection of the role's identity-based policy and the session policies." Both limits and the intersection model are confirmed by the quotas page.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html and https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_assumerole.html

---

### Finding 2: GetRoleCredentials has no Policy parameter — blocking the session policy consolidation pattern

- **Claim:** IAM Identity Center issues credentials via its proprietary GetRoleCredentials portal API, not directly via STS AssumeRole. GetRoleCredentials accepts only three parameters — accessToken, accountId, and roleName — with no request body and no Policy parameter. A user or application obtaining credentials through the standard Identity Center path cannot inject a session policy at issuance time.
- **Verdict:** CONFIRMED
- **Evidence:** GetRoleCredentials API reference lists exactly three URI parameters: accessToken (passed as bearer token header), accountId (query parameter), and roleName (query parameter). The request format is a GET with no request body and no Policy field. This is definitive — no Policy parameter exists in the API specification.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html

---

### Finding 3: Role chaining workaround and 1-hour session cap

- **Claim:** A post-issuance chained AssumeRole from Identity Center credentials is technically viable as a workaround. However, IAM role chaining imposes a hard 1-hour session duration ceiling regardless of the permission set's configured session duration (up to 12 hours).
- **Verdict:** CONFIRMED
- **Evidence:** The AssumeRole API reference explicitly states that role chaining limits sessions to a maximum of 1 hour and that specifying DurationSeconds greater than one hour when role chaining causes the operation to fail. The Methods to assume a role page confirms: "When you use role chaining, the role's session duration is limited to one hour." The permission set session duration page confirms the configurable range is 1–12 hours, validating the stated contrast.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html and https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage-assume.html and https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html

---

### Finding 4: ABAC via session tags as the native Identity Center consolidation mechanism

- **Claim:** ABAC via session tags is the native Identity Center mechanism for differentiating permissions within a single permission set. Identity Center propagates user attributes as session tags; permission set policies can reference these via aws:PrincipalTag condition keys. This reduces permission set proliferation but requires consistent resource tagging and cannot produce an arbitrary per-session allow list of actions.
- **Verdict:** CONFIRMED
- **Evidence:** The ABAC overview page (source 5) confirms session tag propagation from user attributes and tag-based access matching. The ABAC policy creation page (source 6) explicitly documents aws:PrincipalTag usage with a concrete JSON example matching a CostCenter tag on resources against the principal's CostCenter session tag. The investigation's characterization of the mechanism's limitation (cannot restrict action namespace the way a session policy can) is accurate — ABAC enforces resource-level matching, not action-level restriction.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html and https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html

---

### Finding 5: GetFederationToken requires IAM user credentials and is incompatible with Identity Center

- **Claim:** The AWS-documented identity broker pattern (GetFederationToken) explicitly supports the broad-base-role + session-policy model for custom federation scenarios. However, GetFederationToken requires an IAM user principal as the calling entity, making it architecturally incompatible with Identity Center user identities.
- **Verdict:** CONFIRMED
- **Evidence:** GetFederationToken API reference states: "You must call the GetFederationToken operation using the long-term security credentials of an IAM user." The API accepts a Policy parameter and PolicyArns parameter. The requirement for IAM user long-term credentials as the base principal is explicit and unambiguous in the API documentation. Identity Center does not issue or manage IAM user credentials.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html

---

### Finding 6: Permission set proliferation as the Identity Center consolidation ceiling and ABAC's role

- **Claim:** The practical consolidation ceiling under Identity Center is the permission set itself: one permission set maps to one IAM role per account, and role proliferation shifts from the IAM layer to the permission set layer. ABAC reduces this by allowing one permission set to serve users with distinct attribute-based access; without ABAC, each distinct permission profile requires a distinct permission set.
- **Verdict:** CONFIRMED
- **Evidence:** The permission set concept page confirms that Identity Center provisions one IAM role per account per permission set and attaches the permission set's policies to it. The ABAC pages confirm that a single permission set with attribute-matching conditions can differentiate access for multiple users based on their organizational attributes, reducing the need for one-permission-set-per-use-case. The relationship between ABAC adoption and permission set count reduction is accurately characterized.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html and https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| None | — | All findings confirmed. All sources verified. No remediation required. |

---

## Overall Assessment

All 13 sources resolve and match their claimed titles and content. All 6 key findings are confirmed against live AWS documentation. The central structural claim — that GetRoleCredentials accepts no Policy parameter, blocking the broad-base-role consolidation pattern from operating through Identity Center's standard credential path — is precisely confirmed by the API reference, which lists exactly three accepted parameters with no Policy field. The role chaining 1-hour cap, the session policy intersection model, the ABAC mechanism with aws:PrincipalTag, the GetFederationToken IAM-user-principal requirement, and the permission set proliferation dynamics are all directly supported by official AWS documentation. The EC2Admin example attributed to the AWS Security Blog is confirmed by web search. No contradictions, internal conflicts, or unsupported claims were identified. The investigation is factually sound and ready to commit.
