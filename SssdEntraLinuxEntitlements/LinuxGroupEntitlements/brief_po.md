# Linux Group Entitlements from Entra ID via SSSD — Product Brief

**Date:** 2026-02-28
**Risk Level:** MEDIUM

---

## What Is This?

> Each person can get their own Linux login with permissions controlled by their Entra ID group memberships, replacing shared accounts.

---

## What Does This Mean for Us?

Today, multiple people share the same Linux accounts (admin, developer, oracle), making it impossible to tell who did what. This investigation confirms that the technology exists to give each person a unique login where their permissions come automatically from the groups they belong to in the company directory.

---

## Key Points

- A person in both the admins and dbops groups automatically gets both sudo (admin) access and database file access on the same server, with no manual per-user setup needed.
- Login access to specific servers can be restricted by group: only dbops members can connect to database servers, only developers to dev servers.
- All session activity is logged under the individual's name, providing full audit trail for compliance.
- Permissions update automatically when someone is added to or removed from a group in Entra ID, with up to 90 minutes cache delay.
- The existing SSM Session Manager workflow does not change for end users; they still connect the same way but land as themselves instead of a shared account.

---

## Next Steps

**PO/EM Decision:**

> Approve the proof-of-concept scope: 4 Entra groups mapped to Linux entitlements on 2-3 test EC2 instances. Decide whether Entra Domain Services cost (approximately $109/month as of early 2025; verify current pricing) is acceptable for the test environment.

**Engineering Work Items:**
- Set up network connectivity between AWS VPC and directory service (Entra DS or on-prem AD DS)
- Domain-join a test Amazon Linux 2023 EC2 instance using realmd and SSSD
- Create 4 AD security groups (linux-admins, linux-developers, linux-dbops, linux-readonly) and assign test users
- Deploy sudoers rules and validate multi-group entitlements for a single test user
- Validate SSM RunAs with SSSD-resolved usernames and confirm audit log content

**Leadership Input Required:**

> Architecture decision needed on directory intermediary: Entra Domain Services (managed, Azure-hosted, ongoing cost) versus on-premises AD DS (self-managed, existing infrastructure if available). This affects networking, cost, and operational complexity.

---

## Open Questions

- How long does it take for a group membership change in Entra ID to be reflected on a Linux host? What is the worst-case delay?
- If we need to emergency-revoke someone's access, can we force-clear the SSSD cache on target hosts?
- What happens if the directory service goes down? Can people still log in with cached credentials, and for how long?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
