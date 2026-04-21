# RHEL vs Oracle Linux Patching and Kernel Divergence — Product Brief

**Date:** 2026-04-20
**Risk Level:** MEDIUM

---

## What Is This?

> Updates for Oracle Linux and Red Hat must be managed separately to ensure security and system uptime.

---

## What Does This Mean for Us?

System maintenance for Oracle Linux can often happen without turning services off, while Red Hat systems usually need a restart for similar updates.

---

## Key Points

- Oracle Linux allows 'invisible' security updates for critical components like web security (openssl) without stopping the application.
- There is a small delay in receiving some security updates on Oracle Linux compared to Red Hat.
- Automated tools used to manage these systems must be configured specifically for each type of Linux to avoid reporting errors.

---

## Next Steps

**PO/EM Decision:**

> Review the uptime requirements for critical services to determine if Oracle Linux's live-patching features justify the multi-vendor management overhead.

**Engineering Work Items:**
- Create separate SSM Patch Baselines for RHEL and Oracle Linux in all AWS accounts.
- Verify application performance on UEK 8 (Kernel 6.12) for core product services.

---

## Open Questions

- How much downtime could we avoid annually by leveraging Ksplice user-space patching?
- Are there any legacy applications that strictly require the RHEL-Compatible Kernel (RHCK)?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
