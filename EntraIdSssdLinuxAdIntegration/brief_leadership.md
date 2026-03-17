# Entra ID and SSSD Linux Identity Integration: End-to-End Architecture — Engineering Leadership Brief

**Date:** 2026-03-17

---

## Headline

> Linux identity against AD or Entra ID is a four-layer pipeline where each layer has a silent default failure mode — the combined risk is higher than any single sub-system suggests

---

## So What

The pipeline runs UID/GID mapping -> FreeIPA sudo policy -> SSSD caching -> AD forest topology. Each layer has at least one default that works correctly in small, single-domain, on-premises deployments and fails silently at scale or in AWS: ID mapping drifts in multi-domain forests, the wrong SSSD sudo provider drops group rules without logging, offline auth is disabled by default, and AWS Managed AD is a separate forest despite looking like a child domain. These defaults compound — a fleet can appear functional while silently failing on group-scoped sudo rules, serving stale identity data, and having no path to resolve corp UID attributes in AWS.

---

## Key Points

- UID consistency requires an explicit configuration decision (ID mapping mode vs POSIX attributes) and is not guaranteed by SSSD defaults in multi-domain forests — the ldap_idmap_default_domain_sid pin must be deployed uniformly via config management or UID drift occurs silently
- FreeIPA sudo centralization has four silent gap vectors: wrong provider type (ldap instead of ipa), local /etc/sudoers shadowing LDAP rules, up to 6-hour revocation propagation lag, and a two-hop AD group indirection that breaks if IPA external group membership is not kept in sync with AD
- SSSD offline auth (cache_credentials) is off by default — users cannot log in at all during IDM outages; large-group memberships cause cold-cache login latency of 2-10 minutes on first login; both require deliberate configuration choices with documented tradeoffs
- AWS Managed AD with a subdomain name (aws.corp.example.com) is a separate AD forest — POSIX attributes stored in the corporate forest are not visible to SSSD on AWS-joined hosts; Hybrid Edition (GA August 2025) is the only AWS-managed path that eliminates this constraint
- Pure cloud Entra ID requires a different SSSD provider stack (idp, SSSD 2.11+) or Himmelblau — the ad provider is incompatible; both alternatives carry UID consistency caveats weaker than the traditional AD provider

---

## Action Required

> Commission an audit of current sssd.conf across the fleet covering: ldap_id_mapping mode and domain_sid pin, sudo_provider type, cache_credentials state, and entry_cache_nowait_percentage. Results will surface which of the four silent failure modes are currently active in production.

---

*Full engineering investigation: [investigation.md](investigation.md)*
