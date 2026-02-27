# Investigation: LZA identityCenter Config Block — Declarative Surface, Limits, and ABAC Gap

**Date:** 2026-02-27
**Status:** Complete

---

## LZA identityCenter Config Block — Ownership Surface at a Glance

| IdC Capability | LZA Key / Mechanism | LZA-Managed? | If Not LZA — What Manages It |
| --- | --- | --- | --- |
| Delegated admin account for IdC | identityCenter.delegatedAdminAccount | Yes | N/A |
| Permission set definition (policies, duration) | identityCenterPermissionSets[].policies, sessionDuration | Yes | N/A |
| AWS-managed policy attach | policies.awsManaged[] | Yes | N/A |
| Customer-managed policy attach | policies.customerManaged[] | Yes — policy must pre-exist | N/A |
| LZA-vended policy attach | policies.acceleratorManaged[] + policySets[].identityCenterDependency:true | Yes — LZA creates and attaches | N/A |
| Inline policy on permission set | policies.inlinePolicy (file path) | Yes | N/A |
| Permissions boundary on permission set | policies.permissionsBoundary | Yes | N/A |
| Relay state (console redirect URL) | Not present in IdentityCenterPermissionSetConfig | No | Console or aws ssoadmin CLI; AWS CloudFormation AWS::SSO::PermissionSet supports it |
| Group-to-permission-set assignment | identityCenterAssignments[].principals[type:GROUP] | Yes | N/A |
| User-to-permission-set assignment | identityCenterAssignments[].principals[type:USER] | Yes | N/A |
| Assignment scope — specific accounts | identityCenterAssignments[].deploymentTargets.accounts[] | Yes | N/A |
| Assignment scope — OU | identityCenterAssignments[].deploymentTargets.organizationalUnits[] | Yes — direct children only | Nested OUs must be listed explicitly |
| Management account assignments | identityCenterAssignments[].deploymentTargets | Partial — known bug history | Console fallback if pipeline fails |
| ABAC Attributes for Access Control | No key in identityCenter block | No — confirmed gap | Console; aws ssoadmin create-instance-access-control-attribute-configuration; CloudFormation AWS::SSO::InstanceAccessControlAttributeConfiguration; Terraform aws_ssoadmin_instance_access_control_attributes |
| IdC user/group creation | Not supported | No — explicit LZA limitation | SCIM provisioning from Entra ID; manual IdC console |
| MFA policy for IdC instance | Not supported | No | Console only as of mid-2024 |
| IdC instance-level settings | Not supported | No | Console only |

> relayState is absent from LZA's IdentityCenterPermissionSetConfig across all documented versions (v1.3.x through v1.10.x). ABAC attribute configuration (CreateInstanceAccessControlAttributeConfiguration) has no LZA equivalent — it is the single most operationally significant gap for organizations using the SSMSessionRunAs ABAC pipeline.

---

## Question

> How does LZA's identityCenter config block declaratively manage permission sets, assignment mappings, and ABAC attribute configurations — and what are the limits of what it can express?

---

## Context

Landing Zone Accelerator on AWS (LZA) manages IAM Identity Center (IdC) configuration declaratively via the identityCenter block in iam-config.yaml. For organizations that are past initial deployment — with SCIM running, Entra ID federated, and ABAC partially configured — understanding precisely which IdC surface is owned by LZA versus which must be managed outside it (via console, CLI, or supplemental IaC) is critical for config drift prevention and for safely extending the ABAC pipeline (e.g., wiring the SSMSessionRunAs session-tag path established by the prior SsmRunAsUserMultiGroupConflict investigation). The settled finding from that investigation — that SSMSessionRunAs must be sourced from a user-level ABAC attribute, not group membership — presupposes that 'Attributes for Access Control' is correctly configured in IdC. This investigation determines whether LZA owns that configuration or whether it is an explicit gap.

---

## Key Findings

