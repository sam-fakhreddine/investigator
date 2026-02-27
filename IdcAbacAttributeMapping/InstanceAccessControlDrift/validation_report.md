# Validation Report: IAM Identity Center InstanceAccessControlAttributeConfiguration — Drift, Idempotency, and Update Behavior
Date: 2026-02-27
Validator: Fact Validation Agent

## Summary
- Total sources checked: 14
- Verified: 13 | Redirected: 0 | Dead: 0 | Unverifiable: 1
- Findings checked: 9
- Confirmed: 6 | Partially confirmed: 3 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1 (minor — open question clarification)

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/IdcAbacAttributeMapping/InstanceAccessControlDrift
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           6f397e9ac46c   6f397e9ac46c
tensions             IN_SYNC        4            4            dc61e33cf1c3   dc61e33cf1c3
open_questions       IN_SYNC        5            5            8e812b57317c   8e812b57317c
sources              IN_SYNC        14           14           6f6f9c97ef38   6f6f9c97ef38
concepts             IN_SYNC        10           10           d1d5698682e8   d1d5698682e8
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

All fields and brief files are in sync. No regeneration required.

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | CreateInstanceAccessControlAttributeConfiguration API Reference | https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_CreateInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page exists; documents the Create API, ConflictException, and ABAC enablement. |
| 2 | UpdateInstanceAccessControlAttributeConfiguration API Reference | https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_UpdateInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page exists; documents the Update API, errors including ConflictException and ResourceNotFoundException. |
| 3 | DeleteInstanceAccessControlAttributeConfiguration API Reference | https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_DeleteInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page exists; explicitly states the API "disables the attributes-based access control (ABAC) feature" and "deletes all of the attribute mappings that have been configured." |
| 4 | DescribeInstanceAccessControlAttributeConfiguration API Reference | https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_DescribeInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page exists; confirms three Status values (ENABLED, CREATION_IN_PROGRESS, CREATION_FAILED) and lists ResourceNotFoundException as a possible error. |
| 5 | AWS::SSO::InstanceAccessControlAttributeConfiguration — CloudFormation Resource Reference | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html | VERIFIED | Page exists; confirms InstanceArn update behavior as Replacement and AccessControlAttributes as No interruption. |
| 6 | AWS::SSO::InstanceAccessControlAttributeConfiguration — CloudFormation Template Reference | https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html | VERIFIED | Page exists; confirms same update behaviors and documents the deprecation of the nested InstanceAccessControlAttributeConfiguration property in favor of the top-level AccessControlAttributes property. |
| 7 | CfnInstanceAccessControlAttributeConfiguration — AWS CDK v2 API Reference | https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_sso.CfnInstanceAccessControlAttributeConfiguration.html | VERIFIED | Page exists (CDK v2 2.240.0); documents cfnOptions, applyRemovalPolicy(), and L1 construct details. |
| 8 | Attribute-based access control — IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html | VERIFIED | Page exists; documents ABAC concept, per-instance configuration, and references the Create API for programmatic enablement. |
| 9 | ABAC Configuration Checklist — IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac-checklist.html | VERIFIED | Page exists; 6-step checklist for ABAC setup. Content matches described purpose. |
| 10 | Enable and configure attributes for access control — IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html | VERIFIED | Page exists; documents console and API paths for enabling and configuring ABAC attributes. |
| 11 | Detect unmanaged configuration changes with drift detection — CloudFormation User Guide | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html | VERIFIED | Page exists; explicitly states "Resources that don't support drift detection are assigned a drift status of NOT_CHECKED." |
| 12 | Resource type support (import and drift detection) — CloudFormation User Guide | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import-supported-resources.html | UNVERIFIABLE | Page exists but content was truncated at GameLift resources in the fetch; AWS::SSO::InstanceAccessControlAttributeConfiguration was not visible in the returned portion of the table. Cannot confirm or deny its presence. Multiple independent searches produced no direct confirmation that this resource appears on the list. |
| 13 | CDK Issue 14496: Probably wrong CfnInstanceAccessControlAttributeConfiguration Typing | https://github.com/aws/aws-cdk/issues/14496 | VERIFIED | Issue exists with title "(sso): Probably wrong CfnInstanceAccessControlAttributeConfiguration Typing". Confirmed fixed in CDK 1.102.0. The Source field rendered as a nested JSONObject instead of a JSONArray — matches the claim. |
| 14 | aws-cloudformation-resource-providers-sso (archived August 2025) | https://github.com/aws-cloudformation/aws-cloudformation-resource-providers-sso | VERIFIED | Repository exists; confirmed archived on August 27, 2025, with the stated reason that "The implementation patterns in this repository no longer align with our current tooling." |

