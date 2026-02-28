# Entra ID as an Identity Source for Linux SSSD on AWS EC2 Instances — Engineering Leadership Brief

**Date:** 2026-02-28

---

## Headline

> Entra ID cannot serve as a direct SSSD identity source for Linux; every viable path requires a managed Active Directory intermediary or the Azure Arc agent framework, each with distinct cost and operational trade-offs.

---

## So What

Replacing local Linux users with directory-sourced accounts requires deploying either Entra Domain Services (Azure-hosted, ~$110+/mo, requires cross-cloud VPN) or AWS Managed Microsoft AD (AWS-hosted, $72-288/mo, no VPN but inverts identity authority away from Entra ID). The Azure Arc path avoids managed AD entirely but has an unresolved compatibility issue with SSM Session Manager RunAs.

---

## Key Points

- Base Entra ID lacks LDAP and Kerberos, so SSSD cannot use it directly -- an intermediary managed AD or Arc agent is required in all paths.
- Entra Domain Services + cross-cloud VPN (Path A) preserves Entra ID as identity source but introduces network dependency and Azure running costs (~$145+/mo for DS + VPN).
- AWS Managed Microsoft AD (Path C) keeps the directory in-VPC with no cross-cloud dependency for Linux auth, but Entra Connect Sync only pushes from AD to Entra ID, not reverse -- making AWS Managed AD the de facto identity source.
- Azure Arc with AADSSHLoginForLinux (Path D) is the only path using Entra ID directly, but it creates local users on first SSH login, conflicting with SSM RunAs which needs the user to exist before session start.
- UID consistency across EC2 fleet requires pinning the domain SID in sssd.conf or managing explicit POSIX attributes in whichever AD is used. Entra DS Enterprise/Premium SKUs now support custom attributes, but these are string-typed extensions, not RFC 2307 POSIX attributes.

---

## Action Required

> Decide whether to accept Entra Domain Services cost and cross-cloud VPN complexity (Path A) to keep Entra ID as the identity source, or accept AWS Managed AD as the directory source of truth (Path C) for operational simplicity. Prototype the chosen path in the lab environment before committing.

---

*Full engineering investigation: [investigation.md](investigation.md)*
