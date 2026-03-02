# Validation Report: IAM Session Policies and Role Sprawl Reduction (Rollup)
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 28
- Verified: 25 | Redirected: 0 | Dead: 0 | Unverifiable: 3
- Findings checked: 8
- Confirmed: 7 | Partially confirmed: 1 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/IamSessionPolicies
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        8            8            019ea4ab0143   019ea4ab0143
tensions             IN_SYNC        6            6            70a58c81c96c   70a58c81c96c
open_questions       IN_SYNC        7            7            18847520e12b   18847520e12b
sources              IN_SYNC        28           28           cbd043091546   cbd043091546
concepts             IN_SYNC        8            8            b7b93e3e4b56   b7b93e3e4b56
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

All fields in sync. No remediation required.

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | AWS IAM User Guide: Session Policies | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session | VERIFIED | Page confirmed live; dedicated session policies section present; documents all seven policy types including session policies |
| 2 | AWS STS API Reference: AssumeRole | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html | VERIFIED | Policy and PolicyArns parameters confirmed; 2,048-char combined plaintext limit documented; 1-hour role-chaining cap documented |
| 3 | AWS STS API Reference: AssumeRoleWithSAML | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html | VERIFIED | Policy and PolicyArns parameters confirmed; same limits documented |
| 4 | AWS STS API Reference: AssumeRoleWithWebIdentity | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html | VERIFIED | Policy and PolicyArns parameters confirmed; same limits documented |
| 5 | AWS STS API Reference: GetFederationToken | https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html | VERIFIED | IAM user principal requirement confirmed; Policy parameter accepted; not usable with role credentials |
| 6 | AWS IAM User Guide: IAM Quotas and Limits | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html | VERIFIED | 2,048-char limit for combined inline policy + managed ARNs confirmed; 10 managed ARN maximum confirmed; PackedPolicySize separate limit referenced |
| 7 | AWS IAM User Guide: Policy Evaluation Logic | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html | VERIFIED | Page live; documents identity-based + resource-based = union; identity-based + permissions boundary = intersection; note: session policy evaluation logic is described on the access_policies.html page, not this one |
| 8 | AWS IAM User Guide: Permissions Boundaries | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html | VERIFIED | Three-way intersection (identity-based + permissions boundary + session policy) explicitly documented with diagram |
| 9 | AWS IAM User Guide: Session Tags | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html | VERIFIED | ABAC via session tags documented; packed binary budget shared between session policies and session tags confirmed |
| 10 | AWS IAM User Guide: Policy Evaluation — Session Policies and Permissions Boundaries | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_assumerole.html | VERIFIED | Page live; title: "Permissions for AssumeRole, AssumeRoleWithSAML, and AssumeRoleWithWebIdentity"; intersection of session policy + role identity-based policy confirmed |
| 11 | AWS IAM User Guide: Requesting Temporary Credentials | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html | VERIFIED | Page live; all STS credential request methods documented |
| 12 | AWS IAM User Guide: Monitor and Control Actions with Assumed Roles | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_monitor.html | VERIFIED | Page live; title: "Monitor and control actions taken with assumed roles" |
| 13 | AWS IAM User Guide: Logging IAM and STS API Calls with CloudTrail | https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html | VERIFIED | Multiple AssumeRole CloudTrail log examples confirmed; inline Policy parameter absent from all requestParameters examples shown |
| 14 | AWS IAM User Guide: IAM Policy Testing with the IAM Policy Simulator | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html | VERIFIED | Page live; session policies not mentioned as a supported input type; absence confirmed |
| 15 | IAM SimulatePrincipalPolicy API Reference | https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulatePrincipalPolicy.html | VERIFIED | No session policy parameter accepted; PolicyInputList, PermissionsBoundaryPolicyInputList, and ResourcePolicy parameters documented — no session policy input |
| 16 | GetRoleCredentials API Reference — AWS IAM Identity Center Portal API | https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html | VERIFIED | Exactly three parameters confirmed: accessToken, accountId, roleName; no Policy or PolicyArns parameter present |
| 17 | AWS IAM Identity Center User Guide: Permission Sets | https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsets.html | VERIFIED | Permission sets described; session duration configuration confirmed; no caller-supplied session policy mechanism mentioned |
| 18 | Manage AWS accounts with permission sets — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html | VERIFIED | One permission set creates IAM roles in each assigned account confirmed; reusability across accounts confirmed |
| 19 | AWS IAM Identity Center User Guide: Attributes for Access Control (ABAC) | https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html | VERIFIED | ABAC attribute propagation at authentication time documented; terminology uses "attributes" not "session tags" explicitly, but the mechanism is consistent |
| 20 | Attribute-based access control — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html | VERIFIED | ABAC in Identity Center confirmed; "fewer permission sets needed" benefit explicitly documented; session attribute propagation confirmed |
| 21 | Create permission policies for ABAC in IAM Identity Center — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html | VERIFIED | aws:PrincipalTag condition keys matched against resource tags confirmed with policy example |
| 22 | AWS IAM Identity Center User Guide: Getting Credentials | https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html | VERIFIED | Page live; credential retrieval via Identity Center (portal and CLI sso login) documented |
| 23 | Set session duration for AWS accounts — AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html | VERIFIED | Maximum 12-hour session duration for permission sets confirmed; default 1 hour confirmed |
| 24 | Create fine-grained session permissions using IAM managed policies — AWS Security Blog | https://aws.amazon.com/blogs/security/create-fine-grained-session-permissions-using-iam-managed-policies/ | VERIFIED | Page confirmed live; AWS Security Blog article on managed policy ARNs as session policies |
| 25 | Build an end-to-end attribute-based access control strategy with AWS IAM Identity Center and Okta — AWS Security Blog | https://aws.amazon.com/blogs/security/build-an-end-to-end-attribute-based-access-control-strategy-with-aws-sso-and-okta/ | VERIFIED | Page confirmed live; ABAC with Identity Center and Okta as external IdP is the topic; body content not fully rendered but title and existence confirmed |
| 26 | Understanding the API options for securely delegating access to your AWS account — AWS Security Blog | https://aws.amazon.com/blogs/security/understanding-the-api-options-for-securely-delegating-access-to-your-aws-account/ | UNVERIFIABLE | Fetch returned an error (sibling call failure); URL structure is consistent with AWS Security Blog and the title is plausible — could not confirm independently |
| 27 | Resolve the AWS STS PackedPolicyTooLarge IAM Assume Role Error — AWS re:Post | https://repost.aws/knowledge-center/iam-role-aws-sts-error | VERIFIED | Confirmed via web search; article resolves exactly this error; packed binary format limit and session tag budget sharing documented |
| 28 | AWS IAM User Guide: Switching Roles via Console | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html | VERIFIED | Page confirmed live; title: "Switch from a user to an IAM role (console)" |

