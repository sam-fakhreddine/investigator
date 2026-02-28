# Investigation: Entra ID as an Identity Source for Linux SSSD on AWS EC2 Instances

**Date:** 2026-02-28
**Status:** Complete

---

## Integration Path Comparison

| Path | Identity Source for SSSD | POSIX UID/GID | Network Requirement | Azure Cost | AWS Cost | SSM RunAs Compatible |
| --- | --- | --- | --- | --- | --- | --- |
| Path A: Entra Domain Services + VPN + SSSD ad_provider | Entra DS managed AD (LDAP/Kerberos) | Algorithmic (SSSD SID mapping) or manual in Entra DS | AWS-Azure site-to-site VPN or Direct Connect/ExpressRoute | ~$110/mo (Standard SKU) + VPN gateway | VPN gateway (~$35/mo) | Yes -- user exists via NSS/SSSD, SSM resolves via getpwnam |
| Path B: Entra Domain Services + AWS AD Connector + SSSD ad_provider | Entra DS via AD Connector proxy | Same as Path A | AWS-Azure site-to-site VPN | ~$110/mo (Standard SKU) + VPN gateway | AD Connector (Small ~$36/mo) + VPN | Yes -- same resolution path |
| Path C: AWS Managed Microsoft AD + Entra Connect Sync + SSSD ad_provider | AWS Managed AD (native in VPC) | Algorithmic (SSSD SID mapping) or synced POSIX attrs | None cross-cloud for SSSD; Entra Connect Sync VM needed | Entra Connect Sync VM | Managed AD ($72-$288/mo) | Yes -- user exists via NSS/SSSD |
| Path D: Azure Arc + AADSSHLoginForLinux extension | Entra ID directly (OAuth/certificate-based SSH) | Dynamically created local user on first login | Outbound HTTPS from EC2 to Azure Arc endpoints | Arc is free; extension is free | None | Unclear -- Arc creates local users dynamically, SSM RunAs needs pre-existing user at session start |
| Path E: Entra ID directly (no Domain Services) | Not viable | N/A | N/A | N/A | N/A | N/A |

> Path E is not viable because base Entra ID does not expose LDAP or Kerberos endpoints. SSSD requires one of these protocols. All viable paths require either Entra Domain Services, AWS Managed AD, or the Azure Arc agent framework.

---

## Question

> Can Entra ID serve as an identity source for Linux SSSD on AWS EC2 instances, and what are the viable integration paths?

---

## Context

The environment uses Entra ID (vk2ck.onmicrosoft.com, M365 E5 dev tenant) as the identity provider, with AWS IAM Identity Center federated via SAML/SCIM. EC2 instances run Amazon Linux 2023 in ca-central-1. Currently, local Linux users are created via userdata and SSM RunAs maps per-user ABAC tags (extensionAttribute1 -> costCenter -> SSMSessionRunAs) to local OS accounts. The goal is to replace local shared role accounts with directory-sourced personal accounts, so that Linux user identity is centrally managed in Entra ID rather than provisioned ad-hoc on each instance. The Lambda broker approach and Windows (solved by native AD join) are out of scope.

---

## Key Findings

