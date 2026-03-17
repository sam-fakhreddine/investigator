# Glossary — Entra ID and SSSD Linux Identity Integration: End-to-End Architecture

Quick definitions of key terms and concepts referenced in this investigation.

---

## ldap_id_mapping

SSSD configuration boolean (default true for ad provider) selecting between algorithmic UID generation from the AD SID and directory-resident POSIX attribute reading. When true, uidNumber and gidNumber in AD are silently ignored. The two modes are mutually exclusive per domain.

## murmurhash (SSSD ID mapping)

The non-cryptographic hash function used by the SSSD sss_idmap library to map a domain SID to a slice index within the configured UID range. Same SID always produces the same hash; however, slice assignment for secondary domains is order-dependent in multi-domain forests, producing inconsistent UIDs across nodes without the ldap_idmap_default_domain_sid pin.

## ldap_idmap_default_domain_sid

An sssd.conf option that pins a specific domain SID to slice zero of the ID range, bypassing the murmurhash algorithm for that domain. Required for guaranteed cross-node UID consistency on the primary domain in multi-domain AD forest environments.

## SSSD idp provider

Introduced in SSSD 2.11.0, this provider integrates Linux hosts with OAuth2/OIDC identity providers including Entra ID (idp_type = entra_id) without requiring LDAP or Kerberos. POSIX IDs are auto-generated locally using a hash of the cloud object identifier, with a documented but unquantified hash-collision risk.

## Himmelblau

An open-source PAM/NSS daemon authenticating Linux systems against Entra ID via OAuth2/OIDC and Microsoft Graph API. Supports storing POSIX attributes in Entra ID schema extensions via the aad-tool CLI, providing fleet-wide UID consistency without a separate on-premises LDAP store.

## ipaSudoRule objectClass

FreeIPA LDAP objectClass extending sudoRole with DN-based membership attributes (memberUser, memberHost, memberAllowCmd, memberDenyCmd). Allows referencing IPA group and host-group objects by DN for dynamic membership resolution. Requires the SSSD IPA sudo provider — the generic LDAP sudo provider cannot traverse these DN references and silently omits group-scoped rules.

## IPA external group

An IPA group with objectClass ipaExternalGroup that holds foreign SIDs (Active Directory users or groups) as members. AD identities are mapped into IPA external groups, which are nested inside IPA POSIX groups used in sudo rules — the only supported path for granting AD-sourced users FreeIPA sudo access.

## LDB (sysdb) cache

The primary SSSD on-disk identity store — an LDAP-like embedded database at /var/lib/sss/db/cache_<domain>.ldb. Stores all fetched identity objects: users, groups, sudo rules, HBAC policy, SSH keys, and autofs maps. Only the Backend process writes to it; Responders (NSS, PAM, sudo) read from it. Default TTL 5400 seconds.

## Offline credential cache

A salted password hash stored per-user in the sysdb LDB. Enables password authentication when the identity server is unreachable. Disabled by default (cache_credentials = false). Without it, users cannot authenticate at all during IDM outages.

## entry_cache_nowait_percentage

When a lookup arrives after this percentage of entry_cache_timeout has elapsed, SSSD returns the stale cached entry immediately and refreshes in the background. Prevents blocking waits at the cost of brief staleness; critical for avoiding login latency spikes on large deployments when cache entries approach their TTL.

## Active Directory Forest (isolation boundary)

The top-level security and replication boundary in Active Directory. AWS Managed AD always creates a new, separate forest regardless of subdomain naming. No directory objects (users, groups, POSIX attributes, GPOs) replicate across a forest trust; only Kerberos authentication referrals cross it.

## SSSD ad_provider Single-Forest Constraint

SSSD's ad_provider binds LDAP and Kerberos to the single AD forest the Linux host is joined to. It cannot natively LDAP-query a trusted foreign forest's DCs. Organizations requiring Linux hosts to authenticate users from a trusted forest must use winbind or an IPA+trust configuration, or adopt AWS Managed AD Hybrid Edition which eliminates the separate-forest constraint.

## AWS Managed AD Hybrid Edition

An AWS Directory Service offering (GA August 2025) that extends an existing on-premises AD domain into AWS by deploying AWS-managed DCs as members of the on-premises forest. Unlike Standard and Enterprise Managed AD, Hybrid Edition hosts DCs in the same forest — full replication, same schema, POSIX attributes visible — eliminating all cross-forest identity constraints.

---

*Back to: [investigation.md](investigation.md)*
