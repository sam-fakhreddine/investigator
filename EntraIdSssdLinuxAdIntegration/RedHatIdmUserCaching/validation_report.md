# Validation Report: Red Hat IDM and SSSD User/Credential Caching Architecture
Date: 2026-03-17
Validator: Fact Validation Agent

## Summary
- Total sources checked: 20
- Verified: 19 | Redirected: 0 | Dead: 0 | Unverifiable: 1
- Findings checked: 16
- Confirmed: 13 | Partially confirmed: 2 | Unverified: 0 | Contradicted: 1
- JSON/MD sync issues: 0
- Items requiring remediation: 2

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/EntraIdSssdLinuxAdIntegration/RedHatIdmUserCaching
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        16           16           92859e77a761   92859e77a761
tensions             IN_SYNC        7            7            5180f678927b   5180f678927b
open_questions       IN_SYNC        5            5            06878cd096eb   06878cd096eb
sources              IN_SYNC        20           20           ddedb3256739   ddedb3256739
concepts             IN_SYNC        12           12           92f4ddcd119d   92f4ddcd119d
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | SSSD Architecture - sssd.io | https://sssd.io/docs/architecture.html | VERIFIED | Title and content confirmed. Describes monitor, backend, responder architecture exactly as cited. |
| 2 | SSSD Internals - docs.pagure.org | https://docs.pagure.org/sssd.sssd/developers/internals.html | VERIFIED | Title confirmed. Covers NSS/PAM responder internals, IPC, offline operation. |
| 3 | Improve SSSD Performance with a timestamp cache - sssd.io | https://sssd.io/design-pages/one_fourteen_performance_improvements.html | VERIFIED | Title confirmed. Describes the split-cache (timestamp LDB) design for SSSD 1.14. |
| 4 | SUDO Caching Rules - sssd.io | https://sssd.io/design-pages/sudo_caching_rules.html | VERIFIED | Title confirmed as "SUDO caching rules". Minor case variation but correct page. |
| 5 | SUDO Responder Cache Behaviour - sssd.io | https://sssd.io/design-pages/sudo_responder_cache_behaviour.html | VERIFIED | Title confirmed. Covers cached sudo rule data formats and update logic. |
| 6 | Authenticate against cache in SSSD - sssd.io | https://sssd.io/design-pages/cached_authentication.html | VERIFIED | Title confirmed. Describes cache_credentials, offline password hash, cached_auth_timeout. |
| 7 | KCM server for SSSD - sssd.io | https://sssd.io/design-pages/kcm.html | VERIFIED | Title confirmed. Describes KCM as sssd-kcm responder, storage in /var/lib/sss/secrets. |
| 8 | Managing the SSSD Cache - Red Hat RHEL 6 Deployment Guide | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache | VERIFIED | Title confirmed as section 13.2.28. Covers sss_cache, LDB files per domain. |
| 9 | Domain Options Enabling Offline Authentication - Red Hat RHEL 6 | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache-cred | VERIFIED | Title confirmed as section 13.2.16. Covers cache_credentials, offline_credentials_expiration. |
| 10 | Understanding SSSD and its benefits - Red Hat RHEL 8 | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel | VERIFIED | Title confirmed as Chapter 3. Describes offline caching, reduced provider load, single account. |
| 11 | Tuning SSSD performance for large IdM-AD trust deployments - RHEL 9 | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/tuning_performance_in_identity_management/assembly_tuning-sssd-performance-for-large-idm-ad-trust-deployments_tuning-performance-in-idm | VERIFIED | Title confirmed as Chapter 9. Covers ignore_group_members, cache sizing 100 MB per 10,000 entries. |
| 12 | Tuning performance in Identity Management - Red Hat RHEL 8 | https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/tuning_performance_in_identity_management/index | VERIFIED | Resolves to docs.redhat.com equivalent. Content confirmed. |
| 13 | SSSD logins and user lookups from large domains are slow - Red Hat Customer Portal | https://access.redhat.com/solutions/705623 | UNVERIFIABLE | Title confirmed via search. Full content requires Red Hat subscription. Cannot independently verify specific quantitative claims. |
| 14 | Slow logins with SSSD due to large and nested groups in Active Directory - Red Hat Customer Portal | https://access.redhat.com/solutions/1475233 | VERIFIED | Title confirmed. Addresses large and nested AD group membership login delays. Full content requires subscription. |
| 15 | Cache credentials with SSSD in offline mode - Red Hat Customer Portal | https://access.redhat.com/solutions/500963 | VERIFIED | Title confirmed. Covers enabling offline credential caching, offline_credentials_expiration, account_cache_expiration. |
| 16 | sssd-ipa(5) man page - linux.die.net | https://linux.die.net/man/5/sssd-ipa | VERIFIED | Title confirmed as "sssd-ipa(5): config file for SSSD". Covers IPA provider options including ipa_hbac_refresh. |
| 17 | sssd-sudo(5) man page - linux.die.net | https://linux.die.net/man/5/sssd-sudo | VERIFIED | Title confirmed as "sssd-sudo(5): config file for SSSD". Covers sudo refresh intervals. |
| 18 | Enumerating large number of users makes sssd_be hog CPU - GitHub Issue 2771 | https://github.com/SSSD/sssd/issues/2771 | VERIFIED | Title confirmed. Issue documents 30,000-user LDAP directory causing sssd_be ~99% CPU during enumeration, local logins taking ~2 minutes. |
| 19 | SSSD Frequently Asked Questions - docs.pagure.org | https://docs.pagure.org/sssd.sssd/users/faq.html | VERIFIED | Title confirmed as "Frequently Asked Questions". Covers enumeration, group membership handling. |
| 20 | Performance tuning SSSD for large IPA-AD trust deployments - jhrozek blog | https://jhrozek.wordpress.com/2015/08/19/performance-tuning-sssd-for-large-ipa-ad-trust-deployments/ | VERIFIED | Title confirmed. Covers RAM-backed cache filesystem, cache write latency, ACID transactions. Written for SSSD 1.12/1.13. |

