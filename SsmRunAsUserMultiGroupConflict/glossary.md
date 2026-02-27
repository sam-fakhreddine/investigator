# Glossary — SSM RunAs Sync Pipeline — Entra ID, IAM Identity Center, and LZA

Quick definitions of key terms and concepts referenced in this investigation.

---

## SSMSessionRunAs

An IAM session tag key recognized by AWS Systems Manager Session Manager. When present on the calling principal's session, Session Manager uses the tag's value as the OS username for the shell session on the managed node. Checked before the account-level default (runAsDefaultUser). Cannot be multi-valued. Must originate from a per-user ABAC attribute — not group membership — for IdC-federated users in multi-group scenarios.

## RunAs (Session Manager)

A Session Manager feature that starts a session as a specified OS user rather than the default ssm-user account. Controlled via the SSMSessionRunAs principal tag (highest priority) or the runAsDefaultUser field in the SSM-SessionManagerRunShell account-level preferences document (fallback). Once enabled, failure to resolve a valid OS user causes session failure — there is no further fallback to ssm-user.

## IAM Identity Center (IdC)

AWS service (formerly AWS SSO) that manages federated access to AWS accounts. Assigns users and groups to permission sets, which map to AWSReservedSSO_ IAM roles in member accounts. Supports ABAC via Attributes for Access Control, passing user attributes as session tags into each federated session. Hard-rejects SAML assertions containing duplicate or multi-valued attributes when ABAC is enabled.

## ABAC (Attributes for Access Control)

The IAM Identity Center instance-level configuration that maps user-profile attributes to IAM session tags (aws:PrincipalTag) during federation. Configured via the CreateInstanceAccessControlAttributeConfiguration API. Not managed by LZA in any version — must be configured via the IdC console, aws ssoadmin CLI, CloudFormation AWS::SSO::InstanceAccessControlAttributeConfiguration, or Terraform aws_ssoadmin_instance_access_control_attributes.

## AWSReservedSSO_ role

An IAM role automatically created and managed by IAM Identity Center in each member account for each permission-set-to-account assignment. These roles are protected — customers cannot tag or modify them directly. The SSMSessionRunAs session tag must be passed via SAML or ABAC, not via a static role tag.

## LZA customizations-config.yaml

The optional LZA configuration file for deploying resources not natively supported by LZA core. Supports cloudFormationStackSets (service-managed StackSets targeting OUs or Root) and cloudFormationStacks (per-named-account stacks). The CUSTOMIZATIONS pipeline stage processes this file after all security and operations stages complete. The correct LZA surface for delivering org-wide SSM-SessionManagerRunShell RunAs configuration.

## cloudFormationStackSets (LZA)

An LZA customizations-config resource type that deploys a CloudFormation StackSet with service-managed permissions to target OUs or Root. Supports auto-deployment, which automatically creates stack instances in new member accounts when they join a target OU — without requiring an LZA pipeline run. The correct LZA-native mechanism for org-wide SSM-SessionManagerRunShell RunAs enforcement.

## StackSet Auto-Deployment

A CloudFormation StackSets feature (service-managed permissions only) that automatically deploys a new stack instance to any account that joins a targeted OU or organization. Triggered by Organizations account-creation lifecycle events, not by the LZA pipeline. Closes the new-account gap between LZA's PREPARE and CUSTOMIZATIONS stages for StackSet-delivered configuration.

## New-Account Gap

The temporal window between when LZA creates a new member account (Prepare stage, via Control Tower Account Factory) and when the CUSTOMIZATIONS stage completes and applies cloudFormationStackSets resources to that account. During this window, SSM-SessionManagerRunShell has default (unconfigured) RunAs settings. StackSet auto-deployment can close this gap via Organizations lifecycle events.

## SCP Guardrail for SSM Document

A Service Control Policy attached to an OU or Root that denies ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument on the SSM-SessionManagerRunShell resource. Prevents member account administrators from modifying the preferences document after it has been set by the StackSet. Must exempt the StackSet service role and LZA pipeline role. Applies to all current and future member accounts in scope.

## SCIM attribute precedence

AWS documents two confirmed precedence relationships in IdC ABAC evaluation: console-configured attributes (InstanceAccessControlAttributeConfiguration) override SAML assertion values for the same key, and SCIM-synchronized attributes override SAML assertion values for the same key. The relative ordering between console-configured and SCIM-synchronized attributes when both specify the same key is not documented by AWS and requires empirical testing.

## LZA identityCenter block

The top-level configuration object in iam-config.yaml that declares LZA's management of IAM Identity Center. Contains name, delegatedAdminAccount, identityCenterPermissionSets, and identityCenterAssignments. Has no sub-keys for ABAC attribute configuration, instance settings, relay state, MFA policy, or user/group creation. ABAC attribute configuration is the most operationally significant confirmed gap.

---

*Back to: [investigation.md](investigation.md)*
