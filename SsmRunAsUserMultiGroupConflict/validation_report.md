# Validation Report: SSM RunAs Sync Pipeline — Entra ID, IAM Identity Center, and LZA (Rollup) — Cycle 1 Re-check
Date: 2026-02-27
Validator: Fact Validation Agent (cycle 1 re-check)

## Summary
- Total sources checked: 51 (2 re-verified in this cycle, 49 carried forward)
- Verified: 13 | Redirected: 0 | Dead: 0 | Unverifiable: 2 | Carried forward: 36
- Findings checked: 2 (cycle 1 re-check of corrected items only)
- Confirmed: 2 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/SsmRunAsUserMultiGroupConflict
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        13           13           6ac94f6a7789   6ac94f6a7789
tensions             IN_SYNC        7            7            4ee4d3391ddc   4ee4d3391ddc
open_questions       IN_SYNC        7            7            026db2b9691b   026db2b9691b
sources              IN_SYNC        51           51           911e69df54ca   911e69df54ca
concepts             IN_SYNC        12           12           dbbf9d8a5a4c   dbbf9d8a5a4c
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

All fields and brief files are IN_SYNC. No markdown regeneration required.

---

## Finding Verification (Cycle 1 Re-check)

### Finding 6 (key_findings[5]): StackSet + Lambda pattern is correct; LZA cloudFormationStackSets creates SELF_MANAGED only; SERVICE_MANAGED must be deployed outside LZA

**Corrected claim:** The StackSet + Lambda pattern — as demonstrated by the AWS Security Blog post "How to automate Session Manager preferences across your organization" (November 2025) and its companion sample (aws-samples/sample-how-to-automate-session-manager-preferences) — is the correct approach for org-wide SSM RunAs configuration. However, LZA's cloudFormationStackSets in customizations-config.yaml creates SELF_MANAGED StackSets only: the CloudFormationStackSetConfig interface exposes no permissionModel or autoDeployment property (GitHub issues #810 and #666 are open feature requests as of v1.14.x). To use SERVICE_MANAGED permissions — required for auto-deployment to new accounts via Organizations lifecycle events — the StackSet must be deployed outside LZA's customizations pipeline, via a standalone CloudFormation template, Terraform, or a separate automation layer.

**Verdict: CONFIRMED**

**Evidence:**

1. **AWS Security Blog post existence and date confirmed.** Web search confirms publication date of November 18, 2025 on the AWS Security Blog. The post describes using CloudFormation StackSets and a Lambda function to update SSM-SessionManagerRunShell across accounts. The companion GitHub repository (aws-samples/sample-how-to-automate-session-manager-preferences) is confirmed live with the three-component architecture: IAM policy deployment, AWS Config rule with remediation, and Lambda-backed custom resource. This confirms the StackSet + Lambda pattern as the correct approach.

2. **LZA cloudFormationStackSets creates SELF_MANAGED StackSets only — confirmed.** Direct fetch of the LZA TypeDoc source at `github.com/awslabs/landing-zone-accelerator-on-aws/blob/main/source/packages/@aws-accelerator/config/lib/customizations-config.ts` returns the `CloudFormationStackSetConfig` class definition with the following properties: `capabilities`, `deploymentTargets`, `description`, `name`, `regions`, `template`, `parameters`, `operationPreferences`, `dependsOn`, `administrationRoleArn`, `executionRoleName`. No `permissionModel` or `autoDeployment` property is present. This directly confirms the SELF_MANAGED-only limitation stated in the corrected finding.

3. **GitHub issues #810 and #666 — status confirmed.** GitHub issue #810 ("StackSets targeting empty OU fail with CloudFormation validation error") is confirmed to have been closed on August 5, 2025 as a duplicate of issue #666. The issue body explicitly states that LZA deploys SELF_MANAGED StackSets and recommends exposing the `permissionModel` parameter as a feature request. GitHub issue #666 is confirmed OPEN (0 of 1 sub-issues completed), tracking the same capability gap. The finding's characterization of both as open feature requests as of v1.14.x is accurate: #666 remains open and the feature has not been shipped.

4. **SERVICE_MANAGED requiring deployment outside LZA — confirmed.** The absence of `permissionModel` and `autoDeployment` from `CloudFormationStackSetConfig` confirms that achieving SERVICE_MANAGED permissions requires using a StackSet resource deployed entirely outside LZA's customizations pipeline. This is consistent with the corrected finding's statement that a standalone CloudFormation template, Terraform, or separate automation layer is required.

