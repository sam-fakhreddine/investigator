# Glossary — SSSD with Entra ID for Per-User Linux Identity and Group-Based Entitlements on AWS EC2

Quick definitions of key terms and concepts referenced in this investigation.

---

## SSSD (System Security Services Daemon)

Linux daemon that provides access to identity and authentication providers (AD, LDAP, Kerberos). Acts as a caching proxy between NSS/PAM and the directory, resolving users, groups, and sudo rules. Configured via sssd.conf with id_provider=ad for Active Directory integration.

## Entra Domain Services (Entra DS)

A managed Microsoft service (formerly Azure AD Domain Services) that provides LDAP, Kerberos, and NTLM authentication endpoints backed by Entra ID. Deployed into an Azure VNet as managed domain controllers. Synchronizes users one-way from Entra ID. Starts at approximately $110/month (Standard SKU). Cloud-only users must change their password once to generate Kerberos/NTLM hashes.

## NSS (Name Service Switch)

Linux mechanism configured in /etc/nsswitch.conf that determines how system databases (passwd, group) are resolved. Adding 'sss' as a source routes lookups through SSSD, making directory users visible to all OS-level identity queries including SSM RunAs.

## Algorithmic SID-to-UID/GID Mapping

SSSD's default method (ldap_id_mapping=true) for generating POSIX UIDs and GIDs from Active Directory SIDs using murmurhash3. Deterministic and consistent across all joined hosts when the domain SID is pinned in sssd.conf. Avoids the need for POSIX attributes in AD.

## realmd

Linux service that discovers and joins identity domains. Automates Kerberos keytab creation, sssd.conf generation, and nsswitch/PAM configuration when joining an AD domain via the 'realm join' command.

## AADSSHLoginForLinux Extension

Azure VM extension that enables Entra ID-based SSH authentication using short-lived OpenSSH certificates. Creates local Linux users on first login. Works on non-Azure servers via Azure Arc. Does not use SSSD; uses its own PAM/NSS integration.

## simple_allow_groups

SSSD access control option that restricts which AD groups can log into a specific host. Provides per-host login restriction based on directory group membership, evaluated after authentication with full nested group resolution.

## ad_gpo_access_control

SSSD option that enforces Windows Group Policy Object (GPO) Allow Log On Locally rights on Linux hosts. Provides centralized login restriction management from AD without per-host sssd.conf changes.

## sudoRole LDAP Object

AD schema extension for storing sudo rules centrally in LDAP. SSSD's sudo provider fetches these rules with smart refresh, avoiding the need to distribute sudoers files to each host. Alternative to file-based /etc/sudoers.d/ deployment.

## AWS Managed Microsoft AD

AWS Directory Service offering that provides a fully managed Active Directory in the AWS VPC. Supports SSSD domain join for EC2 Linux instances without cross-cloud network dependency. Can sync users to Entra ID via Entra Connect Sync (AD-to-Entra direction only).

## AWS AD Connector

AWS Directory Service proxy that forwards LDAP and Kerberos requests to an existing Active Directory without caching. Requires VPN to the target AD. Primarily useful for AWS service integrations (WorkSpaces, FSx), not for direct SSSD enrollment.

---

*Back to: [investigation.md](investigation.md)*
