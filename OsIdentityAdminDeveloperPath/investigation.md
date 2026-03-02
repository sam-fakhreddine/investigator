# Investigation: OS Identity Admin Surface for Developer-Run AWS EC2 Access via SSMSessionRunAs

**Date:** 2026-03-02
**Status:** Complete

---

## Administration Surface Summary

| Dimension | Pattern | Admin Surface Eliminated? | Residual Burden | Best Automation Path |
| --- | --- | --- | --- | --- |
| AD group management | Synced on-prem groups (Entra Connect) | No — write-blocked in cloud | Windows AD admin must manage membership on-prem | None; developers cannot self-service synced groups via Graph API or Terraform azuread |
| AD group management | Cloud-native Entra groups + group writeback via Cloud Sync | Partial — developers can manage cloud groups, writeback carries members to AD | Members must be on-prem-synced users; cloud-only users cannot write back. Requires Entra ID P1 + writeback provisioning agent setup (one-time admin task) | Terraform azuread_group_member resource; Graph API; Entra self-service My Groups portal (P1 required) |
| AD group management | Cloud-native Entra groups with PIM for Groups (just-in-time) | Partial — developers self-activate eligible membership | Group itself must be cloud-native (PIM does not support synced groups); requires Entra ID P2 / ID Governance license; initial PIM policy setup by admin | PIM for Groups eligible assignment; developers activate membership in My Apps / My Groups with optional MFA + justification |
| AD group management | Entitlement Management access packages | Partial — developers request access via access package portal | Access package creation and policy setup is an admin or delegated access package manager task; requires Entra ID Governance license | Entitlement management access package with group membership resource; approval workflows configurable |
| Linux OS user provisioning | Local user in /etc/passwd baked into AMI (Packer or EC2 Image Builder) | Yes at runtime — user exists from instance launch; no per-fleet admin action needed | AMI rebuild required when user set changes; build pipeline maintenance | Packer + Ansible provisioner or EC2 Image Builder component YAML; users baked into golden AMI |
| Linux OS user provisioning | Local user created at launch via cloud-init user-data | Yes at runtime for new instances; gaps on existing fleet | Every existing instance not rebuilt needs a separate remediation pass; user-data runs once at first boot only | cloud-init cloud-config users module; parameterize at launch via Terraform aws_launch_template user_data |
| Linux OS user provisioning | Local user pushed post-launch via Run Command | No — requires an explicit execution step | Run Command must be triggered manually or via automation (EventBridge, Lambda, pipeline step) on each new instance | aws ssm send-command targeting by tag; AWS-RunShellScript document with useradd shell command |
| Linux OS user provisioning | SSSD domain join — user resolved from AD at session time | Yes completely — no local /etc/passwd entry required | Domain join itself is a one-time per-image or per-instance operation (already investigated in SssdEntraLinuxEntitlements); AD user account must exist in AD | SSSD is a complete elimination of the Linux OS user provisioning burden when domain join is in place |

> The lowest-administration path for developer teams is SSSD domain join (eliminates Linux user provisioning) combined with cloud-native Entra security groups managed via Terraform azuread or Entra self-service (avoids Windows AD admin for group membership). Both enablers require one-time admin setup but no recurring sysadmin involvement.

---

## Question

> In a hybrid Entra ID + on-prem Active Directory environment using SSM Session Manager SSMSessionRunAs on EC2 Linux, what is the minimum administration surface required for (a) AD group management and (b) Linux OS user provisioning, is any of it architecturally eliminable, and what developer-friendly automation patterns are documented for what cannot be eliminated?

---

## Context

The team are software developers doing AWS work, allergic to traditional sysadmin and IAM administration. The environment is hybrid: on-prem Windows Active Directory synced to Microsoft Entra ID via Entra Connect. SSMSessionRunAs resolves a named Linux OS user; that user must exist on the instance or in the domain at session start. Two patterns exist: local OS users in /etc/passwd, or SSSD domain-joined instances where identity resolves from AD. Group membership in AD controls IdC permission set assignment, which gates who can start sessions. The investigation covers: whether AD group management can be self-serviced by developers without engaging a Windows AD admin; whether Linux OS user provisioning can be eliminated or automated without a Linux sysadmin; and whether combining SSSD + Entra self-service removes both burdens simultaneously.

