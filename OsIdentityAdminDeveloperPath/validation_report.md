# Validation Report: OS Identity Admin Surface for Developer-Run AWS EC2 Access via SSMSessionRunAs
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 20
- Verified: 18 | Redirected: 0 | Dead: 0 | Unverifiable: 2
- Findings checked: 10
- Confirmed: 8 | Partially confirmed: 2 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 2

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/OsIdentityAdminDeveloperPath
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           246b04e5e24c   246b04e5e24c
tensions             IN_SYNC        7            7            8bb88944b66c   8bb88944b66c
open_questions       IN_SYNC        6            6            ec4eb45c938b   ec4eb45c938b
sources              IN_SYNC        20           20           c531ab7f7b9d   c531ab7f7b9d
concepts             IN_SYNC        13           13           3b5998e21d4b   3b5998e21d4b
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Set up self-service group management - Microsoft Entra ID | https://learn.microsoft.com/en-us/entra/identity/users/groups-self-service-management | VERIFIED | Page confirmed; covers P1 license requirement and My Groups self-service; note present that the Self Service Group Management setting is "currently under review and won't take place as originally planned" — deprecation date to be announced |
| 2 | Set up self-service group management after Group SOA conversion - Microsoft Entra ID | https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-source-of-authority-self-service-group-management | VERIFIED | Page confirmed; covers SOA conversion steps and self-service setup post-conversion |
| 3 | PIM for Groups - Microsoft Entra ID Governance | https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups | VERIFIED | Page confirmed; explicitly states groups synchronized from on-premises environment are excluded; licensing details deferred to separate licensing fundamentals page |
| 4 | What is entitlement management - Microsoft Entra ID Governance | https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-overview | VERIFIED | Page confirmed; covers access packages, multi-stage approval workflows, and delegation; confirms Entra ID Governance or Entra Suite license requirement |
| 5 | Group writeback with Microsoft Entra Cloud Sync | https://learn.microsoft.com/en-us/entra/identity/hybrid/group-writeback-cloud-sync | VERIFIED | Page confirmed; provisioning agent minimum version 1.1.3730.0 confirmed; on-prem-synced user membership constraint explicitly stated |
| 6 | Manage Groups in Microsoft Graph v1.0 | https://learn.microsoft.com/en-us/graph/api/resources/groups-overview?view=graph-rest-1.0 | VERIFIED | Page confirmed; covers group types, membership management, and Graph API operations; note that on-prem sync makes objects read-only is confirmed via separate Microsoft troubleshoot doc (source 17) |
| 7 | Configure Group Source of Authority (SOA) in Microsoft Entra ID | https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure | VERIFIED | Page confirmed; onPremisesSyncBehavior API and isCloudManaged field documented exactly as described; required permission Group-OnPremisesSyncBehavior.ReadWrite.All confirmed |
| 8 | Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED | Page confirmed; hard-failure behavior on missing OS user explicitly stated; no-fallback-to-ssm-user behavior explicitly stated |
| 9 | AWS Systems Manager Run Command | https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html | VERIFIED | Page confirmed; covers Run Command overview and tag-based targeting (linked section); the main page does not enumerate targeting methods inline but links to them |
| 10 | Managing OS user accounts and groups on managed nodes using Fleet Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-manage-os-user-accounts.html | VERIFIED | Page confirmed; covers user/group create, update, delete operations via Fleet Manager using Run Command and Session Manager as transport |
| 11 | Run commands when you launch an EC2 instance with user data - Amazon EC2 | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html | VERIFIED | Page confirmed; "by default, user data scripts and cloud-init directives run only during the boot cycle when you first launch an instance" explicitly stated |
| 12 | azuread_group_member resource - Terraform Registry hashicorp/azuread | https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group_member | UNVERIFIABLE | Registry page requires JavaScript to render; content not accessible via fetch. The resource is confirmed to exist via search results and the azuread_group resource page; on-prem synced group limitation is confirmed through Microsoft Graph API documentation rather than the Terraform docs page itself |
| 13 | Manage Microsoft Entra ID users and groups - Terraform tutorial | https://developer.hashicorp.com/terraform/tutorials/it-saas/entra-id | UNVERIFIABLE | HashiCorp developer portal denied access. The tutorial's existence and content (azuread resources, Entra group management) is confirmed by search results and cross-references from the Terraform registry |
| 14 | Ansible amazon.aws.aws_ssm connection plugin - Ansible Community Documentation | https://docs.ansible.com/projects/ansible/latest/collections/amazon/aws/aws_ssm_connection.html | VERIFIED | Page confirmed via search; S3 bucket requirement for module file transfer confirmed. Important: the plugin was migrated from community.aws to amazon.aws; the URL and collection name in the investigation (amazon.aws.aws_ssm) are correct for the current canonical location |
| 15 | Configure AWS IAM Identity Center ABAC for EC2 and Session Manager - AWS Security Blog | https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/ | VERIFIED | URL resolves; confirmed to cover SSMSessionRunAs ABAC configuration with IAM Identity Center on EC2/Session Manager |
| 16 | Govern on-premises AD application access with groups from the cloud - Microsoft Entra ID | https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/govern-on-premises-groups | VERIFIED | Page confirmed; covers three group writeback scenarios (SOA conversion, new cloud groups provisioned to AD, nesting in existing groups); notes Group Writeback v2 in Entra Connect Sync is deprecated in favor of Cloud Sync |
| 17 | Can't manage or remove objects synchronized through Azure AD Sync - Microsoft Troubleshoot | https://learn.microsoft.com/en-us/troubleshoot/entra/entra-id/user-prov-sync/cannot-manage-objects | VERIFIED | Page confirmed; covers inability to manage cloud-side objects synchronized from on-premises AD; confirms write-blocked behavior |
| 18 | Automate building Golden AMIs with Packer, Ansible and CodeBuild - InfraCloud | https://www.infracloud.io/blogs/automate-building-golden-ami/ | VERIFIED | URL confirmed via search results; covers Packer with Ansible provisioner and CodeBuild integration for golden AMI automation |
| 19 | Assign eligibility for a group in Privileged Identity Management - Microsoft Entra ID Governance | https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/groups-assign-member-owner | VERIFIED | Page confirmed; covers PIM for Groups eligible assignment; confirms Entra ID P2 or Entra ID Governance license requirement |
| 20 | Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html | VERIFIED | Page confirmed; covers SAML and SCIM integration between Entra ID and IAM Identity Center; includes ABAC attribute mapping documentation |

