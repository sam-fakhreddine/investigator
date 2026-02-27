# Glossary — LZA SSM RunAs Synchronization Across Member Accounts

Quick definitions of key terms and concepts referenced in this investigation.

---

## SSM-SessionManagerRunShell

The account-level SSM preferences document that controls Session Manager behavior, including runAsEnabled (boolean) and runAsDefaultUser (string OS username). Each AWS account has its own copy in each region — it cannot be satisfied by a cross-account shared document. Changes to this document take effect for subsequent sessions; in-flight sessions are not affected.

## LZA customizations-config.yaml

The optional LZA configuration file for deploying resources not natively supported by LZA core, including cloudFormationStacks (per-named-account CFN stacks) and cloudFormationStackSets (service-managed StackSets targeting OUs or Root). The CUSTOMIZATIONS pipeline stage processes this file after all security and operations stages complete.

## LZA global-config sessionManager block

A sub-block under the logging section of global-config.yaml that configures Session Manager log destinations (S3, CloudWatch Logs) and which IAM roles receive the Session Manager logging policy. It does not expose any RunAs-related fields and is not the correct surface for configuring SSM-SessionManagerRunShell content.

## LZA ssmAutomation (security-config)

A section of security-config.yaml that defines SSM Automation or Command documents to be created in the Audit account and shared with target OUs or accounts. The sharing is implemented via ModifyDocumentPermission, which grants other accounts access to reference the document — it does not copy the document into each member account. Not suitable for deploying account-level Session Manager preferences.

## cloudFormationStackSets (LZA)

An LZA customizations-config resource type that deploys a CloudFormation StackSet with service-managed permissions to target OUs or Root. Supports auto-deployment, which automatically creates stack instances in new member accounts when they join a target OU — without requiring an LZA pipeline run. This is the correct LZA mechanism for org-wide document configuration enforcement.

## CFN Custom Resource (Lambda-backed)

A CloudFormation resource (AWS::CloudFormation::CustomResource or Custom::*) backed by a Lambda function that executes arbitrary API calls during stack create, update, and delete events. Used to call ssm:UpdateDocument or ssm:CreateDocument on SSM-SessionManagerRunShell within each member account as part of a StackSet deployment.

## StackSet Auto-Deployment

A CloudFormation StackSets feature (service-managed permissions only) that automatically deploys a new stack instance to any account that joins a targeted OU or organization. Triggered by Organizations account-creation lifecycle events, not by the LZA pipeline. Closes the new-account gap between LZA's PREPARE and CUSTOMIZATIONS stages.

## LZA Pipeline Stages

The LZA AWSAccelerator-Pipeline runs sequentially: Source → Build → Prepare → Accounts → Bootstrap → Review → Logging → Organization → SecurityAudit → Deploy (Operations/ResourcePolicy) → Customizations. A new account is created in the Prepare stage and receives customizations-config resources only when the pipeline reaches the Customizations stage — many minutes later in the same run, or in a future triggered run.

## SCP Guardrail for SSM Document

A Service Control Policy attached to an OU or Root that denies ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument on the SSM-SessionManagerRunShell resource. Prevents member account administrators from modifying the preferences document after it has been set by the StackSet. SCPs apply to all current and future member accounts in scope and do not require a pipeline run to take effect.

## LZA Preserve Behavior for RunAs

A specific LZA behavioral guarantee: when the pipeline updates SSM-SessionManagerRunShell (e.g., to update logging settings), it reads the existing runAsEnabled and runAsDefaultUser values and preserves them rather than overwriting them with defaults. This prevents LZA pipeline runs from regressing RunAs settings that were established by a StackSet or manual configuration.

## New-Account Gap

The temporal window between when LZA creates a new member account (Prepare stage, via Control Tower Account Factory) and when the CUSTOMIZATIONS stage completes and applies cloudFormationStackSets resources to that account. During this window, the account has the default (unconfigured) SSM-SessionManagerRunShell document. StackSet auto-deployment can close this gap for StackSet-delivered configuration.

---

*Back to: [investigation.md](investigation.md)*
