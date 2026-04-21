# Kernel Live Patching: RHEL kpatch vs. Oracle Linux Ksplice — Engineering Leadership Brief

**Date:** 2025-05-15

---

## Headline

> RHEL live patching requires reboots every 6 months, while Oracle Linux Ksplice supports the full 10-year lifecycle.

---

## So What

Oracle Linux offers superior uptime for critical kernels, but RHEL's model ensures closer alignment with tested baselines at the cost of biannual reboots.

---

## Key Points

- RHEL kpatch is limited to kernel-space; Ksplice can patch userspace libraries like glibc and openssl.
- Ksplice requires Premier Support ($$) whereas kpatch is included in Standard/Premium RHEL subscriptions.
- Compliance reporting in SSM remains a friction point as standard scans typically ignore in-memory patch state.

---

## Action Required

> Evaluate whether the operational benefit of userspace patching and 10-year kernel longevity justifies the cost of Oracle Premier Support.

---

*Full engineering investigation: [investigation.md](investigation.md)*
