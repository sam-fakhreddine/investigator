# Investigation: Pulumi @pulumi/azuread for Entra Group Management in IAM Identity Center Hybrid Environments

**Date:** 2026-03-02
**Status:** Complete

---

## Question

> In a hybrid Entra ID + on-prem Active Directory environment, what does the Pulumi @pulumi/azuread provider support for managing Entra group membership for IAM Identity Center permission set assignments — specifically for cloud-native groups, SOA-converted groups, and the developer-managed PR-based workflow — and what are its documented limitations compared to the Terraform hashicorp/azuread provider?

---

## Context

The team uses AWS IAM Identity Center federated via Entra ID. Groups in Entra ID are assigned to IAM Identity Center permission sets, making group membership the access control plane for AWS. The environment is hybrid: on-prem Windows Active Directory synced to Entra via Entra Connect. Developers want to manage group membership without involving a Windows AD admin. Prior research established that on-prem-synced groups (onPremisesSyncEnabled=true) are cloud write-blocked — Graph API, Terraform azuread, and Pulumi azuread all fail for these groups. The viable path is cloud-native Entra security groups, with optional group writeback to on-prem AD via Entra Cloud Sync. A SOA conversion path exists (onPremisesSyncBehavior / isCloudManaged) that converts formerly-synced groups to cloud-managed. Terraform hashicorp/azuread is the team's current tool; they want to evaluate Pulumi @pulumi/azuread as a TypeScript-native alternative.

---

## Pulumi @pulumi/azuread — Capability Matrix for Hybrid Entra + IAM Identity Center

| Capability | Pulumi @pulumi/azuread | Notes |
| --- | --- | --- |
| Cloud-native group creation | Supported — azuread.Group | security_enabled=true, no members limit |
| Cloud-native group member add/remove | Supported — azuread.GroupMember | Group.ReadWrite.All or Directory.ReadWrite.All required |
| On-prem-synced group member write | Blocked at Graph API layer | Identical to Terraform azuread; not a provider limitation |
| SOA-converted group member write | Supported post-conversion | Conversion requires Group-OnPremisesSyncBehavior.ReadWrite.All; conversion itself is not automated by either provider |
| AWS IAM Identity Center assignment | Supported — aws.ssoadmin.AccountAssignment | principalType: GROUP, principalId: Identity Store group GUID |
| Cross-provider stack (Entra + AWS in one program) | Supported natively | Multiple providers in a single TypeScript stack; no adapter needed |
| pulumi preview on PR (CI gate) | Supported — pulumi/actions GitHub Action | comment-on-pr posts diff output as PR comment |
| State backend: Pulumi Cloud | Supported — default | Transactional locking, audit log, team RBAC |
| State backend: S3 (DIY) | Supported — pulumi login s3://... | No DynamoDB locking built-in; concurrent run risk |
| State backend: Azure Blob (DIY) | Supported — pulumi login azblob://... | Same DIY caveats as S3 |
| Provider version vs upstream Terraform | v6.8.0 bridges terraform-provider-azuread v3.7.0 | Upstream at v3.8.0 (Feb 2026); typically 4-8 week lag |
| Access package (Entitlement Mgmt) | Partial — uses /beta Graph endpoint | Microsoft flagged /beta/identityGovernance as unsupported; GA endpoint pending upstream Terraform fix |

> Graph API permissions needed: Group.ReadWrite.All (or Directory.ReadWrite.All) for group membership. Group-OnPremisesSyncBehavior.ReadWrite.All is additionally required only if performing SOA conversion, which is a one-time admin action outside the IaC workflow.

---

## Key Findings

