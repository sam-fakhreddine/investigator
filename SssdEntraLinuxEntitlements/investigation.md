# Investigation: SSSD with Entra ID for Per-User Linux Identity and Group-Based Entitlements on AWS EC2

**Date:** 2026-02-28
**Status:** Complete

---

## Integration Path Comparison: Feasibility, Key Requirement, and Group Entitlement Support

| Path | Feasibility | Key Requirement | Group Entitlement Support |
| --- | --- | --- | --- |
| A: Entra Domain Services + VPN + SSSD | High | AWS-Azure site-to-site VPN (~$145+/mo combined) | Full -- Entra groups sync to Entra DS; SSSD resolves as Linux groups; sudoers and file DAC work natively |
| B: Entra DS + AWS AD Connector + SSSD | Medium | VPN + AD Connector ($36/mo) -- AD Connector adds AWS service integration but no direct SSSD benefit | Same as Path A -- AD Connector is a pass-through proxy |
| C: AWS Managed AD + Entra Connect Sync + SSSD | High (with caveat) | Custom sync agent for Entra-to-AD user provisioning; Entra Connect Sync only pushes AD-to-Entra | Full -- groups created in AWS Managed AD are SSSD-native; but Entra ID is no longer the identity source of truth |
| D: Azure Arc + AADSSHLoginForLinux | Low for SSM RunAs | Arc agent on every EC2 instance; user must SSH in via Arc before SSM RunAs can resolve the username | Limited -- Arc creates local users on first login; no native group-to-Linux mapping; would require separate entitlement mechanism |
| E: Entra ID directly (no intermediary) | Not viable | Entra ID lacks LDAP and Kerberos endpoints | None -- SSSD cannot connect |

> Paths A and C are the two viable candidates. Path A preserves Entra ID as identity source but requires cross-cloud VPN. Path C is operationally simpler but makes AWS Managed AD the identity source. Path D has an unresolved SSM RunAs sequencing problem. Path E is architecturally impossible.

---

## Question

> Is SSSD/realmd domain join with Entra ID a feasible replacement for shared role-based Linux accounts in the SSMRunAs pipeline, using per-user identities with group-based entitlements instead of per-role RunAs mapping?

---

## Context

The current SSMRunAs pipeline maps Entra ID extension attributes through ABAC tags to shared local Linux accounts (admin, developer, oracle). This model prevents individual accountability in audit logs, creates blast radius risk when shared credentials are compromised, and requires custom Lambda provisioning of local OS users on every instance. SSSD/realmd domain join offers an alternative: each person gets a personal Linux username resolved from a directory service, with permissions derived from Entra ID group memberships (sudo, file access, login restriction) rather than per-role shared accounts. However, Entra ID alone lacks LDAP/Kerberos, so every viable path requires an intermediary directory service, each with distinct cost, network, and identity-authority trade-offs.

---

## Key Findings

