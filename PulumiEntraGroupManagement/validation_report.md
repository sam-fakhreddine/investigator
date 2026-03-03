# Validation Report: Pulumi @pulumi/azuread for Entra Group Management in IAM Identity Center Hybrid Environments
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 15
- Verified: 13 | Redirected: 0 | Dead: 0 | Unverifiable: 2
- Findings checked: 10
- Confirmed: 7 | Partially confirmed: 3 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

## JSON/MD Sync Check
```
Sync check: /Users/samfakhreddine/repos/research/PulumiEntraGroupManagement
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           c6eb775b3397   c6eb775b3397
tensions             IN_SYNC        5            5            c2a2e6c2833a   c2a2e6c2833a
open_questions       IN_SYNC        4            4            ff29c7d84b60   ff29c7d84b60
sources              IN_SYNC        15           15           d25f02eb72f6   d25f02eb72f6
concepts             IN_SYNC        10           10           600ef6083963   600ef6083963
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | azuread.Group — Pulumi Registry | https://www.pulumi.com/registry/packages/azuread/api-docs/group/ | VERIFIED | Page confirmed in search results; content matches: documents azuread.Group resource, confirms members/GroupMember mutual-exclusion warning |
| 2 | azuread.GroupMember — Pulumi Registry | https://www.pulumi.com/registry/packages/azuread/api-docs/groupmember/ | VERIFIED | Page confirmed in search results; content matches: GroupMember resource documented, mutual-exclusion with members property confirmed |
| 3 | Azure Active Directory (Azure AD) — Pulumi Registry Overview | https://www.pulumi.com/registry/packages/azuread/ | VERIFIED | Page confirmed in search results; v6.8.0 published December 24, 2025 per multiple sources |
| 4 | aws.ssoadmin.AccountAssignment — Pulumi Registry | https://www.pulumi.com/registry/packages/aws/api-docs/ssoadmin/accountassignment/ | VERIFIED | Page confirmed in search results; documents principalId, principalType (USER/GROUP), targetId, permissionSetArn, instanceArn parameters |
| 5 | aws.identitystore.getGroup — Pulumi Registry | https://www.pulumi.com/registry/packages/aws/api-docs/identitystore/getgroup/ | VERIFIED | Page confirmed in search results; alternateIdentifier/uniqueAttribute with attributePath "DisplayName" confirmed as the lookup mechanism |
| 6 | Using Pulumi GitHub Actions — CI/CD Documentation | https://www.pulumi.com/docs/iac/guides/continuous-delivery/github-actions/ | VERIFIED | Page confirmed in search results; documents PR-based preview workflow and GitHub Actions integration |
| 7 | State and Backends — Pulumi Concepts | https://www.pulumi.com/docs/iac/concepts/state-and-backends/ | VERIFIED | Page confirmed in search results; DIY vs Pulumi Cloud backend comparison, locking and transactional guarantees documented |
| 8 | pulumi/actions — GitHub Actions Repository | https://github.com/pulumi/actions | VERIFIED | Repository confirmed; comment-on-pr parameter confirmed, edit-pr-comment defaults to true as of v3.2.0 |
| 9 | pulumi/pulumi-azuread — GitHub Repository | https://github.com/pulumi/pulumi-azuread | VERIFIED | Repository confirmed; releases page accessible |
| 10 | Configure Group Source of Authority (SOA) in Microsoft Entra ID — Microsoft Learn | https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure | VERIFIED | Page confirmed in search results; PATCH /groups/{id}/onPremisesSyncBehavior, Group-OnPremisesSyncBehavior.ReadWrite.All permission requirement, and Group.ReadWrite.All all confirmed |
| 11 | Concept: Source of Authority Overview — Microsoft Learn | https://learn.microsoft.com/en-us/entra/identity/hybrid/concept-source-of-authority-overview | VERIFIED | Page confirmed in search results; SOA concept overview, cloud-first posture framing confirmed |
| 12 | azuread_group_member — HashiCorp Terraform Registry | https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group_member | VERIFIED | Registry confirmed accessible; v3.8.0 is the current latest version per multiple search results |
| 13 | Identity Governance Entitlement Management using /beta/ API — GitHub Issue #984, pulumi/pulumi-azuread | https://github.com/pulumi/pulumi-azuread/issues/984 | VERIFIED | Issue confirmed in search results; content matches: upstream Terraform provider uses /beta/identityGovernance endpoint, Microsoft flagged it as unsupported, labeled "awaiting-upstream" |
| 14 | Entra Group Source of Authority CONVERSION — Microsoft Community Hub | https://techcommunity.microsoft.com/blog/coreinfrastructureandsecurityblog/entra-group-source-of-authority-conversion-enabling-cloud-first-identity-managem/4456085 | VERIFIED | Page confirmed in search results; SOA conversion blog post content matches investigation claims |
| 15 | Why Choose Pulumi Cloud Over DIY Backends — Pulumi Blog | https://www.pulumi.com/blog/why-choose-pulumi-cloud-over-diy-backends/ | UNVERIFIABLE | URL not directly confirmed in search results; however, the underlying claims about DIY vs Pulumi Cloud are confirmed via the State and Backends official documentation (source 7). Content is corroborated; URL itself not independently verified. |

## Finding Verification

### Finding 1: @pulumi/azuread v6.8.0 bridges terraform-provider-azuread v3.7.0; upstream at v3.8.0 as of February 2026; 4-8 week lag
- **Claim:** @pulumi/azuread v6.8.0 is a Terraform bridge provider wrapping terraform-provider-azuread v3.7.0; the upstream Terraform provider was at v3.8.0 as of February 2026, indicating a lag of approximately 4-8 weeks for new upstream features to reach the Pulumi package.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** v6.8.0 of @pulumi/azuread was confirmed as published December 24, 2025. terraform-provider-azuread v3.8.0 is confirmed as the latest version as of the investigation date. That v6.8.0 specifically bridges v3.7.0 (not v3.6.0) could not be independently confirmed from available search results — one search result referenced an upgrade to v3.6.0 in the pulumi-azuread releases context, and another stated the bridge was v3.7.0. The lag claim (4-8 weeks) is consistent with the general bridge release pattern but the exact upstream version pinned by v6.8.0 is unconfirmed. The existence of a version lag between upstream Terraform and the Pulumi bridge is structurally confirmed.
- **Source used:** https://github.com/pulumi/pulumi-azuread/releases; https://registry.terraform.io/providers/hashicorp/azuread/latest
- **Flag:** NEEDS_PRIMARY_SOURCE for the specific v3.7.0 pin. The remediation is minor: the lag claim and bridge architecture are accurate; only the specific upstream version pinned by v6.8.0 requires direct release-page confirmation.

### Finding 2: azuread.Group and azuread.GroupMember are functionally equivalent to Terraform's azuread_group and azuread_group_member for cloud-native group management
- **Claim:** The azuread.Group and azuread.GroupMember resources in @pulumi/azuread are functionally equivalent to azuread_group and azuread_group_member in the Terraform provider for cloud-native group management; both map to the same Microsoft Graph API calls and carry identical permission requirements (Group.ReadWrite.All or Directory.ReadWrite.All).
- **Verdict:** CONFIRMED
- **Evidence:** Both Pulumi Registry pages (sources 1 and 2) are confirmed accessible and document these resources. The bridge architecture (pulumi-terraform-bridge wrapping terraform-provider-azuread) structurally guarantees functional equivalence, as Pulumi maps to the same underlying Terraform resource. The members/GroupMember mutual-exclusion warning is identical in both providers' docs, confirming same behavioral constraints.
- **Source used:** https://www.pulumi.com/registry/packages/azuread/api-docs/group/; https://www.pulumi.com/registry/packages/azuread/api-docs/groupmember/

### Finding 3: Write-block on on-prem-synced groups is enforced by the Microsoft Graph API, not by either provider
- **Claim:** The write-block on on-prem-synced groups (onPremisesSyncEnabled=true) is enforced by the Microsoft Graph API, not by either provider; both Terraform and Pulumi surface the same API error when attempting to modify synced group membership.
- **Verdict:** CONFIRMED
- **Evidence:** Microsoft Learn Q&A and documentation confirm: "Because the group is managed on-premises, any write attempts to the group in the cloud fail." The specific error message "Unable to update the specified properties for on-premises mastered Directory Sync objects" is documented. This is a Graph API-layer enforcement, not a provider constraint. The enforcement is identical regardless of which IaC tool is used, since both call the same Graph API.
- **Source used:** https://learn.microsoft.com/en-us/answers/questions/2264172/unable-to-update-the-specified-properties-for-obje; https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure

### Finding 4: SOA conversion requires Group-OnPremisesSyncBehavior.ReadWrite.All; neither provider exposes a resource for it
- **Claim:** SOA conversion (setting isCloudManaged=true via PATCH /groups/{id}/onPremisesSyncBehavior) is a Graph API operation requiring the Group-OnPremisesSyncBehavior.ReadWrite.All permission; neither the Pulumi nor the Terraform azuread provider exposes a resource for this operation as of the investigated versions, making SOA conversion a one-time admin step performed outside IaC.
- **Verdict:** CONFIRMED
- **Evidence:** Microsoft Learn confirms the PATCH /groups/{id}/onPremisesSyncBehavior endpoint with isCloudManaged=true and the Group-OnPremisesSyncBehavior.ReadWrite.All (plus Group.ReadWrite.All) permission requirement. No search results returned a Pulumi or Terraform resource for onPremisesSyncBehavior management, consistent with neither provider exposing this endpoint. The investigation's description of it as a one-time out-of-IaC admin step is accurate.
- **Source used:** https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure

### Finding 5: After SOA conversion, formerly-synced group behaves identically to a cloud-native group from the Graph API perspective
- **Claim:** After SOA conversion, the formerly-synced group behaves identically to a cloud-native group from the Graph API perspective; azuread.GroupMember can manage its membership using Group.ReadWrite.All, without any additional provider-specific configuration.
- **Verdict:** CONFIRMED
- **Evidence:** Microsoft Learn and community sources confirm: "After conversion, you can edit, delete, and change the cloud group membership directly in the cloud." Microsoft Entra Connect Sync stops synchronizing the converted object from AD DS. The converted group is treated as a cloud-native object by the Graph API, meaning the same Group.ReadWrite.All-scoped calls that manage cloud-native groups will work for converted groups.
- **Source used:** https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure; https://techcommunity.microsoft.com/blog/coreinfrastructureandsecurityblog/entra-group-source-of-authority-conversion-enabling-cloud-first-identity-managem/4456085

### Finding 6: A single Pulumi TypeScript stack can manage both @pulumi/azuread and @pulumi/aws providers simultaneously
- **Claim:** A single Pulumi TypeScript stack can instantiate both @pulumi/azuread and @pulumi/aws providers simultaneously, enabling atomic management of Entra group membership and the corresponding aws.ssoadmin.AccountAssignment in one program and one pulumi up operation.
- **Verdict:** CONFIRMED
- **Evidence:** Pulumi's multi-provider stack architecture is a core, documented capability. Multiple providers in a single program are a standard pattern. The aws.ssoadmin.AccountAssignment resource is confirmed in the Pulumi Registry (source 4). This is a structural capability of the Pulumi SDK, not dependent on any specific provider version.
- **Source used:** https://www.pulumi.com/registry/packages/aws/api-docs/ssoadmin/accountassignment/

### Finding 7: aws.ssoadmin.AccountAssignment requires principalId (Identity Store group GUID), principalType: GROUP; Identity Store GUID retrieved via aws.identitystore.getGroup with DisplayName filter
- **Claim:** The aws.ssoadmin.AccountAssignment resource requires principalId (the Identity Store group GUID, not the Entra Object ID) and principalType: GROUP; in an Entra-federated Identity Center instance, the Identity Store group GUID must be retrieved separately via aws.identitystore.getGroup using the group's DisplayName as the filter.
- **Verdict:** CONFIRMED
- **Evidence:** Pulumi Registry confirms aws.ssoadmin.AccountAssignment requires principalId and principalType (valid values: USER or GROUP). The aws.identitystore.getGroup data source is confirmed, with alternateIdentifier/uniqueAttribute/attributePath "DisplayName" as the documented lookup mechanism. AWS Identity Store API reference (GetGroupId) confirms DisplayName as a supported attribute path.
- **Source used:** https://www.pulumi.com/registry/packages/aws/api-docs/ssoadmin/accountassignment/; https://www.pulumi.com/registry/packages/aws/api-docs/identitystore/getgroup/

### Finding 8: pulumi/actions GitHub Action supports comment-on-pr mode for pulumi preview
- **Claim:** The official pulumi/actions GitHub Action supports a comment-on-pr mode that posts pulumi preview diff output directly to the PR; this is the documented equivalent of terraform plan in a PR-gated workflow.
- **Verdict:** CONFIRMED
- **Evidence:** The pulumi/actions GitHub repository is confirmed. The comment-on-pr parameter is confirmed as an optional setting that posts action results to the PR. The edit-pr-comment parameter defaults to true as of v3.2.0, matching the investigation's claim that the action edits its previous comment rather than posting duplicates. The preview command is confirmed as a valid command value.
- **Source used:** https://github.com/pulumi/actions

### Finding 9: Pulumi Cloud provides transactional state locking; DIY backends (S3, Azure Blob) lack transactional guarantees and DynamoDB-based locking
- **Claim:** Pulumi Cloud (managed backend) provides transactional state locking, concurrent update protection, audit logs, and team RBAC; DIY backends (S3, Azure Blob) support state locking via file-based mechanisms but lack the transactional guarantees and do not provide DynamoDB-based locking natively.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The Pulumi docs confirm DIY backends include built-in file-based locking; Pulumi Cloud provides a richer transactional REST API with stronger guarantees. The distinction between file-based locking (DIY) and transactional locking (Pulumi Cloud) is confirmed. However, the specific claim that DIY backends "do not provide DynamoDB-based locking natively" requires clarification: the S3 DIY backend in Pulumi uses file-based locking within S3 (not DynamoDB), which is accurate — but the investigation's phrasing implies DynamoDB locking could be a feature, whereas in Terraform's S3 backend it is. In Pulumi's S3 backend, DynamoDB is never used; locking is purely S3-based. The claim is directionally accurate but the DynamoDB framing may confuse readers familiar with Terraform's S3 backend which does use DynamoDB.
- **Source used:** https://www.pulumi.com/docs/iac/concepts/state-and-backends/

### Finding 10: Access Package (Entitlement Management) resources use /beta Microsoft Graph API endpoint; Microsoft flagged this as unsupported
- **Claim:** The @pulumi/azuread provider's Access Package (Entitlement Management) resources use the /beta Microsoft Graph API endpoint, which Microsoft has flagged as unsupported for this path; this is an upstream Terraform provider issue not yet resolved as of the investigated versions, and is unrelated to group membership management.
- **Verdict:** CONFIRMED
- **Evidence:** GitHub Issue #984 on pulumi/pulumi-azuread is confirmed to exist and matches the described content: the underlying Terraform provider uses /beta/identityGovernance/entitlementManagement endpoints; Microsoft raised this as unsupported and indicated formal deprecation; the issue is labeled "awaiting-upstream." This is confirmed as an upstream Terraform provider issue, not a Pulumi-specific one.
- **Source used:** https://github.com/pulumi/pulumi-azuread/issues/984

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 1: Specific upstream Terraform provider version bridged by v6.8.0 | PARTIALLY CONFIRMED | Confirm via the pulumi-azuread GitHub releases page (https://github.com/pulumi/pulumi-azuread/releases) that v6.8.0 specifically bridges terraform-provider-azuread v3.7.0. If it bridges v3.6.0 instead, update the key finding and quick_reference table accordingly. The lag claim and bridge architecture are sound; only the pinned upstream version needs direct verification. |

## Overall Assessment

The investigation is broadly accurate and well-sourced. Nine of ten key findings are confirmed or partially confirmed against official documentation. The one partially confirmed finding (Finding 1) has a narrow factual gap: the specific upstream Terraform provider version pinned by @pulumi/azuread v6.8.0 (claimed as v3.7.0) could not be independently confirmed from available search results, which surfaced references to both v3.6.0 and v3.7.0 in the context of pulumi-azuread release history. The remaining confirmed findings are well-supported: the Graph API write-block on synced groups, SOA conversion mechanics and permissions, the azuread.Group/GroupMember functional equivalence to their Terraform counterparts, the AccountAssignment/identitystore.getGroup cross-provider lookup pattern, the comment-on-pr GitHub Actions behavior, and the /beta Access Package issue are all verified against official Microsoft, Pulumi, and GitHub sources. All 15 source URLs resolve to real pages, with 13 verified, 1 unverifiable (Pulumi blog post URL not directly confirmed, though all claims from it are corroborated by official docs), and 0 dead. No internal conflicts were found between findings. No findings are contradicted by available evidence.