- @pulumi/azuread v6.8.0 is a Terraform bridge provider wrapping terraform-provider-azuread v3.7.0; the upstream Terraform provider was at v3.8.0 as of February 2026, indicating a lag of approximately 4-8 weeks for new upstream features to reach the Pulumi package.
- The azuread.Group and azuread.GroupMember resources in @pulumi/azuread are functionally equivalent to azuread_group and azuread_group_member in the Terraform provider for cloud-native group management; both map to the same Microsoft Graph API calls and carry identical permission requirements (Group.ReadWrite.All or Directory.ReadWrite.All).
- The write-block on on-prem-synced groups (onPremisesSyncEnabled=true) is enforced by the Microsoft Graph API, not by either provider; both Terraform and Pulumi surface the same API error when attempting to modify synced group membership.
- SOA conversion (setting isCloudManaged=true via PATCH /groups/{id}/onPremisesSyncBehavior) is a Graph API operation requiring the Group-OnPremisesSyncBehavior.ReadWrite.All permission; neither the Pulumi nor the Terraform azuread provider exposes a resource for this operation as of the investigated versions, making SOA conversion a one-time admin step performed outside IaC.
- After SOA conversion, the formerly-synced group behaves identically to a cloud-native group from the Graph API perspective; azuread.GroupMember can manage its membership using Group.ReadWrite.All, without any additional provider-specific configuration.
- A single Pulumi TypeScript stack can instantiate both @pulumi/azuread and @pulumi/aws providers simultaneously, enabling atomic management of Entra group membership and the corresponding aws.ssoadmin.AccountAssignment in one program and one pulumi up operation.
- The aws.ssoadmin.AccountAssignment resource requires principalId (the Identity Store group GUID, not the Entra Object ID) and principalType: GROUP; in an Entra-federated Identity Center instance, the Identity Store group GUID must be retrieved separately via aws.identitystore.getGroup using the group's DisplayName as the filter.
- The official pulumi/actions GitHub Action supports a comment-on-pr mode that posts pulumi preview diff output directly to the PR; this is the documented equivalent of terraform plan in a PR-gated workflow.
- Pulumi Cloud (managed backend) provides transactional state locking, concurrent update protection, audit logs, and team RBAC; DIY backends (S3, Azure Blob) use file-based locking stored alongside state in the bucket — there is no DynamoDB-style external lock table as in Terraform's S3 backend, making concurrent pipeline runs a risk without Pulumi Cloud's transactional guarantees.
- The @pulumi/azuread provider's Access Package (Entitlement Management) resources use the /beta Microsoft Graph API endpoint, which Microsoft has flagged as unsupported for this path; this is an upstream Terraform provider issue not yet resolved as of the investigated versions, and is unrelated to group membership management.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| azuread.Group | Pulumi resource (in @pulumi/azuread) that creates and manages a cloud-native Entra ID security or Microsoft 365 group. Supports the members property (full desired-state membership) or can be used with separate azuread.GroupMember resources for individual membership management. |
| azuread.GroupMember | Pulumi resource that manages a single group membership entry. Takes groupObjectId and memberObjectId. Cannot be used concurrently with the members property on azuread.Group for the same group; doing so causes member conflicts. |
| pulumi-terraform-bridge | The Pulumi library that wraps upstream Terraform providers into Pulumi SDK packages. @pulumi/azuread is generated from terraform-provider-azuread via this bridge. Feature parity is near-complete but subject to a release lag of weeks to months between upstream Terraform provider releases and the corresponding Pulumi package release. |
| SOA Conversion (Source of Authority) | A Microsoft Entra ID operation that converts a formerly on-premises-synced group to cloud-managed authority by setting isCloudManaged=true via PATCH /groups/{id}/onPremisesSyncBehavior. After conversion, Entra Connect/Cloud Sync stops honoring on-prem changes to the group. Requires the Group-OnPremisesSyncBehavior.ReadWrite.All Graph permission. GA as of late 2025. |
| Group-OnPremisesSyncBehavior.ReadWrite.All | Microsoft Graph application permission required to call the /onPremisesSyncBehavior endpoint for SOA conversion. This permission is separate from Group.ReadWrite.All and must be explicitly granted to the service principal performing the conversion. Not required for normal group membership management after conversion. |
| aws.ssoadmin.AccountAssignment | Pulumi resource (in @pulumi/aws) equivalent to Terraform's aws_ssoadmin_account_assignment. Assigns a permission set to a principal (user or group) in a specific AWS account. Requires principalId (Identity Store GUID), principalType (GROUP or USER), targetId (AWS account ID), permissionSetArn, and instanceArn. |
| aws.identitystore.getGroup | Pulumi data source that looks up a group in the IAM Identity Center identity store by DisplayName. In an Entra-federated Identity Center instance, federated Entra groups appear in the identity store and can be retrieved by display name to obtain their Identity Store group GUID for use as principalId in AccountAssignment. |
| DIY Backend (Pulumi) | Pulumi's self-managed state storage option, configured via pulumi login s3://, azblob://, or gs://. Includes built-in file-based state locking but lacks the transactional guarantees, team RBAC, audit logs, and concurrent update protection provided by Pulumi Cloud. |
| pulumi/actions | Official Pulumi GitHub Action. In PR workflows, comment-on-pr: true posts the output of pulumi preview as a PR comment, providing the same visibility as terraform plan output in Terraform CI workflows. The action edits its previous comment rather than posting duplicates on re-run. |
| Graph API write-block on synced groups | Microsoft Graph API enforces that groups with onPremisesSyncEnabled=true cannot have their membership modified via cloud API calls. This is a Graph API-level constraint, not a Pulumi or Terraform provider limitation. Both providers surface the same error on attempt. |

