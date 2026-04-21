# RHEL vs Oracle Linux Patching and Kernel Divergence — Engineering Leadership Brief

**Date:** 2026-04-20

---

## Headline

> Oracle Linux provides superior live-patching depth but requires distinct operational workflows for security compliance.

---

## So What

Managing a dual-distro fleet increases configuration complexity in AWS SSM and introduces variable security windows due to advisory timing gaps.

---

## Key Points

- Ksplice offers zero-downtime updates for glibc and openssl on Oracle Linux, significantly reducing reboot requirements compared to RHEL.
- Separate SSM Patch Manager baselines are technically mandatory due to divergent vendor metadata (RHSA vs ELSA).
- UEK provides earlier access to modern kernel features (Kernel 6.12) but mandates independent validation from standard RHEL-certified stacks.

---

## Action Required

> Decide whether to standardize on Ksplice for the entire OL fleet or maintain a unified patching policy that accepts RHEL's reboot requirements.

---

*Full engineering investigation: [investigation.md](investigation.md)*