- The LZA identityCenter block in iam-config.yaml contains four top-level keys: name (required, logical label for the IdC instance — not an AWS resource ID), delegatedAdminAccount (optional, account name to receive delegated admin rights), identityCenterPermissionSets (optional array), and identityCenterAssignments (optional array). There is no ABAC, no instance-settings, and no relay-state key at any level.
- Permission sets are declared via identityCenterPermissionSets. Each entry supports: name, sessionDuration (in minutes), and a policies sub-object containing awsManaged (ARN or short name list), customerManaged (name list — policies must pre-exist in the target account), acceleratorManaged (names of policies that LZA itself creates via a linked policySets entry with identityCenterDependency:true), inlinePolicy (path to a JSON file in the config repo), and permissionsBoundary (either customerManagedPolicy or awsManagedPolicyName). relayState is not a supported key in any documented LZA version (v1.3.x through v1.10.x); setting a relay state on a permission set requires either the console, the aws ssoadmin update-permission-set CLI, or a CloudFormation AWS::SSO::PermissionSet resource managed outside LZA.
- The acceleratorManaged policy type creates a cross-file dependency: the policy name referenced under acceleratorManaged must also appear in the policySets array of iam-config.yaml with the identityCenterDependency flag set to true. LZA provisions the policy before attaching it to the permission set, resolving the chicken-and-egg problem of customer-managed policies that do not yet exist at pipeline time.
- When LZA modifies a permission set (e.g., adding a managed policy), the pipeline calls the IdC UpdatePermissionSet API, then calls ProvisionPermissionSet with scope ALL_PROVISIONED_ACCOUNTS. The re-provisioning step pushes updated IAM role policy attachments into every member account that has an assignment for that permission set. Existing active IAM role sessions (temporary credentials in use) are not immediately invalidated by re-provisioning — they remain valid until the session duration configured on the permission set expires (up to 12 hours). Updated permissions do not take effect on in-flight sessions.
- Assignments are declared via identityCenterAssignments. Each entry links a named principal (USER or GROUP) to a named permission set, with a deploymentTargets scope. LZA resolves group and user names against the IdC identity store at pipeline time — the group or user must already exist in the IdC identity store (provisioned via SCIM or manually) before LZA can create the assignment. LZA does not create IdC users or groups; this is an explicit, documented limitation.
- The deploymentTargets scoping for assignments supports both accounts (explicit account name list) and organizationalUnits (OU name list). When an OU is specified, LZA creates assignments only for accounts that are direct children of that OU at the time the pipeline runs. Accounts in nested child OUs are not included automatically — each nested OU must be explicitly listed. This is a known documented limitation (GitHub issue #220). Newly vended accounts that join a targeted OU after the pipeline last ran do not receive assignments automatically; the next LZA pipeline execution applies them.
- Management account assignments have a documented history of failure in LZA (GitHub issues #215, #496). The root cause is that a delegated admin account cannot make certain IdC API calls targeting the management account's scope. Assignments targeting the management account or the Root OU may require console-based manual intervention in some LZA versions. The issue is acknowledged upstream and has seen partial fixes; operators should verify current behavior against their deployed LZA version before relying on management account assignments via LZA.
- LZA does NOT manage the 'Attributes for Access Control' (ABAC) configuration of the IdC instance. There is no key in the identityCenter block — or anywhere in iam-config.yaml — that maps to the CreateInstanceAccessControlAttributeConfiguration / UpdateInstanceAccessControlAttributeConfiguration API. Enabling ABAC and specifying which user-profile attributes to expose as session tags (e.g., mapping an Entra custom extension attribute to the SSMSessionRunAs session tag) must be done outside LZA via: (a) the IdC console Settings page, (b) the aws ssoadmin create-instance-access-control-attribute-configuration CLI command, (c) CloudFormation using AWS::SSO::InstanceAccessControlAttributeConfiguration, or (d) Terraform using the aws_ssoadmin_instance_access_control_attributes resource. If LZA is the primary IaC tool and no supplemental IaC owns this resource, the ABAC attribute configuration exists only in the IdC control plane with no declarative source-of-truth.
- AWS documentation confirms two specific attribute precedence relationships in IAM Identity Center ABAC evaluation: (1) attributes configured via the 'Attributes for access control' console page (InstanceAccessControlAttributeConfiguration) override SAML assertion values for the same attribute key; and (2) SCIM-synchronized user-profile attributes take precedence over SAML assertion values for the same key. Both relationships are explicitly documented. The relative priority between console-configured attributes and SCIM-synchronized attributes when both are present for the same key is not explicitly documented by AWS — treating this as a confirmed three-tier linear hierarchy (console > SCIM > SAML) goes beyond what the source material states and is an inference. The practical implication for teams debugging unexpected SSMSessionRunAs values: both the IdC ABAC console configuration and the SCIM sync are confirmed to override SAML claims, so either source could be the effective value. Teams should check both the 'Attributes for access control' console page and the SCIM-synchronized profile attributes before concluding the SAML claim pipeline is broken — but the winner between console and SCIM, when both specify the same key, cannot be determined from AWS documentation alone and represents an open question.
- Permission set and assignment changes made directly in the IdC console or via CLI are not reflected back in iam-config.yaml and will be overwritten on the next LZA pipeline run. LZA treats its YAML configuration as the authoritative desired state for the resources it manages. Resources created outside LZA (e.g., additional permission sets created manually) are not tracked by LZA and are not deleted by it, but any LZA-managed permission set modified outside LZA will be reverted to the YAML-declared state on the next pipeline execution.
- LZA does not expose any configuration surface for the following IdC instance-level settings: MFA policy configuration, session settings for the access portal, instance-level trusted token issuer configuration, or application assignment configurations. These remain console-only or are managed via separate IaC outside the LZA identityCenter block.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| identityCenter block (LZA) | The top-level configuration object in iam-config.yaml that declares LZA's management of IAM Identity Center. Contains name (required logical label), delegatedAdminAccount (optional), identityCenterPermissionSets (optional array), and identityCenterAssignments (optional array). Has no sub-keys for ABAC, instance settings, relay state, MFA policy, or user/group creation. |
| identityCenterPermissionSets | Array of permission set declarations within the LZA identityCenter block. Each entry declares the name, session duration, and policy configuration (awsManaged, customerManaged, acceleratorManaged, inlinePolicy, permissionsBoundary). LZA creates, updates, and re-provisions each declared permission set on every pipeline run. |
| acceleratorManaged policy type | A policy source type in identityCenterPermissionSets.policies that references policies LZA creates in member accounts before attaching them to the permission set. Requires a corresponding entry in the policySets array with identityCenterDependency:true. Solves the pre-existence dependency that customerManaged policies require. |
| identityCenterAssignments | Array of assignment declarations linking a principal (USER or GROUP by name) to a named permission set, scoped to specific accounts or OUs via deploymentTargets. Principals must already exist in the IdC identity store. OU scoping applies only to direct child accounts, not nested OUs. |
| deploymentTargets (assignments) | The scoping mechanism for identityCenterAssignments entries. Supports accounts (explicit list) and organizationalUnits (OU name list). OU-scoped assignments apply to direct children only at pipeline run time. Newly vended accounts receive assignments on the next pipeline execution, not immediately upon account creation. |
| ProvisionPermissionSet (IdC API) | The IAM Identity Center API action LZA invokes after updating a permission set to propagate policy changes to all assigned accounts. Called with scope ALL_PROVISIONED_ACCOUNTS after any permission set modification. Does not immediately invalidate existing active IAM role sessions — in-flight sessions remain valid until their configured session duration expires. |
| Attributes for Access Control (ABAC) | The IAM Identity Center instance-level configuration that specifies which user-profile attributes are passed as IAM session tags (aws:PrincipalTag) during federation. Configured via CreateInstanceAccessControlAttributeConfiguration API. Not managed by LZA — must be configured via console, CLI, CloudFormation AWS::SSO::InstanceAccessControlAttributeConfiguration, or Terraform aws_ssoadmin_instance_access_control_attributes. |
| delegatedAdminAccount | An optional LZA identityCenter key that specifies the account to receive delegated administrator rights for the IdC instance. When set, LZA calls the Organizations RegisterDelegatedAdministrator API. Changing this value requires removing the existing configuration first, running the pipeline, then setting the new value — in-place updates are not supported. |
| SCIM attribute precedence | AWS documentation confirms two specific precedence relationships for ABAC attribute evaluation in IAM Identity Center: (1) console-configured attributes (InstanceAccessControlAttributeConfiguration) override SAML assertion values for the same key; and (2) SCIM-synchronized attributes take precedence over SAML assertion values for the same key. Both two-way relationships are documented. The relative ordering between console-configured attributes and SCIM-synchronized attributes is not explicitly documented by AWS — the commonly assumed three-tier linear hierarchy (console > SCIM > SAML) is an inference beyond what AWS states. Teams using both sources for the same attribute key cannot determine the winner from documentation alone. |
| permissionsBoundary | An optional LZA identityCenterPermissionSets sub-key that sets a permissions boundary on a permission set. Accepts either customerManagedPolicy (name and path) or awsManagedPolicyName. Applies the boundary to the AWSReservedSSO_ role provisioned in each member account. |
| AWSReservedSSO_ role | The IAM role IdC automatically creates per-permission-set per-account when an assignment is provisioned. LZA does not directly manage these roles — they are side effects of assignment provisioning. These roles cannot be tagged by customers and cannot carry static session tags such as SSMSessionRunAs. |

---

## Tensions & Tradeoffs

- LZA's identityCenter block provides strong declarative control over permission set policy content and assignment topology, but it does not own the ABAC attribute mapping layer. Organizations that want full IaC coverage of their IdC configuration must use a supplemental tool (Terraform, CloudFormation, CLI) specifically for the InstanceAccessControlAttributeConfiguration resource — creating a split-ownership model that requires coordination to prevent drift.
- The OU-scoped assignment behavior (direct children only, not nested) creates a tension between configuration simplicity and accuracy. An operator who adds a permission set assignment scoped to 'Workloads' OU may believe it covers all workload accounts, but accounts in nested OUs (e.g., 'Workloads/Prod') are silently excluded until they are explicitly listed or until the parent OU assignment is split into per-OU entries.
- LZA treats its YAML as desired state for the resources it manages. Console or CLI modifications to LZA-managed permission sets and assignments are overwritten on the next pipeline run. This is the correct IaC contract, but it creates friction for operators who habitually use the console for testing or emergency changes — those changes are ephemeral and leave no audit trail in the config repo.
- ABAC attribute evaluation in IAM Identity Center involves at least two confirmed override relationships — console-configured attributes override SAML assertions, and SCIM-synchronized attributes override SAML assertions — but the relative ordering between console-configured and SCIM-synchronized attributes is not documented by AWS. This creates a compounding debugging problem: teams that built their ABAC pipeline using Entra claim transformation rules may find SAML values are overridden by either SCIM attributes or console-configured attributes (or both), but cannot determine from AWS documentation which of those two sources takes precedence when both specify the same key. The effective SSMSessionRunAs value may not match any single expected source, requiring investigators to check both the IdC 'Attributes for access control' console page and the SCIM-synchronized profile before concluding the SAML pipeline is broken — but the console-vs-SCIM resolution remains an empirical question, not a documented one.
- LZA's active session non-invalidation behavior on permission set updates means a user who receives reduced permissions (e.g., a policy removed from their permission set) retains those permissions in their current session until the session expires. For high-sensitivity permission changes, operators must manually revoke active sessions via the IdC console or use a policy-based revocation mechanism.

---

## Open Questions

- Does LZA support the relayState field on permission sets in any version post-v1.10? The field is supported by the underlying IdC CreatePermissionSet API and by CloudFormation AWS::SSO::PermissionSet, but it was not found in any documented LZA IdentityCenterPermissionSetConfig schema. Verification against the current main branch source (packages/@aws-accelerator/config/lib/models/iam-config.ts) is warranted.
- When LZA runs a pipeline and a new account has just been vended into an OU that is targeted by an identityCenterAssignment, does LZA's pipeline automatically detect the new account and create the assignment in that same run, or does a second pipeline run always be required? The timing dependency between account vending and assignment creation is not explicitly documented.
- Is there a supported pattern for using LZA customizations (post-pipeline hooks) to invoke the aws ssoadmin create-instance-access-control-attribute-configuration API, so that ABAC attribute configuration can be version-controlled adjacent to the LZA config repo rather than maintained in a separate IaC stack?
- What is the current behavior of LZA management account assignments in the latest release (v1.14.x)? Historical issues #215 and #496 indicate this was broken in v1.7.0 and partially addressed, but it is unclear whether it is fully resolved for all partition types.
- Does LZA expose any mechanism to import or reconcile IdC resources that were created outside LZA (e.g., permission sets created manually before LZA adoption) without destroying and recreating them?
- What is the effective precedence between console-configured attributes (InstanceAccessControlAttributeConfiguration) and SCIM-synchronized attributes when both specify the same ABAC attribute key in IAM Identity Center? AWS documentation confirms each overrides SAML assertions independently, but does not document the relative ordering between them. Teams using both sources simultaneously cannot predict the winning value from documentation alone — this requires empirical testing or an AWS support clarification.

---

## Sources & References

- [IIdentityCenterConfig interface — LZA TypeDoc v1.10.0](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.10.0/typedocs/latest/interfaces/___packages__aws_accelerator_config_lib_models_iam_config.IIdentityCenterConfig.html)
- [IdentityCenterPermissionSetConfig — LZA TypeDoc v1.3.2](https://awslabs.github.io/landing-zone-accelerator-on-aws/latest/typedocs/v1.3.2/classes/_aws_accelerator_config.IdentityCenterPermissionSetConfig.html)
- [IdentityCenterAssignmentConfig — LZA TypeDoc v1.9.2](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.10.0/typedocs/v1.9.2/classes/_aws_accelerator_config.IdentityCenterAssignmentConfig.html)
- [IdentityCenterConfig — LZA TypeDoc v1.6.0](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.6.0/typedocs/latest/classes/_aws_accelerator_config.IdentityCenterConfig.html)
- [IAM Configuration — LZA DeepWiki](https://deepwiki.com/awslabs/landing-zone-accelerator-on-aws/3.5-iam-configuration)
- [AWS Landing Zone Accelerator — Part 5: Identity & Access Management (Adam Divall)](https://www.adamdivall.co.uk/article/step-by-step-guides/landing-zone-accelerator-part-5/)
- [identityCenter: Error Assigning IAM Permissions to Management Account — GitHub Issue #215](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/215)
- [IAM Identity Center fails to create Management Account assignments (v1.7.0+) — GitHub Issue #496](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/496)
- [identityCenter: Solution Doesn't Handle Nested Organizational Units — GitHub Issue #220](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/220)
- [LZA does not support IIC user/group creation — GitHub Issue #533](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/533)
- [v1.5 REGRESSION: new IdentityCenterAssignmentConfig principal syntax — GitHub Issue #338](https://github.com/awslabs/landing-zone-accelerator-on-aws/issues/338)
- [Manage AWS accounts with permission sets — AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html)
- [Create, manage, and delete permission sets — AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsets.html)
- [ProvisionPermissionSet — IAM Identity Center API Reference](https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_ProvisionPermissionSet.html)
- [Attribute-based access control — AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html)
- [Attributes for access control — AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html)
- [Enable and configure attributes for access control — AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html)
- [CreateInstanceAccessControlAttributeConfiguration — IAM Identity Center API Reference](https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_CreateInstanceAccessControlAttributeConfiguration.html)
- [AWS::SSO::InstanceAccessControlAttributeConfiguration — AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html)
- [aws_ssoadmin_instance_access_control_attributes — Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssoadmin_instance_access_control_attributes)
- [Configure AWS IAM Identity Center ABAC for EC2 and Systems Manager Session Manager — AWS Security Blog](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [Understanding authentication sessions in IAM Identity Center — AWS](https://docs.aws.amazon.com/singlesignon/latest/userguide/authconcept.html)
- [Define a custom session duration and terminate active sessions in IAM Identity Center — AWS Security Blog](https://aws.amazon.com/blogs/security/define-a-custom-session-duration-and-terminate-active-sessions-in-iam-identity-center/)
- [Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center — AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html)
- [Using Terraform with Landing Zone Accelerator on AWS — AWS Cloud Operations Blog](https://aws.amazon.com/blogs/mt/using-terraform-with-landing-zone-accelerator-on-aws/)
