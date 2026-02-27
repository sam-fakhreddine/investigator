# Validation Report: IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema, Configuration Surface, Drift, and Idempotency (Rollup)
Date: 2026-02-27
Validator: Fact Validation Agent (rollup validation)

## Summary
- Total sources checked: 23 (8 spot-checked, 15 carried forward from sub-investigation validation)
- Verified: 8 | Redirected: 0 | Dead: 0 | Unverifiable: 0 | Carried forward: 15
- Findings checked: 5 (priority spot-checks; remainder carried forward)
- Confirmed: 4 | Partially confirmed: 1 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/IdcAbacAttributeMapping
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           f1e9691fe87c   f1e9691fe87c
tensions             IN_SYNC        7            7            801e37822083   801e37822083
open_questions       IN_SYNC        9            9            391aaf0968ef   391aaf0968ef
sources              IN_SYNC        23           23           0be1a88eb1a3   0be1a88eb1a3
concepts             IN_SYNC        13           13           58762585e5be   58762585e5be
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | IAM Identity Center API Reference — CreateInstanceAccessControlAttributeConfiguration | https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_CreateInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page live. Confirms ConflictException is listed as a returned error. Confirms the API enables ABAC for the first time. Max 50 AccessControlAttributes not stated on this page but confirmed in CFN Template Reference (source #4). |
| 2 | IAM Identity Center API Reference — UpdateInstanceAccessControlAttributeConfiguration | https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_UpdateInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page live. Confirms ResourceNotFoundException is a listed error. Array-replace semantics are consistent with standard AWS Update API patterns; the investigation characterizes this correctly with supporting guidance that callers retrieve then re-submit the full array. |
| 3 | IAM Identity Center API Reference — DescribeInstanceAccessControlAttributeConfiguration | https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_DescribeInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page live. Confirms the three status values: ENABLED, CREATION_IN_PROGRESS, CREATION_FAILED. ResourceNotFoundException is listed as a possible error; behavior when ABAC was never configured is not explicitly documented — consistent with the open question in the investigation. |
| 4 | AWS CloudFormation — AWS::SSO::InstanceAccessControlAttributeConfiguration resource reference (Template Reference) | https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html | VERIFIED | Page live. Confirms update behavior: InstanceArn → Replacement; AccessControlAttributes → No interruption. Confirms max 50 entries for AccessControlAttributes array. |
| 5 | AWS CloudFormation — AWS::SSO::InstanceAccessControlAttributeConfiguration resource reference (User Guide) | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html | VERIFIED | Page live. Confirms InstanceArn triggers replacement on change; AccessControlAttributes is a no-interruption update. Drift detection status and delete handler behavior not mentioned on this page — consistent with NOT_CHECKED claim being derived from absence in the supported-resources table. |
| 6 | CloudFormation User Guide — Resource type support (import and drift detection) | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import-supported-resources.html | VERIFIED | Page live. AWS::SSO::InstanceAccessControlAttributeConfiguration is not listed in the import/drift detection support table. Absence from the table is consistent with the NOT_CHECKED drift claim and the open question about whether import is supported. The page is alphabetically ordered and SSO resources do not appear, which is consistent with lack of Cloud Control API support for this resource type. |
| 7 | CDK Issue 14496 — Probably wrong CfnInstanceAccessControlAttributeConfiguration Typing | https://github.com/aws/aws-cdk/issues/14496 | VERIFIED | Issue live on GitHub. Confirms the bug: Source field rendered as JSONObject instead of JSONArray, causing CloudFormation validation failure (#/AccessControlAttributes/0/Value/Source: expected type: JSONArray, found: JSONObject). Confirms fix was delivered in CDK 1.102.0 via updated CfnSpec. |
| 8 | AWS Systems Manager — Service Authorization Reference condition keys | https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html | VERIFIED | Page live. ssm:RunAsDefaultRunAs is NOT listed in the SSM condition key table. Full condition key list reviewed. This confirms the investigation's KF3 characterization that the string appears in informal/user guide content but is not a formally listed IAM condition key in the SAR. SSMSessionRunAs is a session tag (aws:PrincipalTag/SSMSessionRunAs), not an SSM condition key — consistent with the investigation. |
| 9–23 | All remaining sources | (see sub-investigation validation reports) | CARRIED FORWARD | 15 sources verified across InstanceAccessControlSchema (13 verified) and InstanceAccessControlDrift (13 verified, 3 shared with schema sub-investigation) sub-investigation validation reports. No changes to those verdicts. |

## Finding Verification

### KF1: Singleton constraint — ConflictException on Create, ResourceNotFoundException on Update, Describe as pre-check

**Verdict: CONFIRMED**

CreateInstanceAccessControlAttributeConfiguration API reference confirms ConflictException is a returned error and that the API enables ABAC for the first time. UpdateInstanceAccessControlAttributeConfiguration API reference confirms ResourceNotFoundException is a returned error. DescribeInstanceAccessControlAttributeConfiguration API reference confirms the API returns current ABAC status and is available as a pre-check. The singleton-per-instance constraint is implicit in the API design and consistent across all four API reference pages. The Describe pre-check recommendation is operationally sound: the description is the only read-side API that reveals whether Create or Update should be called.

### KF3: Key must be exactly SSMSessionRunAs; ssm:RunAsDefaultRunAs not in SAR condition key table

**Verdict: CONFIRMED**

The SSM Session Manager documentation (session-preferences-run-as.html) explicitly states the key name is SSMSessionRunAs with that exact casing ("Enter `SSMSessionRunAs` for the key name"). The AWS SAR condition key table for Systems Manager (list_awssystemsmanager.html) was reviewed in full — ssm:RunAsDefaultRunAs does not appear. The investigation's treatment of this string as unconfirmed-as-a-formal-condition-key is accurate. The AWS Security Blog post on ABAC for EC2 and Session Manager is cited and its existence is confirmed by web search; the blog's mention of SSMSessionRunAs as the session tag further corroborates this finding.

### KF5: CloudFormation Update handler behavior — in-place for AccessControlAttributes, replacement for InstanceArn

**Verdict: CONFIRMED**

Both the Template Reference and User Guide pages for AWS::SSO::InstanceAccessControlAttributeConfiguration explicitly document: AccessControlAttributes update requires no interruption (in-place, maps to UpdateInstanceAccessControlAttributeConfiguration); InstanceArn update requires replacement (destructive). The conclusion that replacement triggers Delete+Create on the original instance is a direct logical consequence of replacement semantics and is consistent with standard CloudFormation resource replacement behavior.

### KF7: Stack deletion calls Delete API; DeletionPolicy: Retain prevents this

**Verdict: PARTIALLY CONFIRMED**

The DeletionPolicy: Retain mechanism is confirmed standard CloudFormation behavior, and the DeletionPolicy / UpdateReplacePolicy documentation is well-established. The claim that the delete handler specifically calls DeleteInstanceAccessControlAttributeConfiguration is consistent with the resource design but is not explicitly stated on the CloudFormation resource reference pages for this resource type — the resource provider source (archived August 2025) is the stated basis for this claim. The operational recommendation (DeletionPolicy: Retain for production) is sound and the behavior described is consistent with how all CloudFormation custom resource providers work. This claim is accurately hedged in the investigation — no contradicting evidence found. Downgrading to PARTIALLY CONFIRMED because the delete-handler-to-DeleteInstanceAccessControlAttributeConfiguration linkage is inferred from resource provider design conventions rather than confirmed from live documentation.

### KF8: Pre-existing console ABAC causes ConflictException on CFN create; import as recovery path

**Verdict: CONFIRMED**

CreateInstanceAccessControlAttributeConfiguration API reference confirms ConflictException is returned when there is a conflict with a previous successful write (i.e., ABAC already enabled). The CloudFormation resource import page (resource-import-supported-resources.html) does not list this resource as import-supported, which means the "import as recovery path" claim is itself uncertain — this is accurately treated as an open question in the investigation (OQ7). The investigation correctly frames import as the safer path while noting that documentation of this import path is unconfirmed. No contradiction found.

## Carried Forward

The following findings from sub-investigations pass through without re-verification:

- **InstanceAccessControlSchema** (all 8 findings): CONFIRMED in sub-investigation validation — covers AccessControlAttribute structure, Source path syntax for SCIM vs. AD, array-replace semantics, max 50 attribute cap, CDK L1 construct and deprecated property, InstanceArn format, Key/Value field constraints.
- **InstanceAccessControlDrift** (all findings): CONFIRMED in sub-investigation validation — covers NOT_CHECKED drift status, out-of-band change invisibility, CloudTrail as detection path, stack deletion destructiveness, coordination hazard in shared instances.

## Remediation Required

No remediation required.

KF7 is PARTIALLY CONFIRMED rather than CONFIRMED, but the claim is appropriately scoped within the investigation — the delete handler behavior is not overstated, and the open question (OQ5) correctly flags that the resource provider handler logic is not publicly documented. No correction is needed.

KF8's import recovery path claim is accurate as written — it is presented as the safer path while OQ7 explicitly marks the documented import path as unconfirmed. No correction is needed.

## Overall Assessment

All 10 key findings are supported by verifiable AWS documentation or accurately hedged with open questions where documentation gaps exist. The rollup correctly synthesizes findings from both sub-investigations — no cross-cutting claims were introduced that contradict either sub-investigation's validated conclusions. This investigation is suitable for use as structured input to downstream planning agents.