- SSSD/realmd domain join is a feasible replacement for shared role-based Linux accounts, but requires a managed Active Directory intermediary between Entra ID and Linux. Base Entra ID does not expose LDAP or Kerberos, which SSSD requires. Every viable path uses either Entra Domain Services (Azure-hosted) or AWS Managed Microsoft AD (VPC-hosted).
- Two paths are practical for production: Path A (Entra Domain Services + cross-cloud VPN) preserves Entra ID as the central identity source at ~$145+/month combined Azure/AWS cost. Path C (AWS Managed Microsoft AD) eliminates cross-cloud network dependency at $72-288/month but inverts identity authority away from Entra ID.
- Group-based entitlements work end-to-end through SSSD. AD security groups are resolved as native Linux groups via NSS. A user in multiple AD groups (e.g., linux-admins and linux-dbops) receives all corresponding Linux entitlements simultaneously -- sudo access, file DAC permissions, and login restrictions -- with no per-user host-level configuration.
- SSM Session Manager RunAs is compatible with SSSD-resolved users without any SSM-specific changes. The SSM agent resolves the RunAs username via the OS id command, which queries NSS/SSSD. Directory users are visible to SSM as if they were local /etc/passwd entries. The SSMSessionRunAs ABAC tag maps to the personal username instead of a shared role account.
- Audit trail improves from shared-account attribution to individual accountability. CloudTrail records the federated IAM principal, SSM session logs capture commands under the personal OS username, and Linux audit logs attribute all activity to the individual UID. This closes the current gap where multiple people operate under the same shared account.
- Entra Domain Services synchronizes users one-way from Entra ID, but cloud-only users must change their password at least once after Entra DS is enabled to generate Kerberos/NTLM hashes. This is a hard prerequisite -- users who skip this step cannot authenticate via LDAP/Kerberos.
- GID assignment has two modes with different trade-offs. Algorithmic SID-to-GID mapping (SSSD default) is zero-configuration and cross-host consistent when the domain SID is pinned. Explicit POSIX attributes (gidNumber in AD) allow specific GID values but require AD schema management. Environments with existing file ownership tied to specific GIDs must use explicit attributes or re-chown files.
- Sudoers integration supports file-based rules (%groupname patterns in /etc/sudoers.d/) or centralized AD-stored sudoRole LDAP objects. File-based rules are simpler and deployable via SSM RunCommand; AD-stored rules are centrally managed but require schema extension. Most AWS environments prefer the file-based approach.
- SSSD caches credentials and group memberships locally with a default 90-minute TTL (entry_cache_timeout=5400). Offline authentication works for previously-seen users. This means brief directory outages do not break active sessions, but also means revoked group memberships persist locally for up to 90 minutes -- a security consideration for emergency access revocation.
- The Azure Arc path (Path D) avoids managed AD entirely but has an unresolved SSM RunAs sequencing problem: Arc creates local Linux users only on first SSH login, while SSM RunAs needs the user to exist at session start time. Pre-provisioning users would negate the simplicity of the Arc approach.
- SSSD resolves nested AD group memberships up to a configurable depth (default ldap_group_nesting_level=2). This enables flexible entitlement hierarchies (e.g., all-database-team containing dbops and dba-leads), but deep nesting degrades LDAP query performance. Red Hat recommends keeping nesting shallow.
- For SSM RunAs compatibility, SSSD should be configured with use_fully_qualified_names=false so that plain usernames (e.g., alice) resolve without domain suffixes. Otherwise, the SSMSessionRunAs tag would need fully qualified names (alice@contoso.com), complicating the ABAC mapping from Entra ID extension attributes.
- The reverse sync direction (Entra ID to AWS Managed AD) is not natively supported. Entra Connect Sync pushes from AD to Entra ID only. Entra Cloud Sync supports group writeback but not user provisioning cloud-to-AD. Path C therefore either requires a custom sync agent or accepts AWS Managed AD as the identity source of truth.
- AD group names with spaces cause issues in sudoers files and Linux tooling. SSSD's override_space option can replace spaces with underscores, but has a documented limitation (SSSD issue #5441) where groups containing the override character in their original name fail lookup. Best practice is to create AD groups without spaces from the start.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SSSD (System Security Services Daemon) | Linux daemon that provides access to identity and authentication providers (AD, LDAP, Kerberos). Acts as a caching proxy between NSS/PAM and the directory, resolving users, groups, and sudo rules. Configured via sssd.conf with id_provider=ad for Active Directory integration. |
| Entra Domain Services (Entra DS) | A managed Microsoft service (formerly Azure AD Domain Services) that provides LDAP, Kerberos, and NTLM authentication endpoints backed by Entra ID. Deployed into an Azure VNet as managed domain controllers. Synchronizes users one-way from Entra ID. Starts at approximately $110/month (Standard SKU). Cloud-only users must change their password once to generate Kerberos/NTLM hashes. |
| NSS (Name Service Switch) | Linux mechanism configured in /etc/nsswitch.conf that determines how system databases (passwd, group) are resolved. Adding 'sss' as a source routes lookups through SSSD, making directory users visible to all OS-level identity queries including SSM RunAs. |
| Algorithmic SID-to-UID/GID Mapping | SSSD's default method (ldap_id_mapping=true) for generating POSIX UIDs and GIDs from Active Directory SIDs using murmurhash3. Deterministic and consistent across all joined hosts when the domain SID is pinned in sssd.conf. Avoids the need for POSIX attributes in AD. |
| realmd | Linux service that discovers and joins identity domains. Automates Kerberos keytab creation, sssd.conf generation, and nsswitch/PAM configuration when joining an AD domain via the 'realm join' command. |
| AADSSHLoginForLinux Extension | Azure VM extension that enables Entra ID-based SSH authentication using short-lived OpenSSH certificates. Creates local Linux users on first login. Works on non-Azure servers via Azure Arc. Does not use SSSD; uses its own PAM/NSS integration. |
| simple_allow_groups | SSSD access control option that restricts which AD groups can log into a specific host. Provides per-host login restriction based on directory group membership, evaluated after authentication with full nested group resolution. |
| ad_gpo_access_control | SSSD option that enforces Windows Group Policy Object (GPO) Allow Log On Locally rights on Linux hosts. Provides centralized login restriction management from AD without per-host sssd.conf changes. |
| sudoRole LDAP Object | AD schema extension for storing sudo rules centrally in LDAP. SSSD's sudo provider fetches these rules with smart refresh, avoiding the need to distribute sudoers files to each host. Alternative to file-based /etc/sudoers.d/ deployment. |
| AWS Managed Microsoft AD | AWS Directory Service offering that provides a fully managed Active Directory in the AWS VPC. Supports SSSD domain join for EC2 Linux instances without cross-cloud network dependency. Can sync users to Entra ID via Entra Connect Sync (AD-to-Entra direction only). |
| AWS AD Connector | AWS Directory Service proxy that forwards LDAP and Kerberos requests to an existing Active Directory without caching. Requires VPN to the target AD. Primarily useful for AWS service integrations (WorkSpaces, FSx), not for direct SSSD enrollment. |

