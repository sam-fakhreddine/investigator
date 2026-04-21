# Investigation: RHEL/Oracle Linux Reboot Detection Mechanisms

**Date:** 2024-05-23
**Status:** Complete

---

## Question

> How do `needs-restarting` and `yum-utils`/`dnf-utils` work on RHEL/Oracle Linux (proc maps, deleted library detection via /proc/*/maps) to identify necessary reboots and service restarts, and how do they differ across RHEL 8, 9, and 10? How does the SSM Patch Manager `RebootOption` (`RebootIfNeeded` vs `NoReboot`) parameter impact operational compliance state?

---

## Context

Investigating the internal mechanics of reboot detection on enterprise Linux distributions and their integration with AWS SSM Patch Manager for compliance reporting.

---

## Reboot Detection & SSM Compliance Summary

| Component | Mechanism / Implementation | Operational Impact |
| --- | --- | --- |
| needs-restarting | Scans /proc/[PID]/maps for '(deleted)' shared library segments | Identifies processes running on outdated code in-memory |
| RHEL 8 / 9 | DNF4 (Python) plugin using static 'critical' package lists | Conservative reboot hints; slower execution than DNF5 |
| RHEL 10 | DNF5 (C++) with advisory metadata and systemd integration | Faster, supports JSON output and systemd 'soft-reboots' |
| Oracle Linux | Ksplice in-memory patching + uptrack-show | needs-restarting -r is NOT Ksplice-aware; reports reboot if new RPM is on disk |
| SSM NoReboot | Postpones activation of patched components and kernel | Leaves instance in 'Non-Compliant' (InstalledPendingReboot) state |

---

## Key Findings

- `needs-restarting` identifies necessary reboots by scanning `/proc/[PID]/maps` for entries marked as `(deleted)`, which occurs when a library (e.g., .so) or executable is replaced on disk but still mapped in a running process's memory.
- RHEL 8 and 9 utilize a Python-based DNF4 plugin for `needs-restarting`. This version is slower than its successor and relies on hardcoded lists of 'critical' packages to suggest a full system reboot.
- RHEL 10 introduces DNF5 (written in C++), which features a native `needs-restarting` implementation. It is significantly faster, provides `--json` output, and integrates with `systemd` soft-reboots and `reboot_suggested` advisory metadata.
- Oracle Linux leverages Ksplice technology to apply patches to the kernel and core libraries (like `glibc` and `openssl`) in-memory. However, `needs-restarting -r` is NOT natively aware of these in-memory patches and will still report a reboot as required if a newer kernel package exists on disk. To confirm the 'effective' kernel version and avoid unnecessary reboots, specialized tools like `uptrack-show --available` or `ksplice-show` must be used instead of standard DNF/YUM utilities.
- In AWS SSM Patch Manager, the `RebootOption` parameter directly impacts compliance reporting. Selecting `NoReboot` avoids immediate downtime but causes the instance to be flagged as 'Non-Compliant' with an `InstalledPendingReboot` status until a manual reboot and subsequent scan are completed.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| needs-restarting | A tool from yum-utils/dnf-utils that determines if a system or specific services need to be restarted after package updates by analyzing process memory maps. |
| Ksplice | An Oracle Linux technology that allows for patching the kernel and key userspace libraries (glibc, openssl) without requiring a system reboot. |
| systemd soft-reboot | A RHEL 10/systemd feature that restarts userspace without a full hardware/kernel reboot, reducing downtime for updates that do not affect the kernel. |
| InstalledPendingReboot | An AWS SSM compliance status indicating that patches are installed but the instance requires a reboot to become 'Compliant' in the console. |

---

## Tensions & Tradeoffs

- Uptime vs. Compliance: Postponing reboots (SSM NoReboot) maintains availability but results in technical non-compliance and security risk due to inactive patches.
- Automation vs. Precision: RHEL 8/9 static lists are simple but may over- or under-recommend reboots compared to RHEL 10's metadata-driven approach.

---

## Open Questions

- How do third-party repositories (e.g., EPEL, NVIDIA) currently format metadata to leverage RHEL 10's native reboot suggestions?
- What is the specific overhead of DNF5's memory scanning on high-PID-count systems compared to DNF4?

---

## Sources & References

- [How to check which processes need to be restarted after an update](https://access.redhat.com/solutions/111863)
- [DNF5 needs-restarting command reference](https://dnf5.readthedocs.io/en/latest/command_ref/needs-restarting.8.html)
- [SSM Patch Manager Reboot Options](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-reboot-options.html)
- [Oracle Linux Ksplice User Guide](https://docs.oracle.com/en/operating-systems/oracle-linux/ksplice/user-guide.html)
