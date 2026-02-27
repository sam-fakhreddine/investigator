# Investigation: LZA SSM RunAs Synchronization Across Member Accounts

**Date:** 2026-02-27
**Status:** Complete

---

## LZA Mechanisms for SSM-SessionManagerRunShell RunAs Enforcement

| Mechanism | What It Does | Covers RunAs Fields? | Covers New Accounts? | Gap |
| --- | --- | --- | --- | --- |
| LZA global-config sessionManager block | Configures Session Manager logging destinations (S3, CloudWatch) and IAM role policy attachment | No — runAsEnabled and runAsDefaultUser are not fields in this block | Yes — logging config propagates to all accounts | Cannot set RunAs fields — wrong surface |
| LZA ssmAutomation (security-config documentSets) | Creates SSM Automation/Command documents in Audit account and shares them with target OUs or accounts | Not directly — shares a document reference, does not deploy a local copy into each member account | Partially — new accounts in targeted OUs receive the share after next pipeline run | Shared Session-type documents cannot serve as account-level preferences; SSM-SessionManagerRunShell must be local and owned by each account |
| LZA customizations-config cloudFormationStackSets | Deploys a CFN StackSet (with service-managed permissions) to all accounts in target OUs or Root — can carry a Lambda custom resource that calls ssm:UpdateDocument or ssm:CreateDocument locally in each account | Yes — the Lambda custom resource can set runAsEnabled and runAsDefaultUser in the local SSM-SessionManagerRunShell document | Yes — StackSets with auto-deployment enabled automatically deploy stack instances to newly vended accounts in target OUs | StackSet deployment runs in the CUSTOMIZATIONS stage; there is a window between account vend (PREPARE stage) and StackSet deployment where the new account lacks the RunAs config |
| LZA customizations-config cloudFormationStacks | Deploys a CFN Stack to specific named accounts — not suitable for org-wide rollout | Yes, if targeted at the right account | No — stacks target named accounts; new accounts are not automatically included | Must add new accounts to the config and re-run pipeline for each new account |
| SCP deny ssm:UpdateDocument on SSM-SessionManagerRunShell | Prevents member account admins from modifying the preferences document after it is set | N/A — enforces immutability, does not set the value | Yes — SCP applies org-wide to all accounts including new ones | Does not set the document; must be combined with a deployment mechanism |
| AWS-native: CFN StackSets with auto-deployment (outside LZA) | Service-managed StackSets on Root OU with auto-deployment deliver a Lambda custom resource to every account, including new accounts, without requiring an LZA pipeline run | Yes | Yes — automatic, no pipeline run needed for new accounts | Requires separate operational lifecycle outside LZA; LZA pipeline may conflict if it also manages the same document |

> The canonical LZA-native path is: cloudFormationStackSets in customizations-config.yaml targeting Root OU with auto-deployment enabled, carrying a CFN custom resource (Lambda) that calls ssm:UpdateDocument on SSM-SessionManagerRunShell in each member account. Combine with an SCP that denies ssm:UpdateDocument on that document to protect the setting post-deployment. New-account gap (PREPARE-to-CUSTOMIZATIONS window) requires separate mitigation.

---

## Question

> How can LZA customizations (customizations-config, custom SSM documents, or account-vending hooks) enforce a consistent SSM-SessionManagerRunShell RunAs configuration across all member accounts?

---

## Context

A prior investigation (SsmRunAsUserMultiGroupConflict) established that Session Manager RunAs resolution has exactly two priority layers: (1) the SSMSessionRunAs session tag on the calling principal, and (2) the runAsDefaultUser field in the account-level SSM-SessionManagerRunShell preferences document. The SSM-SessionManagerRunShell document is account-scoped — each AWS member account has its own copy. In a Landing Zone Accelerator (LZA) organization with dozens or hundreds of member accounts federated through IAM Identity Center and Entra ID, ensuring every member account carries a correctly configured SSM-SessionManagerRunShell document — and that new accounts inherit that config at vend time — is a non-trivial configuration management problem. This investigation examines what LZA natively provides for this purpose, where the gaps are, and what supplementary patterns the community uses to fill them.

