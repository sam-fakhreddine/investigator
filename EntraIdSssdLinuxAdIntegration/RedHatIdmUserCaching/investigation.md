# Investigation: Red Hat IDM and SSSD User/Credential Caching Architecture

**Date:** 2026-03-17
**Status:** Complete

---

## Question

> How does Red Hat IDM (FreeIPA) and SSSD user/credential caching work architecturally to avoid slow or failed identity queries for business (non-technical) users on Linux hosts?

---

## Context

Organizations enrolling Linux hosts into Red Hat IDM (FreeIPA) rely on SSSD as the identity broker between the host and the directory. Non-technical users experience login delays or failures when identity servers are unreachable or when directory objects are large. Understanding the caching architecture is prerequisite to diagnosing and sizing these systems.

---

## SSSD Cache Types and Key Parameters

| Cache Type | Storage Location | What Is Stored | Default TTL / Expiry | Key Parameter |
| --- | --- | --- | --- | --- |
| Identity (sysdb) | /var/lib/sss/db/cache_<domain>.ldb | User POSIX attrs (UID, GID, home, shell), group memberships, SSH keys, autofs maps | 5400 seconds (90 min) | entry_cache_timeout |
| Timestamp (split cache) | /var/lib/sss/db/timestamp_<domain>.ldb | lastUpdate and dataExpireTimestamp for each entry (metadata only) | Mirrors sysdb TTL | entry_cache_nowait_percentage |
| Credential (offline auth) | Embedded in sysdb LDB per-user record | Salted password hash (not plaintext) | 0 days = forever; disabled by default | cache_credentials, offline_credentials_expiration |
| Kerberos TGT (KCM) | /var/lib/sss/secrets (KCM store) | Active Kerberos ticket-granting tickets per-user | Ticket lifetime (typically 10-24 h) | sssd-kcm service |
| Sudo rules | sysdb LDB (same domain cache) | LDAP-format sudoRole objects | Smart refresh 15 min, full refresh 6 h | ldap_sudo_smart_refresh_interval, ldap_sudo_full_refresh_interval |
| HBAC rules (IPA only) | sysdb LDB (same domain cache) | Host-based access control policy objects | 5 seconds default refresh | ipa_hbac_refresh |
| SELinux maps (IPA only) | sysdb LDB (same domain cache) | SELinux user-context mappings | Refresh on policy change | ipa_selinux_refresh |

> cache_credentials = false is the default; offline credential caching must be explicitly enabled. The KCM cache is architecturally separate from the identity/credential sysdb.

---

## Key Findings