- Base Entra ID (without Domain Services) does not expose LDAP or Kerberos endpoints. SSSD requires an LDAP or Kerberos backend to function as an identity provider. Therefore, Entra ID alone cannot serve as a direct identity source for SSSD. An intermediary that provides legacy protocol endpoints is required in every viable path.
- Entra Domain Services (formerly Azure AD DS) is a managed service that provides LDAP and Kerberos endpoints backed by Entra ID user objects. It runs in an Azure VNet and synchronizes users one-way from Entra ID. Cloud-only Entra ID users must change their password at least once after Entra DS is enabled so that NTLM and Kerberos password hashes are generated and stored. This is a hard requirement -- users who have never changed their password after Entra DS deployment cannot authenticate via LDAP/Kerberos.
- Entra Domain Services starts at approximately $110/month (Standard SKU) plus Azure VPN gateway costs. The Standard SKU supports up to 25,000 objects and is sufficient for a dev/lab tenant. Enterprise ($292/mo) and Premium ($1,168/mo) SKUs exist for larger environments. Additional charges apply for the load balancer and public IP deployed alongside the managed domain.
- AWS EC2 instances can reach Entra Domain Services LDAP/Kerberos endpoints over a site-to-site VPN between the AWS VPC and the Azure VNet hosting Entra DS. Both AWS and Azure offer managed VPN gateway services that support BGP-based dynamic routing. Required ports include TCP/UDP 53 (DNS), 88 (Kerberos), 389 (LDAP), 636 (LDAPS), and 445 (SMB). Latency between AWS ca-central-1 and the nearest Azure region (Canada Central) is typically 1-5ms over VPN, which is acceptable for SSSD caching scenarios.
- AWS AD Connector is a proxy service that forwards LDAP and Kerberos requests to an existing Active Directory without caching credentials. It can point to Entra Domain Services controllers over a VPN tunnel. AWS documentation and blog posts confirm this pattern for WorkSpaces and Transfer Family. AD Connector does not support Linux domain join via SSSD directly -- EC2 Linux instances would still need SSSD configured with the AD Connector DNS IPs forwarding to Entra DS. The main value of AD Connector in this path is integration with other AWS services (WorkSpaces, FSx, etc.), not for SSSD itself.
- AWS Managed Microsoft AD provides a fully managed Active Directory in the AWS VPC, eliminating cross-cloud network dependency for SSSD. EC2 instances join the AWS Managed AD domain using realmd and SSSD with id_provider=ad. The AWS documentation for Entra Connect Sync with AWS Managed AD describes syncing users FROM AWS Managed AD TO Entra ID -- the standard hybrid identity direction where on-premises AD is the source and Entra ID is the cloud target. The reverse direction (provisioning cloud-only Entra ID users into AWS Managed AD) is not a supported Entra Connect Sync scenario. Microsoft Entra Cloud Sync (the newer, lighter-weight sync agent) supports group writeback from Entra ID to on-premises AD, but does not support user provisioning in the cloud-to-AD direction. Therefore, creating users in AWS Managed AD from cloud-only Entra ID would require a custom solution (e.g., Graph API + LDAP scripting) or a third-party identity governance tool.
- An alternative for Path C is to create users directly in AWS Managed AD (not synced from Entra) and use Entra Connect Sync to push them to Entra ID for SSO. This inverts the identity source: AWS Managed AD becomes the source of truth, and Entra ID receives synced copies. This works for the SSM RunAs use case but contradicts the goal of Entra ID as the central identity source.
- Azure Arc allows non-Azure servers (including AWS EC2) to be enrolled as Arc-enabled servers. The AADSSHLoginForLinux extension can then be deployed, enabling Entra ID-based SSH authentication using short-lived OpenSSH certificates. This does not use SSSD at all -- it uses a Microsoft-provided PAM/NSS module that creates local Linux users on first login. RBAC is managed via Azure roles (Virtual Machine Administrator Login, Virtual Machine User Login). This path avoids LDAP/Kerberos entirely but introduces a dependency on the Azure Arc agent and Azure management plane.
- The AADSSHLoginForLinux extension (used by Azure Arc) was originally Azure-only but Microsoft extended support to Arc-enabled servers. The extension requires outbound HTTPS connectivity to Azure Arc endpoints (no VPN needed). However, it creates local Linux users dynamically on first SSH login. SSM Session Manager RunAs checks for user existence at session start time using OS-level user resolution (getpwnam via NSS). If the Arc-created user does not yet exist when SSM starts the session (because the user has never SSH'd in via Arc), the SSM session will fail. This creates a chicken-and-egg problem for SSM RunAs.
- SSSD with id_provider=ad uses algorithmic SID-to-UID mapping by default (murmurhash3 of the SID). This is deterministic for a given domain SID and RID, producing consistent UIDs across all hosts joined to the same domain, provided the domain SID is pinned in sssd.conf (ldap_idmap_default_domain_sid). Without pinning, slice allocation depends on discovery order and may differ across hosts. Alternatively, POSIX attributes (uidNumber, gidNumber) can be stored in the AD and used by SSSD when ldap_id_mapping=False. Entra Domain Services now supports custom attributes on Enterprise and Premium SKUs, including onPremisesExtensionAttributes (1-15) and directory extensions defined via application registration. However, these are string-typed extension attributes, not the RFC 2307 POSIX schema attributes (uidNumber, gidNumber, loginShell, unixHomeDirectory) that SSSD expects when ldap_id_mapping=False. To use explicit POSIX UIDs with Entra DS, administrators would need to either populate the standard AD POSIX attributes directly on the managed domain controllers (if exposed) or rely on SSSD's algorithmic SID-to-UID mapping.
- SSM Session Manager resolves the RunAs user by checking whether the OS can resolve the username. The SSM agent calls the OS-level user lookup (equivalent to getpwnam). When SSSD is configured and the instance is domain-joined, NSS is configured to query SSSD (via /etc/nsswitch.conf: passwd: files sss). This means directory users are resolvable by SSM without needing local /etc/passwd entries. The SSMSessionRunAs tag value must match the username format that SSSD presents -- typically user@domain or DOMAIN\user for AD-joined systems. The format depends on SSSD configuration (use_fully_qualified_names in sssd.conf).
- For SSM RunAs to work cleanly with SSSD-resolved users, use_fully_qualified_names should be set to False in sssd.conf (or the domain should be set as default_domain_suffix) so that plain usernames (e.g., 'alice') resolve without domain suffixes. Otherwise, the SSMSessionRunAs tag would need to contain the fully qualified name (e.g., 'alice@contoso.com'), which complicates the ABAC mapping from Entra ID extensionAttribute values.
- A trust relationship between AWS Managed Microsoft AD and Entra Domain Services is technically possible if there is VPN connectivity between the AWS VPC and the Azure VNet. However, AWS documentation does not explicitly confirm compatibility, and an AWS re:Post thread notes that Entra Domain Services is not a 'fully featured' AD in the traditional sense. SSSD on Linux does not support forest trusts -- only external (non-transitive) trusts. If a trust is established, EC2 instances joined to AWS Managed AD could resolve users from the trusted Entra DS domain, but this adds complexity without clear benefit over direct domain join to either directory.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Entra Domain Services (Entra DS) | A managed Microsoft service (formerly Azure AD Domain Services) that provides LDAP, Kerberos, and NTLM authentication endpoints backed by Entra ID. Deployed into an Azure VNet as a pair of managed domain controllers. Synchronizes users one-way from Entra ID. Enterprise and Premium SKUs support custom attributes (onPremisesExtensionAttributes 1-15 and directory extensions), though these are not the same as RFC 2307 POSIX schema attributes. Requires cloud-only users to change their password at least once to generate Kerberos/NTLM hashes. |
| SSSD ad_provider | The Active Directory identity provider for SSSD (id_provider=ad in sssd.conf). Discovers AD domain controllers via DNS SRV records, authenticates via Kerberos, and retrieves user/group information via LDAP. Supports algorithmic SID-to-UID mapping or explicit POSIX attributes from AD. Configured automatically by the realmd/realm join workflow. |
| Algorithmic SID-to-UID Mapping | SSSD's default method for generating POSIX UIDs and GIDs from Active Directory SIDs. Uses murmurhash3 on the SID string to assign a deterministic UID. Consistent across hosts when the domain SID is pinned (ldap_idmap_default_domain_sid). Avoids the need to manage POSIX attributes in AD but does not support custom UID assignment. |
| Azure Arc-enabled Servers | A Microsoft service that extends Azure management capabilities to non-Azure machines (on-premises, AWS, GCP). Installs the Azure Connected Machine agent on the server. Enables deployment of Azure VM extensions (including AADSSHLoginForLinux) and management via Azure Resource Manager. Requires outbound HTTPS to Azure endpoints. |
| AADSSHLoginForLinux Extension | An Azure VM extension (publisher Microsoft.Azure.ActiveDirectory) that enables Entra ID-based SSH authentication on Linux. Uses short-lived OpenSSH certificates issued by Entra ID. Creates local Linux user accounts on first login. Works on Azure VMs natively and on non-Azure servers via Azure Arc. Does not use SSSD; uses its own PAM/NSS integration. |
| AWS AD Connector | An AWS Directory Service offering that acts as a stateless proxy, forwarding authentication and directory lookup requests to an existing Active Directory. Does not cache credentials. Requires network connectivity (VPN or Direct Connect) to the target AD domain controllers. Primarily used for AWS service integrations (WorkSpaces, SSO, FSx) rather than direct Linux SSSD enrollment. |
| NSS (Name Service Switch) | The Linux subsystem configured via /etc/nsswitch.conf that determines the order of sources for user, group, and host resolution. When SSSD is installed, the passwd and group entries are configured as 'files sss', meaning the OS first checks local files (/etc/passwd) then SSSD for user lookups. SSM Session Manager's RunAs user resolution depends on NSS to find directory users. |

---

## Tensions & Tradeoffs

- Entra ID as source of truth vs. protocol limitations: The goal is Entra ID as the central identity source, but Entra ID lacks LDAP/Kerberos. Every viable SSSD path requires an intermediary (Entra DS, AWS Managed AD, or Arc agent) that adds cost, complexity, and a synchronization lag between Entra ID and the actual identity store used by Linux hosts.
- Cross-cloud network dependency vs. operational simplicity: Paths using Entra Domain Services (A and B) require persistent VPN connectivity between AWS and Azure, introducing a network dependency that affects SSSD authentication if the tunnel drops. Path C (AWS Managed AD) keeps the directory in-VPC but loses Entra ID as the source of truth unless a sync mechanism is built.
- Azure Arc path elegance vs. SSM RunAs compatibility: Path D (Azure Arc + AADSSHLoginForLinux) is the only path that uses Entra ID directly without a managed AD intermediary, but it creates local users only on first SSH login. SSM RunAs requires the user to already exist at session start time, creating a sequencing problem. A pre-provisioning step would be needed, negating much of the simplicity.
- UID consistency across hosts: Algorithmic SID-to-UID mapping is deterministic when domain SID is pinned, but any misconfiguration results in different UIDs on different hosts, breaking NFS, shared storage, and audit trail correlation. Explicit POSIX attributes in AD are more reliable. Entra DS Enterprise/Premium SKUs now support custom attributes (onPremisesExtensionAttributes and directory extensions), but these are string-typed extensions, not the RFC 2307 POSIX attributes (uidNumber, gidNumber) that SSSD natively consumes with ldap_id_mapping=False.
- Entra Connect Sync direction: Both Entra Connect Sync and the newer Entra Cloud Sync are designed to push users from on-premises/AWS AD to Entra ID, not the reverse. Entra Cloud Sync supports group writeback to on-premises AD but not user provisioning in the cloud-to-AD direction. Using AWS Managed AD with Entra Connect Sync inverts the identity authority, making AWS Managed AD the source of truth rather than Entra ID. This contradicts the stated goal but is the most operationally straightforward path for SSSD on EC2.

---

## Open Questions

- Can Entra Domain Services expose RFC 2307 POSIX attributes (uidNumber, gidNumber, loginShell, unixHomeDirectory) through its LDAP interface for SSSD to use with ldap_id_mapping=False? Enterprise/Premium SKUs now support custom attributes (onPremisesExtensionAttributes and directory extensions), but these are string-typed extensions, not the standard AD POSIX schema classes. It remains unclear whether the managed domain controllers expose the Unix Attributes tab or equivalent POSIX fields that SSSD expects.
- Does the Azure Arc AADSSHLoginForLinux extension create local Linux users with predictable usernames (e.g., matching the Entra UPN prefix), and can these users be pre-provisioned via userdata or a bootstrap script to solve the SSM RunAs sequencing problem?
- What is the observed SSSD cache behavior when the AWS-to-Azure VPN tunnel drops? If the tunnel is down for minutes, do cached credentials allow existing sessions to continue and new sessions to start for recently-seen users?
- For the AWS Managed AD path (Path C), is there a viable way to sync users from cloud-only Entra ID into AWS Managed AD without running a custom sync agent? Entra Connect Sync does not natively support this direction.
- Has AWS or Microsoft published guidance on Entra Domain Services compatibility with AWS Managed Microsoft AD trust relationships? The AWS re:Post thread is inconclusive.
- What is the latency and reliability impact of SSSD Kerberos ticket acquisition over a cross-cloud VPN tunnel under typical AWS ca-central-1 to Azure Canada Central conditions?

---

## Sources & References

- [Sign in to a Linux virtual machine in Azure by using Microsoft Entra ID and OpenSSH - Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/devices/howto-vm-sign-in-azure-ad-linux)
- [How synchronization works in Microsoft Entra Domain Services - Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/domain-services/synchronization)
- [Enable password hash sync for Microsoft Entra Domain Services - Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/domain-services/tutorial-configure-password-hash-sync)
- [Tutorial - Configure LDAPS for Microsoft Entra Domain Services - Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/domain-services/tutorial-configure-ldaps)
- [SSH access to Azure Arc-enabled servers - Microsoft Learn](https://learn.microsoft.com/en-us/azure/azure-arc/servers/ssh-arc-overview)
- [Manually joining an Amazon EC2 Linux instance to your AWS Managed Microsoft AD Active Directory - AWS Directory Service](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/join_linux_instance.html)
- [Connecting your AWS Managed Microsoft AD to Microsoft Entra Connect Sync - AWS Directory Service](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_connect_ms_entra_sync.html)
- [AD Connector - AWS Directory Service](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html)
- [Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Integrating RHEL systems directly with Windows Active Directory - Red Hat Enterprise Linux 10](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/integrating_rhel_systems_directly_with_windows_active_directory/index)
- [SSSD AD Provider - sssd.io](https://sssd.io/docs/ad/ad-provider.html)
- [Microsoft Entra Domain Services Pricing](https://www.microsoft.com/en-us/security/pricing/microsoft-entra-ds)
- [Designing private network connectivity between AWS and Microsoft Azure - AWS Blog](https://aws.amazon.com/blogs/modernizing-with-aws/designing-private-network-connectivity-aws-azure/)
- [Is AWS Managed Microsoft AD (Hybrid Edition) compatible with Microsoft Entra ID Domain Services? - AWS re:Post](https://repost.aws/questions/QUgueJm6EuQvuw4YrEpgs7Pg/is-aws-managed-microsoft-ad-hybrid-edition-compatible-with-microsoft-entra-id-domain-services)
- [Add your WorkSpaces to Microsoft Entra ID using Microsoft Entra Domain Services - AWS Desktop Blog](https://aws.amazon.com/blogs/desktop-and-application-streaming/add-your-workspaces-to-azure-ad-using-azure-active-directory-domain-services/)
- [Linux Azure AD authentication options - Puppeteers](https://www.puppeteers.net/blog/linux-azure-ad-authentication-options/)
- [Using AWS Directory Service for Entra ID Domain Services - AWS Transfer Family](https://docs.aws.amazon.com/transfer/latest/userguide/azure-sftp.html)
- [Create and manage custom attributes for Microsoft Entra Domain Services - Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/domain-services/concepts-custom-attributes)
- [Provisioning Microsoft Entra ID to Active Directory using Microsoft Entra Cloud Sync - Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-configure-entra-to-active-directory)