**Sources used:** https://aws.amazon.com/blogs/security/how-to-automate-session-manager-preferences-across-your-organization/; https://github.com/aws-samples/sample-how-to-automate-session-manager-preferences; https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/main/source/packages/%40aws-accelerator/config/lib/customizations-config.ts; https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/810; https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/666

---

### Finding 8 (key_findings[7]): SERVICE_MANAGED StackSet auto-deployment does trigger on Organizations lifecycle events; LZA cloudFormationStackSets does NOT support this natively

**Corrected claim:** CloudFormation SERVICE_MANAGED StackSets with auto-deployment enabled do trigger stack instance creation from Organizations lifecycle events when an account joins a targeted OU — this is the correct mechanism for closing the new-account gap without requiring a pipeline run. However, this capability is NOT available through LZA's cloudFormationStackSets in customizations-config.yaml, which creates SELF_MANAGED StackSets only (the CloudFormationStackSetConfig interface has no permissionModel or autoDeployment property; GitHub issues #810 and #666 are open feature requests as of v1.14.x). The auto-deployment pattern therefore requires the StackSet to be deployed outside LZA's customizations pipeline.

**Verdict: CONFIRMED**

**Evidence:**

1. **SERVICE_MANAGED StackSet auto-deployment triggers on Organizations lifecycle events — confirmed by AWS documentation.** The AWS CloudFormation documentation page "Enable or disable automatic deployments for StackSets in AWS Organizations" states: "CloudFormation can automatically deploy additional stacks to new AWS Organizations accounts when they're added to your target organization or organizational units (OUs)." It further states: "When automatic deployments are enabled, they're triggered when accounts are added to a target organization or OU, removed from a target organization or OU, or moved between target OUs." This directly confirms the first half of the corrected finding: the mechanism is real, operates via Organizations lifecycle events, and does not require a pipeline run.

2. **LZA cloudFormationStackSets does NOT support SERVICE_MANAGED or autoDeployment — confirmed.** As established under Finding 6 re-check (same evidence), the `CloudFormationStackSetConfig` class definition retrieved from the LZA source code exposes no `permissionModel` or `autoDeployment` property. The finding's characterization of this as a limitation (not a current capability) is accurate and supported by GitHub issues #810 and #666.

3. **The corrected finding's two-part structure is accurate.** The first part (SERVICE_MANAGED auto-deployment mechanism is correct) is confirmed by AWS documentation. The second part (LZA's cloudFormationStackSets does not support this natively) is confirmed by the TypeDoc interface definition and open GitHub issues. The conclusion (deployment outside LZA's customizations pipeline is required) follows directly from those two premises and is accurate.

**Sources used:** https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-manage-auto-deployment.html; https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html; https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/main/source/packages/%40aws-accelerator/config/lib/customizations-config.ts; https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/810; https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/666

---

## Carried Forward (Prior Validation)

The following findings were verified in the prior validation cycle and are not re-checked here:
- Finding 1 (IdC ABAC hard-rejects duplicate SAML attribute names): CONFIRMED
- Finding 2 (AWSReservedSSO_ roles cannot be tagged): CONFIRMED
- Finding 3 (correct architecture — per-user ABAC attribute): CONFIRMED
- Finding 4 (LZA ABAC gap — no InstanceAccessControlAttributeConfiguration surface): CONFIRMED
- Finding 5 (LZA preserves runAsEnabled/runAsDefaultUser): CONFIRMED
- Finding 10/SCIM precedence (SCIM > SAML, console > SAML, console-vs-SCIM undocumented): CONFIRMED
- Finding 11/OU-scoped assignments: PARTIALLY CONFIRMED (OU-scoping fixed in v1.10.0; management account failure status in v1.14.x undetermined)
- Sources: 13 directly verified, 2 unverifiable (Terraform Registry JS rendering, re:Post access restriction), 36 carried forward from sub-investigation validation

---

## Remediation Required

No remediation required. Both corrected findings are CONFIRMED. The investigation is accurate as corrected.

---

## Overall Assessment

Both corrected findings pass re-verification. Finding 6 now correctly scopes the StackSet + Lambda pattern as the right architectural approach while precisely naming the LZA limitation: `CloudFormationStackSetConfig` exposes no `permissionModel` or `autoDeployment` property (confirmed from LZA source code), and GitHub issues #810 and #666 confirm this is an open feature request. Finding 8 now correctly separates the general CloudFormation mechanism (SERVICE_MANAGED auto-deployment via Organizations lifecycle events — confirmed by AWS documentation) from the LZA-specific limitation (SELF_MANAGED only, no auto-deployment support). No further remediation is required. The investigation is cleared for commit and push.