**Note on sources 26:** The AWS Security Blog URL pattern is consistent and the title matches the content domain. The fetch failure was a tooling error (sibling call cancellation), not a dead URL indicator. Assessed as UNVERIFIABLE rather than DEAD for this run.

---

## Finding Verification

### Finding 1: STS AssumeRole Policy and PolicyArns parameters
- **Claim:** The STS AssumeRole API accepts an optional Policy parameter (inline JSON, max 2,048 combined chars with PolicyArns) and up to 10 managed policy ARN references; effective session permissions are the strict intersection of the role's identity-based policies and the session policy.
- **Verdict:** CONFIRMED
- **Evidence:** AWS STS AssumeRole API reference explicitly documents the Policy parameter (max 2,048 chars plaintext, shared with PolicyArns), PolicyArns (up to 10 entries), and states that permissions are the intersection of role policies and session policy. Packed binary format separate limit also documented.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html

---

### Finding 2: GetRoleCredentials has no Policy parameter
- **Claim:** IAM Identity Center issues credentials via GetRoleCredentials, a proprietary portal API accepting only three parameters (accessToken, accountId, roleName) with no Policy parameter — not via STS AssumeRole directly.
- **Verdict:** CONFIRMED
- **Evidence:** AWS IAM Identity Center Portal API Reference for GetRoleCredentials confirms exactly three parameters: accessToken, accountId, roleName. No Policy or PolicyArns parameter exists. The credential issuance path via the access portal and CLI sso login is confirmed to use this API.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html