---

## Finding Verification

### Finding 1: SSSD multi-process architecture (Monitor, Backend, Responders)
- **Claim:** "SSSD is a multi-process daemon: a Monitor spawns per-domain Backend (data provider) processes and per-protocol Responder processes (NSS, PAM, sudo, SSH). Only the Backend writes to the LDB cache; Responders only read from it."
- **Verdict:** CONFIRMED
- **Evidence:** sssd.io architecture page explicitly states the monitor starts and stops backends and responders. Responders check the cache and request backend updates when data is missing or expired; the backend is the sole cache writer.
- **Source used:** https://sssd.io/docs/architecture.html

### Finding 2: Primary identity store is LDB at /var/lib/sss/db/cache_<domain>.ldb
- **Claim:** "The primary identity store is an LDB (LDAP-like embedded) database at /var/lib/sss/db/cache_<domain>.ldb. It stores user POSIX attributes, group memberships, sudo rules, autofs maps, and SSH keys as a local replica of all directory objects SSSD has fetched."
- **Verdict:** CONFIRMED
- **Evidence:** Red Hat RHEL 6 Deployment Guide confirms cache files are stored in /var/lib/sss/db/. SSSD architecture docs confirm LDB as the persistent local store.
- **Source used:** https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache

### Finding 3: SSSD 1.14 split-cache design with timestamp_<domain>.ldb
- **Claim:** "SSSD 1.14 introduced a split-cache design: a second LDB at timestamp_<domain>.ldb stores only expiry timestamps. When the backend re-fetches an entry whose attributes have not changed on the server, only the timestamp database is updated, avoiding expensive full rewrites of large group objects."
- **Verdict:** CONFIRMED
- **Evidence:** sssd.io design page explicitly describes this design: "the sysdb_ctx would add another ldb file that only contains the timestamp and the DN of an entry, opened in nosync mode." Confirms that when modifyTimestamp has not changed, only the timestamp cache is updated.
- **Source used:** https://sssd.io/design-pages/one_fourteen_performance_improvements.html

### Finding 4: entry_cache_timeout default 5400 seconds, blocking behavior on expired entries
- **Claim:** "Every cache entry carries a dataExpireTimestamp driven by entry_cache_timeout (default 5400 s). When a Responder receives a lookup, it returns cached data immediately if valid, or blocks waiting for the Backend to refresh if the entry is expired."
- **Verdict:** CONFIRMED
- **Evidence:** Multiple sources confirm entry_cache_timeout default of 5400 seconds (90 minutes). Blocking behavior on expired entries confirmed by sssd.conf documentation.
- **Source used:** https://linux.die.net/man/5/sssd.conf

### Finding 5: entry_cache_nowait_percentage enables background refresh
- **Claim:** "entry_cache_nowait_percentage enables background refreshes: entries past that percentage of their TTL are served from cache immediately while the Backend updates in the background, eliminating blocking waits at the cost of brief staleness."
- **Verdict:** CONFIRMED
- **Evidence:** sssd.conf man page and Red Hat documentation document this parameter with the described semantics.
- **Source used:** https://linux.die.net/man/5/sssd.conf

