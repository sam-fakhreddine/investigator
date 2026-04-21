# Glossary — Kernel Live Patching: RHEL kpatch vs. Oracle Linux Ksplice

Quick definitions of key terms and concepts referenced in this investigation.

---

## ftrace

The kernel's function tracer used by kpatch to redirect execution from original functions to patched versions at runtime.

## Ksplice Enhanced Client

An Oracle Linux extension that allows live patching of critical userspace libraries like glibc and openssl without restarting processes.

## Shadow Variables

A kpatch mechanism used to associate new data with existing kernel structures when the original structure cannot be resized.

## Cumulative by Replacement

A patching model where a new live patch module contains all previous fixes and completely replaces the existing patch module in memory.

---

*Back to: [investigation.md](investigation.md)*
