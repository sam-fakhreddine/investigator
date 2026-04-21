# Red Hat kpatch and Linux Kernel livepatch Internal Mechanics — Engineering Leadership Brief

**Date:** 2026-04-21

---

## Headline

> Kernel livepatching moves to a more integrated upstream model with klp-build and objtool as of Linux 6.19.

---

## So What

By transitioning to klp-build and leveraging objtool for architectural fixups, the livepatching pipeline is more robust and better aligned with core kernel build processes.

---

## Key Points

- Leverages standard ftrace infrastructure, ensuring broad compatibility with modern Linux kernels.
- Uses INT3 breakpoint mechanics to prevent instruction corruption during live code modification.
- Supports data structure extensions via shadow variables, allowing complex fixes without breaking existing binary interfaces.
- klp-build automates the extraction of binary differences into deployable modules, replacing kpatch-build.

---

## Action Required

> Evaluate the transition to Linux 6.19+ to benefit from the more stable klp-build and objtool-based livepatching pipeline.

---

*Full engineering investigation: [investigation.md](investigation.md)*