---

## Tensions & Tradeoffs

- Using azuread.Group members property vs. separate azuread.GroupMember resources is mutually exclusive for the same group; teams must pick one pattern per group and cannot mix them without causing state drift and unintended member removal.
- The Identity Store group GUID (needed for aws.ssoadmin.AccountAssignment) is distinct from the Entra Object ID (produced by azuread.Group); in a federated Identity Center, there is no direct cross-provider output reference — a separate aws.identitystore.getGroup lookup by DisplayName is required, introducing a naming dependency between Entra group display name and Identity Center group display name.
- DIY state backends (S3, Azure Blob) offer data sovereignty and avoid Pulumi Cloud costs, but lack transactional locking and team RBAC; for a developer team running concurrent CI pipelines against shared IAM Identity Center resources, a race on S3 state could corrupt assignments.
- The @pulumi/azuread provider tracks terraform-provider-azuread closely but with a multi-week lag; teams that need a Graph API capability that was added to the upstream Terraform provider recently may need to wait for the next Pulumi bridge release before it is available in TypeScript.
- SOA conversion requires a one-time admin operation (Group-OnPremisesSyncBehavior.ReadWrite.All) that is not surfaced as an IaC resource in either provider; this creates an out-of-band step that must be performed by an admin with elevated permissions before developer-controlled IaC can take over group membership.

---

## Open Questions

- Whether the @pulumi/azuread provider will add a dedicated resource for SOA conversion (Group-OnPremisesSyncBehavior management), given that neither the upstream Terraform provider nor the Pulumi bridge currently exposes this Graph API endpoint.
- Whether the /beta Microsoft Graph API endpoint used by the access package resources will be deprecated before the upstream Terraform provider migrates to the GA endpoint, and what the failure mode would be if that endpoint is removed.
- Whether Pulumi Cloud's state locking and audit trail would satisfy the team's compliance requirements for tracking who approved group membership changes, or whether an additional PR-level approval workflow (e.g., GitHub CODEOWNERS, branch protection) is needed to complement the IaC audit trail.
- Whether an Identity Center-federated Entra group's Identity Store group GUID is stable and can be hardcoded, or whether it changes on re-provisioning events (e.g., Entra Connect re-sync), affecting the portability of pulumi state.

---

## Sources & References

- [azuread.Group — Pulumi Registry](https://www.pulumi.com/registry/packages/azuread/api-docs/group/)
- [azuread.GroupMember — Pulumi Registry](https://www.pulumi.com/registry/packages/azuread/api-docs/groupmember/)
- [Azure Active Directory (Azure AD) — Pulumi Registry Overview](https://www.pulumi.com/registry/packages/azuread/)
- [aws.ssoadmin.AccountAssignment — Pulumi Registry](https://www.pulumi.com/registry/packages/aws/api-docs/ssoadmin/accountassignment/)
- [aws.identitystore.getGroup — Pulumi Registry](https://www.pulumi.com/registry/packages/aws/api-docs/identitystore/getgroup/)
- [Using Pulumi GitHub Actions — CI/CD Documentation](https://www.pulumi.com/docs/iac/guides/continuous-delivery/github-actions/)
- [State and Backends — Pulumi Concepts](https://www.pulumi.com/docs/iac/concepts/state-and-backends/)
- [pulumi/actions — GitHub Actions Repository](https://github.com/pulumi/actions)
- [pulumi/pulumi-azuread — GitHub Repository](https://github.com/pulumi/pulumi-azuread)
- [Configure Group Source of Authority (SOA) in Microsoft Entra ID — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure)
- [Concept: Source of Authority Overview — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/hybrid/concept-source-of-authority-overview)
- [azuread_group_member — HashiCorp Terraform Registry](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group_member)
- [Identity Governance Entitlement Management using /beta/ API — GitHub Issue #984, pulumi/pulumi-azuread](https://github.com/pulumi/pulumi-azuread/issues/984)
- [Entra Group Source of Authority CONVERSION — Microsoft Community Hub](https://techcommunity.microsoft.com/blog/coreinfrastructureandsecurityblog/entra-group-source-of-authority-conversion-enabling-cloud-first-identity-managem/4456085)
- [Why Choose Pulumi Cloud Over DIY Backends — Pulumi Blog](https://www.pulumi.com/blog/why-choose-pulumi-cloud-over-diy-backends/)
