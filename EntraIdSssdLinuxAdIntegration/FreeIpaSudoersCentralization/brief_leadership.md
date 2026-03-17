# FreeIPA / Red Hat IDM Centralized Sudoers Management — Engineering Leadership Brief

**Date:** 2026-03-17

---

## Headline

> FreeIPA centralizes sudo policy in LDAP with host-group and user-group scoping; SSSD enforces rules locally with a cache that survives IPA server outages

---

## So What

The architecture eliminates per-host /etc/sudoers drift: rules are stored once in 389-DS, replicated across IPA replicas, and pulled to each host by SSSD on a configurable refresh cycle. The local cache provides resilience during network partitions but means rule revocations take up to 6 hours to propagate without cache tuning.

---

## Key Points

- Sudo rules live in cn=sudo,dc=<realm> in FreeIPA 389-DS LDAP and are replicated to all IPA replicas -- no single point of failure for rule storage.
- SSSD on each host caches rules in a local SQLite database; sudo decisions are made against that cache, so the IPA server does not need to be reachable at the moment of each sudo invocation.
- Rules are scoped along three independent axes -- user or user group, host or host group, command or command group -- enabling fine-grained least-privilege policy across the fleet.
- AD-sourced users can receive FreeIPA sudo rules, but only through IPA external groups that map AD SIDs into IPA POSIX groups -- a two-hop indirection that adds operational overhead.
- Using the generic LDAP sudo provider instead of the IPA sudo provider causes group-scoped rules to silently not apply -- a known misconfiguration with no error output.
- Local /etc/sudoers entries shadow LDAP rules by default under files-first nsswitch ordering; full centralization requires purging local sudoers or inverting the nsswitch source order.

---

*Full engineering investigation: [investigation.md](investigation.md)*
