# FreeIPA / Red Hat IDM Centralized Sudoers Management — Product Brief

**Date:** 2026-03-17
**Risk Level:** MEDIUM

---

## What Is This?

> FreeIPA sudo centralization is production-ready for RHEL fleets but has four known gaps affecting completeness: local shadowing, AD-user mapping complexity, cache lag on revocation, and silent provider misconfiguration

---

## What Does This Mean for Us?

Teams adopting FreeIPA for sudo centralization get a well-supported LDAP-backed policy store with offline enforcement and full sudoers feature parity, but must actively manage four risks that undermine centralization completeness without triggering visible errors.

---

## Key Points

- FreeIPA sudo rules support the full sudoers feature set: NOPASSWD, RunAs user/group, command negation, time-boxed rules, and sudoOrder-based precedence.
- Command groups (ipaSudoCmdGrp) allow reusable command collections across rules -- equivalent to Cmnd_Alias in local sudoers but stored in LDAP and managed via the IPA API.
- SSSD sudo cache refresh is tunable: the default smart refresh is 15 minutes for expiring entries, but the default full refresh is 6 hours, meaning revoked rules can remain active on cached hosts without a manual cache flush.
- Non-RHEL distributions (Debian, Ubuntu) lack native package support for the sssd-ipa sudo provider, increasing integration risk for mixed-OS fleets.
- The sssctl sudo-check tool enables pre-flight verification of effective sudo policy for a user without requiring an actual sudo attempt -- useful for audit and change-verification workflows.

---

## Next Steps

**PO/EM Decision:**

> Determine whether the fleet includes non-RHEL hosts or AD-sourced users that require sudo access, as both scenarios require additional architecture decisions before committing to FreeIPA sudo centralization.

**Engineering Work Items:**
- Audit current /etc/sudoers content across the fleet to identify rules that need migration and entries that would conflict with centralization under files-first nsswitch ordering
- Inventory all Linux hosts not enrolled in IPA or running non-RHEL distributions to scope the coverage gap
- Map AD-sourced users or groups that require sudo access and define the IPA external group structure needed to bridge them into FreeIPA sudo rules
- Define acceptable cache-lag tolerance for sudo rule revocation and decide whether sudo_cache_timeout tuning or a documented manual cache-flush procedure is required

**Leadership Input Required:**

> Decide whether the up-to-3-hour maximum cache lag for rule revocation is acceptable for the organization security posture, or whether a shorter TTL with increased IPA server query load is preferred.

---

## Open Questions

- Which Linux distributions are in the fleet, and which hosts are already IPA-joined with sudo_provider=ipa configured vs the generic ldap provider?
- Are there hosts with local /etc/sudoers content that would shadow centrally managed rules under the default files-first nsswitch ordering?
- Have any AD-sourced users been granted sudo access via IPA external groups, and is that SID-to-group mapping kept in sync with AD group changes?
- What is the current sudo_cache_timeout configuration across enrolled hosts, and is there a documented emergency cache-flush procedure for immediate rule revocation?
- Is sssctl sudo-check used in any audit or deployment pipeline to verify effective sudo policy before changes go live?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
