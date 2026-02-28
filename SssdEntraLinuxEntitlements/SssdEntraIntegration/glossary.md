# Glossary — Entra ID as an Identity Source for Linux SSSD on AWS EC2 Instances

Quick definitions of key terms and concepts referenced in this investigation.

---

## Entra Domain Services (Entra DS)

A managed Microsoft service (formerly Azure AD Domain Services) that provides LDAP, Kerberos, and NTLM authentication endpoints backed by Entra ID. Deployed into an Azure VNet as a pair of managed domain controllers. Synchronizes users one-way from Entra ID. Enterprise and Premium SKUs support custom attributes (onPremisesExtensionAttributes 1-15 and directory extensions), though these are not the same as RFC 2307 POSIX schema attributes. Requires cloud-only users to change their password at least once to generate Kerberos/NTLM hashes.

## SSSD ad_provider

The Active Directory identity provider for SSSD (id_provider=ad in sssd.conf). Discovers AD domain controllers via DNS SRV records, authenticates via Kerberos, and retrieves user/group information via LDAP. Supports algorithmic SID-to-UID mapping or explicit POSIX attributes from AD. Configured automatically by the realmd/realm join workflow.

## Algorithmic SID-to-UID Mapping

SSSD's default method for generating POSIX UIDs and GIDs from Active Directory SIDs. Uses murmurhash3 on the SID string to assign a deterministic UID. Consistent across hosts when the domain SID is pinned (ldap_idmap_default_domain_sid). Avoids the need to manage POSIX attributes in AD but does not support custom UID assignment.

## Azure Arc-enabled Servers

A Microsoft service that extends Azure management capabilities to non-Azure machines (on-premises, AWS, GCP). Installs the Azure Connected Machine agent on the server. Enables deployment of Azure VM extensions (including AADSSHLoginForLinux) and management via Azure Resource Manager. Requires outbound HTTPS to Azure endpoints.

## AADSSHLoginForLinux Extension

An Azure VM extension (publisher Microsoft.Azure.ActiveDirectory) that enables Entra ID-based SSH authentication on Linux. Uses short-lived OpenSSH certificates issued by Entra ID. Creates local Linux user accounts on first login. Works on Azure VMs natively and on non-Azure servers via Azure Arc. Does not use SSSD; uses its own PAM/NSS integration.

## AWS AD Connector

An AWS Directory Service offering that acts as a stateless proxy, forwarding authentication and directory lookup requests to an existing Active Directory. Does not cache credentials. Requires network connectivity (VPN or Direct Connect) to the target AD domain controllers. Primarily used for AWS service integrations (WorkSpaces, SSO, FSx) rather than direct Linux SSSD enrollment.

## NSS (Name Service Switch)

The Linux subsystem configured via /etc/nsswitch.conf that determines the order of sources for user, group, and host resolution. When SSSD is installed, the passwd and group entries are configured as 'files sss', meaning the OS first checks local files (/etc/passwd) then SSSD for user lookups. SSM Session Manager's RunAs user resolution depends on NSS to find directory users.

---

*Back to: [investigation.md](investigation.md)*
