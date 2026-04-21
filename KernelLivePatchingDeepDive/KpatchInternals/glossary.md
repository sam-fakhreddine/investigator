# Glossary — Red Hat kpatch and Linux Kernel livepatch Internal Mechanics

Quick definitions of key terms and concepts referenced in this investigation.

---

## -fentry

A GCC compiler option that inserts a call to a profiling function (mcount/fentry) at the very beginning of every function, providing an ideal hook point for ftrace and livepatching.

## klp_ftrace_handler

The specific ftrace callback registered by the livepatch subsystem that performs the actual redirection of execution to the patched version of a function.

## INT3

The 0xCC opcode used to trigger a software breakpoint exception, allowing the kernel to safely pause or redirect execution while patching multi-byte instructions.

## klp-build

The modern replacement for kpatch-build as of Linux 6.19, serving as the official tool for generating livepatch modules from source diffs in the upstream kernel.

## objtool

The kernel's binary analysis and manipulation tool, which now handles architectural fixups (like ppc64le TOC management) for livepatch modules, replacing legacy GCC plugins.

## Shadow Variable

An API in the livepatch subsystem that associates additional data with existing data structures via a hash table keyed by the object's memory address.

---

*Back to: [investigation.md](investigation.md)*
