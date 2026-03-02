# Validation Report: IAM Session Policy Mechanics
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 12
- Verified: 12 | Redirected: 0 | Dead: 0 | Unverifiable: 0
- Findings checked: 10
- Confirmed: 9 | Partially confirmed: 1 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/IamSessionPolicies/SessionPolicyMechanics
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           b92c672675c3   b92c672675c3
tensions             IN_SYNC        5            5            2dc3d87833b4   2dc3d87833b4
open_questions       IN_SYNC        5            5            9464e1d0d268   9464e1d0d268
sources              IN_SYNC        12           12           ce2525c5b385   ce2525c5b385
concepts             IN_SYNC        10           10           8665876c2673   8665876c2673
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | AWS IAM User Guide: Session Policies | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session | VERIFIED | Page titled "Policies and permissions in AWS Identity and Access Management"; session policy section confirmed, including STS API list and intersection rule |
| 2 | AWS STS API Reference: AssumeRole | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html | VERIFIED | Page titled "AssumeRole - AWS Security Token Service"; Policy param, PolicyArns (up to 10), 2,048-char limit, PackedPolicySize, and role-chaining 1-hour cap all documented |
| 3 | AWS STS API Reference: AssumeRoleWithSAML | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html | VERIFIED | Page titled "AssumeRoleWithSAML - AWS Security Token Service"; Policy and PolicyArns params, 2,048-char limit, intersection rule, PackedPolicySize all confirmed |
| 4 | AWS IAM User Guide: Requesting Temporary Credentials | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html | VERIFIED | Page titled "Request temporary security credentials"; all four STS session-policy APIs listed; session policy intersection rule confirmed |
| 5 | AWS IAM User Guide: IAM Quotas and Limits | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html | VERIFIED | Page titled "IAM and AWS STS quotas"; 2,048-char combined limit and 10 managed policy ARN cap explicitly documented under "Role session policies" |
| 6 | AWS IAM User Guide: Policy Evaluation Logic | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html | VERIFIED | Page titled "Policy evaluation logic"; covers explicit deny, intersection with permissions boundaries and SCPs; does not explicitly cover session policies on this page — session policy evaluation logic is on the access_policies.html page (source 1) |
| 7 | AWS IAM User Guide: Permissions Boundaries | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html | VERIFIED | Page titled "Permissions boundaries for IAM entities"; three-way intersection of identity-based policy, permissions boundary, and session policy explicitly documented with diagram |
| 8 | AWS IAM User Guide: Session Tags | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html | VERIFIED | Page titled "Pass session tags in AWS STS"; packed binary budget shared between session tags and session policies explicitly documented |
| 9 | AWS IAM Identity Center User Guide: Permission Sets | https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsets.html | VERIFIED | Page titled "Create, manage, and delete permission sets"; covers permission set as access definitions stored in Identity Center; no session policy injection parameter documented |
| 10 | AWS IAM Identity Center User Guide: Attributes for Access Control (ABAC) | https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html | VERIFIED | Page titled "Attributes for access control"; confirms user directory attributes are passed for access control; technical detail on session tag format is covered by source 8 rather than this page |
| 11 | AWS IAM Identity Center User Guide: Getting Credentials | https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html | VERIFIED | Page titled "Getting IAM Identity Center user credentials for the AWS CLI or AWS SDKs"; OIDC device-code authorization flow via `aws configure sso` confirmed; no session policy parameter on GetRoleCredentials confirmed via separate API reference check |
| 12 | AWS IAM User Guide: Switching Roles via Console | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html | VERIFIED | Page titled "Switch from a user to an IAM role (console)"; console role-switch procedure documented; page contains no session policy parameter — absence confirms the claim; programmatic-only nature confirmed by session policy documentation (source 1) |

## Finding Verification

### Finding 1: Session policy APIs (AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity, GetFederationToken)
- **Claim:** Session policies are passed as parameters to STS AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity, and GetFederationToken — they are not attached to the role itself and have no existence outside the credential issuance call.
- **Verdict:** CONFIRMED
- **Evidence:** Source 1 (access_policies.html) explicitly lists all four APIs as the mechanisms for passing session policies. Source 4 (id_credentials_temp_request.html) confirms all four support session policies. Source 2 (AssumeRole API reference) documents the Policy and PolicyArns parameters. The GetFederationToken API reference confirms session policies are supported there as well (DurationSeconds range 900–129,600 seconds / 36 hours maximum also confirmed).
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session, https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html

### Finding 2: Intersection-only rule
- **Claim:** The effective permission set for a role session is the intersection of the role's identity-based policies and the supplied session policies; a session policy cannot grant permissions the role does not already possess.
- **Verdict:** CONFIRMED
- **Evidence:** Source 1 states: "The permissions for a session are the intersection of the identity-based policies for the IAM entity (user or role) used to create the session and the session policies." Source 2 (AssumeRole API reference) repeats: "Session permissions are the intersection of the role's identity-based policy and the session policies." The cannot-expand constraint is consistently documented.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session

### Finding 3: Dual size constraints (plaintext 2,048-char and packed binary limit)
- **Claim:** Two separate size constraints apply: a 2,048-character plaintext limit on the combined inline policy and PolicyArns payload, and a separate packed binary format limit that counts session tags in the same budget — a request can fail the packed limit even if it satisfies the plaintext limit.
- **Verdict:** CONFIRMED
- **Evidence:** Source 5 (IAM quotas) documents the 2,048-char combined limit. Source 2 (AssumeRole) documents PackedPolicySize as a response element and states requests fail when the packed limit is exceeded. Source 8 (session tags) explicitly states: "An AWS conversion compresses the passed session policies and session tags combined into a packed binary format with a separate limit." The independence of the two limits is confirmed.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html, https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html, https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

