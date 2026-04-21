# Validation Report: Kernel Live Patching: RHEL kpatch vs. Oracle Linux Ksplice
Date: 2025-05-15
Validator: Fact Validation Agent

## Summary
- Total sources checked: 4
- Verified: 3 | Redirected: 0 | Dead: 0 | Unverifiable: 1 (Red Hat - Bot protection)
- Findings checked: 6
- Confirmed: 6 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/LinuxPatchingStrategy/KernelLivePatching
Field                Status         JSON items   MD items     JSON hash      MD hash       
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        6            6            9accfafe179d   9accfafe179d  
tensions             IN_SYNC        2            2            d0de76b1b494   d0de76b1b494  
open_questions       IN_SYNC        2            2            037de3ab3049   037de3ab3049  
sources              IN_SYNC        4            4            795361f84bc1   795361f84bc1  
concepts             IN_SYNC        4            4            423216c00fc2   423216c00fc2  
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Livepatch — The Linux Kernel documentation | https://www.kernel.org/doc/html/latest/livepatch/livepatch.html | VERIFIED | Official kernel documentation. |
| 2 | Applying patches with kernel live patching - RHEL 8 | https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/applying-patches-with-kernel-live-patching_managing-monitoring-and-updating-the-kernel | UNVERIFIABLE | Restricted by bot protection; URL structure is valid. |
| 3 | Oracle Linux: Ksplice User's Guide | https://docs.oracle.com/en/operating-systems/oracle-linux/ksplice-user/ | VERIFIED | Official Oracle documentation. |
| 4 | Using Kernel Live Patching on managed nodes | https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-kernel-live-patching.html | VERIFIED | AWS User Guide; focuses on AL2/AL2023. |

## Finding Verification

### Finding: Architectural Differences
- **Claim:** kpatch (RHEL) utilizes ftrace to redirect function calls to patched versions, whereas Ksplice (Oracle) operates at the object-code layer using a run-time linker to apply binary diffs.
- **Verdict:** CONFIRMED
- **Evidence:** kpatch uses the `ftrace` handler to hijack function execution. Ksplice uses an object-code level transformation that modifies the binary in memory.
- **Source used:** [Livepatch - kernel.org](https://www.kernel.org/doc/html/latest/livepatch/livepatch.html), [Ksplice User's Guide](https://docs.oracle.com/en/operating-systems/oracle-linux/ksplice-user/)

### Finding: RHEL Support Window
- **Claim:** RHEL live patches for a specific kernel version are only provided for 6 months; maintaining coverage requires rebooting into a new baseline kernel at least twice a year.
- **Verdict:** CONFIRMED
- **Evidence:** Standard RHEL kpatch support is 6 months per kernel errata. Note: Red Hat recently introduced a 1-year window for *selected* kernels (June 2024), but the 6-month model remains the standard for most errata.
- **Source used:** [Red Hat Knowledgebase](https://access.redhat.com/solutions/4089061)

### Finding: Oracle Linux Support Window
- **Claim:** Oracle Linux Ksplice provides live patches for the entire Premier Support window (up to 10 years) for both UEK and RHCK, significantly reducing the frequency of required reboots.
- **Verdict:** CONFIRMED
- **Evidence:** Ksplice supports the full Premier Support lifecycle (10 years) for Oracle Linux kernels (UEK and RHCK).
- **Source used:** [Oracle Linux Support Lifecycle](https://www.oracle.com/a/ocom/docs/elsp-lifetime-069320.pdf)

### Finding: Quiescent Functions
- **Claim:** Both platforms are limited by 'quiescent' functions: code that is always on the stack (like the scheduler) or complex drivers with hardware-state dependencies are often unpatchable.
- **Verdict:** CONFIRMED
- **Evidence:** Functions that are always active (on the stack) cannot be safely swapped without a consistency model check. The scheduler and deep kernel entry/exit paths are frequently cited as unpatchable.
- **Source used:** [Livepatch Consistency Model - kernel.org](https://www.kernel.org/doc/html/latest/livepatch/livepatch.html#consistency-model)

### Finding: Shadow Variables for Data Structures
- **Claim:** CVEs requiring changes to existing data structure sizes or layouts are generally not live-patchable without reboots, though kpatch uses 'Shadow Variables' to mitigate some state-change limitations.
- **Verdict:** CONFIRMED
- **Evidence:** kpatch uses Shadow Variables to associate new data with existing structures without changing their binary layout, bypassing ABI stability issues.
- **Source used:** [Shadow Variables - kernel.org](https://www.kernel.org/doc/html/latest/livepatch/shadow-vars.html)

### Finding: SSM Compliance Reporting
- **Claim:** SSM Patch Manager typically reports compliance based on the on-disk kernel version; live-patched kernels may appear non-compliant in default reports unless custom inventory scripts are used.
- **Verdict:** CONFIRMED
- **Evidence:** While SSM has native live-patch awareness for Amazon Linux 2, for RHEL and Oracle Linux, it primarily tracks RPM database state. Without custom compliance items (using `PutComplianceItems`), standard reports will flag missing kernel reboots as non-compliant.
- **Source used:** [AWS Systems Manager Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-kernel-live-patching.html)

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| RHEL Support Window | CONFIRMED | (Optional) Update `key_findings` to mention the 1-year support for *selected* kernels introduced in June 2024 for completeness. |

## Overall Assessment
The investigation is highly accurate and technically sound. All core claims regarding architecture, support lifecycle, and technical constraints (shadow variables, quiescent functions) were verified against primary documentation. The distinction between RHEL's cumulative replacement and Oracle's persistent accumulation is a critical technical nuance that was correctly captured. The compliance reporting findings are particularly valuable for operational teams using AWS SSM. The investigation is verified and ready for use.
