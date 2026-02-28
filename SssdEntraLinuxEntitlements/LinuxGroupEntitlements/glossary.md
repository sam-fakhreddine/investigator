# Glossary — Linux Group Entitlements from Entra ID via SSSD

Quick definitions of key terms and concepts referenced in this investigation.

---

## SSSD (System Security Services Daemon)

Linux daemon that provides access to identity and authentication providers (AD, LDAP, Kerberos). Acts as a caching proxy between NSS/PAM and the directory, resolving users, groups, and sudo rules.

## NSS (Name Service Switch)

Linux mechanism configured in /etc/nsswitch.conf that determines how system databases (passwd, group, sudoers) are resolved. Adding 'sss' as a source routes lookups through SSSD.

## Algorithmic ID Mapping

SSSD's default mode (ldap_id_mapping=true) that converts AD SIDs to POSIX UIDs/GIDs using murmurhash3. Produces consistent IDs across all joined hosts without requiring POSIX attributes in AD.

## simple_allow_groups

SSSD access control option that restricts which AD groups are permitted to log into a specific host. Evaluated after authentication; full nested group hierarchy is resolved before the check.

## ad_gpo_access_control

SSSD option that enforces Windows Group Policy Object (GPO) Allow Log On Locally rights on Linux hosts. Provides centralized login restriction management from AD without per-host configuration.

## sudoRole LDAP Object

Schema extension for storing sudo rules in LDAP/AD. SSSD's sudo provider can fetch these centrally managed rules with smart refresh, avoiding the need to distribute sudoers files to each host.

## realmd

Linux service that discovers and joins identity domains. Automates Kerberos keytab creation, sssd.conf generation, and nsswitch/PAM configuration when joining an AD domain.

## Entra Domain Services

Microsoft-managed Active Directory Domain Services in Azure that provides LDAP and Kerberos endpoints. Required intermediary for SSSD since Entra ID alone does not expose these protocols.

## override_space

SSSD configuration option that replaces spaces in AD user and group names with a specified character (typically underscore). Needed because Linux tools handle spaces in names poorly.

## entry_cache_timeout

SSSD parameter controlling how long resolved user/group entries are cached locally before re-querying the directory. Default 5400 seconds (90 minutes). Enables offline operation.

---

*Back to: [investigation.md](investigation.md)*
