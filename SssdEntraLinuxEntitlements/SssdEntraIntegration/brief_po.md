# Entra ID as an Identity Source for Linux SSSD on AWS EC2 Instances — Product Brief

**Date:** 2026-02-28
**Risk Level:** MEDIUM

---

## What Is This?

> Using Entra ID as the single source for Linux server logins on AWS requires deploying an additional directory service -- there is no direct plug-and-play integration.

---

## What Does This Mean for Us?

The team cannot simply point Linux servers at Entra ID for logins. An intermediary service must be deployed and maintained, adding monthly cost ($110-290) and either a network link between AWS and Azure, or accepting that a separate directory in AWS becomes the primary user store for Linux access.

---

## Key Points

- Entra ID by itself does not speak the protocols that Linux servers use for user logins (LDAP and Kerberos).
- The most architecturally clean path (Entra Domain Services + VPN) keeps Entra ID as the master user list but requires a persistent network tunnel between AWS and Azure.
- The operationally simplest path (AWS Managed AD) puts the user directory inside AWS but means the Linux user list is no longer directly managed in Entra ID.
- There is an experimental path using Azure Arc that avoids extra directories entirely, but it has a known compatibility gap with the existing SSM session access system.
- All paths require a proof-of-concept in the lab environment before production commitment.

---

## Next Steps

**PO/EM Decision:**

> Choose between Entra-ID-as-source (Path A, higher cost and complexity) and AWS-Managed-AD-as-source (Path C, simpler operations but split identity authority). Allocate lab time for a proof-of-concept sprint.

**Engineering Work Items:**
- Stand up Entra Domain Services in the dev tenant and establish a site-to-site VPN to the AWS lab VPC (Path A PoC).
- Deploy an Amazon Linux 2023 EC2 instance, join it to the Entra DS domain via SSSD, and validate SSM RunAs with a directory user.
- If Path C is preferred, deploy AWS Managed Microsoft AD (Standard) and test SSSD domain join with SSM RunAs.
- Investigate the Azure Arc + AADSSHLoginForLinux path to determine if SSM RunAs user pre-provisioning can be automated.

**Leadership Input Required:**

> Architecture decision needed: is Entra ID as the single identity source a hard requirement, or is it acceptable for AWS Managed AD to be the Linux identity source with Entra Connect Sync pushing users to Entra ID for cloud SSO?

---

## Open Questions

- What is the monthly cost difference between the Entra Domain Services path and the AWS Managed AD path, including VPN and compute for sync agents?
- If we go with AWS Managed AD, how do we keep Linux usernames and Entra ID identities in sync without manual effort?
- Can we prototype the Azure Arc path quickly to test whether SSM RunAs works with Arc-created users?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
