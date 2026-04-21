# Kernel Live Patching Safety and Consistency Models — Engineering Leadership Brief

**Date:** 2026-04-21

---

## Headline

> Kernel live patching provides a safe, reboot-less update path through a robust per-task consistency model.

---

## So What

Reliable runtime patching reduces downtime for critical security fixes but depends on specific hardware support for reliable stack traces.

---

## Key Points

- Upstream klp uses a hybrid of kpatch and kGraft to balance transition speed and safety.
- Patching requires HAVE_RELIABLE_STACKTRACE support; unsupported architectures revert to slower, less reliable methods.
- Blocked tasks are the primary cause of stalled patches, requiring operational monitoring of the transition state.

---

## Action Required

> Ensure production kernels are compiled with CONFIG_LIVEPATCH and objtool support to enable these safety features.

---

*Full engineering investigation: [investigation.md](investigation.md)*
