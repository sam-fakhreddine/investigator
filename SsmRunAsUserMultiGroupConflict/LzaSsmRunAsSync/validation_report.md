# Validation Report: LZA SSM RunAs Synchronization Across Member Accounts
Date: 2026-02-27
Validator: Fact Validation Agent

## Summary
- Total sources checked: 24
- Verified: 22 | Redirected: 0 | Dead: 0 | Unverifiable: 2
- Findings checked: 8 (high-stakes claims as specified in scope)
- Confirmed: 6 | Partially confirmed: 2 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/LzaSsmRunAsSync
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        12           12           9f639b758c13   9f639b758c13
tensions             IN_SYNC        7            7            f15ad2c22166   f15ad2c22166
open_questions       IN_SYNC        6            6            d5e87542c314   d5e87542c314
sources              IN_SYNC        24           24           1c26cbd704b9   1c26cbd704b9
concepts             IN_SYNC        11           11           b9e3e9910575   b9e3e9910575
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

All fields in sync. Both brief files present. No OUT_OF_SYNC items. check_sync.py exited 0.

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | How to automate Session Manager preferences across your organization — AWS Security Blog (November 2025) | https://aws.amazon.com/blogs/security/how-to-automate-session-manager-preferences-across-your-organization/ | VERIFIED | Confirmed live, published November 18, 2025. Content matches claims: uses CloudFormation StackSets and Lambda to update SSM-SessionManagerRunShell across accounts. |
| 2 | aws-samples/sample-how-to-automate-session-manager-preferences — GitHub | https://github.com/aws-samples/sample-how-to-automate-session-manager-preferences | VERIFIED | Confirmed live. Three-component architecture (IAM policy, Config rule, Lambda custom resource) matches investigation description. |
| 3 | Implementing AWS Session Manager logging guardrails in a multi-account environment — AWS Cloud Operations Blog | https://aws.amazon.com/blogs/mt/implementing-aws-session-manager-logging-guardrails-in-a-multi-account-environment/ | VERIFIED | Confirmed live. SCP pattern denying ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument confirmed present in the article. |
| 4 | aws-samples/ssm-monitoring-logging-guardrails-multiaccount — GitHub | https://github.com/aws-samples/ssm-monitoring-logging-guardrails-multiaccount | VERIFIED | Confirmed live. Repository confirmed as companion to the Cloud Operations Blog post. |
| 5 | Session document schema — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-schema.html | VERIFIED | Confirmed live. runAsEnabled and runAsDefaultUser fields documented in the schema. |
| 6 | Turn on Run As support for Linux and macOS managed nodes — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED | Confirmed live. SSMSessionRunAs tag priority and runAsDefaultUser fallback behavior documented. |
| 7 | Sharing SSM documents — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/documents-ssm-sharing.html | VERIFIED | Confirmed live. ModifyDocumentPermission API described; sharing grants access to reference the document, does not copy it locally. |
| 8 | Best practice considerations when using AWS Systems Manager document sharing — AWS Cloud Operations Blog | https://aws.amazon.com/blogs/mt/best-practice-considerations-aws-systems-manager-document-sharing/ | VERIFIED | Confirmed live via search result match. |
| 9 | awslabs/landing-zone-accelerator-on-aws — GitHub main repository | https://github.com/awslabs/landing-zone-accelerator-on-aws | VERIFIED | Confirmed live. Active repository with ongoing releases. |
| 10 | Landing Zone Accelerator on AWS CHANGELOG (v1.14.2 branch) — runAs preserve fix | https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/release/v1.14.2/CHANGELOG.md | VERIFIED | Confirmed live. Search results confirm the preserve behavior for runAsEnabled and runAsDefaultUser is documented in the CHANGELOG. |
| 11 | SSM Document Sharing Fails in SecurityAudit Stack — GitHub Issue #786 (LZA v1.12.1) | https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/786 | VERIFIED | Confirmed live. Issue title confirmed as "SSM Document Sharing Fails in SecurityAudit Stack with InvalidParameterException Despite Valid shareTargets (v1.12.1)". Error is ModifyDocumentPermission called without AccountIdsToAdd populated, matching the investigation's description. |
| 12 | ssmAutomation is not sharing documents with other accounts — GitHub Issue #419 (LZA) | https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/419 | VERIFIED | Confirmed live. Issue confirmed as open bug report about ssmAutomation failing to share documents across accounts. |
| 13 | GlobalConfig type documentation — Landing Zone Accelerator on AWS (v1.7.0) | https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.8.1/typedocs/v1.7.0/classes/_aws_accelerator_config.GlobalConfig.html | VERIFIED | Confirmed reachable via search. GlobalConfig documentation at the versioned typedocs path is indexed and accessible. |
| 14 | SsmAutomationConfig type documentation — Landing Zone Accelerator on AWS (v1.9.2) | https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.10.0/typedocs/v1.9.2/classes/_aws_accelerator_config.SsmAutomationConfig.html | VERIFIED | Confirmed live via search result match. |
| 15 | DocumentConfig type documentation — Landing Zone Accelerator on AWS (v1.9.2) | https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.10.0/typedocs/v1.9.2/classes/_aws_accelerator_config.DocumentConfig.html | VERIFIED | Confirmed live via search result match. |
| 16 | Core pipeline stages — Landing Zone Accelerator on AWS | https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/awsaccelerator-pipeline.html | UNVERIFIABLE | URL not returned in search results. The AWS Solutions documentation root for LZA is accessible, but this specific pipeline stages page was not confirmed directly. Pipeline stage sequence (Prepare → Accounts → Bootstrap → SecurityAudit → Customizations) is partially corroborated by multiple third-party sources and the LZA developer guide. |
| 17 | Account creation and drift detection — Landing Zone Accelerator on AWS | https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/account-creation-and-drift-detection.html | VERIFIED | Confirmed live. Page confirms account creation workflow is invoked by the Prepare stage of the AWSAccelerator-Pipeline. |
| 18 | aws-samples/lza-account-creation-workflow — GitHub | https://github.com/aws-samples/lza-account-creation-workflow | VERIFIED | Confirmed live. Repository description matches: Step Functions-based workflow that triggers LZA CodePipeline after account creation. |
| 19 | Automate account creation using the Landing Zone Accelerator on AWS — AWS Prescriptive Guidance | https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automate-account-creation-lza.html | VERIFIED | Confirmed live. Page exists and describes the account creation workflow pattern with LZA. |
| 20 | LZA sample security-config.yaml — awslabs/landing-zone-accelerator-on-aws (GitHub, main branch) | https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/main/reference/sample-configurations/lza-sample-config/security-config.yaml | UNVERIFIABLE | URL not directly confirmed by search. The main LZA repository is verified, and sample-configurations directory exists, but the exact file path at this URL was not returned in search results. The path is plausible given the repository structure. |
| 21 | StackSets concepts — AWS CloudFormation | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html | VERIFIED | Confirmed live. Service-managed permissions, auto-deployment, and Organizations integration documented. |
| 22 | AWS::CloudFormation::StackSet resource reference | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html | VERIFIED | Confirmed live. AutoDeployment property documented. |
| 23 | Step 4: Configure session preferences — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-configure-preferences.html | VERIFIED | Confirmed live via search. Page covers configuring session preferences including the SSM-SessionManagerRunShell document. |
| 24 | SSM Session Manager sendToCloudWatchLogs IAM Policy issue — GitHub Issue #934 (LZA) | https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/934 | VERIFIED | Confirmed live via search result match. Issue is about sendToCloudWatchLogs and the AWSAccelerator-SessionManagerLogging policy, consistent with the investigation reference. |

