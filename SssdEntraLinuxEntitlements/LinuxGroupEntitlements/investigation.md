# Investigation: Linux Group Entitlements from Entra ID via SSSD

**Date:** 2026-02-28
**Status:** Complete

---

## Entitlement Flow: Entra Group to Linux Permission

| Layer | Component | Mechanism | Key Config |
| --- | --- | --- | --- |
| Identity Source | Entra ID / AD DS | Security group membership | Groups synced to AD DS or Entra DS |
| Domain Join | realmd + SSSD | Kerberos + LDAP via ad provider | realm join DOMAIN; sssd.conf id_provider=ad |
| NSS Resolution | nss_sss module | getpwnam/getgrnam via nsswitch.conf | passwd: files sss; group: files sss |
| GID Assignment | SSSD id_mapping | Algorithmic SID-to-GID (murmurhash3) or AD POSIX attrs | ldap_id_mapping=true (default) or false |
| Group Name Format | SSSD full_name_format | user@domain or short name | use_fully_qualified_names=false; override_space=_ |
| Sudo Entitlement | /etc/sudoers.d/ files | %groupname ALL=(ALL) ... patterns | Deploy via SSM RunCommand or config mgmt |
| File Permissions | Linux DAC (POSIX) | Secondary group membership grants file access | User added to oracle/dba group via AD membership |
| Login Restriction | SSSD access_provider | simple_allow_groups or ad_gpo_access_control | Per-host group allow lists |
| SSM Session | SSM Agent RunAs | id command via NSS resolves SSSD users | SSMSessionRunAs tag -> personal username |
| Audit | CloudTrail + session logs | IAM principal + OS username in logs | S3/CloudWatch session logging |

> Entra ID groups must flow through a directory service that speaks LDAP/Kerberos (Entra Domain Services or synced on-prem AD DS). Pure cloud-only Entra ID cannot be consumed by SSSD directly.

---

## Question

> How do Entra ID group memberships flow through to Linux groups and sudoers on SSSD-joined EC2 instances, enabling group-based entitlements as a replacement for shared role-based Linux accounts?

---

## Context

Environment uses Entra ID with 10 test users across 4 groups (admins, developers, dbops, readonly), AWS EC2 instances running Amazon Linux 2023, and currently shared local Linux users with SSM RunAs ABAC. Goal is personal Linux usernames with group-based entitlements. Need to confirm a user like Alice can hold simultaneous memberships in linux-admins (sudo) and linux-dbops (oracle file group) on the same host.

---

## Key Findings

