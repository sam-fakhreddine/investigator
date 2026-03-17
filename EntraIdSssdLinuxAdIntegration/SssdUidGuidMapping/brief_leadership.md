# SSSD UID/GID Mapping: ID Mapping vs POSIX Attributes (AD and Entra ID) — Engineering Leadership Brief

**Date:** 2026-03-17

---

## Headline

> SSSD UID mapping has two modes with different fleet-consistency guarantees; pure cloud Entra ID requires a different stack entirely

---

## So What

The default SSSD behavior (algorithmic ID mapping from AD SIDs) achieves cross-node UID consistency without directory preparation, but breaks silently in multi-domain forests without an explicit configuration pin. POSIX-attribute mode provides a hard UID guarantee but requires directory population work that Microsoft tooling no longer makes easy. Pure cloud Entra ID is not compatible with either traditional mode — it requires SSSD 2.11+ idp provider or Himmelblau.

---

## Key Points

- ID-mapping mode (default): SID-to-UID translation is deterministic on single-domain fleets; multi-domain fleets need ldap_idmap_default_domain_sid pinned in sssd.conf and deployed uniformly via config management or UID drift occurs silently
- POSIX-attribute mode: only mode with a hard cross-node UID guarantee; requires populating uidNumber/gidNumber on every AD object (IDMU GUI removed in WS2016; use PowerShell or tooling)
- Pure Entra ID (cloud-only) cannot use the ad provider at all — SSSD 2.11+ idp provider or Himmelblau is required; both have known UID-collision or consistency caveats that need evaluation before fleet adoption
- Microsoft supported path for POSIX attributes in Entra-centric environments routes through an on-premises LDAP proxy (ECMA2 connector) — organizations wanting to eliminate on-prem infrastructure hit a contradiction here

---

## Action Required

> If the fleet is migrating toward Entra ID, evaluate the UID-consistency guarantees of SSSD idp provider vs. Himmelblau schema extensions before committing to a mapping mode — the choice affects NFS, shared filesystems, and any system relying on stable UID/GID across nodes.

---

*Full engineering investigation: [investigation.md](investigation.md)*