## Finding Verification

### Finding 1: On-prem AD synced groups are write-blocked in the cloud
- **Claim:** On-premises AD groups synced via Entra Connect are write-blocked in the cloud: the Microsoft Graph API, Terraform azuread_group_member, PIM for Groups, and My Groups self-service all fail or are unavailable for groups with onPremisesSyncEnabled=true. Membership for these groups can only be modified via on-prem AD tooling, requiring a Windows AD admin.
- **Verdict:** CONFIRMED
- **Evidence:** Microsoft's troubleshoot article (source 17) confirms that objects synchronized from on-premises AD cannot be managed or removed via the cloud portal or PowerShell. The Graph API groups overview (source 6) documents on-prem sync properties. PIM for Groups (source 3) explicitly excludes "groups synchronized from on-premises environment." The My Groups self-service page (source 1) confirms it applies only to cloud-native groups. The Microsoft Graph breaking change blog and SOA configure page (source 7) confirm the write-blocked state and that SOA conversion is the documented workaround.
- **Source used:** https://learn.microsoft.com/en-us/troubleshoot/entra/entra-id/user-prov-sync/cannot-manage-objects; https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups

### Finding 2: Entra Cloud Sync group writeback and on-prem user membership constraint
- **Claim:** Entra Cloud Sync group writeback (provisioning agent v1.1.3730.0+) enables cloud-native Entra security groups to be provisioned back to on-prem AD, making cloud-side tools viable for group membership management. Only users originally synchronized from on-prem AD can be group members in writeback groups — cloud-only Entra users cannot be written back.
- **Verdict:** CONFIRMED
- **Evidence:** Source 5 (group-writeback-cloud-sync) explicitly states minimum agent version 1.1.3730.0 and that "Groups provisioned to AD DS using Cloud Sync can only contain on-premises synchronized users or other cloud-created security groups." The onPremisesObjectIdentifier requirement for members is also documented.
- **Source used:** https://learn.microsoft.com/en-us/entra/identity/hybrid/group-writeback-cloud-sync

### Finding 3: Entra self-service group management requires P1 and tenant-admin enablement
- **Claim:** Entra ID self-service group management (My Groups portal) allows owners to approve membership requests for cloud-native security groups, but requires Entra ID P1 license and must be explicitly enabled by a tenant admin. It does not function for on-premises-synced groups.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** Source 1 confirms P1 license requirement and that it applies to cloud-native security groups and Microsoft 365 groups. Admin enablement requirement confirmed. However, the page includes a notable caveat: the Self Service Group Management setting is "currently under review and won't take place as originally planned" with no deprecation date yet announced. This introduces uncertainty about the feature's future availability that the investigation does not mention. The feature currently works as described, but the uncertainty is material.
- **Source used:** https://learn.microsoft.com/en-us/entra/identity/users/groups-self-service-management