- SSSD is a multi-process daemon: a Monitor spawns per-domain Backend (data provider) processes and per-protocol Responder processes (NSS, PAM, sudo, SSH). Only the Backend writes to the LDB cache; Responders only read from it.
- The primary identity store is an LDB (LDAP-like embedded) database at /var/lib/sss/db/cache_<domain>.ldb. It stores user POSIX attributes, group memberships, sudo rules, autofs maps, and SSH keys as a local replica of all directory objects SSSD has fetched.
- SSSD 1.14 introduced a split-cache design: a second LDB at timestamp_<domain>.ldb stores only expiry timestamps. When the backend re-fetches an entry whose attributes have not changed on the server, only the timestamp database is updated, avoiding expensive full rewrites of large group objects.
- Every cache entry carries a dataExpireTimestamp driven by entry_cache_timeout (default 5400 s). When a Responder receives a lookup, it returns cached data immediately if valid, or blocks waiting for the Backend to refresh if the entry is expired.
- entry_cache_nowait_percentage enables background refreshes: entries past that percentage of their TTL are served from cache immediately while the Backend updates in the background, eliminating blocking waits at the cost of brief staleness.
- SSSD transitions to offline mode when the backend cannot reach the LDAP/Kerberos server. In offline mode, identity data continues to be served from the LDB cache as long as entries have not yet expired; authentication succeeds only if cache_credentials = true was set and the user has logged in at least once while online.
- cache_credentials is false by default, meaning offline authentication is not available unless explicitly enabled. When enabled, a salted password hash is stored per-user in the sysdb LDB, governed by offline_credentials_expiration (days; 0 = never expire).
- The Kerberos TGT credential cache is managed by the sssd-kcm process and stored separately in /var/lib/sss/secrets. It survives KCM restarts and reboots. It is architecturally distinct from the identity LDB cache and from the offline password hash.
- The sudo rule cache uses two independent refresh cycles: a smart refresh (default every 15 min) fetches only rules modified since last sync; a full refresh (default every 6 h) replaces all rules. Each sudo invocation also triggers an on-demand per-user rule freshness check.
- The IPA backend (FreeIPA) extends the generic LDAP provider with additional cached object types: HBAC rules (refreshed every 5 s by default via ipa_hbac_refresh), SELinux user maps, and Kerberos policy. These are not available with a vanilla LDAP provider.
- The IPA provider enforces HBAC access decisions locally using cached policy, so access control works even briefly offline; a capability that requires a full LDAP bind in vanilla LDAP configurations.
- enumerate = false (the default) means SSSD does not pre-populate the cache with all users and groups at startup. Entries are cached only on first lookup. This keeps startup load low but means first-ever lookups for a user are always live directory queries with no cache hit.
- Enabling enumerate = true on large directories causes severe CPU storms in sssd_be: with 30,000 LDAP users, documented cases show sssd_be consuming ~99% CPU during enumeration, blocking all login operations for minutes.
- First-login latency spikes when SSSD must resolve large or deeply nested group memberships during login. NSS calls can time out after 58 seconds; in extreme cases (80,000+ group members) login took up to 5 minutes, and sssd_be was killed by the internal watchdog.
- ignore_group_members = true instructs SSSD to cache group metadata but not member lists, providing a major performance improvement in large-group environments at the cost of group-member enumeration accuracy.
- Red Hat official SSSD performance guidance for large IdM-AD trust deployments recommends mounting the SSSD cache directory on a RAM-backed filesystem and sizing approximately 100 MB per 10,000 LDAP entries.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| LDB (sysdb) cache | An LDAP-like embedded on-disk database that is SSSD primary persistent store. One file per domain. Stores all identity objects (users, groups, sudo rules, SSH keys, autofs maps). Only the Backend process writes to it. |
| Timestamp cache | A second per-domain LDB introduced in SSSD 1.14 that stores only lastUpdate and dataExpireTimestamp fields. Allows TTL updates without rewriting full object blobs, dramatically reducing write latency for entries whose attributes have not changed. |
| Offline credential cache | A salted password hash stored inside the sysdb LDB per user record. Enables password authentication when the identity server is unreachable. Disabled by default (cache_credentials = false). Governed by offline_credentials_expiration and account_cache_expiration. |
| KCM (Kerberos Cache Manager) | A separate SSSD responder process (sssd-kcm) that stores live Kerberos TGTs in /var/lib/sss/secrets. Persists across SSSD restarts and reboots. Architecturally distinct from the identity LDB cache. |
| Online vs offline mode | SSSD switches to offline mode when the backend fails to reach the LDAP or Kerberos server. In offline mode, identity data is served from LDB as long as entries are not expired; authentication requires a cached credential hash. Reconnection probing introduces up to 6-second delays per probe cycle. |
| entry_cache_timeout | The primary TTL governing how long any cached identity object (user, group, etc.) is considered fresh before the backend must re-query the directory. Default 5400 seconds (90 minutes). Separate timeout parameters exist per object type (e.g. entry_cache_group_timeout, entry_cache_sudo_timeout). |
| entry_cache_nowait_percentage | When a lookup arrives after this percentage of entry_cache_timeout has elapsed since the last cache write, SSSD returns the stale cached entry immediately and refreshes in the background. Prevents blocking waits at the cost of brief staleness. |
| enumerate | Boolean domain parameter controlling whether SSSD proactively downloads all users and groups from the directory at startup. Defaults to false. When true, enables getent passwd/group to list all users but causes CPU-intensive bulk fetches that can block logins on large directories. |
| IPA provider | The SSSD backend plugin specific to FreeIPA / Red Hat IDM. Extends the LDAP provider with auto-discovery, HBAC policy enforcement (cached, offline-capable), SELinux user mapping, and native sudo integration. Distinct from the generic ldap or ad providers. |
| HBAC cache | FreeIPA-specific access policy objects cached in sysdb by the IPA provider. SSSD evaluates access rules locally against the cache. ipa_hbac_refresh (default 5 s) controls how often SSSD re-fetches policy from the IPA server. Enforced even when offline using last-fetched rules. |
| Sudo rule cache | Sudo policy objects stored in the sysdb LDB. Refreshed via two parallel cycles: smart refresh (incremental, every 15 min by default) and full refresh (complete replacement, every 6 h by default). Per-user rule freshness is also checked on each sudo invocation. |
| ignore_group_members | IPA/LDAP provider option that tells SSSD to cache group objects without fetching or storing member lists. Eliminates the primary source of large-group write latency. Group membership for sudo and HBAC evaluation still works via the memberof attribute on user objects. |

---

## Tensions & Tradeoffs

