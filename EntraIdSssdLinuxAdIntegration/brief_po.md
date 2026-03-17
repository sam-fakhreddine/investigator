# Entra ID and SSSD Linux Identity Integration: End-to-End Architecture — Product Brief

**Date:** 2026-03-17
**Risk Level:** HIGH

---

## What Is This?

> Linux identity integration has identifiable, configurable gaps at each of four pipeline layers — all carrying medium-to-high risk that is not surfaced by authentication success alone

---

## What Does This Mean for Us?

Linux hosts successfully authenticating against AD or Entra ID does not imply the identity pipeline is functioning correctly. Group-scoped sudo rules may be silently dropped, users may be receiving different UIDs on different hosts, offline login may be impossible, and corp identity attributes may be invisible to AWS-joined hosts. None of these conditions produce visible errors at authentication time — they manifest as file-ownership mismatches, privilege gaps, outage-time login failures, and identity provisioning blockers discovered under operational pressure.

---

## Key Points

- UID mapping mode must be decided once and deployed uniformly before fleet expansion — switching modes after files are owned by algorithmically-generated UIDs requires a coordinated UID migration across all shared filesystems
- FreeIPA sudo centralization is incomplete unless the sudo provider is explicitly set to ipa, local /etc/sudoers is purged or nsswitch order is inverted, and the IPA external group structure for AD users is maintained in sync with AD group changes
- Offline auth requires cache_credentials = true to be useful — without it, any IDM server outage (planned or not) produces complete login failures on all enrolled Linux hosts, a direct business continuity risk
- AWS Managed AD POSIX attribute gap blocks Linux workload delivery for corp users on AWS-joined hosts — this must be resolved before those workloads can function; options are POSIX attribute re-provisioning in the AWS forest, Hybrid Edition adoption, or architectural shift to winbind/IPA+trust
- Sudo rule revocation after a privilege escalation incident takes up to 6 hours under default cache settings — if immediate revocation is a security requirement, a documented manual sss_cache invalidation procedure and runbook must exist before an incident occurs

---

## Next Steps

**PO/EM Decision:**

> Prioritize three decisions before any fleet expansion or Entra ID migration: (1) UID mapping mode selection with fleet-wide consistency plan, (2) offline auth policy (cache_credentials on/off) with explicit security sign-off, (3) AWS forest POSIX attribute provisioning path or Hybrid Edition feasibility assessment.

**Engineering Work Items:**
- Engineering: audit sssd.conf across all production hosts for ldap_id_mapping, ldap_idmap_default_domain_sid, sudo_provider, and cache_credentials settings
- Engineering: inventory all hosts with local /etc/sudoers content that would shadow IPA-managed rules and define a migration plan
- Engineering: measure first-login latency for users in the largest AD groups in the environment and determine whether ignore_group_members or entry_cache_nowait_percentage tuning is required
- Engineering spike: assess AWS Managed AD Hybrid Edition feasibility against on-premises DC functional level and SSM registration prerequisites
- Engineering: define the emergency sudo revocation runbook (sss_cache -G on all enrolled hosts) and validate it works end-to-end before an incident requires it
- Engineering: evaluate SSSD 2.11 idp provider vs Himmelblau for any Entra ID pure-cloud environments, specifically testing UID reproducibility across node reimages and documenting collision behavior

**Leadership Input Required:**

> Three decisions require explicit leadership sign-off: (1) offline auth policy — enabling cache_credentials stores password hashes on host disks, a security posture choice; (2) Hybrid Edition adoption — requires cross-team alignment between cloud platform and on-premises AD operations; (3) acceptable sudo revocation lag — the 6-hour default may not meet security policy for privileged access management.

---

## Open Questions

- Do all nodes in the fleet share the same id_range and ldap_idmap_default_domain_sid in sssd.conf, and have we ever observed UID mismatches across nodes on shared filesystems?
- Is sudo_provider=ipa (not ldap) explicitly configured on all IPA-enrolled hosts, and has it been verified that group-scoped sudo rules are actually applying in production?
- Is cache_credentials enabled, and if not, what is the documented plan for Linux host logins during an IDM server outage?
- Which Linux workloads in AWS depend on corp AD UID or GID attributes, and what happens to those workloads today given the forest isolation constraint?
- Is there a runbook for immediate sudo rule revocation that does not rely on waiting for the 6-hour full cache refresh cycle?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
