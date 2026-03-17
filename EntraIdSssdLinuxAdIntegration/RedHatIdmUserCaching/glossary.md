# Glossary — Red Hat IDM and SSSD User/Credential Caching Architecture

Quick definitions of key terms and concepts referenced in this investigation.

---

## LDB (sysdb) cache

An LDAP-like embedded on-disk database that is SSSD primary persistent store. One file per domain. Stores all identity objects (users, groups, sudo rules, SSH keys, autofs maps). Only the Backend process writes to it.

## Timestamp cache

A second per-domain LDB introduced in SSSD 1.14 that stores only lastUpdate and dataExpireTimestamp fields. Allows TTL updates without rewriting full object blobs, dramatically reducing write latency for entries whose attributes have not changed.

## Offline credential cache

A salted password hash stored inside the sysdb LDB per user record. Enables password authentication when the identity server is unreachable. Disabled by default (cache_credentials = false). Governed by offline_credentials_expiration and account_cache_expiration.

## KCM (Kerberos Cache Manager)

A separate SSSD responder process (sssd-kcm) that stores live Kerberos TGTs in /var/lib/sss/secrets. Persists across SSSD restarts and reboots. Architecturally distinct from the identity LDB cache.

## Online vs offline mode

SSSD switches to offline mode when the backend fails to reach the LDAP or Kerberos server. In offline mode, identity data is served from LDB as long as entries are not expired; authentication requires a cached credential hash. Reconnection probing introduces up to 6-second delays per probe cycle.

## entry_cache_timeout

The primary TTL governing how long any cached identity object (user, group, etc.) is considered fresh before the backend must re-query the directory. Default 5400 seconds (90 minutes). Separate timeout parameters exist per object type (e.g. entry_cache_group_timeout, entry_cache_sudo_timeout).

## entry_cache_nowait_percentage

When a lookup arrives after this percentage of entry_cache_timeout has elapsed since the last cache write, SSSD returns the stale cached entry immediately and refreshes in the background. Prevents blocking waits at the cost of brief staleness.

## enumerate

Boolean domain parameter controlling whether SSSD proactively downloads all users and groups from the directory at startup. Defaults to false. When true, enables getent passwd/group to list all users but causes CPU-intensive bulk fetches that can block logins on large directories.

## IPA provider

The SSSD backend plugin specific to FreeIPA / Red Hat IDM. Extends the LDAP provider with auto-discovery, HBAC policy enforcement (cached, offline-capable), SELinux user mapping, and native sudo integration. Distinct from the generic ldap or ad providers.

## HBAC cache

FreeIPA-specific access policy objects cached in sysdb by the IPA provider. SSSD evaluates access rules locally against the cache. ipa_hbac_refresh (default 5 s) controls how often SSSD re-fetches policy from the IPA server. Enforced even when offline using last-fetched rules.

## Sudo rule cache

Sudo policy objects stored in the sysdb LDB. Refreshed via two parallel cycles: smart refresh (incremental, every 15 min by default) and full refresh (complete replacement, every 6 h by default). Per-user rule freshness is also checked on each sudo invocation.

## ignore_group_members

IPA/LDAP provider option that tells SSSD to cache group objects without fetching or storing member lists. Eliminates the primary source of large-group write latency. Group membership for sudo and HBAC evaluation still works via the memberof attribute on user objects.

---

*Back to: [investigation.md](investigation.md)*