---

## Key Findings

- LZA's global-config.yaml sessionManager block exposes only three fields — sendToCloudWatchLogs, sendToS3, and attachPolicyToIamRoles — and has no surface for runAsEnabled or runAsDefaultUser. Session Manager RunAs preferences cannot be configured through this block; it is a logging-and-policy-attachment surface only.
- LZA's ssmAutomation section in security-config.yaml creates SSM documents (Command or Automation type) in the Audit account and shares them with target OUs via the ModifyDocumentPermission API. This is a document-sharing mechanism, not a document-deployment mechanism: the document remains owned by the Audit account and is referenced by member accounts, not copied locally. The SSM-SessionManagerRunShell preferences document must exist as a locally-owned document in each member account and cannot be satisfied by a cross-account share.
- The ssmAutomation share mechanism had a documented bug in LZA v1.12.1 (GitHub issue #786) where the SecurityAudit stack's Custom::SSMShareDocument resource invoked ModifyDocumentPermission without properly resolving account IDs from shareTargets, silently failing to share. This was fixed in subsequent releases but illustrates the operational fragility of relying on share-based delivery.
- LZA preserves existing runAsEnabled and runAsDefaultUser values in SSM-SessionManagerRunShell when the pipeline runs — it does not overwrite them. This behavior was added specifically to prevent LZA from resetting customer-configured RunAs settings, confirming that LZA never natively writes RunAs values into the preferences document during its standard pipeline execution.
- The correct LZA-native delivery path for RunAs configuration is the customizations-config.yaml cloudFormationStackSets surface: a service-managed StackSet targeting Root OU (or all member-account OUs) can carry a CloudFormation custom resource backed by a Lambda function that calls ssm:UpdateDocument (or ssm:CreateDocument if the document is absent) on SSM-SessionManagerRunShell locally within each member account. This is the pattern demonstrated in the AWS Security Blog post 'How to automate Session Manager preferences across your organization' (November 2025) and its companion GitHub repository aws-samples/sample-how-to-automate-session-manager-preferences.
- CloudFormation StackSets with service-managed permissions support an auto-deployment setting that automatically creates stack instances in new accounts as they join a target OU. When this flag is enabled on the Root-targeting StackSet, newly vended member accounts receive the RunAs configuration deployment automatically — without requiring a subsequent LZA pipeline run.
- There is a documented gap between the LZA pipeline's PREPARE stage (where the new account is created and enrolled in Control Tower) and the CUSTOMIZATIONS stage (where StackSet-delivered resources are deployed). During this window, the new account exists in the organization but its SSM-SessionManagerRunShell document has not yet been configured with RunAs settings. The auto-deployment flag on the StackSet closes this gap for StackSet resources specifically, because StackSet instance deployment is triggered by Organizations lifecycle events rather than waiting for the LZA pipeline's CUSTOMIZATIONS stage to run.
- LZA cloudFormationStacks (as opposed to cloudFormationStackSets) targets specific named accounts defined in the config file. It does not automatically include newly vended accounts and requires a config update followed by a full pipeline run to extend coverage. It is not suitable for org-wide enforcement of RunAs settings.
- An SCP denying ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument actions on the SSM-SessionManagerRunShell resource can be applied org-wide to prevent member account administrators from modifying the preferences document after it has been configured. The AWS Cloud Operations Blog post 'Implementing AWS Session Manager logging guardrails in a multi-account environment' (2023) demonstrates this SCP pattern. SCPs apply to all current and future member accounts in the target OU, making them a durable guardrail independent of pipeline run timing.
- The LZA account-creation workflow (aws-samples/lza-account-creation-workflow) is a Service Catalog-backed Step Functions state machine that triggers the LZA CodePipeline after account creation. Customizations-stage resources — including cloudFormationStackSets — are applied during that triggered pipeline run. Without auto-deployment on the StackSet, the new account still depends on the pipeline completing its CUSTOMIZATIONS stage before RunAs is set.
- Out-of-band manual modifications to SSM-SessionManagerRunShell in a member account are not detected or remediated by LZA natively. LZA's preserve behavior means the pipeline will not overwrite a manually changed runAsDefaultUser value. Drift remediation requires either: (A) an AWS Config custom rule that detects unexpected runAsDefaultUser values and triggers SSM Automation remediation, or (B) an SCP that prevents unauthorized modification in the first place.
- The aws-samples/sample-how-to-automate-session-manager-preferences solution uses a three-component architecture: (1) optional IAM policy deployment via LZA configuration, (2) an optional AWS Config rule with automated SSM Automation remediation to enforce instance profile compliance, and (3) a CloudFormation custom resource (Lambda) that updates SSM-SessionManagerRunShell with specified preferences. This solution is explicitly designed for LZA environments and deploys via cloudFormationStackSets.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SSM-SessionManagerRunShell | The account-level SSM preferences document that controls Session Manager behavior, including runAsEnabled (boolean) and runAsDefaultUser (string OS username). Each AWS account has its own copy in each region — it cannot be satisfied by a cross-account shared document. Changes to this document take effect for subsequent sessions; in-flight sessions are not affected. |
| LZA customizations-config.yaml | The optional LZA configuration file for deploying resources not natively supported by LZA core, including cloudFormationStacks (per-named-account CFN stacks) and cloudFormationStackSets (service-managed StackSets targeting OUs or Root). The CUSTOMIZATIONS pipeline stage processes this file after all security and operations stages complete. |
| LZA global-config sessionManager block | A sub-block under the logging section of global-config.yaml that configures Session Manager log destinations (S3, CloudWatch Logs) and which IAM roles receive the Session Manager logging policy. It does not expose any RunAs-related fields and is not the correct surface for configuring SSM-SessionManagerRunShell content. |
| LZA ssmAutomation (security-config) | A section of security-config.yaml that defines SSM Automation or Command documents to be created in the Audit account and shared with target OUs or accounts. The sharing is implemented via ModifyDocumentPermission, which grants other accounts access to reference the document — it does not copy the document into each member account. Not suitable for deploying account-level Session Manager preferences. |
| cloudFormationStackSets (LZA) | An LZA customizations-config resource type that deploys a CloudFormation StackSet with service-managed permissions to target OUs or Root. Supports auto-deployment, which automatically creates stack instances in new member accounts when they join a target OU — without requiring an LZA pipeline run. This is the correct LZA mechanism for org-wide document configuration enforcement. |
| CFN Custom Resource (Lambda-backed) | A CloudFormation resource (AWS::CloudFormation::CustomResource or Custom::*) backed by a Lambda function that executes arbitrary API calls during stack create, update, and delete events. Used to call ssm:UpdateDocument or ssm:CreateDocument on SSM-SessionManagerRunShell within each member account as part of a StackSet deployment. |
| StackSet Auto-Deployment | A CloudFormation StackSets feature (service-managed permissions only) that automatically deploys a new stack instance to any account that joins a targeted OU or organization. Triggered by Organizations account-creation lifecycle events, not by the LZA pipeline. Closes the new-account gap between LZA's PREPARE and CUSTOMIZATIONS stages. |
| LZA Pipeline Stages | The LZA AWSAccelerator-Pipeline runs sequentially: Source → Build → Prepare → Accounts → Bootstrap → Review → Logging → Organization → SecurityAudit → Deploy (Operations/ResourcePolicy) → Customizations. A new account is created in the Prepare stage and receives customizations-config resources only when the pipeline reaches the Customizations stage — many minutes later in the same run, or in a future triggered run. |
| SCP Guardrail for SSM Document | A Service Control Policy attached to an OU or Root that denies ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument on the SSM-SessionManagerRunShell resource. Prevents member account administrators from modifying the preferences document after it has been set by the StackSet. SCPs apply to all current and future member accounts in scope and do not require a pipeline run to take effect. |
| LZA Preserve Behavior for RunAs | A specific LZA behavioral guarantee: when the pipeline updates SSM-SessionManagerRunShell (e.g., to update logging settings), it reads the existing runAsEnabled and runAsDefaultUser values and preserves them rather than overwriting them with defaults. This prevents LZA pipeline runs from regressing RunAs settings that were established by a StackSet or manual configuration. |
| New-Account Gap | The temporal window between when LZA creates a new member account (Prepare stage, via Control Tower Account Factory) and when the CUSTOMIZATIONS stage completes and applies cloudFormationStackSets resources to that account. During this window, the account has the default (unconfigured) SSM-SessionManagerRunShell document. StackSet auto-deployment can close this gap for StackSet-delivered configuration. |

---

## Tensions & Tradeoffs

- LZA's preserve behavior for runAsEnabled and runAsDefaultUser protects customer-configured values from pipeline regression, but it also means LZA cannot be used to enforce RunAs values org-wide through its native config — intentional configuration by the pipeline is blocked by the same mechanism that protects against accidental overwrite.
- Using a StackSet with auto-deployment to deliver RunAs configuration operates outside the LZA pipeline's orchestration model. If the LZA pipeline later modifies the same SSM-SessionManagerRunShell document (for logging updates), the preserve behavior should protect RunAs fields — but this interaction depends on LZA correctly reading and re-emitting those fields, which is an implementation detail that could regress in future LZA versions.
- The ssmAutomation share mechanism in security-config.yaml is the most visible LZA surface for SSM documents, but it cannot deploy account-level Session Manager preferences because sharing does not create a local document copy. Engineers unfamiliar with this distinction may attempt to use ssmAutomation for this purpose and discover the gap only at session-start time.
- An SCP that denies ssm:UpdateDocument on SSM-SessionManagerRunShell effectively makes the document immutable for member account administrators — but the LZA pipeline's management account role and the StackSet's service-linked role must be exempted from the SCP (or the SCP must target only non-management principals) or the enforcement mechanism itself will be blocked from writing the value.
- StackSet auto-deployment uses Organizations lifecycle events to trigger instance creation in new accounts. This is faster than waiting for an LZA pipeline run, but it depends on the StackSet being already present in the organization — if the StackSet itself is deployed via LZA and the initial LZA pipeline has not yet run in a new region, the StackSet instance will not exist to auto-deploy.
- AWS Config rule-based remediation can detect and correct drift in runAsDefaultUser values, but Config rules that check SSM document content (not a standard managed rule category) require custom Lambda-based rules. Deploying custom Config rules org-wide is itself a configuration management problem that mirrors the original one.
- The new-account gap exists even with StackSet auto-deployment if the StackSet stack instance creation takes longer than the window before engineers attempt their first Session Manager session in the new account. The gap duration is undocumented and depends on Organizations event propagation latency and Lambda execution time.

---

## Open Questions

- Does LZA's preserve behavior for runAsEnabled and runAsDefaultUser apply when LZA creates SSM-SessionManagerRunShell for the first time in a new account (where the document does not yet exist), or only when updating an existing document? If LZA creates the document with default values and the StackSet updates it afterward, what is the document version state?
- What is the documented or empirically observed latency between an Organizations CreateManagedAccount lifecycle event and the delivery of a StackSet stack instance with auto-deployment? This determines the practical length of the new-account gap.
- Does the SCP deny pattern for ssm:UpdateDocument on SSM-SessionManagerRunShell need to exempt the AWSServiceRoleForCloudFormationStackSetsOrgAdmin role (the StackSet service-linked role), or does StackSet deployment assume a member-account role that is outside SCP scope?
- LZA's ssmAutomation documentSets createDocuments approach — does it create the document in the Audit account only, or does it create a copy in each member account in the shareTargets list? The distinction between create-and-share and create-per-account determines whether this surface could be repurposed for SSM-SessionManagerRunShell delivery with a Session-type document.
- Are there LZA feature requests or open GitHub issues requesting a native runAsDefaultUser or runAsEnabled field in the global-config sessionManager block, which would allow LZA to manage RunAs settings without a separate StackSet?
- When runAsDefaultUser is set in SSM-SessionManagerRunShell and the referenced OS user does not exist on a specific managed node, does the SSM agent emit a distinct error code that can be correlated across accounts via CloudTrail or SSM session history — enabling automated detection of misconfigured accounts without starting a session?

---

## Sources & References

- [How to automate Session Manager preferences across your organization — AWS Security Blog (November 2025)](https://aws.amazon.com/blogs/security/how-to-automate-session-manager-preferences-across-your-organization/)
- [aws-samples/sample-how-to-automate-session-manager-preferences — GitHub](https://github.com/aws-samples/sample-how-to-automate-session-manager-preferences)
- [Implementing AWS Session Manager logging guardrails in a multi-account environment — AWS Cloud Operations Blog](https://aws.amazon.com/blogs/mt/implementing-aws-session-manager-logging-guardrails-in-a-multi-account-environment/)
- [aws-samples/ssm-monitoring-logging-guardrails-multiaccount — GitHub](https://github.com/aws-samples/ssm-monitoring-logging-guardrails-multiaccount)
- [Session document schema — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-schema.html)
- [Turn on Run As support for Linux and macOS managed nodes — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Sharing SSM documents — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/documents-ssm-sharing.html)
- [Best practice considerations when using AWS Systems Manager document sharing — AWS Cloud Operations Blog](https://aws.amazon.com/blogs/mt/best-practice-considerations-aws-systems-manager-document-sharing/)
- [awslabs/landing-zone-accelerator-on-aws — GitHub main repository](https://github.com/awslabs/landing-zone-accelerator-on-aws)
- [Landing Zone Accelerator on AWS CHANGELOG (v1.14.2 branch) — runAs preserve fix](https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/release/v1.14.2/CHANGELOG.md)
- [SSM Document Sharing Fails in SecurityAudit Stack — GitHub Issue #786 (LZA v1.12.1)](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/786)
- [ssmAutomation is not sharing documents with other accounts — GitHub Issue #419 (LZA)](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/419)
- [GlobalConfig type documentation — Landing Zone Accelerator on AWS (v1.7.0)](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.8.1/typedocs/v1.7.0/classes/_aws_accelerator_config.GlobalConfig.html)
- [SsmAutomationConfig type documentation — Landing Zone Accelerator on AWS (v1.9.2)](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.10.0/typedocs/v1.9.2/classes/_aws_accelerator_config.SsmAutomationConfig.html)
- [DocumentConfig type documentation — Landing Zone Accelerator on AWS (v1.9.2)](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.10.0/typedocs/v1.9.2/classes/_aws_accelerator_config.DocumentConfig.html)
- [Core pipeline stages — Landing Zone Accelerator on AWS](https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/awsaccelerator-pipeline.html)
- [Account creation and drift detection — Landing Zone Accelerator on AWS](https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/account-creation-and-drift-detection.html)
- [aws-samples/lza-account-creation-workflow — GitHub](https://github.com/aws-samples/lza-account-creation-workflow)
- [Automate account creation using the Landing Zone Accelerator on AWS — AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automate-account-creation-lza.html)
- [LZA sample security-config.yaml — awslabs/landing-zone-accelerator-on-aws (GitHub, main branch)](https://github.com/awslabs/landing-zone-accelerator-on-aws/blob/main/reference/sample-configurations/lza-sample-config/security-config.yaml)
- [StackSets concepts — AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html)
- [AWS::CloudFormation::StackSet resource reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html)
- [Step 4: Configure session preferences — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-configure-preferences.html)
- [SSM Session Manager sendToCloudWatchLogs IAM Policy issue — GitHub Issue #934 (LZA)](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/934)
