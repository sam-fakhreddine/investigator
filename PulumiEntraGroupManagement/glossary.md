# Glossary — Pulumi @pulumi/azuread for Entra Group Management in IAM Identity Center Hybrid Environments

Quick definitions of key terms and concepts referenced in this investigation.

---

## azuread.Group

Pulumi resource (in @pulumi/azuread) that creates and manages a cloud-native Entra ID security or Microsoft 365 group. Supports the members property (full desired-state membership) or can be used with separate azuread.GroupMember resources for individual membership management.

## azuread.GroupMember

Pulumi resource that manages a single group membership entry. Takes groupObjectId and memberObjectId. Cannot be used concurrently with the members property on azuread.Group for the same group; doing so causes member conflicts.

## pulumi-terraform-bridge

The Pulumi library that wraps upstream Terraform providers into Pulumi SDK packages. @pulumi/azuread is generated from terraform-provider-azuread via this bridge. Feature parity is near-complete but subject to a release lag of weeks to months between upstream Terraform provider releases and the corresponding Pulumi package release.

## SOA Conversion (Source of Authority)

A Microsoft Entra ID operation that converts a formerly on-premises-synced group to cloud-managed authority by setting isCloudManaged=true via PATCH /groups/{id}/onPremisesSyncBehavior. After conversion, Entra Connect/Cloud Sync stops honoring on-prem changes to the group. Requires the Group-OnPremisesSyncBehavior.ReadWrite.All Graph permission. GA as of late 2025.

## Group-OnPremisesSyncBehavior.ReadWrite.All

Microsoft Graph application permission required to call the /onPremisesSyncBehavior endpoint for SOA conversion. This permission is separate from Group.ReadWrite.All and must be explicitly granted to the service principal performing the conversion. Not required for normal group membership management after conversion.

## aws.ssoadmin.AccountAssignment

Pulumi resource (in @pulumi/aws) equivalent to Terraform's aws_ssoadmin_account_assignment. Assigns a permission set to a principal (user or group) in a specific AWS account. Requires principalId (Identity Store GUID), principalType (GROUP or USER), targetId (AWS account ID), permissionSetArn, and instanceArn.

## aws.identitystore.getGroup

Pulumi data source that looks up a group in the IAM Identity Center identity store by DisplayName. In an Entra-federated Identity Center instance, federated Entra groups appear in the identity store and can be retrieved by display name to obtain their Identity Store group GUID for use as principalId in AccountAssignment.

## DIY Backend (Pulumi)

Pulumi's self-managed state storage option, configured via pulumi login s3://, azblob://, or gs://. Includes built-in file-based state locking but lacks the transactional guarantees, team RBAC, audit logs, and concurrent update protection provided by Pulumi Cloud.

## pulumi/actions

Official Pulumi GitHub Action. In PR workflows, comment-on-pr: true posts the output of pulumi preview as a PR comment, providing the same visibility as terraform plan output in Terraform CI workflows. The action edits its previous comment rather than posting duplicates on re-run.

## Graph API write-block on synced groups

Microsoft Graph API enforces that groups with onPremisesSyncEnabled=true cannot have their membership modified via cloud API calls. This is a Graph API-level constraint, not a Pulumi or Terraform provider limitation. Both providers surface the same error on attempt.

---

*Back to: [investigation.md](investigation.md)*
