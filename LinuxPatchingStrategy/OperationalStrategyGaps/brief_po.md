# Tiered Linux Patching Strategy on EC2 — Product Brief

**Date:** 2026-04-21
**Risk Level:** MEDIUM

---

## What Is This?

> Patching Linux servers without reboots has hidden costs and limits.

---

## What Does This Mean for Us?

While we can fix some security bugs without restarting, we cannot fix everything this way. Deferring restarts for too long creates risk for future maintenance windows.

---

## Key Points

- Major security fixes sometimes still require a full restart if they touch the core of the system.
- Special paid subscriptions are needed for zero-downtime patching on Oracle Linux in AWS.
- The best way to keep our systems healthy is to replace them with fresh, updated versions rather than patching them in place.
- RHEL 10 supports zero-downtime features from day one, with an extended 1-year support window for mainstream kernels.

---

## Next Steps

**PO/EM Decision:**

> Decide whether the cost of Oracle Premier Support is justified for zero-downtime glibc/OpenSSL patching.

**Engineering Work Items:**
- Validate RHEL BYOS vs Marketplace cost implications for kpatch usage.
- Audit current EKS clusters for 'snowflake' nodes that have been patched in-place instead of replaced.

**Leadership Input Required:**

> Confirm if the 6-to-12 month reboot window (depending on RHEL version) aligns with the organizational compliance policy.

---

## Open Questions

- How often are we currently performing full reboots versus live patching?
- Do we have a process to track CVEs that cannot be live-patched?
- Are we using immutable node replacement for our EKS clusters?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