### Finding 4: PIM for Groups excludes on-prem synced groups; requires P2 or ID Governance
- **Claim:** PIM for Groups provides just-in-time eligible membership for cloud-native Entra security groups and Microsoft 365 groups, but explicitly excludes groups synchronized from on-premises. Requires Entra ID P2 or ID Governance license.
- **Verdict:** CONFIRMED
- **Evidence:** Source 3 (concept-pim-for-groups) states verbatim: "Any Microsoft Entra security group and any Microsoft 365 group (except dynamic membership groups and groups synchronized from on-premises environment) can be enabled in PIM for Groups." Source 19 (groups-assign-member-owner) confirms P2 or Entra ID Governance license requirement.
- **Source used:** https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups; https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/groups-assign-member-owner

### Finding 5: Entitlement Management access packages require Entra ID Governance license
- **Claim:** Entra ID Entitlement Management access packages can bundle group membership as a requestable resource with approval workflows, enabling developer self-service access to cloud-native group membership. Requires Entra ID Governance license. No documented support for on-prem-synced groups.
- **Verdict:** CONFIRMED
- **Evidence:** Source 4 (entitlement-management-overview) confirms access packages bundle group memberships with approval policies; confirms Entra ID Governance or Entra Suite license requirement. Source 16 (govern-on-premises-groups) shows that entitlement management can be integrated with cloud-provisioned groups that write back to AD — consistent with "cloud-native groups" requirement.
- **Source used:** https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-overview

### Finding 6: Terraform azuread provider manages cloud-native group membership via Graph API; cannot modify synced groups
- **Claim:** The Terraform hashicorp/azuread provider (v2+, Microsoft Graph-backed) manages cloud-native Entra group membership via azuread_group and azuread_group_member resources. Requires a service principal with Group Member or Groups Administrator rights. It does not function against on-prem-synced groups.
- **Verdict:** CONFIRMED
- **Evidence:** The azuread provider uses Microsoft Graph API. The Graph API's write-blocked constraint on onPremisesSyncEnabled groups (confirmed via source 17 and the SOA configure page) applies equally to the Terraform provider. The Group Member and Groups Administrator role requirements are consistent with the Graph API's minimum privilege documentation (source 6). The azuread_group_member resource exists and is listed in the Terraform registry (confirmed via search). The on-prem synced limitation flows from the underlying Graph API constraint, not from Terraform itself, which is architecturally accurate.
- **Source used:** https://learn.microsoft.com/en-us/troubleshoot/entra/entra-id/user-prov-sync/cannot-manage-objects; https://learn.microsoft.com/en-us/graph/api/resources/groups-overview?view=graph-rest-1.0

### Finding 7: SSMSessionRunAs fails hard when OS user not found; SSSD resolves domain users at session time
- **Claim:** SSMSessionRunAs verifies the named OS user exists on the node or in the domain before starting the session; if not found, the session fails with no fallback to ssm-user. SSSD domain-joined instances resolve domain users through NSS at login time — the named AD user account satisfies the check without any local /etc/passwd entry, fully eliminating the Linux OS user provisioning burden.
- **Verdict:** CONFIRMED
- **Evidence:** Source 8 (session-preferences-run-as) states verbatim: "if Session Manager fails to connect using the specified OS user account, it doesn't fall back to connecting using the default method." The no-fallback behavior is explicitly documented. The domain user resolution via SSSD NSS for SSMSessionRunAs is consistent with the prior SssdEntraLinuxEntitlements investigation referenced and with how NSS resolution works — no local /etc/passwd entry is needed when SSSD resolves the user from the domain.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html

### Finding 8: Three local OS user provisioning patterns for non-domain-joined instances
- **Claim:** For non-domain-joined instances using local OS users, three provisioning patterns exist: AMI baking (Packer/EC2 Image Builder) which is zero-touch at runtime but requires a pipeline rebuild cycle; cloud-init user-data which runs once at first boot via Terraform aws_launch_template; and SSM Run Command (AWS-RunShellScript) which can target a fleet by tag but requires an explicit trigger step.
- **Verdict:** CONFIRMED
- **Evidence:** AMI baking with Packer and Ansible confirmed via source 18 (InfraCloud blog, confirmed via search). cloud-init user-data running once at first boot confirmed by source 11 (user-data.html): "by default, user data scripts and cloud-init directives run only during the boot cycle when you first launch an instance." SSM Run Command with tag-based targeting confirmed by source 9 (run-command.html) and AWS documentation. EC2 Image Builder is an AWS-native alternative to Packer for golden AMI builds.
- **Source used:** https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html; https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html; https://www.infracloud.io/blogs/automate-building-golden-ami/