---

### Finding 3: Role chaining as hybrid path — 1-hour ceiling
- **Claim:** Post-issuance role chaining is the only viable hybrid path: Identity Center issues credentials, then the application calls STS AssumeRole with a session policy using those credentials as the principal. AWS imposes a hard 1-hour session ceiling on all role-chained sessions regardless of the permission set's configured duration (up to 12 hours).
- **Verdict:** CONFIRMED
- **Evidence:** AssumeRole API reference explicitly states: "if you assume a role using role chaining and provide a DurationSeconds parameter value greater than one hour, the operation fails." Permission set maximum session duration of 12 hours is confirmed. The 1-hour ceiling is not configurable. The post-issuance chaining workaround is consistent with the GetRoleCredentials constraint (no Policy parameter at issuance, so a second AssumeRole call is the only injection point).
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html; https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html

---

### Finding 4: ABAC via session tags — Identity Center native, different control surface
- **Claim:** ABAC via session tags is the Identity Center-native mechanism for reducing permission set proliferation: Identity Center propagates user directory attributes as session tags at authentication time; permission set policies use aws:PrincipalTag condition keys matched against resource tags. ABAC reduces permission set count but operates on a fundamentally different control surface than session policies — it enforces resource-level access based on tag matching, not action-level restriction across the session.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** ABAC mechanism in Identity Center is confirmed: attributes from the identity source are propagated during authentication; aws:PrincipalTag conditions are used in permission policies to match resource tags; ABAC reducing permission set count is explicitly documented. The claim that Identity Center propagates attributes specifically as "session tags" (STS session tags) is the nuance: the Identity Center ABAC documentation uses the term "attributes" and confirms they are passed as principal tags for policy evaluation, which aligns with the session tag mechanism. The configure-abac-policies page confirms aws:PrincipalTag in permission set conditions. The distinction that ABAC enforces resource-level access rather than action-level restriction is accurate and consistent with how condition-key matching works. The claim is substantively correct but the specific characterization of attributes as "session tags" is not uniformly stated in the Identity Center ABAC pages themselves (they use "attributes" / "principal tags").
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html; https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html; https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html

---

### Finding 5: PackedPolicySize — two independent limits, unpublished byte ceiling
- **Claim:** Two independent size constraints apply: a 2,048-character plaintext limit on the combined inline policy JSON and managed policy ARN strings (whitespace counts), and a separate opaque packed binary limit whose byte ceiling AWS does not publish. Session tags share this binary budget; a call can fail PackedPolicyTooLarge even when the plaintext budget is not exhausted.
- **Verdict:** CONFIRMED
- **Evidence:** AssumeRole API reference and IAM quotas page confirm 2,048-char combined plaintext limit. AssumeRole, AssumeRoleWithSAML, and AssumeRoleWithWebIdentity all document a separate packed binary format limit without publishing the byte ceiling — only percentage feedback via PackedPolicySize response element. Session tags documentation confirms they share the packed binary budget with session policies. AWS re:Post knowledge-center article on PackedPolicyTooLarge confirms the failure mode and the byte ceiling's opacity.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html; https://repost.aws/knowledge-center/iam-role-aws-sts-error

---