### Finding 4: Up to 10 managed policy ARNs via PolicyArns
- **Claim:** Up to 10 managed policy ARNs can be passed via the PolicyArns parameter in a single AssumeRole call, in addition to one inline JSON policy document via the Policy parameter.
- **Verdict:** CONFIRMED
- **Evidence:** Source 5 (IAM quotas): "You can pass a maximum of 10 managed policy ARNs when you create a session." and "You can pass only one JSON policy document when you programmatically create a temporary session." Source 2 (AssumeRole API reference) documents PolicyArns as accepting up to 10 ARNs.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html, https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html

### Finding 5: Resource-based policy session ARN bypass
- **Claim:** When a resource-based policy grants access to the session ARN (not the role ARN), those permissions are not filtered by the session policy — the bypass applies only when the session ARN itself is the named principal in the resource policy.
- **Verdict:** CONFIRMED
- **Evidence:** Source 1 (access_policies.html) states: "A resource-based policy can specify the ARN of the session as a principal. In that case, the permissions from the resource-based policy are added after the session is created. The resource-based policy permissions are not limited by the session policy." The scoping caveat (applies only when session ARN, not role ARN, is the named principal) is confirmed by the same page which shows distinct diagrams for each scenario.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session

### Finding 6: Three-way intersection with permissions boundaries
- **Claim:** When both a permissions boundary and a session policy are active on the same session, the effective permissions are the three-way intersection of identity-based policy, permissions boundary, and session policy.
- **Verdict:** CONFIRMED
- **Evidence:** Source 7 (access_policies_boundaries.html) states: "The entity's identity-based policy permissions are limited by the session policy and the permissions boundary. The effective permissions for this set of policy types are the intersection of all three policy types. An explicit deny in any of these policies overrides the allow." Page includes a diagram illustrating the three-way intersection.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html

### Finding 7: Role-chaining 1-hour cap
- **Claim:** Role chaining — where one assumed role calls AssumeRole again — caps the resulting session at one hour maximum, regardless of the DurationSeconds parameter or the target role's configured maximum session duration.
- **Verdict:** CONFIRMED
- **Evidence:** Source 2 (AssumeRole API reference) documents this limit. The AWS re:Post knowledge center article and multiple secondary sources confirm: "If you assume a role using role chaining and provide a DurationSeconds parameter value greater than one hour, the operation fails." This is a hard AWS limit documented in the AssumeRole API reference, not merely community observation.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html

### Finding 8: Console role-switch has no session policy parameter
- **Claim:** The AWS Management Console role-switch flow does not expose a session policy parameter; session policies are exclusively a programmatic or CLI capability.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The console role-switch documentation (source 12) contains no session policy parameter — the form accepts only account ID, role name, display name, and color. Session policy documentation (source 1) defines session policies as being passed "when you programmatically create a temporary credential session," confirming programmatic-only access. However, no source contains an explicit negative statement such as "session policies are not available in the console role-switch flow." The absence is evident from the documentation structure but is not explicitly stated as a constraint in any official doc.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html, https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session

### Finding 9: IAM Identity Center OIDC flow does not expose session policy parameter
- **Claim:** IAM Identity Center issues temporary credentials through an OIDC device-code authorization flow and does not expose a session policy parameter to the caller — the permission set inline and managed policies constitute the full permission definition at issuance time.
- **Verdict:** CONFIRMED
- **Evidence:** Source 11 (howtogetcredentials.html) confirms the OIDC device-code flow via `aws configure sso`. The IAM Identity Center Portal API Reference for GetRoleCredentials (the underlying API) accepts only three parameters: accessToken, accountId, and roleName — no Policy or PolicyArns parameter exists. This is the definitive confirmation that no session policy injection point is available to callers in the Identity Center credential flow.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html

### Finding 10: Identity Center ABAC session tags share packed policy size budget
- **Claim:** IAM Identity Center ABAC passes user directory attributes as session tags at federation time; session tags share the packed policy size budget with any session policies present in a given credential issuance.
- **Verdict:** CONFIRMED
- **Evidence:** Source 10 (attributesforaccesscontrol.html) confirms user directory attributes are passed for access control at federation time. Source 8 (id_session-tags.html) explicitly confirms session tags and session policies share a combined packed binary size budget: "An AWS conversion compresses the passed session policies and session tags combined into a packed binary format with a separate limit." The Identity Center ABAC mechanism uses standard STS session tags, so the shared budget applies.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 8: Console role-switch has no session policy parameter | PARTIALLY CONFIRMED | The claim is accurate in practice and well-supported by the documentation structure, but no official doc contains an explicit negative statement. Consider adding a qualifier: "the console role-switch documentation does not expose a session policy parameter; the official session policy documentation defines session policies as a programmatic API capability." This is a hedging refinement, not a factual correction. |

## Overall Assessment

All 12 sources are verified and accessible. Nine of ten key findings are fully confirmed by official AWS documentation. The tenth finding (console role-switch has no session policy parameter) is accurate and well-evidenced by the absence of the parameter in the console documentation and by session policy documentation framing the feature as programmatic-only — but no official source contains a direct explicit statement of this constraint, making PARTIALLY CONFIRMED the technically correct verdict.

The investigation's core mechanistic claims are solid: the intersection-only rule, dual size limits (plaintext 2,048 characters and separate packed binary), PolicyArns limit of 10, role-chaining 1-hour cap, three-way intersection with permissions boundaries, session ARN resource-policy bypass, and Identity Center's absence of a caller-supplied session policy parameter are all confirmed by primary official documentation. The GetRoleCredentials API reference definitively confirms the Identity Center finding — the API accepts only accountId, roleName, and accessToken, with no policy injection surface.

No findings require correction. The single remediation item is a minor hedging refinement and does not affect the investigation's conclusions.
