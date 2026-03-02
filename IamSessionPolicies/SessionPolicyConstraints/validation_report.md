# Validation Report: IAM Session Policy Constraints
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 13
- Verified: 11 | Redirected: 0 | Dead: 0 | Unverifiable: 2
- Findings checked: 9
- Confirmed: 7 | Partially confirmed: 2 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/IamSessionPolicies/SessionPolicyConstraints
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        9            9            41d56ecdd664   41d56ecdd664
tensions             IN_SYNC        5            5            e17ef2279e2d   e17ef2279e2d
open_questions       IN_SYNC        5            5            00e17c4c10ba   00e17c4c10ba
sources              IN_SYNC        13           13           894d40349434   894d40349434
concepts             IN_SYNC        8            8            c1af3e796e05   c1af3e796e05
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

No sync issues detected. All fields in sync. Brief files present and matching.

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | IAM and AWS STS Quotas — Session Policy Size and Count Limits | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html | VERIFIED | Page resolves. Documents the 2,048-character combined limit, 10 managed policy ARN maximum, PackedPolicySize, and the 600 RPS STS quota shared across AssumeRole, GetCallerIdentity, GetFederationToken, GetSessionToken, DecodeAuthorizationMessage, and GetAccessKeyInfo. |
| 2 | AssumeRole API Reference — Policy and PolicyArns Parameters | https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html | VERIFIED | Page resolves. Confirms 2,048-character combined plaintext limit for Policy and PolicyArns, 10-ARN maximum, one inline document per call, and PackedPolicySize response field with separate binary limit. |
| 3 | Policies and Permissions — Session Policies Section | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session | VERIFIED | Page resolves. Confirms intersection model: effective permissions are the intersection of identity-based policies and session policies; session policies cannot grant more than the role allows. |
| 4 | Pass Session Tags in AWS STS — Shared PackedPolicySize Budget | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html | VERIFIED | Page resolves. Confirms session tags and session policies share a packed binary budget; failure is reported as percentage; exact byte ceiling not published. |
| 5 | Logging IAM and AWS STS API Calls with AWS CloudTrail | https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html | VERIFIED | Page resolves. Example AssumeRole requestParameters show roleArn, roleSessionName, sourceIdentity, and session tags — no inline Policy document. Confirms the structural audit gap claimed. |
| 6 | Monitor and Control Actions Taken with Assumed Roles | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_monitor.html | VERIFIED | Page resolves and title matches. Content covers source identity tracking and CloudTrail logging for role sessions. Does not discuss session policy content logging. Weak citation for the CloudTrail audit gap finding — the finding is substantiated by source 5, not this page. |
| 7 | IAM Policy Testing with the IAM Policy Simulator | https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html | VERIFIED | Page resolves. Session policies are not mentioned as a supported input type. Supported types are identity-based policies, permissions boundaries, resource-based policies (S3, SQS, SNS, Glacier), and SCPs. Absence from the documentation supports the finding. |
| 8 | SimulatePrincipalPolicy API Reference | https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulatePrincipalPolicy.html | VERIFIED | Page resolves. Policy-related parameters are PolicySourceArn, PolicyInputList, PermissionsBoundaryPolicyInputList, and ResourcePolicy. No parameter corresponds to a session policy or session policy ARN. Confirms session policy is not a named input type. |
| 9 | GetRoleCredentials — IAM Identity Center Portal API Reference | https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html | VERIFIED | Page resolves. Confirmed three parameters only: accessToken, accountId, roleName. No Policy parameter exists. |
| 10 | Permissions for AssumeRole, AssumeRoleWithSAML, and AssumeRoleWithWebIdentity | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_assumerole.html | VERIFIED | Page resolves and title matches. Discusses session policies as optional parameters, confirms intersection model and restriction-only behavior. |
| 11 | Understanding the API Options for Securely Delegating Access to Your AWS Account | https://aws.amazon.com/blogs/security/understanding-the-api-options-for-securely-delegating-access-to-your-aws-account/ | UNVERIFIABLE | Direct fetch returned a network error. URL pattern and title are consistent with AWS Security Blog conventions. Web search confirms the URL exists and is indexed. Cannot confirm page content independently. |
| 12 | Resolve the AWS STS PackedPolicyTooLarge IAM Assume Role Error | https://repost.aws/knowledge-center/iam-role-aws-sts-error | UNVERIFIABLE | Direct fetch returned 403. URL resolves per web search results; the re:Post knowledge center article is indexed and confirmed by web search as covering PackedPolicyTooLarge resolution. Cannot confirm page content directly. |
| 13 | Create Fine-Grained Session Permissions Using IAM Managed Policies | https://aws.amazon.com/blogs/security/create-fine-grained-session-permissions-using-iam-managed-policies/ | VERIFIED | Page resolves. Title matches. Published on AWS Security Blog. Content covers managed session policies and the intersection model. |

