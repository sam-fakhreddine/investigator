# Validation Report: RHEL/Oracle Linux Reboot Detection Mechanisms
Date: 2025-01-24
Validator: Fact Validation Agent

## Summary
- Total sources checked: 4
- Verified: 4 | Redirected: 0 | Dead: 0 | Unverifiable: 0
- Findings checked: 5
- Confirmed: 5 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/LinuxPatchingStrategy/RebootDetectionMechanisms
Field                Status         JSON items   MD items     JSON hash      MD hash       
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        5            5            4d178f633fe3   4d178f633fe3  
tensions             IN_SYNC        2            2            a8a084b6c655   a8a084b6c655  
open_questions       IN_SYNC        2            2            43bc0c986c3b   43bc0c986c3b  
sources              IN_SYNC        4            4            265747fe7f31   265747fe7f31  
concepts             IN_SYNC        4            4            4d639f3606b6   4d639f3606b6  
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | How to check which processes need to be restarted after an update | https://access.redhat.com/solutions/111863 | VERIFIED | Official Red Hat Solution for reboot detection. |
| 2 | DNF5 needs-restarting command reference | https://dnf5.readthedocs.io/en/latest/command_ref/needs-restarting.8.html | VERIFIED | Documentation for the DNF5 version of the tool. |
| 3 | SSM Patch Manager Reboot Options | https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-reboot-options.html | VERIFIED | AWS documentation on RebootIfNeeded vs NoReboot. |
| 4 | Oracle Linux Ksplice User Guide | https://docs.oracle.com/en/operating-systems/oracle-linux/ksplice/user-guide.html | VERIFIED | Official guide for Ksplice in-memory patching. |

## Finding Verification

### Finding: Mechanism of `needs-restarting`
- **Claim:** `needs-restarting` identifies necessary reboots by scanning `/proc/[PID]/maps` for entries marked as `(deleted)`, which occurs when a library (e.g., .so) or executable is replaced on disk but still mapped in a running process's memory.
- **Verdict:** CONFIRMED
- **Evidence:** External research confirms the tool scans `/proc/*/maps` for the `(deleted)` string to find unlinked files still held in memory by running processes.
- **Source used:** https://access.redhat.com/solutions/111863; https://baeldung.com/linux/check-processes-need-restarted

### Finding: RHEL 8/9 implementation
- **Claim:** RHEL 8 and 9 utilize a Python-based DNF4 plugin for `needs-restarting`. This version is slower than its successor and relies on hardcoded lists of 'critical' packages to suggest a full system reboot.
- **Verdict:** CONFIRMED
- **Evidence:** In RHEL 8/9, `needs-restarting` is part of `yum-utils` (or `dnf-utils`) and is implemented as a Python script. For the `-r` flag, it checks a hardcoded list of packages (kernel, glibc, systemd, etc.).
- **Source used:** Inspection of `/usr/bin/needs-restarting` on RHEL systems; https://ansible.com/blog/red-hat-enterprise-linux-patching-automation

### Finding: RHEL 10 and DNF5
- **Claim:** RHEL 10 introduces DNF5 (written in C++), which features a native `needs-restarting` implementation. It is significantly faster, provides `--json` output, and integrates with `systemd` soft-reboots and `reboot_suggested` advisory metadata.
- **Verdict:** CONFIRMED
- **Evidence:** DNF5 is written in C++, includes `needs-restarting` as a built-in command, supports `--json`, and uses `reboot_suggested` metadata from advisories rather than a hardcoded list. It also integrates with systemd's soft-reboot functionality.
- **Source used:** https://dnf5.readthedocs.io/en/latest/command_ref/needs-restarting.8.html

### Finding: Oracle Linux Ksplice Awareness
- **Claim:** Oracle Linux leverages Ksplice technology to apply patches to the kernel and core libraries in-memory. However, `needs-restarting -r` is NOT natively aware of these in-memory patches and will still report a reboot as required if a newer kernel package exists on disk.
- **Verdict:** CONFIRMED
- **Evidence:** `needs-restarting -r` compares the booted kernel version with the highest version available on disk. Ksplice patches in-memory without updating the `uname -r` version string or the on-disk kernel package state in a way that `needs-restarting` recognizes, leading to false positives. `uptrack-show` is required for accuracy.
- **Source used:** https://docs.oracle.com/en/operating-systems/oracle-linux/ksplice/user-guide.html

### Finding: AWS SSM Patch Manager Compliance
- **Claim:** In AWS SSM Patch Manager, selecting `NoReboot` avoids immediate downtime but causes the instance to be flagged as 'Non-Compliant' with an `InstalledPendingReboot` status until a manual reboot and subsequent scan are completed.
- **Verdict:** CONFIRMED
- **Evidence:** AWS documentation and user reports confirm that `NoReboot` results in an `InstalledPendingReboot` status for patches, which rolls up to an overall `Non-Compliant` status for the node until a reboot and rescan occur.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-reboot-options.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| None | N/A | No remediation required. |

## Overall Assessment
The investigation is highly accurate and technically sound. All key findings regarding the evolution of reboot detection from RHEL 8 to RHEL 10, the specific limitations of standard tools on Oracle Linux when using Ksplice, and the compliance implications of SSM Patch Manager configurations have been verified against official documentation and technical specifications. The investigation can be trusted as a baseline for patching strategy decisions.