---

## Tensions & Tradeoffs

- Entra ID as identity source vs protocol limitations: The goal is Entra ID as the single identity authority, but it lacks LDAP/Kerberos. Every SSSD path requires an intermediary directory service that adds cost ($110-288/month), synchronization lag, and operational complexity. The fundamental tension is that Linux identity protocols and modern cloud identity providers have incompatible designs.
- Cross-cloud VPN dependency vs operational simplicity: Path A (Entra DS) preserves Entra ID as identity source but requires persistent AWS-Azure VPN connectivity for SSSD authentication. Path C (AWS Managed AD) eliminates network dependency but splits identity authority. There is no path that achieves both goals simultaneously.
- Individual accountability vs access revocation speed: Personal usernames with SSSD provide full audit trail, but SSSD's 90-minute cache means revoked group memberships (including sudo) persist locally after removal in the directory. Emergency revocation requires force-clearing SSSD caches on target hosts, adding operational procedure overhead.
- Algorithmic ID mapping vs existing file ownership: SSSD's default SID-to-GID mapping requires no AD configuration but produces arbitrary GID values. Environments with file systems owned by specific GIDs (e.g., oracle data GID 1001) must either set explicit POSIX attributes in AD or re-chown all existing files -- both are significant migration efforts.
- Azure Arc elegance vs SSM RunAs compatibility: Path D uses Entra ID directly without managed AD, but creates local users only on first SSH login. SSM RunAs needs the user to exist before session start. Pre-provisioning users defeats the purpose of the dynamic approach.
- Local sudoers files vs centralized AD sudo rules: File-based sudoers (/etc/sudoers.d/) are simple but create config drift risk across the fleet. AD-stored sudoRole objects are centrally managed but require schema extension and more complex SSSD configuration. The choice determines whether sudo governance is managed in AD or via configuration management tooling.
- Fully qualified names vs short names: SSSD defaults to user@domain format which prevents cross-domain collisions but complicates SSMSessionRunAs ABAC tag values, sudoers patterns, and file ownership displays. Short names are cleaner but risk collisions in multi-domain environments.
- Entra Connect Sync direction: The sync tooling (both Entra Connect Sync and Cloud Sync) is designed to push users from AD to Entra ID, not the reverse. Using AWS Managed AD (Path C) with Entra Connect Sync inverts identity authority, making AWS AD the source of truth. This is operationally straightforward but contradicts the goal of Entra ID as the central identity source.

