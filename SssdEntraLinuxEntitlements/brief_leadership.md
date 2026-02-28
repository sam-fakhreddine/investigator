# SSSD with Entra ID for Per-User Linux Identity and Group-Based Entitlements on AWS EC2 — Engineering Leadership Brief

**Date:** 2026-02-28

---

## Headline

> SSSD domain join with Entra ID is feasible for replacing shared Linux accounts with per-user identities and group-based entitlements, but every path requires a managed AD intermediary with distinct cost and identity-authority trade-offs.

---

## So What

The SSMRunAs pipeline can be upgraded from shared role accounts to personal usernames with group-derived permissions. Two production-viable paths exist: Entra Domain Services over cross-cloud VPN (~$145+/month, preserves Entra ID as identity source) or AWS Managed Microsoft AD (~$72-288/month, simpler operations but AWS AD becomes the identity source). Both paths provide full group-to-Linux-entitlement flow including sudo, file DAC, and login restriction via SSSD.

---

## Key Points

- SSSD resolves AD groups as native Linux groups; multi-group membership works (e.g., alice in both linux-admins for sudo and linux-dbops for file access). SSM RunAs resolves SSSD users via NSS with no SSM-specific changes needed.
- Path A (Entra Domain Services + VPN) keeps Entra ID as the single identity source but introduces cross-cloud network dependency and Azure running costs. Cloud-only users must change their password once to generate Kerberos hashes.
- Path C (AWS Managed Microsoft AD) is operationally simpler with the directory in-VPC, but Entra Connect Sync only pushes AD-to-Entra, not reverse. A custom sync agent would be needed to keep Entra ID as the user creation point.
- Path D (Azure Arc) avoids managed AD entirely but has an unresolved SSM RunAs sequencing problem: users are created on first SSH login, but SSM needs the user to exist at session start time.
- Audit trail improves from shared-account to individual-user attribution across CloudTrail, SSM session logs, and Linux audit logs. SSSD cache (90-minute default) means revoked entitlements persist locally until TTL expires.

---

## Action Required

> Select between Path A (Entra DS + VPN) and Path C (AWS Managed AD) based on whether Entra ID as sole identity source is a hard requirement or negotiable. Fund a 2-week proof-of-concept on the chosen path using the existing lab environment (vk2ck.onmicrosoft.com tenant, AWS account 326963733675).

---

*Full engineering investigation: [investigation.md](investigation.md)*