---

## Key Findings

- On-premises AD groups synced via Entra Connect are write-blocked in the cloud: the Microsoft Graph API, Terraform azuread_group_member, PIM for Groups, and My Groups self-service all fail or are unavailable for groups with onPremisesSyncEnabled=true. Membership for these groups can only be modified via on-prem AD tooling, requiring a Windows AD admin.
- Entra Cloud Sync group writeback (provisioning agent v1.1.3730.0+) enables cloud-native Entra security groups to be provisioned back to on-prem AD, making cloud-side tools (Graph API, Terraform azuread, self-service) viable for group membership management. The hard constraint is that only users originally synchronized from on-prem AD can be group members in writeback groups — cloud-only Entra users cannot be written back.
- Entra ID self-service group management (My Groups portal) allows owners to approve membership requests for cloud-native security groups, but requires Entra ID P1 license and must be explicitly enabled by a tenant admin. It does not function for on-premises-synced groups. As of early 2026, the Microsoft Learn documentation for this feature carries an active notice that the Self Service Group Management setting is currently under review and may not proceed as originally planned — teams relying on this portal should verify current availability before building a workflow around it.
- PIM for Groups provides just-in-time eligible membership for cloud-native Entra security groups and Microsoft 365 groups, but explicitly excludes groups synchronized from on-premises. Requires Entra ID P2 or ID Governance license.
- Entra ID Entitlement Management access packages can bundle group membership as a requestable resource with approval workflows, enabling developer self-service access to cloud-native group membership. Requires Entra ID Governance license. No documented support for on-prem-synced groups.
- The Terraform hashicorp/azuread provider (v2+, Microsoft Graph-backed) manages cloud-native Entra group membership via azuread_group and azuread_group_member resources. This enables IaC-driven group management with PR-based review as the approval gate, requiring only a service principal with Group Member or Groups Administrator rights. It does not function against on-prem-synced groups.
- SSMSessionRunAs verifies the named OS user exists on the node or in the domain before starting the session; if not found, the session fails with no fallback to ssm-user. SSSD domain-joined instances resolve domain users through NSS at login time — the named AD user account satisfies the check without any local /etc/passwd entry, fully eliminating the Linux OS user provisioning burden.
- For non-domain-joined instances using local OS users, three provisioning patterns exist: AMI baking (Packer/EC2 Image Builder) which is zero-touch at runtime but requires a pipeline rebuild cycle; cloud-init user-data which runs once at first boot via Terraform aws_launch_template; and SSM Run Command (AWS-RunShellScript) which can target a fleet by tag but requires an explicit trigger step.
- Ansible with the amazon.aws.aws_ssm connection plugin and aws_ec2 dynamic inventory can manage OS users across a fleet of EC2 instances without SSH keys, using SSM as the transport layer. This is developer-friendly for teams already using Terraform/AWS tooling, but introduces Ansible as a dependency and requires an S3 bucket for module file transfer.
- The minimal-admin architecture is SSSD domain join (eliminates all Linux OS user provisioning) combined with cloud-native Entra security groups managed by developers via Terraform azuread or Entra self-service My Groups. Both require a one-time admin setup: domain join configuration and enabling cloud group self-service. No recurring Windows AD admin or Linux sysadmin involvement is needed after that setup.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SSMSessionRunAs | An IAM tag (key: SSMSessionRunAs, value: OS username) applied to IAM users or roles. When Session Manager Run As support is enabled, it resolves the OS user from this tag and verifies existence on the node or in the domain before starting the session. Session fails hard if the user is not found — no fallback. |
| onPremisesSyncEnabled | A Microsoft Graph property on Entra group objects. When true, the group was synchronized from on-premises AD via Entra Connect. Groups in this state are read-only in the cloud — Graph API, Terraform azuread, PIM for Groups, and My Groups self-service cannot modify their membership. |
| Entra Group Source of Authority (SOA) | The authority that owns and can modify a group — either on-premises AD or Microsoft Entra (cloud). Groups synced from AD have on-prem SOA and are cloud read-only. SOA can be converted to cloud via the onPremisesSyncBehavior API (isCloudManaged field), enabling cloud-side management. Requires Group-OnPremisesSyncBehavior.ReadWrite.All permission. |
| Entra Cloud Sync Group Writeback | A feature of the Entra provisioning agent (v1.1.3730.0+) that provisions cloud-native Entra security groups back to on-premises AD DS. Only members who were originally synchronized from on-prem AD can be included in writeback groups. Cloud-only Entra users cannot be written back. Requires Entra ID P1 license. |
| Entra Self-Service Group Management (My Groups) | A tenant feature that allows group owners to manage membership and allows users to request to join groups via the My Groups portal. Only available for cloud-native Entra security groups and Microsoft 365 groups. Requires Entra ID P1. Must be enabled by a tenant admin. |
| PIM for Groups | Privileged Identity Management for Groups enables just-in-time eligible membership in Entra security groups and Microsoft 365 groups. Users activate membership on-demand with optional MFA, justification, and approval. Explicitly does not support groups synchronized from on-premises AD. Requires Entra ID P2 or ID Governance license. |
| Entitlement Management Access Package | An Entra ID Governance construct that bundles resources (including group memberships) into a requestable unit. Users self-request access; policies define approval steps and expiration. Delegates access package management to non-admins. Requires Entra ID Governance license. |
| Terraform azuread provider | The hashicorp/azuread Terraform provider (v2+) uses the Microsoft Graph API to manage Entra objects. azuread_group and azuread_group_member resources manage cloud-native group membership as code. Requires a service principal with Group Member or Groups Administrator directory role. Cannot modify on-premises-synced groups. |
| cloud-init users module | A cloud-init directive (users block in cloud-config format) that creates OS user accounts on first boot from EC2 user-data. Runs once at initial instance launch. Parameterizable via Terraform aws_launch_template. Does not apply to already-running instances. |
| SSM Run Command (AWS-RunShellScript) | An AWS Systems Manager capability that executes shell commands on managed EC2 instances. Supports tag-based targeting to run commands across a fleet simultaneously. Can be used to invoke useradd across all instances matching a tag. Requires an explicit trigger (console, CLI, EventBridge, or pipeline step). |
| SSSD Domain Join | System Security Services Daemon configured to join a Linux instance to an Active Directory domain. Once joined, NSS resolves AD user identities at login time — no local /etc/passwd entry required. SSMSessionRunAs accepts a domain username; SSSD satisfies the check via domain lookup. Eliminates the Linux OS user provisioning burden entirely. |
| Ansible amazon.aws.aws_ssm connection plugin | An Ansible connection plugin that uses AWS Systems Manager as the transport instead of SSH. Combined with the aws_ec2 dynamic inventory plugin, it enables Ansible playbooks to target EC2 fleets by tag without key pairs. Requires an S3 bucket for module transfer. Relevant for post-launch OS configuration at fleet scale. |
| AMI Baking (Packer / EC2 Image Builder) | Pre-provisioning OS users into a golden AMI using Packer (with Ansible or shell provisioners) or EC2 Image Builder (YAML component documents). Users are present from first boot with zero runtime admin action. Change requires a pipeline rebuild and AMI rotation; suited for stable, known user sets. |