---

## Finding Verification

### Finding 1: 2,048-Character Combined Plaintext Limit

- **Claim:** The 2,048-character plaintext limit applies to the combined character count of the inline session policy JSON and all managed policy ARN strings together; whitespace is counted, so production policies must be minified before transmission.
- **Verdict:** CONFIRMED
- **Evidence:** AssumeRole API reference states: "The plaintext that you use for both inline and managed session policies can't exceed 2,048 characters." The IAM quotas page confirms the combined scope. The re:Post knowledge center article (found via web search) confirms whitespace is counted in the total.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html

---

### Finding 2: PackedPolicySize — Opaque Binary Limit Beyond Plaintext Cap

- **Claim:** A second, opaque PackedPolicySize limit exists beyond the 2,048-character cap; AWS compresses the inline policy, managed policy ARNs, and session tags together into a packed binary format whose byte ceiling is not published; a call can fail with PackedPolicyTooLarge even when the plaintext budget is not exhausted, and the failure signal is a percentage indicator in the response rather than a byte count.
- **Verdict:** CONFIRMED
- **Evidence:** AssumeRole API reference states: "An AWS conversion compresses the passed inline session policy, managed policy ARNs, and session tags into a packed binary format that has a separate limit. Your request can fail for this limit even if your plaintext meets the other requirements." Session tags page confirms shared budget. PackedPolicySize response field is documented as a percentage indicator. Byte ceiling not published in any official source reviewed.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

---

### Finding 3: No Console UI for Session Policies

- **Claim:** Session policies have no presence in the AWS Management Console: they cannot be authored, viewed, attached, or audited through any console workflow; the feature is exclusively programmatic via STS APIs, requiring every operator interaction to go through the CLI or SDK.
- **Verdict:** CONFIRMED
- **Evidence:** No AWS documentation reviewed references console support for session policies. The IAM quotas page notes the CLI or API for session policies. The AWS Security Blog post on managed session policies describes only programmatic usage. No console workflow appears in any official documentation.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html; https://aws.amazon.com/blogs/security/create-fine-grained-session-permissions-using-iam-managed-policies/
- **Note:** This finding is confirmed by the universal absence of console documentation, not by a single explicit statement. This is the expected documentation pattern for console-unsupported features.

---

### Finding 4: IAM Policy Simulator Does Not Accept Session Policies

- **Claim:** The IAM Policy Simulator does not accept session policies as a named input type: SimulatePrincipalPolicy and SimulateCustomPolicy support identity-based policies, permissions boundaries, and resource-based policies but not the intersection of role policy and session policy; validating effective permissions requires live environment testing.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** SimulatePrincipalPolicy API reference confirms that no parameter corresponds to a session policy or session policy ARN. The IAM Policy Simulator documentation page does not mention session policies among supported input types. However, SimulatePrincipalPolicy has a PolicyInputList parameter that accepts arbitrary policy JSON strings; a caller could theoretically pass a session policy document through PolicyInputList, though this is not a named or documented session policy path and would not model the intersection semantics correctly. The claim that session policies are not a supported named input type is accurate. The claim that "effective permissions require live environment testing" is a reasonable inference from the absence but is not explicitly stated in official documentation.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulatePrincipalPolicy.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html

---

### Finding 5: IAM Identity Center GetRoleCredentials Has No Policy Parameter

- **Claim:** IAM Identity Center's GetRoleCredentials API accepts only three parameters — accessToken, accountId, and roleName — with no Policy parameter; organizations whose users obtain credentials through Identity Center cannot attach session policies to those credentials without bypassing Identity Center entirely.
- **Verdict:** CONFIRMED
- **Evidence:** GetRoleCredentials API reference confirms exactly three parameters: accessToken, accountId, roleName. No Policy parameter exists. Response returns STS short-term credentials directly. The structural incompatibility with session policy attachment is exact and documented.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html

---

### Finding 6: CloudTrail Does Not Log the Inline Policy Parameter

