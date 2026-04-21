# Investigation: Optimal Weekly Patching Strategy for RHEL and Oracle Linux on EC2

**Date:** 2024-05-24
**Status:** Complete

---

## Question

> What is the documented optimal weekly patching strategy for RHEL 8/9/10 and Oracle Linux EC2 fleets that maximizes security compliance while minimizing reboots via SSM Patch Manager and Kernel Live Patching?

---

## Context

Synthesis of specialized investigations into reboot detection, live patching, distribution divergence, SSM configuration, and operational gaps for enterprise Linux fleets on AWS.

---

## Optimal Patching Strategy Summary

| Component | RHEL 8/9/10 (Optimal) | Oracle Linux 8/9 (Optimal) |
| --- | --- | --- |
| Approval Delay | 7d (Security) / 14d (Bugfix) | 7d (Security) / 14d (Bugfix) |
| Live Patching | kpatch (Kernel space only) | Ksplice (Kernel + glibc/openssl) |
| Reboot Cycle | Mandatory 6-12 months | Optional (Up to 10 years) |
| SSM Baseline | Filter: RHSA / RHBA | Filter: ELSA / ELBA |
| Reboot Option | RebootIfNeeded / NoReboot (HA) | RebootIfNeeded / NoReboot (HA) |
| Detection Tool | needs-restarting (DNF4/5) | ksplice-show / uptrack-show |

> RHEL 10 extends the kpatch window to 1 year; Oracle Ksplice requires Premier Support for userspace patching.

---

## Key Findings

- The documented optimal strategy utilizes a tiered auto-approval model: Security updates are approved after 7 days, Bugfix updates after 14 days, and Enhancements after 30 days or via manual review.
- For RHEL 8 and 9, kernel live patching via kpatch requires a system reboot at least every 6 months to transition to a new baseline, while RHEL 10 extends this window to 1 year for AWS-optimized kernels.
- Oracle Linux with Ksplice provides superior uptime by supporting live patches for the full 10-year Premier Support window and enabling zero-downtime updates for critical userspace libraries like glibc and openssl.
- AWS SSM Patch Manager requires separate custom baselines for RHEL and Oracle Linux due to divergent metadata prefixes (RHSA vs ELSA) and vendor-specific advisory classification systems.
- Using the NoReboot parameter in SSM enables staged patching for high-availability tiers but results in a Non-Compliant status with InstalledPendingReboot metadata until a reboot and scan are completed.
- needs-restarting (dnf-utils) identifies required reboots by scanning /proc/[PID]/maps for deleted library segments, but standard versions are not natively aware of Ksplice in-memory patches.
- RHEL 10's DNF5 features faster, metadata-driven reboot detection and supports systemd soft-reboots, which restart userspace without a full hardware or kernel restart.
- Operational 'reboot debt' accumulates when live patching is used exclusively, leading to unpatched userspace libraries and increased kernel complexity that heightens the risk of failure during eventual restarts.
- Security compliance reporting in SSM often reflects the on-disk kernel version, potentially resulting in false-negative audit findings for instances that are effectively patched in-memory via kpatch or Ksplice.
- For immutable infrastructure such as EKS worker nodes, the optimal patching strategy is node replacement (AMI swap) rather than in-place patching to prevent configuration drift and 'snowflake' nodes.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| InstalledPendingReboot | An SSM metadata property indicating patches are installed on-disk but the system requires a reboot to activate them and return to a 'Compliant' state. |
| kpatch | Red Hat's implementation of kernel live patching using ftrace-based function redirection to apply security fixes without downtime. |
| Ksplice | Oracle Linux technology for zero-downtime patching of the kernel and critical userspace libraries like glibc and OpenSSL at the object-code level. |
| Reboot Debt | The accumulation of unapplied updates and configuration changes that can only be cleared by a system restart, increasing operational risk over time. |
| systemd soft-reboot | A RHEL 10 feature that restarts the userspace environment without a full hardware or kernel reboot, significantly reducing maintenance downtime. |
| UEK (Unbreakable Enterprise Kernel) | An Oracle-built Linux kernel based on modern mainline LTS releases, optimized for performance and stability on cloud infrastructure. |

---

## Tensions & Tradeoffs

- Compliance vs. Availability: Staged patching (NoReboot) maintains uptime but triggers Non-Compliant alerts in SSM, requiring operational coordination to bridge the reporting gap.
- Automation vs. Stability: Auto-approving enhancement updates can lead to unexpected system behavior, favoring a longer delay or manual approval for these non-security changes.
- Baseline Drift: Excessive reliance on live patching can lead to running kernels that diverge significantly from the on-disk baseline, complicating disaster recovery and troubleshooting.

---

## Open Questions

- What is the average statistical delay between the release of an RHSA and its corresponding ELSA for Oracle Linux RHCK images?
- To what extent will RHEL 10 kpatch implementation bridge the gap with Ksplice regarding automated userspace library patching?
- What is the specific overhead of DNF5's memory scanning on high-PID-count systems compared to DNF4?

---

## Sources & References

- [How patch baselines work](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-how-it-works-baselines.html)
- [Red Hat Enterprise Linux Kernel Live Patching](https://access.redhat.com/articles/kernel-live-patching)
- [Oracle Linux Ksplice Overview](https://www.oracle.com/linux/ksplice/)
- [DNF5 needs-restarting command reference](https://dnf5.readthedocs.io/en/latest/command_ref/needs-restarting.8.html)
- [Updating EKS Managed Node Groups](https://docs.aws.amazon.com/eks/latest/userguide/managed-node-update.html)
- [Oracle Linux: Unbreakable Enterprise Kernel (UEK)](https://www.oracle.com/linux/unbreakable-enterprise-kernel/)
- [Red Hat Enterprise Linux 10 Product Lifecycle](https://access.redhat.com/support/policy/updates/errata#Red_Hat_Enterprise_Linux_10)