---

## Tensions & Tradeoffs

- The lowest-overhead runtime pattern for Linux users (SSSD domain join) requires domain join infrastructure — either AWS Managed Microsoft AD or a network path to on-prem DC — which is itself an architecture dependency. Teams that avoid this dependency must accept ongoing OS user provisioning work.
- Entra Cloud Sync group writeback enables cloud-managed groups to appear in on-prem AD, but only for members synchronized from on-prem. Cloud-only Entra users (e.g., contractors or external identities not in on-prem AD) cannot be members of writeback groups, creating a class of users that still require on-prem AD admin involvement.
- Self-service group management via My Groups or PIM for Groups requires Entra ID P1 or P2 licenses respectively. Teams on Entra ID Free or Microsoft 365 plans without upgrade cannot use these patterns and must fall back to admin-mediated group changes.
- AMI baking produces zero-touch runtime behavior but creates a coupling between the user set and the AMI version. Adding a developer to the RunAs user set requires an AMI rebuild and a rolling replacement of running instances — a higher operational cost than a fleet-wide Run Command execution.
- Terraform azuread as the group management mechanism requires the service principal's credentials to be stored securely and rotated. It also means group membership changes flow through a PR and CI pipeline, which is developer-friendly for audit but slower than portal-based approval for urgent access needs.
- PIM for Groups and Entitlement Management both provide self-service but target different governance models: PIM is time-bounded just-in-time access; Entitlement Management supports persistent assignments with lifecycle review. Mixing both adds complexity to the access model for a developer team.
- SSM Run Command targeting by tag addresses fleet-wide user provisioning but introduces an explicit trigger dependency. Without automation (EventBridge new-instance event or a launch lifecycle hook), newly launched instances from Auto Scaling Groups may be missing the OS user until the command is re-run.

