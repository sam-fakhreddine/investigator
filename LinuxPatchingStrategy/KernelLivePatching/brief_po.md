# Kernel Live Patching: RHEL kpatch vs. Oracle Linux Ksplice — Product Brief

**Date:** 2025-05-15
**Risk Level:** MEDIUM

---

## What Is This?

> Choosing between RHEL and Oracle Linux impacts how often systems must restart for security updates.

---

## What Does This Mean for Us?

RHEL systems must restart twice a year for security, while Oracle Linux systems can theoretically run for years without interruption, though at a higher subscription cost.

---

## Key Points

- RHEL keeps security fixes free but forces a restart every 6 months to stay current.
- Oracle Linux can fix major security holes in web servers and databases without a restart.
- Both systems still require restarts for hardware changes or very complex security fixes that cannot be patched 'live'.
- Security reports may incorrectly show the system is unpatched even after a live fix is applied.

---

## Next Steps

**PO/EM Decision:**

> Decide if 'Zero Downtime' is a high-priority requirement for the product's SLA.

**Engineering Work Items:**
- Assess the cost difference between RHEL Premium and Oracle Premier Support.
- Identify critical applications that benefit from glibc/openssl live patching.

**Leadership Input Required:**

> Architects should confirm if the current SSM Patch Manager setup can be customized to report 'Effective Kernel' compliance.

---

## Open Questions

- How often do we currently restart for kernel updates?
- Do our security scanners recognize live patches, or do we have a reporting gap?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
