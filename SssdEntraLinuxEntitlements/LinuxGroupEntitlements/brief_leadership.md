# Linux Group Entitlements from Entra ID via SSSD — Engineering Leadership Brief

**Date:** 2026-02-28

---

## Headline

> SSSD enables per-user Linux entitlements derived from Entra ID group memberships, eliminating shared accounts while preserving file permission and sudo models.

---

## So What

Replacing shared role-based Linux accounts with personal usernames and group-based entitlements closes an audit gap (individual accountability) and reduces blast radius of credential compromise. The technical path is well-established but requires a directory service intermediary between Entra ID and Linux.

---

## Key Points

- SSSD resolves AD groups as native Linux groups; a user in multiple AD groups gets all corresponding Linux entitlements simultaneously (sudo, file access, login restriction).
- SSM RunAs works with SSSD-resolved users because the SSM agent uses the id command which respects NSS/SSSD. No SSM-specific changes needed beyond the username tag.
- Audit trail improves: CloudTrail captures the federated identity, session logs capture commands under the personal OS username, and Linux audit logs attribute actions to individual UIDs.
- Key prerequisite: Entra ID groups must flow through Entra Domain Services or synced on-prem AD DS, since SSSD requires LDAP/Kerberos protocols that Entra ID alone does not expose.
- Main risk is GID consistency: if existing file systems use specific group IDs (e.g., oracle data files), algorithmic ID mapping will not match them. Explicit POSIX attributes or file re-ownership would be needed.

---

## Action Required

> Decide on the directory intermediary (Entra Domain Services vs on-prem AD DS) and the network path from AWS VPCs to that directory, as this is the critical path prerequisite for all subsequent work.

---

*Full engineering investigation: [investigation.md](investigation.md)*