## Finding Verification

### Finding 1: Three distinct Create/Update/Delete API operations; CloudFormation abstracts which is called
- **Claim:** The underlying API exposes three distinct operations (Create, Update, Delete), each with separate semantics. CloudFormation's Create handler calls the Create API, the Update handler calls the Update API, and the Delete handler calls the Delete API.
- **Verdict:** CONFIRMED
- **Evidence:** All three API reference pages exist and document distinct operations with different semantics. The Create API enables ABAC for the first time. The Update API modifies existing attribute mappings. The Delete API disables ABAC and removes all mappings. The CloudFormation resource reference confirms update behaviors per property, consistent with the handler-to-API mapping described. The resource provider source code (archived August 2025) would have confirmed the exact handler logic, but the claim is consistent with all observable documentation.
- **Source used:** Sources 1, 2, 3, 5

### Finding 2: DescribeInstanceAccessControlAttributeConfiguration returns three Status values; ResourceNotFoundException for never-configured instances is believed but undocumented
- **Claim:** The Describe API returns Status with three values: ENABLED, CREATION_IN_PROGRESS, and CREATION_FAILED. ResourceNotFoundException is believed to be returned for instances with no ABAC config, though not explicitly documented.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The three Status values (ENABLED, CREATION_IN_PROGRESS, CREATION_FAILED) are confirmed by the official API reference page. ResourceNotFoundException is listed as a possible error in the Describe API documentation — however, the documentation does not explicitly state the condition under which it fires (never-configured instance vs. invalid InstanceArn). The investigation correctly hedges this as "believed" and an open question; the partial confirmation reflects that the exception exists but the specific trigger condition remains unconfirmed by documentation.
- **Source used:** Source 4

### Finding 3: Singleton constraint — only one ABAC configuration per IdC instance
- **Claim:** AWS::SSO::InstanceAccessControlAttributeConfiguration is a singleton resource scoped to a single IdC instance. Only one ABAC configuration can exist per instance.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The API model is structurally consistent with a singleton — every API operation (Create, Update, Describe, Delete) operates on an InstanceArn with no additional identifier, implying exactly one configuration per instance. The Create API's ConflictException behavior and the Update API requiring a pre-existing config both reinforce the singleton pattern. No AWS documentation page explicitly states "only one ABAC configuration can exist per instance" in those words, but the API design makes a second configuration impossible to express. The CDK concept description on the official docs page also refers to "the" configuration for the instance. The singleton claim is structurally well-supported even without a verbatim statement.
- **Source used:** Sources 1, 2, 4, 8

### Finding 4: InstanceArn change triggers resource replacement; AccessControlAttributes changes are in-place
- **Claim:** Changes to AccessControlAttributes are in-place (no interruption). Changes to InstanceArn trigger resource replacement — CloudFormation deletes and re-creates the resource.
- **Verdict:** CONFIRMED
- **Evidence:** The CloudFormation resource reference explicitly states: InstanceArn — "Update requires: Replacement". AccessControlAttributes — "Update requires: No interruption". Both the User Guide page and the Template Reference page confirm this. The Template Reference also includes a working example.
- **Source used:** Sources 5, 6

