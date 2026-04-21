# Optimal Weekly Patching Strategy for RHEL and Oracle Linux on EC2 — Engineering Leadership Brief

**Date:** 2024-05-24

---

## Headline

> Standardize on a tiered auto-approval strategy with live-patching and scheduled node replacement to balance security and uptime.

---

## So What

Reliance on live-patching without reboots creates 'reboot debt' and compliance reporting gaps that can mask actual security risks and increase recovery complexity.

---

## Key Points

- Implement a 7/14/30 day auto-approval delay for Security, Bugfix, and Enhancement patches respectively to automate the majority of updates.
- Utilize kpatch for RHEL (mandatory reboot every 6-12 months) and Ksplice for Oracle Linux (supports critical userspace patching).
- Adopt RHEL 10's DNF5 and soft-reboot features to minimize maintenance downtime during mandatory system restarts.
- Prioritize immutable node replacement (AMI swap) for EKS and stateless tiers to eliminate configuration drift and 'snowflake' nodes.

---

## Action Required

> Establish a maximum 'Reboot Debt' threshold (e.g., 180 days) for all stateful EC2 instances to ensure periodic baseline synchronization.

---

*Full engineering investigation: [investigation.md](investigation.md)*
