# SSSD UID/GID Mapping: ID Mapping vs POSIX Attributes (AD and Entra ID) — Product Brief

**Date:** 2026-03-17
**Risk Level:** MEDIUM

---

## What Is This?

> SSSD UID/GID mapping mode is an infrastructure decision with security and stability implications across the entire Linux fleet

---

## What Does This Mean for Us?

How Linux hosts translate cloud or AD identities to POSIX user IDs affects file ownership, NFS access, sudo rules, and audit logs. Getting this wrong produces silent mismatches — a user on two different nodes appears as different owners of the same file — which creates both security and compliance risk. The choice of mapping mode must be made once and applied uniformly across the fleet before onboarding users.

---

## Key Points

- Two modes exist: auto-generate UIDs from the AD SID (no directory prep needed, some multi-domain risk) vs. read UIDs from directory attributes (guaranteed consistency, requires attribute population on every user and group object)
- Pure cloud Entra ID forces a third path: SSSD 2.11+ idp provider or Himmelblau — neither has the same operational maturity as the AD provider, and both carry documented UID-collision or consistency caveats
- Microsoft deprecated the IDMU GUI for managing POSIX attributes in 2016 — populating uidNumber/gidNumber at scale now requires PowerShell scripting or third-party tooling, adding engineering effort to the POSIX-attribute mode option
- Fleet centralization of UID mapping relies on consistent sssd.conf deployment (Ansible/Puppet); one misconfigured node with a wrong id_range silently generates different UIDs for the same user, not an authentication error

---

## Next Steps

**PO/EM Decision:**

> Prioritize a decision on UID mapping mode before any fleet expansion or Entra ID migration begins; this decision is difficult to reverse once UIDs are assigned and files are owned.

**Engineering Work Items:**
- Engineering: audit current sssd.conf across fleet for id_range and ldap_idmap_default_domain_sid consistency
- Engineering: evaluate SSSD 2.11 idp provider vs. Himmelblau for Entra ID pure-cloud environments, specifically testing UID reproducibility across node reimages
- Engineering: document the UID range configured on each domain and validate no overlap exists between algorithmic UIDs and any locally allocated system UIDs
- Engineering: if POSIX-attribute mode is selected, design the PowerShell or tooling workflow for populating uidNumber/gidNumber on AD objects at scale, including a process for new user onboarding

**Leadership Input Required:**

> Confirm whether the fleet is expected to remain on on-premises AD, migrate to Entra ID, or support a hybrid mix — this determines which mapping mode and tooling stack is viable and scopes the engineering effort.

---

## Open Questions

- Do any of our Linux nodes currently use different id_range values in sssd.conf, and have we ever observed UID mismatches across nodes?
- Are any shared filesystems (NFS, CIFS, EFS, GPFS) in use that would be affected by UID changes if we switch mapping modes?
- Is SSSD 2.11+ already deployed on our fleet, or would supporting the idp provider require an OS-level upgrade?
- Has anyone evaluated whether Himmelblau schema extension approach is compatible with our Entra ID tenant application registration policies?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
