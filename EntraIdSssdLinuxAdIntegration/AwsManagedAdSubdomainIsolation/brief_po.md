# AWS Managed AD Subdomain Namespace: Forest Isolation and Identity Boundaries — Product Brief

**Date:** 2026-03-17
**Risk Level:** HIGH

---

## What Is This?

> Linux identity on AWS-joined hosts cannot rely on corp AD attributes across the trust — a data provisioning gap exists that blocks Linux workload delivery

---

## What Does This Mean for Us?

The naming convention aws.corp.example.com gives the appearance of tight integration with corp AD, but the two forests are isolated. Engineering cannot automatically inherit UID/GID or group memberships across the trust for Linux hosts. This must be resolved before Linux workloads that depend on corp identities can function correctly.

---

## Key Points

- Trust enables corp users to log into AWS-joined Linux hosts via Kerberos — authentication works, identity attribute lookup does not
- POSIX attributes (UID, GID, home dir, shell) must exist in the aws.corp.example.com forest or be replicated to its Global Catalog — neither happens automatically
- GPOs from corp AD do not apply to machines in the AWS forest — each forest manages its own policies
- AD Connector is not a solution for Linux: it is a proxy with no domain-hosting capability
- Hybrid Edition resolves forest isolation entirely but is a different product with on-premises prerequisites and a separate evaluation track
- Any resolution path requires engineering effort: either POSIX attribute provisioning in the AWS forest, or Hybrid Edition migration, or a winbind/IPA-based alternative to SSSD

---

## Next Steps

**PO/EM Decision:**

> Determine which Linux workloads require corp AD POSIX attributes and set a deadline for the identity provisioning decision.

**Engineering Work Items:**
- Engineering spike: evaluate POSIX attribute provisioning options in aws.corp.example.com forest (manual, synced via script, or via AWS Managed AD LDIF schema extension)
- Engineering spike: assess Hybrid Edition feasibility against on-premises DC and functional-level prerequisites
- Engineering: document which SSSD configurations are needed to support cross-forest authentication for corp users on AWS-joined hosts
- Engineering: validate that the forest trust direction (one-way vs two-way) meets requirements for all AWS services in scope (not just EC2 Linux)

**Leadership Input Required:**

> Decision on Hybrid Edition requires alignment between cloud platform team and on-premises AD operations team — leadership should facilitate that conversation.

---

## Open Questions

- Which Linux workloads today depend on corp AD UID/GID attributes, and what happens to those workloads if those attributes are not visible from the AWS forest?
- Is the on-premises AD functional level at Windows Server 2012 R2 or higher, and are there two on-premises DCs available to register with SSM for Hybrid Edition?
- Is the current trust configured as one-way or two-way, and have all AWS services in scope been validated against their trust-direction requirements?
- What is the plan for POSIX attribute lifecycle management if attributes must be maintained independently in both the corp and AWS forests?
- Has SSSD's cross-forest authentication been tested end-to-end on an AWS-joined Linux host with a corp AD user, including group membership resolution?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