---

## Open Questions

- What is the production cost comparison between Path A (Entra DS + VPN + Azure networking) and Path C (AWS Managed AD + optional Entra Connect Sync VM) when accounting for all infrastructure components, and does the cost differential justify the identity-authority trade-off?
- Can Entra Domain Services expose RFC 2307 POSIX attributes (uidNumber, gidNumber) through its LDAP interface for SSSD, or are environments forced to use algorithmic SID-to-UID mapping? Enterprise/Premium SKUs support custom attributes, but these are string-typed extensions, not standard AD POSIX schema fields.
- For Path C (AWS Managed AD), is there a viable automated mechanism to provision cloud-only Entra ID users into AWS Managed AD without building a custom sync agent (e.g., Graph API polling + LDAP writes)?
- What is the observed SSSD cache behavior when the AWS-to-Azure VPN tunnel drops under Path A? Do cached credentials allow new sessions for recently-seen users, and what is the failure mode for never-before-seen users?
- Does Amazon Linux 2023 ship with a sufficiently recent SSSD version to support all referenced features (ad_gpo_access_control, override_space, nested group resolution, sudo provider)?
- How will sudoers files and SSSD configuration be deployed and lifecycle-managed across the EC2 fleet? SSM RunCommand, Ansible, or AMI baking are all viable, but the fleet management approach must be decided before scaling beyond the proof of concept.
- Is the 90-minute SSSD cache delay for group membership revocation acceptable for security-sensitive entitlements like sudo, or does the environment require a forced-cache-clear mechanism for emergency access revocation?
- Does the Azure Arc AADSSHLoginForLinux extension create local users with predictable usernames matching the Entra UPN prefix, and can these be pre-provisioned to solve the SSM RunAs sequencing problem?

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
- [RHEL 8 - Connecting RHEL systems directly to AD using SSSD](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/integrating_rhel_systems_directly_with_windows_active_directory/connecting-rhel-systems-directly-to-ad-using-sssd_integrating-rhel-systems-directly-with-active-directory)
- [sssd-ad(5) Linux man page - SSSD Active Directory provider](https://linux.die.net/man/5/sssd-ad)
- [RHEL 7 - Group Policy Object Access Control with SSSD](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-gpo)
- [sssd-simple(5) - Simple access control provider man page](https://linux.die.net/man/5/sssd-simple)
- [RHEL 6 - SSSD Domain Options: Enabling Offline Authentication](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache-cred)
- [AWS SSM - Logging session activity](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-auditing.html)
- [Anatomy of SSSD user lookup - jhrozek](https://jhrozek.wordpress.com/2015/03/11/anatomy-of-sssd-user-lookup/)
- [amazon-ssm-agent shell_unix.go - RunAs user lookup source code](https://github.com/aws/amazon-ssm-agent/blob/b9654b268afcb7e70a9cc6c6d9b7d2a676f5b468/agent/session/plugins/shell/shell_unix.go)
- [SUDO administration with AD - haxor.no](https://haxor.no/en/article/sudo-with-ad)
- [Managing SUDO from Active Directory - Michael Waterman](https://michaelwaterman.nl/2022/10/21/managing-sudo-from-active-directory/)
- [Microsoft Learn - Join a RHEL VM to Entra Domain Services](https://learn.microsoft.com/en-us/entra/identity/domain-services/join-rhel-linux-vm)
- [SSSD issue #5441 - override_space character matching documented limitation](https://github.com/SSSD/sssd/issues/5441)
- [GPO-Based Access Control - SSSD design documentation](https://sssd.io/design-pages/active_directory_gpo_integration.html)
- [SSSD does not enumerate all groups with id command for large nested group sets](https://access.redhat.com/solutions/69120)
