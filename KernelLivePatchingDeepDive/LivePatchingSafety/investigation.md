# Investigation: Kernel Live Patching Safety and Consistency Models

**Date:** 2026-04-21
**Status:** Complete

---

## Question

> Deep dive into the safety and consistency models of kernel live patching. Explain how the kernel ensures a patch is safely applied using quiescent states, stack checking, and consistency models (e.g., kpatch vs kGraft). What happens when a task is blocked while executing a function that needs patching?

---

## Context

This investigation explores the technical mechanisms that allow the Linux kernel to apply code patches at runtime without rebooting, focusing on the safety protocols that prevent kernel panics or inconsistent states during the transition.

---

## Kernel Live Patching Safety Mechanisms

| Mechanism | Description | Safety Role |
| --- | --- | --- |
| Hybrid Consistency | Per-task migration between 'universes' | Ensures no task sees partial patches |
| Stack Checking | Inspects sleeping task call stacks | Verifies it's safe to flip a blocked task's state |
| Quiescent States | Migration at syscall exit/entry | Provides safe points for task state transitions |
| Fake Signals | Waking tasks from interruptible sleep | Forces progress for tasks blocked in syscalls |

---

## Key Findings

- The Linux kernel livepatching (klp) subsystem employs a hybrid consistency model that merges kpatch's stack checking with kGraft's per-task lazy migration.
- A 'Universe' model is used to track patch state; each task is either in the 'old' or 'new' universe and never executes a mix of both versions during a single execution flow.
- Redirection to patched functions is implemented via ftrace and -fentry hooks, allowing the kernel to intercept calls at the function entry point.
- Stack checking relies on the HAVE_RELIABLE_STACKTRACE feature and objtool to ensure that a sleeping task is not currently executing any function targeted for patching before migrating its state.
- Tasks that are blocked in interruptible sleep are woken up using 'fake signals' to encourage them to reach a quiescent state (like a syscall boundary) where migration can safely occur.
- If a task remains blocked in a patched function indefinitely, the transition is stalled; administrators can monitor progress via sysfs and manually cancel the transition if necessary.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Universe Model | A tracking mechanism where every task is assigned to either the original or the patched version of the code, ensuring atomicity at the task level. |
| Quiescent State | A safe point in task execution, typically a syscall boundary or kernel-to-user transition, where the task holds no kernel locks and its state is stable for migration. |
| ftrace hooks | The underlying redirection mechanism that uses compiler-generated NOPs at function start to jump to patch code. |
| Hybrid Consistency | The integration of kpatch (immediate stack check) and kGraft (lazy per-task migration) techniques into the upstream kernel livepatching core. |

---

## Tensions & Tradeoffs

- Immediate patching via stack checking provides faster transitions but requires architecture-specific reliable stack unwinding, which is not available on all platforms.
- Forcing a patch transition (bypassing safety checks) can resolve stuck transitions but permanently disables safe module unloading to prevent potential panics.

---

## Open Questions

- How do out-of-order execution and memory barriers impact the reliability of ftrace hooks during high-concurrency function entry?
- What is the specific impact of live patching on proprietary or out-of-tree kernel modules that may not be visible to objtool?

---

## Sources & References

- [Livepatch — The Linux Kernel documentation](https://www.kernel.org/doc/html/latest/livepatch/livepatch.html)
- [Livepatch Consistency Model](https://www.kernel.org/doc/html/latest/livepatch/consistency-model.html)
- [A hybrid approach to kernel live patching](https://lwn.net/Articles/633105/)
