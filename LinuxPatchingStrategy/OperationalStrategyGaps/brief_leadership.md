# Tiered Linux Patching Strategy on EC2 — Engineering Leadership Brief

**Date:** 2026-04-21

---

## Headline

> Tiered patching on EC2 requires balancing live-patching uptime with infrastructure consistency.

---

## So What

Live patching reduces reboots but introduces 'reboot debt' and licensing complexities that can lead to configuration drift and operational instability if not managed via node replacement.

---

## Key Points

- Live patching support windows vary by version; while RHEL 8/9 use a 6-month window, RHEL 10 extends this to 1 year for mainstream and AWS-optimized kernels.
- Oracle Ksplice on EC2 requires Premier Support (Paid) and is not available via standard marketplace images for free.
- EKS nodes should prioritize AMI replacement over in-place patching to maintain immutability and prevent drift.
- Technical constraints prevent live-patching CVEs affecting core data structures or assembly code.

---

## Action Required

> Standardize on immutable node replacement as the primary patching mechanism, using live patching only as an emergency bridge for critical CVEs.

---

*Full engineering investigation: [investigation.md](investigation.md)*
