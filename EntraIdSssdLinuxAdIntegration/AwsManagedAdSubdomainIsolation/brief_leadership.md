# AWS Managed AD Subdomain Namespace: Forest Isolation and Identity Boundaries — Engineering Leadership Brief

**Date:** 2026-03-17

---

## Headline

> AWS Managed AD with a subdomain name is a separate AD forest — not a child domain — with hard boundaries on what crosses the trust

---

## So What

Teams assuming aws.corp.example.com inherits corp identity data (users, POSIX attributes, GPOs) via the naming convention are building on a false premise. Authentication can cross the trust; directory data cannot. Linux identity (UID/GID) must be provisioned in the AWS forest or the architecture must shift to Hybrid Edition.

---

## Key Points

- AWS Managed AD always creates a new forest — subdomain naming is cosmetic and does not establish a child-domain relationship with corp AD
- Forest trust enables Kerberos authentication referrals for corp users on AWS-joined Linux hosts, but no objects replicate across the trust
- POSIX attributes (UID/GID) stored in corp AD are invisible to SSSD on aws.corp.example.com-joined hosts — this is a concrete blocker for Linux workload identity
- AD Connector cannot solve this: it is a proxy only and cannot host a domain join target for Linux
- Hybrid Edition (GA August 2025) is the only AWS-managed option that avoids the cross-forest problem by extending the on-premises domain into AWS — but it requires on-premises DC registration via SSM and a 2012 R2+ functional level
- Schema extensions are supported on AWS Managed AD via LDIF, but apply only to the aws.corp.example.com forest independently from corp AD

---

## Action Required

> Audit whether Linux workloads relying on corp AD POSIX attributes have a viable attribute provisioning path in the AWS forest, or escalate the Hybrid Edition feasibility assessment.

---

*Full engineering investigation: [investigation.md](investigation.md)*
