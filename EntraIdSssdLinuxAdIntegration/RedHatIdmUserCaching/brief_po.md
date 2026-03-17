# Red Hat IDM and SSSD User/Credential Caching Architecture — Product Brief

**Date:** 2026-03-17
**Risk Level:** HIGH

---

## What Is This?

> SSSD identity caching on Linux hosts has well-known failure modes that produce login delays or complete login failures all caused by identifiable configurable gaps in the default setup

---

## What Does This Mean for Us?

Linux hosts using Red Hat IDM/FreeIPA authenticate through SSSD, which maintains a local cache of user identity data. The default configuration is conservative: offline auth is disabled, no users are pre-loaded into cache, and nothing prevents first-login cold-cache latency. Users experience failures when the IDM server is unreachable (because offline auth is off) or slow logins when they belong to large groups (because group membership resolution blocks login). These are known, documented, and configurable but require deliberate choices with security and operational tradeoffs.

---

## Key Points

- If the IDM server goes offline, users cannot log in by default; this is a business continuity risk for any Linux host that relies on IDM for authentication
- First login for any user is always a live directory query with no cache warmup; users in large groups (thousands of members) have documented login times of 2-10 minutes
- The local cache TTL is 90 minutes by default, meaning identity changes (password resets, account disables) do not propagate to hosts until the cache expires or is manually flushed
- Sudo rule changes can take up to 15 minutes (smart refresh) or 6 hours (full refresh) to reach hosts, so privilege escalation changes are not instant
- The IPA provider caches access policy (HBAC) locally, meaning access rules survive brief outages, but if HBAC refresh is tuned aggressively this adds per-login latency

---

## Next Steps

**PO/EM Decision:**

> Prioritize an audit of SSSD configuration on production Linux hosts to determine current offline auth posture and confirm cache TTL settings are aligned with business continuity and security requirements

**Engineering Work Items:**
- Audit all production SSSD configurations for cache_credentials setting and document which hosts have offline auth enabled vs disabled
- Identify users or services logging into hosts with large group memberships and measure actual first-login latency in production
- Review current entry_cache_timeout and entry_cache_nowait_percentage values against the 90-minute default and assess whether they match the IDM server SLA
- Determine whether sudo rule propagation delay (up to 6 h for full refresh) is acceptable for privileged access changes, or whether manual cache invalidation procedures are needed

**Leadership Input Required:**

> Decision required on offline auth policy: enabling cache_credentials improves availability but stores a password hash on each Linux host disk; this is a security posture choice that needs explicit sign-off

---

## Open Questions

- Is cache_credentials currently enabled on production RHEL hosts enrolled in IDM, and if not, what is the plan if IDM becomes unreachable?
- What is the largest group membership any user in our environment has, and has login latency for those users been measured?
- Is entry_cache_nowait_percentage configured to prevent blocking logins when cache entries expire, or are users potentially experiencing blocking waits at the 90-minute cache cycle?
- How quickly does an account disable in IDM propagate to prevent login on enrolled RHEL hosts, and is it bounded by the cache TTL?
- Are sudo rule changes critical enough to require manual sss_cache invalidation, or is the 15-minute smart refresh interval acceptable?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
