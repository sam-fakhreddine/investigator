# Investigation: Red Hat kpatch and Linux Kernel livepatch Internal Mechanics

**Date:** 2026-04-21
**Status:** Complete

---

## Question

> Deep dive into the internal mechanics of Red Hat kpatch and the Linux kernel livepatch subsystem. Explain the exact mechanism of function redirection using ftrace and INT3 instructions, how klp-build (replacing kpatch-build) creates payload modules, and how objtool handles architectural fixups (replacing GCC plugins).

---

## Context

Red Hat kpatch and the Linux livepatch subsystem provide a rebootless patching mechanism for the running kernel. This investigation details the function redirection mechanism, the modern klp-build compilation pipeline, and the management of architectural fixups via objtool.

---

## Quick Reference

| Mechanism | Description | Key Technology |
| --- | --- | --- |
| Function Redirection | Intercepts function calls at the -fentry site to redirect execution to patched code. | ftrace (klp_ftrace_handler) |
| Instruction Update | Safely modifies running code by replacing instructions with breakpoints. | INT3 (0xCC opcode) |
| Module Creation | Extracts binary differences between original and patched kernels into ELF objects. | klp-build / objtool |
| Data Extension | Associates metadata with existing objects via an RCU-protected hash table. | Shadow Variables |

---

## Key Findings

- The Linux livepatch subsystem leverages the ftrace profiling infrastructure to intercept and redirect function execution. By registering a ftrace_ops handler (klp_ftrace_handler) at a function's -fentry call site, the subsystem modifies the instruction pointer (IP) on the stack, causing the CPU to jump directly to the patched function body.
- Instruction modification on a live system is performed using the INT3 (breakpoint) mechanism. Ftrace replaces the first byte of a call site with the 0xCC opcode; CPUs hitting this trigger a breakpoint exception handler that safely manages the redirection or waits for instruction updates to complete, avoiding issues with multi-byte instruction modification.
- As of Linux 6.19 (Feb 2026), the legacy kpatch-build pipeline has been superseded by klp-build for upstream kernel livepatching. klp-build generates patch modules through a dual-compilation process of original and patched kernel sources using -ffunction-sections and -fdata-sections, extracting changed sections and their relocations into a standalone patch module.
- Architectural fixups and binary normalization, previously handled by GCC plugins in the kpatch-build pipeline, have migrated to objtool in the upstream kernel. On architectures like ppc64le, objtool now manages Table of Contents (TOC) pointer reloading (r2 register) and other necessary fixups when transitioning between original and patched function contexts.
- Shadow variables provide a mechanism for extending kernel data structures without altering their binary layout. New metadata is stored in a global, RCU-protected hash table (klp_shadow_hash) and associated with the original object's pointer, allowing patches to track new state while maintaining structure size compatibility.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| -fentry | A GCC compiler option that inserts a call to a profiling function (mcount/fentry) at the very beginning of every function, providing an ideal hook point for ftrace and livepatching. |
| klp_ftrace_handler | The specific ftrace callback registered by the livepatch subsystem that performs the actual redirection of execution to the patched version of a function. |
| INT3 | The 0xCC opcode used to trigger a software breakpoint exception, allowing the kernel to safely pause or redirect execution while patching multi-byte instructions. |
| klp-build | The modern replacement for kpatch-build as of Linux 6.19, serving as the official tool for generating livepatch modules from source diffs in the upstream kernel. |
| objtool | The kernel's binary analysis and manipulation tool, which now handles architectural fixups (like ppc64le TOC management) for livepatch modules, replacing legacy GCC plugins. |
| Shadow Variable | An API in the livepatch subsystem that associates additional data with existing data structures via a hash table keyed by the object's memory address. |

---

## Tensions & Tradeoffs

- The reliance on ftrace and -fentry introduces a small overhead for every patched function call, which may be significant in high-frequency execution paths.
- Binary diffing is sensitive to compiler optimizations and section layout changes, which can lead to larger patch modules or extraction failures if not carefully managed.
- Shadow variables introduce an additional lookup step (hash table access) when accessing extended state, unlike native structure fields which are fixed offsets.

---

## Open Questions

- What are the precise performance impacts of shadow variable lookups in critical networking or storage paths?
- How does the livepatch consistency model (stack checking) impact system responsiveness during the transition period of a large patch?
- Are there specific GCC versions or optimization flags that significantly degrade the efficiency of klp-build?

---

## Sources & References

- [Kernel Livepatching (KLP)](https://www.kernel.org/doc/html/latest/livepatch/livepatch.html)
- [Ftrace: The hidden INT3](https://lwn.net/Articles/576443/)
- [Shadow Variables Documentation](https://www.kernel.org/doc/Documentation/livepatch/shadow-vars.txt)
- [kpatch: dynamic kernel patching](https://github.com/dynup/kpatch)