- Longer entry_cache_timeout reduces directory load and avoids blocking lookups but means identity changes (password resets, group modifications, account disables) propagate to hosts only after the TTL expires, a security and operational tension.
- enumerate = true pre-warms the cache for fast getent lookups and avoids first-login cold-cache latency, but generates severe CPU and network load on large directories that can make logins impossible during the enumeration window.
- entry_cache_nowait_percentage resolves the staleness-vs-blocking tradeoff by returning stale data immediately, but means some lookups may reflect directory state that is up to entry_cache_timeout seconds old, an ambiguous freshness guarantee.
- cache_credentials = false (the default) is the safest posture against credential replay on a compromised host, but means users cannot authenticate at all if the identity server is unreachable, a high-availability risk for critical workloads.
- ignore_group_members dramatically reduces login latency for large-group environments but breaks getent group member enumeration and any application that depends on reading group member lists from NSS rather than querying the directory directly.
- ipa_hbac_refresh defaults to 5 seconds to keep access policy fresh, but frequent refreshes add per-login latency and server load in environments with many concurrent SSH sessions; raising it too high delays propagation of access revocations.
- The KCM credential cache persists Kerberos TGTs across reboots (intentional for reliability), which also means a stolen or compromised host retains valid tickets until expiry, a security-vs-usability tradeoff not present in traditional in-memory ccache implementations.

---

## Open Questions

- Does the IPA provider HBAC cache remain valid and enforced indefinitely in offline mode, or does SSSD eventually deny access once the cached policy reaches an internal staleness threshold?
- What is the precise behavior when an entry in the sysdb LDB has expired (past entry_cache_timeout) but the backend is offline: does SSSD serve the stale entry or return a lookup failure?
- Is there a documented maximum cache size or entry count beyond which LDB lookup performance degrades measurably, and does Red Hat publish sizing guidance specific to identity-only (non-AD-trust) deployments?
- How does SSSD handle the race condition where a user identity entry expires and the backend is simultaneously transitioning from offline to online mode: do queued requests pile up or are they answered from stale cache?
- For sudo rule evaluation with large nested groups, does SSSD resolve group membership from the local sysdb cache or does it issue live LDAP memberof queries, and does the answer change when ignore_group_members is set?

---

## Sources & References

- [SSSD Architecture - sssd.io](https://sssd.io/docs/architecture.html)
- [SSSD Internals - docs.pagure.org](https://docs.pagure.org/sssd.sssd/developers/internals.html)
- [Improve SSSD Performance with a timestamp cache - sssd.io](https://sssd.io/design-pages/one_fourteen_performance_improvements.html)
- [SUDO Caching Rules - sssd.io](https://sssd.io/design-pages/sudo_caching_rules.html)
- [SUDO Responder Cache Behaviour - sssd.io](https://sssd.io/design-pages/sudo_responder_cache_behaviour.html)
- [Authenticate against cache in SSSD - sssd.io](https://sssd.io/design-pages/cached_authentication.html)
- [KCM server for SSSD - sssd.io](https://sssd.io/design-pages/kcm.html)
- [Managing the SSSD Cache - Red Hat RHEL 6 Deployment Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache)
- [Domain Options Enabling Offline Authentication - Red Hat RHEL 6](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache-cred)
- [Understanding SSSD and its benefits - Red Hat RHEL 8](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel)
- [Tuning SSSD performance for large IdM-AD trust deployments - RHEL 9](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/tuning_performance_in_identity_management/assembly_tuning-sssd-performance-for-large-idm-ad-trust-deployments_tuning-performance-in-idm)
- [Tuning performance in Identity Management - Red Hat RHEL 8](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/tuning_performance_in_identity_management/index)
- [SSSD logins and user lookups from large domains are slow - Red Hat Customer Portal](https://access.redhat.com/solutions/705623)
- [Slow logins with SSSD due to large and nested groups in Active Directory - Red Hat Customer Portal](https://access.redhat.com/solutions/1475233)
- [Cache credentials with SSSD in offline mode - Red Hat Customer Portal](https://access.redhat.com/solutions/500963)
- [sssd-ipa(5) man page - configuration file for SSSD IPA provider](https://linux.die.net/man/5/sssd-ipa)
- [sssd-sudo(5) man page - Configuring sudo with SSSD back end](https://linux.die.net/man/5/sssd-sudo)
- [Enumerating large number of users makes sssd_be hog CPU - GitHub Issue 2771](https://github.com/SSSD/sssd/issues/2771)
- [SSSD Frequently Asked Questions - docs.pagure.org](https://docs.pagure.org/sssd.sssd/users/faq.html)
- [Performance tuning SSSD for large IPA-AD trust deployments - jhrozek blog](https://jhrozek.wordpress.com/2015/08/19/performance-tuning-sssd-for-large-ipa-ad-trust-deployments/)