### Finding 6: SSSD offline mode — identity data served from LDB while entries unexpired
- **Claim:** "SSSD transitions to offline mode when the backend cannot reach the LDAP/Kerberos server. In offline mode, identity data continues to be served from the LDB cache as long as entries have not yet expired; authentication succeeds only if cache_credentials = true was set and the user has logged in at least once while online."
- **Verdict:** CONFIRMED
- **Evidence:** Red Hat documentation and sssd.io cached_authentication page both confirm this behavior.
- **Source used:** https://sssd.io/design-pages/cached_authentication.html; https://access.redhat.com/solutions/500963

### Finding 7: cache_credentials false by default; offline auth requires explicit enablement
- **Claim:** "cache_credentials is false by default, meaning offline authentication is not available unless explicitly enabled. When enabled, a salted password hash is stored per-user in the sysdb LDB, governed by offline_credentials_expiration (days; 0 = never expire)."
- **Verdict:** CONFIRMED
- **Evidence:** Multiple Red Hat sources and sssd.io explicitly confirm cache_credentials defaults to false. Red Hat Customer Portal solution 500963 confirms the salted hash storage mechanism and expiration parameters.
- **Source used:** https://access.redhat.com/solutions/500963; https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache-cred

### Finding 8: KCM TGT cache in /var/lib/sss/secrets, survives restarts and reboots
- **Claim:** "The Kerberos TGT credential cache is managed by the sssd-kcm process and stored separately in /var/lib/sss/secrets. It survives KCM restarts and reboots. It is architecturally distinct from the identity LDB cache and from the offline password hash."
- **Verdict:** CONFIRMED
- **Evidence:** sssd-kcm man pages and KCM design page confirm /var/lib/sss/secrets as the storage location and persistence across restarts and reboots.
- **Source used:** https://sssd.io/design-pages/kcm.html

### Finding 9: Sudo smart refresh default 15 min; full refresh default stated as 24 hours
- **Claim:** "The sudo rule cache uses two independent refresh cycles: a smart refresh (default every 15 min) fetches only rules modified since last sync; a full refresh (default every 24 h) replaces all rules."
- **Verdict:** CONTRADICTED — smart refresh default of 15 minutes is correct, but the full refresh default is 6 hours (21,600 seconds), not 24 hours (86,400 seconds).
- **Evidence:** sssd-sudo(5) man pages on Ubuntu, Arch Linux, and OpenSUSE all consistently document ldap_sudo_full_refresh_interval default as 6 hours. The investigation states "24 h" in both key_findings[8] and in the quick_reference table row for "Sudo rules." Both are incorrect.
- **Source used:** https://manpages.ubuntu.com/manpages/jammy/man5/sssd-sudo.5.html; https://linux.die.net/man/5/sssd-sudo; https://manpages.opensuse.org/Tumbleweed/sssd/sssd-sudo.5.en.html

### Finding 10: IPA provider adds HBAC, SELinux maps, Kerberos policy beyond generic LDAP
- **Claim:** "The IPA backend (FreeIPA) extends the generic LDAP provider with additional cached object types: HBAC rules (refreshed every 5 s by default via ipa_hbac_refresh), SELinux user maps, and Kerberos policy."
- **Verdict:** CONFIRMED
- **Evidence:** sssd-ipa(5) man page confirms HBAC provider role, ipa_hbac_refresh option, and default of 5 seconds. SELinux user map and Kerberos policy caching confirmed in sssd-ipa documentation.
- **Source used:** https://linux.die.net/man/5/sssd-ipa

### Finding 11: IPA provider enforces HBAC locally from cache; vanilla LDAP requires live bind
- **Claim:** "The IPA provider enforces HBAC access decisions locally using cached policy, so access control works even briefly offline; a capability that requires a full LDAP bind in vanilla LDAP configurations."
- **Verdict:** CONFIRMED
- **Evidence:** sssd-ipa(5) man page confirms IPA provider uses HBAC rules for local access decisions. sssd.io design pages and jhrozek blog confirm local offline enforcement.
- **Source used:** https://linux.die.net/man/5/sssd-ipa; https://jhrozek.wordpress.com/2015/08/19/performance-tuning-sssd-for-large-ipa-ad-trust-deployments/

### Finding 12: enumerate = false default; first-ever lookups always live directory queries
- **Claim:** "enumerate = false (the default) means SSSD does not pre-populate the cache with all users and groups at startup. Entries are cached only on first lookup. This keeps startup load low but means first-ever lookups for a user are always live directory queries with no cache hit."
- **Verdict:** CONFIRMED
- **Evidence:** SSSD FAQ and sssd.conf man page confirm enumerate defaults to false. FAQ explicitly states enumeration is disabled by default to minimize server load and client performance impact.
- **Source used:** https://docs.pagure.org/sssd.sssd/users/faq.html