### Finding 6: Session policies absent from Console, Policy Simulator, and CloudTrail
- **Claim:** Session policies have no presence in the AWS Management Console (no authoring, viewing, or attachment workflow), are not accepted by the IAM Policy Simulator (pre-deployment validation requires live environment testing), and the inline Policy document does not appear in documented CloudTrail AssumeRole log examples — leaving a structural audit gap where the effective permission scope of a session cannot be reconstructed post-hoc from CloudTrail alone.
- **Verdict:** CONFIRMED
- **Evidence:** IAM Policy Simulator documentation confirms session policies are not in the list of supported testable policy types — no session policy input parameter exists in SimulatePrincipalPolicy. CloudTrail integration documentation shows multiple AssumeRole examples; none include the inline Policy parameter in requestParameters. The absence from the Console is consistent with the fact that session policies are runtime parameters, not managed entities in IAM. The audit gap claim is substantiated by the CloudTrail documentation's omission of the Policy parameter from all AssumeRole log examples.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html; https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulatePrincipalPolicy.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html

---

### Finding 7: Three-way intersection and resource-based policy session-ARN bypass
- **Claim:** When both a permissions boundary and a session policy are active, effective permissions are the three-way intersection of identity-based policy, permissions boundary, and session policy. When a resource-based policy grants access to the session ARN (not the role ARN) as principal, those permissions bypass the session policy filter entirely.
- **Verdict:** CONFIRMED
- **Evidence:** Permissions boundaries documentation explicitly documents the three-way intersection with a diagram. The IAM access_policies.html session policies section explicitly states: "A resource-based policy can specify the ARN of the session as a principal. In that case, the permissions from the resource-based policy are added after the session is created. The resource-based policy permissions are not limited by the session policy." The contrast with the role ARN case (where the resource-based policy IS subject to session policy filtering) is also documented.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session

---

### Finding 8: Permission set as the practical consolidation ceiling under Identity Center
- **Claim:** The practical consolidation ceiling under Identity Center is the permission set: one permission set maps to one IAM role per account, and role proliferation shifts from the IAM layer to the permission set layer. Without ABAC, each distinct permission profile requires a distinct permission set. ABAC can reduce this only when resource tagging is consistent across accounts.
- **Verdict:** CONFIRMED
- **Evidence:** Identity Center documentation confirms that "IAM Identity Center creates corresponding IAM Identity Center-controlled IAM roles in each assigned account" when a permission set is provisioned — establishing the one-permission-set-per-account-role relationship. The ABAC documentation explicitly lists "fewer permission sets needed" as a direct benefit of ABAC. The tagging-discipline dependency for ABAC is substantiated by configure-abac-policies documentation showing that access differentiation depends on resource tag matching.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html; https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Source 26 (AWS Security Blog: API options for delegating access) | UNVERIFIABLE | Retry URL fetch in a fresh session to confirm accessibility; if confirmed live, no change needed; if dead, remove or replace |

---

## Overall Assessment

This rollup investigation is well-grounded. Seven of eight key findings are CONFIRMED against primary AWS documentation, and one (Finding 4 on ABAC session tags) is PARTIALLY CONFIRMED — the substantive mechanism is correct, but the investigation uses "session tags" as the canonical term for Identity Center-propagated attributes in contexts where the Identity Center documentation uses "attributes" or "principal tags." This is a terminology precision issue rather than a factual error; the underlying behavior is accurate and the configure-abac-policies documentation confirms the aws:PrincipalTag mechanism.

The central structural claim — that GetRoleCredentials accepts exactly three parameters with no Policy field, making session policy injection unavailable to Identity Center users — is confirmed directly against the Portal API Reference. The 1-hour role-chaining ceiling is confirmed against the AssumeRole API reference. The CloudTrail audit gap is substantiated by the absence of the Policy parameter in all documented AssumeRole log examples.

The PackedPolicySize packed-binary opacity claim is confirmed: AWS publishes only a percentage, not a byte ceiling.

One source (Source 26) could not be verified due to a fetch error and should be confirmed live in a follow-up session. No findings depend exclusively on this source.

No contradictions were found between the rollup findings and the documented evidence. No synthesis claims require correction. The investigation's framing — that the session policy consolidation pattern is structurally unavailable through Identity Center's standard credential path, and that ABAC and role chaining are the only viable alternatives with documented ceilings — accurately reflects the state of AWS documentation as of the investigation date.
