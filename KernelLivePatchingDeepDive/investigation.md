# Investigation: Comprehensive Analysis of Kernel Live Patching Mechanisms and Safety Models

**Date:** 2026-04-21
**Status:** Complete

---

## Question

> What are the precise internal mechanisms (object-code transformation, ftrace redirection, trampoline injection) and safety/consistency models (quiescent states, stack checking) that power Red Hat kpatch, the Linux livepatch subsystem, and Oracle Ksplice?

---

## Context

This investigation synthesizes findings on the three primary Linux live patching technologies: the upstream Linux livepatch (klp) subsystem (integrating kpatch and kGraft), and Oracle Ksplice. It covers their redirection mechanisms, binary transformation pipelines, and the safety models used to ensure system consistency.

---

## Live Patching Technology Comparison

| Technology | Redirection Mechanism | Transformation Logic | Consistency Model |
| --- | --- | --- | --- |
| Linux livepatch (klp) | ftrace (-fentry) + INT3 | klp-build / objtool (binary diffing) | Hybrid (Universe model + stack checking) |
| Red Hat kpatch | ftrace (-fentry) | kpatch-build (legacy) | Immediate stack checking |
| Oracle Ksplice | 5-byte JMP trampoline | Pre-Post ELF differencing | Stop-the-world (process freezing) |

> As of Linux 6.19, upstream klp has fully integrated klp-build and objtool for binary normalization and fixups.

---

## Key Findings

- Redirection via ftrace vs. Direct JMP: Upstream Linux livepatch (klp) and kpatch leverage the ftrace -fentry profiling site for redirection, using INT3 breakpoints to safely update instructions. Oracle Ksplice uses a 5-byte JMP trampoline at the function entry point, remaining independent of ftrace but requiring coordination to avoid conflicts with tracing tools.
- Transformation Pipelines: Upstream livepatching has migrated to klp-build and objtool (as of Linux 6.19) for extracting binary differences and handling architectural fixups, such as Table of Contents (TOC) pointer reloading on ppc64le. Ksplice uses a 'Pre-Post ELF Differencing' approach that captures all side effects by comparing dual-compiled objects without specialized compiler plugins.
- Consistency and Safety Models: The Linux kernel employs a hybrid consistency model (merging kpatch and kGraft) using a 'Universe' tracking system. This ensures a task never executes a mix of old and new code versions. Safety is enforced through stack checking (requiring HAVE_RELIABLE_STACKTRACE) and migrating tasks at quiescent states such as syscall boundaries.
- Userspace Patching: Oracle Ksplice's Enhanced Client extends rebootless patching to userspace libraries (glibc, openssl). It uses a 'stop-the-world' mechanism (via ptrace or kernel-assisted freezing) to pause processes, map patched code, and apply trampolines, ensuring no application restarts are required for critical security updates.
- Data Structure Extensions: The Linux livepatch subsystem supports 'Shadow Variables,' an RCU-protected hash table mechanism that associates metadata with existing objects without altering their binary layout, enabling complex fixes that require maintaining new state.
- Handling Blocked Tasks: When tasks are blocked in patched functions, transitions can stall. Linux uses 'fake signals' to wake tasks from interruptible sleep to reach quiescent states. Ksplice relies on kernel-assisted freezing to ensure safe transitions during its stop-the-world phase.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| -fentry | A GCC compiler option inserting a call to a profiling function at function entry, providing the hook point for ftrace-based livepatching. |
| INT3 | The 0xCC opcode used as a software breakpoint to safely manage instruction updates during live code modification. |
| klp-build | The modern tool for generating livepatch modules from source diffs in the upstream kernel, replacing legacy kpatch-build. |
| objtool | The kernel's binary analysis tool which handles architectural fixups (like ppc64le TOC management) for livepatch modules. |
| Pre-Post Differencing | Ksplice's method of identifying code changes by comparing ELF object files generated from original (Pre) and patched (Post) sources. |
| 5-byte JMP Trampoline | A relative jump instruction injected at a function entry point by Ksplice to redirect execution to patched code versions. |
| Enhanced Client | The Ksplice component responsible for applying rebootless updates to userspace shared libraries like glibc and openssl. |
| Universe Model | A tracking mechanism where every task is assigned to either the original or patched code version, ensuring atomicity at the task level. |
| Quiescent State | A safe point in task execution, typically a syscall boundary, where task state is stable for patch migration. |
| Hybrid Consistency | The integration of kpatch (stack checking) and kGraft (lazy per-task migration) techniques into the upstream Linux livepatching core. |
| Shadow Variable | An API associating additional data with existing structures via a hash table keyed by the object address. |

---

## Tensions & Tradeoffs

- Reliance on ftrace and -fentry introduces a small overhead for every patched function call, impacting high-frequency paths.
- Binary diffing is highly sensitive to compiler optimizations and section layout changes, potentially leading to extraction failures.
- Immediate patching via stack checking requires architecture-specific reliable stack unwinding, which limits platform support.
- Ksplice's 5-byte JMP trampoline can conflict with other tools (ftrace, kprobes) that modify function entry points.
- Proprietary aspects of Ksplice's Enhanced Client limit external auditability of its safety checks and userspace freezing mechanisms.

---

## Open Questions

- What are the precise performance impacts of shadow variable lookups in critical networking or storage paths?
- How do Ksplice trampolines interact with modern hardware-level Control-Flow Integrity (CFI) features?
- What is the maximum latency measured during Ksplice's stop-the-world phase in high-concurrency database workloads?
- How does live patching impact out-of-tree or proprietary kernel modules that are invisible to objtool?

---

## Sources & References

- [Kernel Livepatching (KLP)](https://www.kernel.org/doc/html/latest/livepatch/livepatch.html)
- [Livepatch Consistency Model](https://www.kernel.org/doc/html/latest/livepatch/consistency-model.html)
- [Ksplice: Automatic Rebootless Kernel Updates](https://www.ksplice.com/doc/ksplice.pdf)
- [Shadow Variables Documentation](https://www.kernel.org/doc/Documentation/livepatch/shadow-vars.txt)
- [Ftrace: The hidden INT3](https://lwn.net/Articles/576443/)
- [A hybrid approach to kernel live patching](https://lwn.net/Articles/633105/)
- [Oracle Ksplice Product Documentation](https://www.oracle.com/linux/ksplice/)
