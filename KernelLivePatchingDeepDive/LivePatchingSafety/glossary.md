# Glossary — Kernel Live Patching Safety and Consistency Models

Quick definitions of key terms and concepts referenced in this investigation.

---

## Universe Model

A tracking mechanism where every task is assigned to either the original or the patched version of the code, ensuring atomicity at the task level.

## Quiescent State

A safe point in task execution, typically a syscall boundary or kernel-to-user transition, where the task holds no kernel locks and its state is stable for migration.

## ftrace hooks

The underlying redirection mechanism that uses compiler-generated NOPs at function start to jump to patch code.

## Hybrid Consistency

The integration of kpatch (immediate stack check) and kGraft (lazy per-task migration) techniques into the upstream kernel livepatching core.

---

*Back to: [investigation.md](investigation.md)*