- SSSD resolves AD security groups as Linux groups via NSS. When nsswitch.conf contains 'group: files sss', any process calling getgrnam() or initgroups() (including the id command) receives AD group memberships. A user can be a member of multiple AD groups simultaneously, and all are reflected as Linux secondary groups.
- GID assignment has two modes: algorithmic ID mapping (default, ldap_id_mapping=true) uses murmurhash3 on the group SID to generate a deterministic GID consistent across all SSSD-joined hosts; alternatively, ldap_id_mapping=false reads explicit POSIX attributes (gidNumber) from AD. Algorithmic mapping requires no AD schema changes but produces arbitrary GID values.
- POSIX attributes (gidNumber, uidNumber) are NOT required when using SSSD's default algorithmic ID mapping. Groups without POSIX attributes still get valid GIDs. However, if the environment needs specific GID values (e.g., GID 1001 for oracle/dba to match existing file ownership), ldap_id_mapping must be disabled and gidNumber must be set in AD.
- Sudoers integration supports two approaches: (1) local /etc/sudoers.d/ files with %groupname patterns referencing AD groups (e.g., '%linux-admins ALL=(ALL) ALL'), deployed via config management or SSM RunCommand; (2) centrally managed sudo rules stored as sudoRole objects in AD LDAP, fetched by SSSD's sudo provider with smart refresh. Approach 1 is simpler and does not require AD schema extension.
- AD group names with spaces require escaping in sudoers files (e.g., '%Domain\ Admins'). SSSD's override_space option can replace spaces with underscores system-wide, but has a documented limitation where groups containing the override character in their original name may fail lookup (SSSD issue #5441, closed as expected behavior). Best practice is to create AD groups without spaces.
- SSSD supports nested AD group resolution. If GroupC is a member of GroupB which is a member of GroupA, a user in GroupC inherits membership in all three. The ldap_group_nesting_level option (default 2) controls depth. Performance degrades with deep nesting or very large group hierarchies; Red Hat recommends keeping nesting shallow.
- SSSD access_provider controls which users can log into specific hosts. simple_allow_groups restricts login to members of listed AD groups (e.g., only linux-dbops and linux-admins can SSH to database servers). ad_gpo_access_control enforces Windows GPO Allow Log On Locally policies on Linux, requiring no per-host sudoers management for login restrictions.
- The SSM Agent resolves RunAs usernames by executing the id command, which goes through the C library's getpwnam()/getpwuid() functions respecting nsswitch.conf. On an SSSD-joined host, 'id alice@domain' returns the SSSD-resolved UID/GID. Therefore, SSM RunAs works with directory users without any SSM-specific configuration beyond the username tag.
- SSSD caches both credentials and group memberships locally. Default entry_cache_timeout is 5400 seconds (90 minutes). Offline authentication works if the user has previously logged in successfully. Group memberships are cached along with user entries, so file permission checks and sudo rules continue to function during brief directory outages.
- SSM session audit with personal usernames provides full traceability: CloudTrail records the IAM principal (federated identity) that started the session, the target instance, and the RunAs OS username. Session output logs (to S3 or CloudWatch) capture all commands typed during the session under that personal username. Linux audit logs also attribute activity to the individual UID.
- A user like Alice can simultaneously hold linux-admins (granting sudo) and linux-dbops (granting oracle group file access) memberships. Both entitlements apply on any host where SSSD resolves her identity. The Linux kernel evaluates all supplementary groups for file permission checks, and sudoers evaluates all group memberships for privilege escalation rules.
- Entra ID groups cannot be consumed by SSSD directly because SSSD requires LDAP and Kerberos protocols. The groups must flow through either Microsoft Entra Domain Services (managed AD DS in Azure) or be synced to on-premises AD DS via Entra Connect. This is a prerequisite architectural decision.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SSSD (System Security Services Daemon) | Linux daemon that provides access to identity and authentication providers (AD, LDAP, Kerberos). Acts as a caching proxy between NSS/PAM and the directory, resolving users, groups, and sudo rules. |
| NSS (Name Service Switch) | Linux mechanism configured in /etc/nsswitch.conf that determines how system databases (passwd, group, sudoers) are resolved. Adding 'sss' as a source routes lookups through SSSD. |
| Algorithmic ID Mapping | SSSD's default mode (ldap_id_mapping=true) that converts AD SIDs to POSIX UIDs/GIDs using murmurhash3. Produces consistent IDs across all joined hosts without requiring POSIX attributes in AD. |
| simple_allow_groups | SSSD access control option that restricts which AD groups are permitted to log into a specific host. Evaluated after authentication; full nested group hierarchy is resolved before the check. |
| ad_gpo_access_control | SSSD option that enforces Windows Group Policy Object (GPO) Allow Log On Locally rights on Linux hosts. Provides centralized login restriction management from AD without per-host configuration. |
| sudoRole LDAP Object | Schema extension for storing sudo rules in LDAP/AD. SSSD's sudo provider can fetch these centrally managed rules with smart refresh, avoiding the need to distribute sudoers files to each host. |
| realmd | Linux service that discovers and joins identity domains. Automates Kerberos keytab creation, sssd.conf generation, and nsswitch/PAM configuration when joining an AD domain. |
| Entra Domain Services | Microsoft-managed Active Directory Domain Services in Azure that provides LDAP and Kerberos endpoints. Required intermediary for SSSD since Entra ID alone does not expose these protocols. |
| override_space | SSSD configuration option that replaces spaces in AD user and group names with a specified character (typically underscore). Needed because Linux tools handle spaces in names poorly. |
| entry_cache_timeout | SSSD parameter controlling how long resolved user/group entries are cached locally before re-querying the directory. Default 5400 seconds (90 minutes). Enables offline operation. |

---

## Tensions & Tradeoffs

