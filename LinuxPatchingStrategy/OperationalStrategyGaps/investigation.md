# Investigation: Tiered Linux Patching Strategy on EC2

**Date:** 2026-04-21
**Status:** Complete

---

## Question

> What are the operational gaps and caveats for a tiered Linux patching strategy (userspace weekly → kernel live patch → kernel version upgrades) for RHEL/Oracle Linux on EC2? Focus on CVEs that cannot be live-patched, RHEL subscription requirements (Marketplace vs BYOS), Ksplice licensing on EC2, reboot debt accumulation risks, EKS node considerations (drain vs node replacement), and the maturity of RHEL 10 live patching.

---

## Context

Investigation into the operational complexities of maintaining a tiered patching model for RHEL and Oracle Linux on AWS EC2, balancing uptime with security compliance and infrastructure consistency.

---

## Linux Patching Capabilities and Constraints

| Feature | RHEL (EC2) | Oracle Linux (EC2) | Primary Caveat |
| --- | --- | --- | --- |
| Kernel Live Patching | kpatch (6-12 mo window) | Ksplice (Uptime-optimized) | Requires active subscription and CSI |
| Userspace Patching | Standard DNF/YUM | Ksplice (glibc/OpenSSL) | Oracle requires Premier Support tier |
| Licensing on AWS | RHUI (Marketplace) / BYOS | Premier Support (Paid) | Ksplice is not free on AWS/EC2 |
| EKS Node Strategy | Node Replacement | Node Replacement | In-place patching causes configuration drift |
| RHEL 10 Maturity | Day-zero kpatch support (1-yr) | N/A | Extended 1-year window for AWS kernels |

> Live patching reduces reboots but does not eliminate them due to technical limitations and support windows.

---

## Key Findings

- CVEs requiring changes to kernel data structures, early boot code, or assembly-level logic cannot be live-patched and require a full system reboot.
- RHEL subscription behavior varies: AWS Marketplace RHEL is pre-entitled via Red Hat Update Infrastructure (RHUI), while BYOS requires manual registration via subscription-manager.
- Ksplice on EC2 is not included in the free tier of Oracle Linux; it requires a paid Oracle Linux Premier Support subscription and ULN registration with a Customer Support Identifier (CSI).
- Excessive use of live patching leads to 'reboot debt,' resulting in unpatched userspace libraries, increased kernel complexity, and high-risk 'Big Bang' failures during eventual restarts.
- RHEL 10 treats live patching as a mature feature from day zero; notably, the support window for mainstream kernels (including those optimized for AWS EC2) has been extended to 1 year, a significant shift from the 6-month model of RHEL 8 and 9.
- AWS EKS best practice for RHEL/Oracle worker nodes is immutable node replacement (AMI swap) to prevent 'snowflake' node drift, reserving in-place patching for specific stateful exceptions.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Reboot Debt | The accumulation of unapplied updates and configuration changes that can only be cleared by a system restart, increasing the risk of failure during the eventual reboot. |
| kpatch | The Red Hat implementation of kernel live patching that allows applying security fixes without stopping the kernel. |
| Ksplice | Oracle Linux technology for zero-downtime patching of the kernel and critical userspace libraries like glibc and OpenSSL. |
| RHUI | Red Hat Update Infrastructure, a service provided by AWS to allow RHEL instances to access updates without a direct Red Hat subscription. |

---

## Tensions & Tradeoffs

- The conflict between maximizing instance uptime via live patching and maintaining node consistency via immutable infrastructure (AMI replacement).
- The trade-off between the speed of kernel live patching and the risk of 'Frankenstein kernels' where multiple live patches increase runtime complexity.

---

## Open Questions

- What are the specific performance benchmarks for kpatch redirection overhead on high-throughput Nitro-based EC2 instances?
- When is the official General Availability (GA) date for RHEL 10?

---

## Sources & References

- [Red Hat Enterprise Linux Kernel Live Patching](https://access.redhat.com/articles/kernel-live-patching)
- [Oracle Ksplice Inspector](https://ksplice.oracle.com/inspector)
- [Updating EKS Managed Node Groups](https://docs.aws.amazon.com/eks/latest/userguide/managed-node-update.html)
- [Oracle Linux Ksplice: Zero-Downtime Patching](https://www.oracle.com/linux/support/ksplice/)