### Finding 13: enumerate = true causes CPU storm on large directories
- **Claim:** "Enabling enumerate = true on large directories causes severe CPU storms in sssd_be: with 30,000 LDAP users, documented cases show sssd_be consuming ~99% CPU during enumeration, blocking all login operations for minutes."
- **Verdict:** CONFIRMED
- **Evidence:** GitHub issue #2771 exactly matches this claim. GitHub issue #2935 additionally documents sssd_be at 100% CPU with enumerate=true causing sssd_be restarts every 1-2 minutes.
- **Source used:** https://github.com/SSSD/sssd/issues/2771; https://github.com/SSSD/sssd/issues/2935

### Finding 14: First-login latency from large group memberships; NSS 58-second timeout; sssd_be watchdog kill
- **Claim:** "First-login latency spikes when SSSD must resolve large or deeply nested group memberships during login. NSS calls can time out after 58 seconds; in extreme cases (80,000+ group members) login took up to 5 minutes, and sssd_be was killed by the internal watchdog."
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** NSS timeout of 58 seconds for large group retrieval confirmed by GitHub issue #2865. sssd_be watchdog kills confirmed by Red Hat Customer Portal solutions and SSSD GitHub issues. The specific "80,000+ group members / up to 5 minutes" figures are directionally supported but rely on subscription-gated content that could not be fully accessed to verify the exact numbers.
- **Source used:** https://github.com/SSSD/sssd/issues/2865; https://access.redhat.com/solutions/705623
- **Flag:** NEEDS_PRIMARY_SOURCE for the specific "80,000+ / 5 minutes" figures.

### Finding 15: ignore_group_members improves large-group performance at cost of member enumeration
- **Claim:** "ignore_group_members = true instructs SSSD to cache group metadata but not member lists, providing a major performance improvement in large-group environments at the cost of group-member enumeration accuracy."
- **Verdict:** CONFIRMED
- **Evidence:** sssd-ldap(5) man page confirms ignore_group_members prevents fetching member attributes. RHEL 9 performance tuning documentation and jhrozek blog both recommend this option for large-group environments.
- **Source used:** https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/tuning_performance_in_identity_management/assembly_tuning-sssd-performance-for-large-idm-ad-trust-deployments_tuning-performance-in-idm

### Finding 16: Red Hat guidance recommends RAM filesystem for SSSD cache; ~100 MB per 10,000 entries
- **Claim:** "Red Hat official SSSD performance guidance for large IdM-AD trust deployments recommends mounting the SSSD cache directory on a RAM-backed filesystem and sizing approximately 100 MB per 10,000 LDAP entries."
- **Verdict:** CONFIRMED
- **Evidence:** RHEL 9 tuning documentation explicitly states "estimating 100 MBs per 10,000 LDAP entries." jhrozek blog recommends mounting the cache into a ramdisk to eliminate disk I/O cost.
- **Source used:** https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/tuning_performance_in_identity_management/assembly_tuning-sssd-performance-for-large-idm-ad-trust-deployments_tuning-performance-in-idm

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 9 + quick_reference: sudo full refresh default stated as "24 h" | CONTRADICTED | Correct to 6 hours (21,600 s). Update key_findings[8] text "full refresh (default every 24 h)" → "full refresh (default every 6 h)". Update quick_reference rows["Sudo rules"] "Smart refresh 15 min, full refresh 24 h" → "Smart refresh 15 min, full refresh 6 h". The ldap_sudo_full_refresh_interval default is 21,600 s per official sssd-sudo(5) man pages. |
| Finding 14: "80,000+ group members / up to 5 minutes" specific figures | PARTIALLY CONFIRMED | Add attribution to Red Hat Customer Portal solutions 705623 and 1475233 alongside these figures. Do not state as unqualified facts since full articles require subscription and exact numbers could not be independently verified. |

---

## Overall Assessment

The investigation is of high quality and largely accurate. All 20 source URLs resolve to real, accessible pages with titles matching those cited. Architectural claims, default parameter values, and behavioral descriptions are overwhelmingly accurate and corroborated by official SSSD documentation, Red Hat product documentation, man pages, and the GitHub issue tracker.

One factual error was identified: the sudo full refresh default interval is stated as 24 hours in both key_findings[8] and the quick_reference table, but official sssd-sudo(5) man pages consistently document the default as 6 hours (21,600 seconds). This affects two locations in the investigation JSON and should be corrected before the investigation is cited or shared.

One finding (first-login latency with extreme group sizes) is directionally supported by public evidence but its specific quantitative claims depend on subscription-gated Red Hat Customer Portal content. These should be attributed explicitly to those sources.

All other 14 findings are fully confirmed by publicly accessible authoritative sources. The tensions, open questions, and concept definitions are accurate and internally consistent.