- Algorithmic ID mapping vs explicit POSIX attributes: algorithmic mapping requires zero AD configuration and ensures cross-host consistency, but produces arbitrary GID numbers. If existing file systems have files owned by specific GIDs (e.g., oracle data files with GID 1001), those GIDs will not match the algorithmically generated values. Migrating to algorithmic mapping requires chown of existing files or setting explicit POSIX attributes.
- Local sudoers files vs centralized AD sudo rules: /etc/sudoers.d/ files are simple and well-understood but must be distributed to every host (config drift risk). AD-stored sudoRole objects are centrally managed but require AD schema extension and more complex SSSD configuration. Most AWS-centric environments prefer local files deployed via SSM RunCommand or Ansible.
- Fully qualified names vs short names: use_fully_qualified_names=true (SSSD default for AD) prevents collisions across domains but forces user@domain syntax everywhere (scripts, sudoers, file ownership). Setting it to false enables short names but risks collisions if multiple trusted domains exist. Single-domain environments can safely use short names.
- simple_allow_groups vs ad_gpo_access_control for host login restriction: simple_allow_groups is easy to configure per host but requires sssd.conf changes on each machine. GPO-based control is managed centrally from AD but requires GPO infrastructure and has known SSSD bugs around parsing edge cases. The choice depends on whether AD GPO management is already established.
- Nested group depth vs performance: deep nesting enables flexible entitlement hierarchies (e.g., all-database-team contains dbops and dba-leads) but increases LDAP query complexity. SSSD's default nesting level of 2 may miss deeply nested memberships. Increasing ldap_group_nesting_level improves coverage but slows identity resolution.
- Entra Domain Services cost vs on-premises AD: Entra DS is a managed service (approximately $109/mo minimum as of early 2025; verify current pricing on the Azure pricing page) that avoids running domain controllers, but introduces Azure networking requirements (VNet peering or VPN to AWS VPCs). On-premises AD avoids the cost but requires maintaining domain controller infrastructure.

---

## Open Questions

- What is the network path from AWS EC2 instances to Entra Domain Services LDAP/Kerberos endpoints? This requires either Azure-to-AWS VPN/peering or running AD DS domain controllers within the AWS VPC.
- Does Amazon Linux 2023 ship with a sufficiently recent SSSD version to support all referenced features (ad_gpo_access_control, override_space, nested groups)? Version compatibility should be validated.
- If algorithmic ID mapping is used, what are the generated GID values for the four test groups (admins, developers, dbops, readonly)? These must be documented so that file ownership and sudoers rules reference correct values.
- How will sudoers files be deployed and updated across the EC2 fleet? SSM RunCommand, Ansible, or user-data bootstrapping are all viable, but the lifecycle management approach needs to be decided.
- Will the override_space limitation (SSSD issue #5441) affect any planned group names? Group naming conventions should be established before AD group creation to avoid groups with underscores if override_space=_ is used.
- What is the caching behavior when an AD group membership is revoked? SSSD's entry_cache_timeout means a removed group membership may persist locally for up to 90 minutes. Is this acceptable for security-sensitive entitlements like sudo?

---

## Sources & References

- [RHEL 8 - Connecting RHEL systems directly to AD using SSSD](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/integrating_rhel_systems_directly_with_windows_active_directory/connecting-rhel-systems-directly-to-ad-using-sssd_integrating-rhel-systems-directly-with-active-directory)
- [sssd-ad(5) Linux man page - SSSD Active Directory provider](https://linux.die.net/man/5/sssd-ad)
- [RHEL 7 - Group Policy Object Access Control with SSSD](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-gpo)
- [sssd-simple(5) - Simple access control provider man page](https://linux.die.net/man/5/sssd-simple)
- [RHEL 6 - SSSD Domain Options: Enabling Offline Authentication](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache-cred)
- [AWS SSM - Turn on Run As support for Linux managed nodes](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [AWS SSM - Logging session activity](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-auditing.html)
- [Anatomy of SSSD user lookup - jhrozek](https://jhrozek.wordpress.com/2015/03/11/anatomy-of-sssd-user-lookup/)
- [amazon-ssm-agent shell_unix.go - RunAs user lookup source code](https://github.com/aws/amazon-ssm-agent/blob/b9654b268afcb7e70a9cc6c6d9b7d2a676f5b468/agent/session/plugins/shell/shell_unix.go)
- [SUDO administration with AD - haxor.no](https://haxor.no/en/article/sudo-with-ad)
- [Managing SUDO from Active Directory - Michael Waterman](https://michaelwaterman.nl/2022/10/21/managing-sudo-from-active-directory/)
- [Microsoft Learn - Join a RHEL VM to Entra Domain Services](https://learn.microsoft.com/en-us/entra/identity/domain-services/join-rhel-linux-vm)
- [SSSD issue #5441 - override_space character matching documented limitation](https://github.com/SSSD/sssd/issues/5441)
- [GPO-Based Access Control - SSSD design documentation](https://sssd.io/design-pages/active_directory_gpo_integration.html)
- [SSSD does not enumerate all groups with id command for large nested group sets](https://access.redhat.com/solutions/69120)
