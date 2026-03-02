# Glossary — OS Identity Admin Surface for Developer-Run AWS EC2 Access via SSMSessionRunAs

Quick definitions of key terms and concepts referenced in this investigation.

---

## SSMSessionRunAs

An IAM tag (key: SSMSessionRunAs, value: OS username) applied to IAM users or roles. When Session Manager Run As support is enabled, it resolves the OS user from this tag and verifies existence on the node or in the domain before starting the session. Session fails hard if the user is not found — no fallback.

## onPremisesSyncEnabled

A Microsoft Graph property on Entra group objects. When true, the group was synchronized from on-premises AD via Entra Connect. Groups in this state are read-only in the cloud — Graph API, Terraform azuread, PIM for Groups, and My Groups self-service cannot modify their membership.

## Entra Group Source of Authority (SOA)

The authority that owns and can modify a group — either on-premises AD or Microsoft Entra (cloud). Groups synced from AD have on-prem SOA and are cloud read-only. SOA can be converted to cloud via the onPremisesSyncBehavior API (isCloudManaged field), enabling cloud-side management. Requires Group-OnPremisesSyncBehavior.ReadWrite.All permission.

## Entra Cloud Sync Group Writeback

A feature of the Entra provisioning agent (v1.1.3730.0+) that provisions cloud-native Entra security groups back to on-premises AD DS. Only members who were originally synchronized from on-prem AD can be included in writeback groups. Cloud-only Entra users cannot be written back. Requires Entra ID P1 license.

## Entra Self-Service Group Management (My Groups)

A tenant feature that allows group owners to manage membership and allows users to request to join groups via the My Groups portal. Only available for cloud-native Entra security groups and Microsoft 365 groups. Requires Entra ID P1. Must be enabled by a tenant admin.

## PIM for Groups

Privileged Identity Management for Groups enables just-in-time eligible membership in Entra security groups and Microsoft 365 groups. Users activate membership on-demand with optional MFA, justification, and approval. Explicitly does not support groups synchronized from on-premises AD. Requires Entra ID P2 or ID Governance license.

## Entitlement Management Access Package

An Entra ID Governance construct that bundles resources (including group memberships) into a requestable unit. Users self-request access; policies define approval steps and expiration. Delegates access package management to non-admins. Requires Entra ID Governance license.

## Terraform azuread provider

The hashicorp/azuread Terraform provider (v2+) uses the Microsoft Graph API to manage Entra objects. azuread_group and azuread_group_member resources manage cloud-native group membership as code. Requires a service principal with Group Member or Groups Administrator directory role. Cannot modify on-premises-synced groups.

## cloud-init users module

A cloud-init directive (users block in cloud-config format) that creates OS user accounts on first boot from EC2 user-data. Runs once at initial instance launch. Parameterizable via Terraform aws_launch_template. Does not apply to already-running instances.

## SSM Run Command (AWS-RunShellScript)

An AWS Systems Manager capability that executes shell commands on managed EC2 instances. Supports tag-based targeting to run commands across a fleet simultaneously. Can be used to invoke useradd across all instances matching a tag. Requires an explicit trigger (console, CLI, EventBridge, or pipeline step).

## SSSD Domain Join

System Security Services Daemon configured to join a Linux instance to an Active Directory domain. Once joined, NSS resolves AD user identities at login time — no local /etc/passwd entry required. SSMSessionRunAs accepts a domain username; SSSD satisfies the check via domain lookup. Eliminates the Linux OS user provisioning burden entirely.

## Ansible amazon.aws.aws_ssm connection plugin

An Ansible connection plugin that uses AWS Systems Manager as the transport instead of SSH. Combined with the aws_ec2 dynamic inventory plugin, it enables Ansible playbooks to target EC2 fleets by tag without key pairs. Requires an S3 bucket for module transfer. Relevant for post-launch OS configuration at fleet scale.

## AMI Baking (Packer / EC2 Image Builder)

Pre-provisioning OS users into a golden AMI using Packer (with Ansible or shell provisioners) or EC2 Image Builder (YAML component documents). Users are present from first boot with zero runtime admin action. Change requires a pipeline rebuild and AMI rotation; suited for stable, known user sets.

---

*Back to: [investigation.md](investigation.md)*