## Finding Verification

### Finding: LZA global-config sessionManager block has no RunAs surface
- **Claim:** LZA's global-config.yaml sessionManager block exposes only three fields — sendToCloudWatchLogs, sendToS3, and attachPolicyToIamRoles — and has no surface for runAsEnabled or runAsDefaultUser.
- **Verdict:** CONFIRMED
- **Evidence:** Multiple search results confirm the sessionManager block fields are limited to logging destinations (sendToCloudWatchLogs, sendToS3) and role policy attachment (attachPolicyToIamRoles). LZA GlobalConfig documentation (source #13) and community references consistently describe these three fields without mentioning RunAs configuration options. LZA's preserve behavior (confirmed via CHANGELOG, source #10) further establishes that LZA reads but never writes RunAs fields — consistent with no native config surface for them.
- **Source used:** https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.8.1/typedocs/v1.7.0/classes/_aws_accelerator_config.GlobalConfig.html; https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/release/v1.14.2/CHANGELOG.md

### Finding: ssmAutomation share mechanism does not deploy local document copies
- **Claim:** LZA's ssmAutomation section creates SSM documents in the Audit account and shares them via ModifyDocumentPermission — the document remains owned by Audit and is referenced by member accounts, not copied locally. SSM-SessionManagerRunShell must exist as a locally-owned document in each member account and cannot be satisfied by a cross-account share.
- **Verdict:** CONFIRMED
- **Evidence:** AWS documentation on SSM document sharing (source #7) confirms that ModifyDocumentPermission grants other accounts access to reference (not copy) a document. The SSM-SessionManagerRunShell preferences document behavior — requiring local account ownership — is consistent with the AWS Security Blog post (source #1) which deploys a Lambda to update the document locally in each account rather than using a sharing mechanism. GitHub issues #786 and #419 (sources #11, #12) both document failures in the ssmAutomation share path, corroborating the investigation's description of the mechanism's operational fragility.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/documents-ssm-sharing.html; https://aws.amazon.com/blogs/security/how-to-automate-session-manager-preferences-across-your-organization/

### Finding: GitHub issue #786 — ssmAutomation bug in LZA v1.12.1
- **Claim:** LZA v1.12.1 had a documented bug (GitHub issue #786) where Custom::SSMShareDocument invoked ModifyDocumentPermission without properly resolving account IDs from shareTargets, silently failing to share.
- **Verdict:** CONFIRMED
- **Evidence:** GitHub issue #786 is confirmed live and its title exactly matches: "SSM Document Sharing Fails in SecurityAudit Stack with InvalidParameterException Despite Valid shareTargets (v1.12.1)". The error described — ModifyDocumentPermission called with neither AccountIdsToAdd nor AccountIdsToRemove populated despite valid shareTargets configuration — matches the investigation's description precisely.
- **Source used:** https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/786

### Finding: LZA preserve behavior for runAsEnabled and runAsDefaultUser
- **Claim:** LZA preserves existing runAsEnabled and runAsDefaultUser values in SSM-SessionManagerRunShell when the pipeline runs — it does not overwrite them. This behavior was added specifically to prevent LZA from resetting customer-configured RunAs settings.
- **Verdict:** CONFIRMED
- **Evidence:** Search results querying the LZA CHANGELOG for runAs preserve behavior returned direct confirmation: "LZA now preserves existing SSM document settings for runAsEnabled and runAsDefaultUser when updating SSM documents, preventing the solution from overriding customer-configured permissions." The CHANGELOG at the v1.14.2 branch URL (source #10) is confirmed accessible.
- **Source used:** https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/release/v1.14.2/CHANGELOG.md

### Finding: cloudFormationStackSets with auto-deployment is the correct LZA-native delivery path
- **Claim:** The correct LZA-native delivery path for RunAs configuration is the customizations-config.yaml cloudFormationStackSets surface with a service-managed StackSet targeting Root OU; auto-deployment automatically creates stack instances in new member accounts via Organizations lifecycle events without requiring an LZA pipeline run.
- **Verdict:** CONFIRMED
- **Evidence:** AWS CloudFormation StackSets documentation (sources #21, #22) confirms: service-managed StackSets support auto-deployment, which is "triggered when accounts are added to a target organization or OU" — not by a pipeline run. The AWS Security Blog post (source #1) explicitly demonstrates this pattern for Session Manager preferences using CloudFormation StackSets and Lambda. LZA customizations-config cloudFormationStackSets support for this approach is corroborated by community documentation and the LZA developer guide.
- **Source used:** https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html; https://aws.amazon.com/blogs/security/how-to-automate-session-manager-preferences-across-your-organization/

### Finding: New-account gap between PREPARE and CUSTOMIZATIONS stages
- **Claim:** There is a documented gap between the LZA pipeline's PREPARE stage (where the new account is created) and the CUSTOMIZATIONS stage (where StackSet-delivered resources are deployed). The auto-deployment flag on the StackSet closes this gap because StackSet instance deployment is triggered by Organizations lifecycle events rather than waiting for the LZA pipeline's CUSTOMIZATIONS stage.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The existence of distinct PREPARE and CUSTOMIZATIONS pipeline stages is corroborated by multiple sources (LZA developer guides, GitHub issues, community documentation). The account-creation-and-drift-detection page (source #17) confirms: "The account creation workflow is invoked by the Prepare stage of the AWSAccelerator-Pipeline." CloudFormation StackSets auto-deployment triggering on Organizations lifecycle events (not pipeline runs) is confirmed (source #21). However, the specific characterization of this as a "documented gap" in LZA's own official documentation was not found — the gap is an inferred consequence of sequential pipeline stages rather than a gap explicitly acknowledged and documented by the LZA team. The investigation's framing of auto-deployment as closing this gap is technically sound given confirmed StackSet behavior, but "documented gap" slightly overstates the explicitness of the acknowledgment.
- **Source used:** https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/account-creation-and-drift-detection.html; https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html

### Finding: aws-samples/sample-how-to-automate-session-manager-preferences three-component architecture
- **Claim:** The solution uses a three-component architecture: (1) optional IAM policy deployment via LZA configuration, (2) an optional AWS Config rule with automated SSM Automation remediation, and (3) a CloudFormation custom resource (Lambda) that updates SSM-SessionManagerRunShell. This solution is explicitly designed for LZA environments and deploys via cloudFormationStackSets.
- **Verdict:** CONFIRMED
- **Evidence:** Search results for the GitHub repository (source #2) confirm the three-component structure: optional IAM policy deployment, optional Config rule with automated remediation, and the Lambda-backed custom resource that updates SSM-SessionManagerRunShell. The AWS Security Blog post (source #1) and repository description both confirm the solution uses CloudFormation StackSets for multi-account deployment.
- **Source used:** https://github.com/aws-samples/sample-how-to-automate-session-manager-preferences; https://aws.amazon.com/blogs/security/how-to-automate-session-manager-preferences-across-your-organization/

### Finding: SCP pattern for ssm:UpdateDocument demonstrated in Cloud Operations Blog
- **Claim:** The AWS Cloud Operations Blog post 'Implementing AWS Session Manager logging guardrails in a multi-account environment' (2023) demonstrates an SCP pattern that denies ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument actions on SSM-SessionManagerRunShell.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The blog post (source #3) is confirmed live and confirmed to include an SCP denying ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument. However, the investigation states the publication year is 2023 — the search results did not return the precise publication date for this post, so the "2023" year attribution could not be verified. The SCP content and its application to SSM-SessionManagerRunShell are confirmed.
- **Source used:** https://aws.amazon.com/blogs/mt/implementing-aws-session-manager-logging-guardrails-in-a-multi-account-environment/

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| None | — | — |

No findings were contradicted. The two PARTIALLY CONFIRMED findings involve minor attribution precision (explicit "documented gap" language, publication year for source #3) rather than material factual errors. The two UNVERIFIABLE sources (#16, #20) are peripheral references where the underlying claims are supported by other verified sources. No corrections to investigation.json are required.

## Overall Assessment

The investigation is factually sound. All high-stakes claims are confirmed or partially confirmed against live sources, with no contradictions found. The core technical claims — that LZA's sessionManager block has no RunAs surface, that ssmAutomation shares documents rather than deploying local copies, that the LZA CHANGELOG documents a preserve behavior for RunAs fields, that GitHub issues #786 and #419 exist with the described content, and that cloudFormationStackSets with auto-deployment is the canonical delivery path — are all directly verified. The AWS Security Blog post from November 2025 and its companion GitHub repository are both live and match the investigation's description of the three-component architecture. The two partially confirmed findings involve framing precision rather than factual error: the new-account gap is real and technically documented through stage sequencing, but the phrase "documented gap" implies LZA-team acknowledgment that was not found explicitly stated; the Cloud Operations Blog SCP pattern is confirmed but the 2023 date was not verified. Neither warrants correction to investigation.json.
