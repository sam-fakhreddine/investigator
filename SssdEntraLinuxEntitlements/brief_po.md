# SSSD with Entra ID for Per-User Linux Identity and Group-Based Entitlements on AWS EC2 — Product Brief

**Date:** 2026-02-28
**Risk Level:** MEDIUM

---

## What Is This?

> Each person can get their own Linux server login with permissions automatically controlled by their Entra ID group memberships, replacing shared accounts that hide who did what.

---

## What Does This Mean for Us?

Today multiple people share the same Linux accounts (admin, developer, oracle), making audit impossible and creating security risk if one credential leaks. This investigation confirms the technology works to give each person a unique login where their permissions -- admin access, database file access, which servers they can reach -- come automatically from the groups assigned to them in the company directory. Two practical deployment paths exist, each with different cost and management trade-offs.

---

## Key Points

- A person in both the admins and dbops groups automatically gets both admin (sudo) and database file access on the same server, with no manual per-user setup on each machine.
- All session activity is logged under the individual's name instead of a shared account, providing full audit trail for compliance and incident investigation.
- The existing SSM Session Manager workflow does not change for end users; they still connect the same way but land as themselves instead of a shared account.
- Two deployment options: one keeps the Entra ID directory as the single source of truth (higher cost, approximately $145+/month for the intermediary service and network link), the other puts a directory inside AWS (lower cost, simpler operations, but user management splits across two systems).
- When someone is removed from a group in the directory, their permissions update on the servers within 90 minutes. For emergencies, the cache on specific servers can be force-cleared.

---

## Next Steps

**PO/EM Decision:**

> Decide whether Entra ID must remain the single identity source (Path A, higher cost) or whether splitting identity management across Entra ID and AWS AD is acceptable (Path C, simpler operations). Approve lab time for a proof-of-concept sprint on the chosen path.

**Engineering Work Items:**
- Engineering team to deploy the chosen directory service (Entra Domain Services or AWS Managed AD) in the lab environment and establish network connectivity.
- Engineering team to domain-join a test Amazon Linux 2023 EC2 instance using realmd and SSSD, and validate personal username login.
- Engineering team to create 4 AD security groups (linux-admins, linux-developers, linux-dbops, linux-readonly), assign test users to multiple groups, and validate that sudo and file permissions work correctly.
- Engineering team to validate SSM RunAs with SSSD-resolved personal usernames and confirm individual-user attribution in CloudTrail and session logs.
- Engineering team to document the fleet management approach for deploying SSSD configuration and sudoers rules to new EC2 instances at scale.

**Leadership Input Required:**

> Architecture decision required: is Entra ID as the sole identity source a hard requirement (choose Path A with higher cost and cross-cloud VPN), or is it acceptable for an AWS-hosted directory to manage Linux identities with Entra ID handling cloud SSO only (choose Path C with simpler operations)?

---

## Open Questions

- What is the total monthly cost difference between Path A (Entra Domain Services + VPN) and Path C (AWS Managed AD), including all infrastructure components?
- If a person's access needs to be revoked immediately (e.g., offboarding), how quickly can the engineering team force-remove their permissions from all servers?
- How long will the proof-of-concept take, and can the existing lab environment (dev tenant and AWS account) support it without additional procurement?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
