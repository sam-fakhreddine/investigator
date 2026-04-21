# Glossary — Comprehensive Analysis of Kernel Live Patching Mechanisms and Safety Models

Quick definitions of key terms and concepts referenced in this investigation.

---

## -fentry

A GCC compiler option inserting a call to a profiling function at function entry, providing the hook point for ftrace-based livepatching.

## INT3

The 0xCC opcode used as a software breakpoint to safely manage instruction updates during live code modification.

## klp-build

The modern tool for generating livepatch modules from source diffs in the upstream kernel, replacing legacy kpatch-build.

## objtool

The kernel's binary analysis tool which handles architectural fixups (like ppc64le TOC management) for livepatch modules.

## Pre-Post Differencing

Ksplice's method of identifying code changes by comparing ELF object files generated from original (Pre) and patched (Post) sources.

## 5-byte JMP Trampoline

A relative jump instruction injected at a function entry point by Ksplice to redirect execution to patched code versions.

## Enhanced Client

The Ksplice component responsible for applying rebootless updates to userspace shared libraries like glibc and openssl.

## Universe Model

A tracking mechanism where every task is assigned to either the original or patched code version, ensuring atomicity at the task level.

## Quiescent State

A safe point in task execution, typically a syscall boundary, where task state is stable for patch migration.

## Hybrid Consistency

The integration of kpatch (stack checking) and kGraft (lazy per-task migration) techniques into the upstream Linux livepatching core.

## Shadow Variable

An API associating additional data with existing structures via a hash table keyed by the object address.

---

*Back to: [investigation.md](investigation.md)*