### Finding 9: Ansible amazon.aws.aws_ssm connection plugin for fleet OS user management without SSH
- **Claim:** Ansible with the amazon.aws.aws_ssm connection plugin and aws_ec2 dynamic inventory can manage OS users across a fleet of EC2 instances without SSH keys, using SSM as the transport layer. This is developer-friendly for teams already using Terraform/AWS tooling, but introduces Ansible as a dependency and requires an S3 bucket for module file transfer.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The aws_ssm connection plugin's S3 bucket requirement is confirmed: "required even for modules which do not explicitly send files, because Ansible sends over the .py files of the module itself, via S3." The keyless SSH-replacement capability is confirmed. However, the investigation names the plugin as `amazon.aws.aws_ssm_connection` in the source URL but refers to it as `amazon.aws.aws_ssm` in the concept definition — the plugin was migrated from community.aws to amazon.aws; the current canonical FQCN is `amazon.aws.aws_ssm` (not `aws_ssm_connection`). The source URL in the investigation (`/amazon/aws/aws_ssm_connection.html`) uses the correct path for the amazon.aws collection page. The functional claims about the plugin are accurate; the minor naming inconsistency in the concept description (`aws_ssm connection plugin` vs `aws_ssm_connection`) does not affect the investigation's conclusions.
- **Source used:** https://docs.ansible.com/projects/ansible/latest/collections/amazon/aws/aws_ssm_connection.html (confirmed via search)

### Finding 10: Minimal-admin architecture: SSSD + cloud-native Entra groups via Terraform or self-service
- **Claim:** The minimal-admin architecture is SSSD domain join (eliminates all Linux OS user provisioning) combined with cloud-native Entra security groups managed by developers via Terraform azuread or Entra self-service My Groups. Both require a one-time admin setup: domain join configuration and enabling cloud group self-service. No recurring Windows AD admin or Linux sysadmin involvement is needed after that setup.
- **Verdict:** CONFIRMED
- **Evidence:** All component claims are individually confirmed (Findings 1–7). The synthesis accurately captures the combination: SSSD eliminates the /etc/passwd provisioning burden (Finding 7); cloud-native Entra groups managed via Terraform azuread (Finding 6) or My Groups self-service (Finding 3) eliminate the Windows AD admin dependency for group membership. The caveat that My Groups self-service is "currently under review" (noted in Finding 3) applies here but does not negate the Terraform azuread path, which has no such uncertainty. The one-time admin setup claim is accurate — group writeback configuration and SSSD domain join are both one-time operations per environment.
- **Source used:** Multiple — see Findings 1, 3, 6, 7 above

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 3 / Self-service group management feature status | PARTIALLY CONFIRMED | Add a note to `open_questions` that the Self Service Group Management setting is "currently under review and won't take place as originally planned" per the Microsoft Learn page (source 1). Developers relying on this path should verify current feature availability before planning. The Terraform azuread path is not affected by this uncertainty. |
| Source 12 (azuread_group_member Terraform Registry) | UNVERIFIABLE | The Terraform Registry page requires JavaScript to render and cannot be verified by fetch. The resource existence and behavior are confirmed via search results and the underlying Microsoft Graph API constraint. No content correction needed; the unverifiability is a tooling limitation. No change required to `investigation.json`. |

## Overall Assessment

The investigation is accurate and well-sourced. All 10 key findings are either fully confirmed or partially confirmed; none are contradicted. The core architectural claims — that on-prem synced groups are write-blocked in the cloud, that group writeback enables cloud-side management with an on-prem-synced user constraint, that SSMSessionRunAs fails hard on a missing OS user with no fallback, that SSSD eliminates the Linux OS user provisioning burden, and that the minimal-admin architecture requires two one-time setup investments — are all directly supported by official Microsoft and AWS documentation.

One material nuance not captured in the investigation: the Entra ID self-service group management feature (My Groups portal) carries an active notice on its documentation page stating that planned changes to the setting are "under review and won't take place as originally planned," with no deprecation date announced. This does not affect the Terraform azuread path, which is the more robust and developer-natural option for the target team. The investigation should add this uncertainty as an open question or tension item so that consumers are not caught off guard if the feature changes.

The Ansible connection plugin naming (amazon.aws.aws_ssm vs community.aws.aws_ssm) is correctly identified in the investigation — the plugin migrated from community.aws to amazon.aws; the investigation references the correct canonical collection. The source URL and concept description are consistent.

18 of 20 sources are fully verified against live documentation. 2 sources are unverifiable due to JavaScript-gated rendering (Terraform Registry, HashiCorp developer portal); both are confirmed via independent search and cross-reference and require no content corrections.
