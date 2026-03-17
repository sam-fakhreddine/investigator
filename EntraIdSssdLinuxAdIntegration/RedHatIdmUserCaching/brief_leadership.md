# Red Hat IDM and SSSD User/Credential Caching Architecture — Engineering Leadership Brief

**Date:** 2026-03-17

---

## Headline

> SSSD caches identity data locally on each Linux host but offline auth and cache warm-up require explicit configuration choices with meaningful tradeoffs

---

## So What

By default, SSSD serves user identity data from a local LDB cache (90-minute TTL) and handles brief directory outages silently. However, the offline password cache is off by default, enumeration is off by default, and large group memberships cause well-documented first-login latency spikes. The IPA provider (FreeIPA/Red Hat IDM) is architecturally richer than vanilla LDAP: it caches HBAC access policy and sudo rules locally, making access control decisions available even when the server is briefly unreachable.

---

## Key Points

- The LDB on-disk cache holds all fetched identity objects; entries expire after 90 minutes by default and are refreshed on-demand by the backend process when a lookup arrives
- Offline authentication (login when IDM is unreachable) requires cache_credentials = true and is off by default, meaning users cannot log in at all if the server is down without this setting
- First-login for any user not yet in cache requires a live directory query; large or nested group memberships during that query are the primary documented cause of multi-minute login delays
- The IPA provider caches HBAC access policy (not just identity), so access enforcement remains active even briefly offline; this capability is not available with a generic LDAP backend
- Sudo rule caching uses independent smart (15-min) and full (24-h) refresh cycles; each sudo invocation also checks per-user rule freshness, adding a small per-command latency

---

## Action Required

> Determine whether offline credential caching (cache_credentials) is enabled in the current SSSD deployment and whether entry_cache_nowait_percentage is configured to avoid blocking logins on cache expiry

---

*Full engineering investigation: [investigation.md](investigation.md)*