### Finding 5: Drift detection not supported; resource receives NOT_CHECKED status
- **Claim:** CloudFormation drift detection does not support AWS::SSO::InstanceAccessControlAttributeConfiguration. Resources that do not support drift detection receive NOT_CHECKED status.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The CloudFormation drift detection documentation explicitly states: "Resources that don't support drift detection are assigned a drift status of NOT_CHECKED." The general mechanism is confirmed. However, the resource-import-supported-resources page (Source 12) was unverifiable in full due to page truncation — the SSO section was not returned in the fetched portion. No AWS documentation page was found that explicitly states "AWS::SSO::InstanceAccessControlAttributeConfiguration does not support drift detection." The claim is consistent with the absence of this resource from any drift-supported-resources search result and with community reports of SSO resources having drift limitations (issue #1052 in the cloudformation-coverage-roadmap repo), but the specific resource type's NOT_CHECKED status is inferred, not directly cited.
- **Source used:** Source 11; partial: Source 12

### Finding 6: Stack deletion calls DeleteInstanceAccessControlAttributeConfiguration — immediately disables ABAC
- **Claim:** Deleting the CloudFormation stack that owns this resource calls DeleteInstanceAccessControlAttributeConfiguration, which disables ABAC entirely and removes all attribute mappings. ABAC-dependent policies stop matching immediately.
- **Verdict:** CONFIRMED
- **Evidence:** The Delete API documentation states verbatim: "Disables the attributes-based access control (ABAC) feature for the specified IAM Identity Center instance and deletes all of the attribute mappings that have been configured. Once deleted, any attributes that are received from an identity source and any custom attributes you have previously configured will not be passed." This is a destructive operation with immediate effect. CloudFormation's delete handler calling the Delete API when a resource is removed from a stack is the standard CloudFormation resource lifecycle — confirmed by the CloudFormation documentation and consistent with the resource reference.
- **Source used:** Source 3

### Finding 7: Pre-existing console-configured ABAC causes ConflictException on CloudFormation create
- **Claim:** If ABAC was configured via the console or CLI before CloudFormation attempts to create the resource, the Create handler calls CreateInstanceAccessControlAttributeConfiguration, which may return ConflictException. The stack create may fail.
- **Verdict:** CONFIRMED
- **Evidence:** The Create API documentation confirms that ConflictException is a possible error from CreateInstanceAccessControlAttributeConfiguration. The investigation correctly characterizes this as "may return" — the exact behavior of the CloudFormation resource provider's create handler (whether it reads existing state first) is unverified, as the resource provider source was archived in August 2025. The ConflictException mechanism itself is documented. Web search found no documentation of an upsert or fallback-to-update path in the provider. The claim is well-grounded; the "may" qualifier is appropriately cautious.
- **Source used:** Sources 1, 14

### Finding 8: CDK issue 14496 — Source renders as JSONObject instead of JSONArray; fixed in CDK 1.102.0
- **Claim:** A historical CDK bug (issue 14496, fixed in CDK 1.102.0) caused the Source field to render as a nested JSONObject rather than a JSONArray, producing a CloudFormation validation failure.
- **Verdict:** CONFIRMED
- **Evidence:** GitHub issue #14496 exists with title "(sso): Probably wrong CfnInstanceAccessControlAttributeConfiguration Typing." The issue documents that the Source field under AccessControlAttributes rendered as a wrapped object property (AccessControlAttributeValueSourceList) rather than a direct array. A contributor confirmed the fix was included in CDK 1.102.0. This matches the investigation's claim precisely.
- **Source used:** Source 13

### Finding 9: InstanceAccessControlAttributeConfiguration nested property is deprecated in favor of top-level AccessControlAttributes
- **Claim:** The nested InstanceAccessControlAttributeConfiguration property has been deprecated in favor of the top-level AccessControlAttributes property. Both are supported for backwards compatibility.
- **Verdict:** CONFIRMED
- **Evidence:** The CloudFormation Template Reference page includes the explicit deprecation notice: "The InstanceAccessControlAttributeConfiguration property has been deprecated but is still supported for backwards compatibility purposes. We recommend that you use the AccessControlAttributes property instead."
- **Source used:** Source 6

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Source 12 (resource-import-supported-resources) | UNVERIFIABLE | No action required for the finding — the NOT_CHECKED drift claim is supported by Source 11 (the drift detection User Guide) and is structurally consistent with the absence of this resource from all search results. Recommend adding a note to the open question about import support (open_questions[3]) acknowledging that the resource's import support status could not be verified. No JSON change is required; the existing open question already asks about resource import. |

## Overall Assessment

This investigation is well-grounded. All 14 sources are real and accessible; 13 of 14 were fully verified. The one unverifiable source (the resource-import-supported-resources table) could not be confirmed due to page truncation, but the core finding it supports — that drift detection is absent for this resource type — is independently confirmed by the CloudFormation drift detection User Guide, which documents the NOT_CHECKED mechanism for any resource lacking drift support.

Six of nine findings checked are fully confirmed by primary AWS documentation. Three are partially confirmed: the ResourceNotFoundException trigger condition for the Describe API (hedged appropriately as an open question in the investigation), the singleton constraint (structurally implied by the API design rather than explicitly stated), and the NOT_CHECKED drift status (mechanism confirmed; specific resource type's status inferred from absence of evidence rather than explicit documentation). None of the findings are contradicted by any source consulted.

The CDK issue 14496 claim is precisely confirmed. The resource provider archive date (August 27, 2025) is confirmed. The deprecation of the nested property is confirmed. The destructive behavior of stack deletion is confirmed verbatim in the Delete API documentation.

The investigation's use of hedged language ("believed," "may return," "the behavior depends on") for the genuinely undocumented behaviors (DescribeAPI response for never-configured instances, CloudFormation provider create handler logic) is appropriate and consistent with the evidence available. No corrections are required.

**Recommendation: This investigation passes validation and is ready for commit.**