---

## Open Questions

- Can the Entra Cloud Sync group writeback path support a scenario where all developers are on-prem-synced AD users (not cloud-only), making writeback membership constraints irrelevant? This depends on whether the team's Entra user accounts originate from on-prem AD sync or are cloud-only — not investigated here.
- The Microsoft Learn documentation for Entra ID self-service group management (My Groups) carries an active notice that the Self Service Group Management setting is under review and may not proceed as planned. Is this feature still available to new tenants, and if it is deprecated, what is the supported replacement for owner-managed group membership requests without PIM or Entitlement Management licenses?
- Is there a documented pattern for using EventBridge EC2 instance state-change events to trigger SSM Run Command user provisioning automatically on new instances, removing the manual trigger requirement?
- Does converting on-prem group SOA to cloud (isCloudManaged) break existing IdC permission set assignments that relied on that group's membership, or does IdC continue to resolve the same group by object ID?
- What is the Entra ID Governance licensing cost relative to the operational cost of keeping a Windows AD admin engaged for group management? The investigation does not assess organizational licensing posture.
- For SSSD domain join against on-prem AD from EC2 in a private subnet, what network path (Direct Connect, VPN, or AWS Managed Microsoft AD) is required? This is a prerequisite architecture question not covered here (see SssdEntraLinuxEntitlements for domain join mechanics).
- Does the Terraform azuread provider support writing group membership to groups whose SOA has been converted to cloud (formerly synced, now cloud-managed) or only to groups that were always cloud-native?

---

## Sources & References

- [Set up self-service group management - Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/users/groups-self-service-management)
- [Set up self-service group management after Group SOA conversion - Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-source-of-authority-self-service-group-management)
- [PIM for Groups - Microsoft Entra ID Governance](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups)
- [What is entitlement management - Microsoft Entra ID Governance](https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-overview)
- [Group writeback with Microsoft Entra Cloud Sync](https://learn.microsoft.com/en-us/entra/identity/hybrid/group-writeback-cloud-sync)
- [Manage Groups in Microsoft Graph v1.0](https://learn.microsoft.com/en-us/graph/api/resources/groups-overview?view=graph-rest-1.0)
- [Configure Group Source of Authority (SOA) in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure)
- [Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [AWS Systems Manager Run Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html)
- [Managing OS user accounts and groups on managed nodes using Fleet Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-manage-os-user-accounts.html)
- [Run commands when you launch an EC2 instance with user data - Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
- [azuread_group_member resource - Terraform Registry hashicorp/azuread](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group_member)
- [Manage Microsoft Entra ID users and groups - Terraform tutorial](https://developer.hashicorp.com/terraform/tutorials/it-saas/entra-id)
- [Ansible amazon.aws.aws_ssm connection plugin - Ansible Community Documentation](https://docs.ansible.com/projects/ansible/latest/collections/amazon/aws/aws_ssm_connection.html)
- [Configure AWS IAM Identity Center ABAC for EC2 and Session Manager - AWS Security Blog](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [Govern on-premises AD application access with groups from the cloud - Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/govern-on-premises-groups)
- [Can't manage or remove objects synchronized through Azure AD Sync - Microsoft Troubleshoot](https://learn.microsoft.com/en-us/troubleshoot/entra/entra-id/user-prov-sync/cannot-manage-objects)
- [Automate building Golden AMIs with Packer, Ansible and CodeBuild - InfraCloud](https://www.infracloud.io/blogs/automate-building-golden-ami/)
- [Assign eligibility for a group in Privileged Identity Management - Microsoft Entra ID Governance](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/groups-assign-member-owner)
- [Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html)