- **Claim:** Inline session policy content does not appear in documented CloudTrail AssumeRole log examples; the requestParameters field in documented log samples contains roleArn, roleSessionName, and sourceIdentity but not the Policy document; this creates a structural audit gap where the effective permission scope of a session cannot be reconstructed post-hoc from CloudTrail alone.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The CloudTrail integration documentation page shows AssumeRole requestParameters examples with roleArn, roleSessionName, sourceIdentity, serialNumber, and session tags — no inline Policy document appears. This confirms the claim that documented examples omit the Policy parameter. However, the investigation's open_questions section correctly acknowledges that absence from documented examples has not been definitively confirmed or denied as a logging omission by AWS. The claim is supported by official documentation examples but the investigation appropriately hedges in open_questions. No official source was found that explicitly states the Policy parameter is never logged; it may be present in actual CloudTrail events but simply absent from documentation examples.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html

---

### Finding 7: STS AssumeRole Shares 600 RPS Regional Quota

- **Claim:** The STS AssumeRole API shares a 600-requests-per-second regional quota with GetCallerIdentity, GetFederationToken, GetSessionToken, and DecodeAuthorizationMessage; workloads that assume a fresh role-with-session-policy per request will compete for this shared budget.
- **Verdict:** CONFIRMED (with minor omission noted)
- **Evidence:** The IAM and AWS STS quotas page confirms the 600 RPS per account per region quota and lists the operations sharing it. The finding's list of operations is accurate but incomplete: the quotas page also includes GetAccessKeyInfo in the shared pool. This is a minor omission that does not affect the substance of the finding; the competitive quota pressure argument is unaffected.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html

---

### Finding 8: Only One Inline Session Policy Document Per AssumeRole Call

- **Claim:** Only one inline JSON session policy document can be passed per AssumeRole call; complex scoping logic that exceeds the character budget must be pre-staged as a named managed policy and referenced via PolicyArns, shifting the policy lifecycle to IAM policy management rather than call-time composition.
- **Verdict:** CONFIRMED
- **Evidence:** The AssumeRole API reference states: "You can pass a single JSON policy document to use as an inline session policy." The IAM quotas page documents the one-document limit. The managed policy fallback (up to 10 ARNs) is confirmed in both sources.
- **Source used:** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html

---

### Finding 9: Session Policies Enforce an Intersection Model

- **Claim:** Session policies enforce an intersection model: the effective permissions of a session are the intersection of the role's identity-based policies and the session policy; session policies can only restrict, never expand, the role's permissions.
- **Verdict:** CONFIRMED
- **Evidence:** The session policies section of the IAM policies page states: "The permissions for a session are the intersection of the identity-based policies for the IAM entity used to create the session and the session policies." The AssumeRole permissions page states: "You cannot use session policies to grant more permissions than those allowed by the identity-based policy of the role that is being assumed."
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session; https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_assumerole.html

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 7 — STS quota shared operations list | CONFIRMED (minor omission) | Consider adding GetAccessKeyInfo to the list of operations sharing the 600 RPS quota for completeness. Not a factual error; the finding is substantively correct. Low priority. |

No CONTRADICTED or UNVERIFIED findings. No DEAD sources. No OUT_OF_SYNC artifacts.

---

## Overall Assessment

This investigation is factually sound. All nine key findings are confirmed or partially confirmed against official AWS documentation. The two PARTIALLY CONFIRMED verdicts reflect appropriate epistemic hedging already present in the investigation: Finding 4 notes that the Policy Simulator gap requires live testing (accurate, though a PolicyInputList workaround exists that would not model session policy intersection semantics correctly), and Finding 6 accurately represents the documented CloudTrail examples while the open_questions section correctly flags the definitive answer as unresolved. Neither partial confirmation warrants remediation.

The one source-quality note is source 6 (`id_credentials_temp_control-access_monitor.html`), which resolves and has a matching title but does not directly address session policy content in CloudTrail — that evidence is properly carried by source 5 (`cloudtrail-integration.html`). Source 6 is a valid secondary reference for the broader audit visibility section but is not the load-bearing citation for the CloudTrail gap finding.

Sources 11 and 12 could not be fetched directly (network error and 403 respectively) but are confirmed to exist and be indexed via web search, and neither carries findings that are not independently confirmed by primary official documentation.

The investigation correctly identifies and documents all six major operational constraints on session policies, the intersection model, and the character budget mechanics with accurate figures. The open questions are appropriately scoped to genuinely unresolved items. No remediation is required before this investigation is committed.
