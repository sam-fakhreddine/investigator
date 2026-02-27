# Glossary — LZA identityCenter Config Block — Declarative Surface, Limits, and ABAC Gap

Quick definitions of key terms and concepts referenced in this investigation.

---

## identityCenter block (LZA)

The top-level configuration object in iam-config.yaml that declares LZA's management of IAM Identity Center. Contains name (required logical label), delegatedAdminAccount (optional), identityCenterPermissionSets (optional array), and identityCenterAssignments (optional array). Has no sub-keys for ABAC, instance settings, relay state, MFA policy, or user/group creation.

## identityCenterPermissionSets

Array of permission set declarations within the LZA identityCenter block. Each entry declares the name, session duration, and policy configuration (awsManaged, customerManaged, acceleratorManaged, inlinePolicy, permissionsBoundary). LZA creates, updates, and re-provisions each declared permission set on every pipeline run.

## acceleratorManaged policy type

A policy source type in identityCenterPermissionSets.policies that references policies LZA creates in member accounts before attaching them to the permission set. Requires a corresponding entry in the policySets array with identityCenterDependency:true. Solves the pre-existence dependency that customerManaged policies require.

## identityCenterAssignments

Array of assignment declarations linking a principal (USER or GROUP by name) to a named permission set, scoped to specific accounts or OUs via deploymentTargets. Principals must already exist in the IdC identity store. OU scoping applies only to direct child accounts, not nested OUs.

## deploymentTargets (assignments)

The scoping mechanism for identityCenterAssignments entries. Supports accounts (explicit list) and organizationalUnits (OU name list). OU-scoped assignments apply to direct children only at pipeline run time. Newly vended accounts receive assignments on the next pipeline execution, not immediately upon account creation.

## ProvisionPermissionSet (IdC API)

The IAM Identity Center API action LZA invokes after updating a permission set to propagate policy changes to all assigned accounts. Called with scope ALL_PROVISIONED_ACCOUNTS after any permission set modification. Does not immediately invalidate existing active IAM role sessions — in-flight sessions remain valid until their configured session duration expires.

## Attributes for Access Control (ABAC)

The IAM Identity Center instance-level configuration that specifies which user-profile attributes are passed as IAM session tags (aws:PrincipalTag) during federation. Configured via CreateInstanceAccessControlAttributeConfiguration API. Not managed by LZA — must be configured via console, CLI, CloudFormation AWS::SSO::InstanceAccessControlAttributeConfiguration, or Terraform aws_ssoadmin_instance_access_control_attributes.

## delegatedAdminAccount

An optional LZA identityCenter key that specifies the account to receive delegated administrator rights for the IdC instance. When set, LZA calls the Organizations RegisterDelegatedAdministrator API. Changing this value requires removing the existing configuration first, running the pipeline, then setting the new value — in-place updates are not supported.

## SCIM attribute precedence

AWS documentation confirms two specific precedence relationships for ABAC attribute evaluation in IAM Identity Center: (1) console-configured attributes (InstanceAccessControlAttributeConfiguration) override SAML assertion values for the same key; and (2) SCIM-synchronized attributes take precedence over SAML assertion values for the same key. Both two-way relationships are documented. The relative ordering between console-configured attributes and SCIM-synchronized attributes is not explicitly documented by AWS — the commonly assumed three-tier linear hierarchy (console > SCIM > SAML) is an inference beyond what AWS states. Teams using both sources for the same attribute key cannot determine the winner from documentation alone.

## permissionsBoundary

An optional LZA identityCenterPermissionSets sub-key that sets a permissions boundary on a permission set. Accepts either customerManagedPolicy (name and path) or awsManagedPolicyName. Applies the boundary to the AWSReservedSSO_ role provisioned in each member account.

## AWSReservedSSO_ role

The IAM role IdC automatically creates per-permission-set per-account when an assignment is provisioned. LZA does not directly manage these roles — they are side effects of assignment provisioning. These roles cannot be tagged by customers and cannot carry static session tags such as SSMSessionRunAs.

---

*Back to: [investigation.md](investigation.md)*
