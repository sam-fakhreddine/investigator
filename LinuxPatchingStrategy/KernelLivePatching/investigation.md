# Investigation: Kernel Live Patching: RHEL kpatch vs. Oracle Linux Ksplice

**Date:** 2025-05-15
**Status:** Complete

---

## Question

> Compare RHEL live patching via `kpatch` (Red Hat's implementation) with Oracle Linux live patching via `Ksplice` (Unbreakable Enterprise Kernel), including architectural differences, subscription requirements (e.g., Premier support), CVE class live-patchability constraints (e.g., scheduler, driver, data structures), support windows per kernel version (RHEL 8/9/10), cumulative in-memory state behavior, and SSM Patch Manager integration for compliance reporting.

---

## Context

This investigation was prompted by the need to understand the technical and operational trade-offs between RHEL and Oracle Linux live-patching frameworks for enterprise compliance and uptime strategies.

---

## Quick Reference

| Feature | RHEL kpatch | Oracle Linux Ksplice |
| --- | --- | --- |
| Architecture | ftrace-based function redirection | Object-code level transformation |
| Scope | Kernel-space only | Kernel and Userspace (glibc, openssl) |
| Support Window | 6 months per kernel errata | Full Premier Support (up to 10 years) |
| Memory Model | Cumulative by replacement | Persistent accumulation |
| Subscription | Standard/Premium (included) | Premier Support (required) |
| SSM Integration | Native via kpatch-patch packages | Standard package-based orchestration |

> RHEL requires kernel rotation every 6 months to maintain live patch coverage, whereas Ksplice supports individual kernels for their entire lifecycle.

---

## Key Findings

- kpatch (RHEL) utilizes ftrace to redirect function calls to patched versions, whereas Ksplice (Oracle) operates at the object-code layer using a run-time linker to apply binary diffs.
- RHEL live patches for a specific kernel version are only provided for 6 months; maintaining coverage requires rebooting into a new baseline kernel at least twice a year.
- Oracle Linux Ksplice provides live patches for the entire Premier Support window (up to 10 years) for both UEK and RHCK, significantly reducing the frequency of required reboots.
- Both platforms are limited by 'quiescent' functions: code that is always on the stack (like the scheduler) or complex drivers with hardware-state dependencies are often unpatchable.
- CVEs requiring changes to existing data structure sizes or layouts are generally not live-patchable without reboots, though kpatch uses 'Shadow Variables' to mitigate some state-change limitations.
- SSM Patch Manager typically reports compliance based on the on-disk kernel version; live-patched kernels may appear non-compliant in default reports unless custom inventory scripts are used.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| ftrace | The kernel's function tracer used by kpatch to redirect execution from original functions to patched versions at runtime. |
| Ksplice Enhanced Client | An Oracle Linux extension that allows live patching of critical userspace libraries like glibc and openssl without restarting processes. |
| Shadow Variables | A kpatch mechanism used to associate new data with existing kernel structures when the original structure cannot be resized. |
| Cumulative by Replacement | A patching model where a new live patch module contains all previous fixes and completely replaces the existing patch module in memory. |

---

## Tensions & Tradeoffs

- Uptime vs. Baseline Drift: While Ksplice allows 10 years of uptime, the running kernel may drift significantly from the on-disk baseline, complicating troubleshooting and disaster recovery.
- Compliance Reporting: Security scanners often flag 'Effective Kernel' as vulnerable because they check the on-disk version rather than the in-memory state, leading to false-negative audit results.

---

## Open Questions

- What is the exact performance overhead of Ksplice userspace patching (Enhanced Client) compared to standard library execution?
- How do RHEL 10's live patching support windows differ from the 8/9 model as the OS matures?

---

## Sources & References

- [Livepatch — The Linux Kernel documentation](https://www.kernel.org/doc/html/latest/livepatch/livepatch.html)
- [Applying patches with kernel live patching - RHEL 8](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/applying-patches-with-kernel-live-patching_managing-monitoring-and-updating-the-kernel)
- [Oracle Linux: Ksplice User's Guide](https://docs.oracle.com/en/operating-systems/oracle-linux/ksplice-user/)
- [Using Kernel Live Patching on managed nodes](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-kernel-live-patching.html)
