# Investigation: RHEL vs Oracle Linux Patching and Kernel Divergence

**Date:** 2026-04-20
**Status:** Complete

---

## Question

> Identify technical and operational divergence points between RHEL (8/9/10) and Oracle Linux (8/9 equivalents), specifically focusing on UEK (Unbreakable Enterprise Kernel) vs RHEL-compatible kernel, live patching support differences (e.g., Ksplice vs kpatch), CVE coverage gaps between RHSAs and ELSAs (Red Hat vs Oracle advisories), and SSM Patch Manager baseline configuration requirements for each distribution.

---

## Context

This investigation examines the critical technical differences between Red Hat Enterprise Linux and Oracle Linux as they pertain to enterprise patching strategies, kernel lifecycles, and security compliance automation in cloud environments.

---

## RHEL vs Oracle Linux Technical Comparison

| Feature | Red Hat Enterprise Linux (RHEL) | Oracle Linux (OL) |
| --- | --- | --- |
| Default Kernel | RHCK (RHEL-Compatible Kernel) | UEK (Unbreakable Enterprise Kernel) |
| Live Patching Tool | kpatch (RHCK only) | Ksplice (UEK and RHCK) |
| Live Patching Scope | Kernel function-level only | Kernel and user-space libraries (glibc, openssl) |
| Security Advisory | RHSA (Red Hat Security Advisory) | ELSA (Enterprise Linux Security Advisory) |
| SSM Baseline | Mandatory RHEL-specific baseline | Mandatory OL-specific baseline |

> Oracle Linux maintains binary compatibility with RHEL but diverges significantly in its kernel release cycle and live-patching depth.

---

## Key Findings

- Oracle Linux's UEK (Unbreakable Enterprise Kernel) follows an independent release cycle and is generally more modern than RHEL's RHCK; for example, OL 9/10 utilizes UEK 8 (Kernel 6.12), which matches RHEL 10's kernel base but was available earlier.
- Live patching on Oracle Linux via Ksplice provides superior operational depth compared to RHEL's kpatch, as Ksplice supports both UEK and RHCK while also enabling 'Zero-Downtime' patching for critical user-space libraries like glibc and openssl.
- A mandatory operational delay exists for RHCK patches on Oracle Linux due to the requirement for Oracle to repackage Red Hat source code, resulting in a timing gap between RHSA and ELSA releases.
- CVE severity ratings often diverge between Red Hat and Oracle (e.g., 'Important' vs 'Critical'), which can trigger different automated patching responses depending on vendor-specific advisory metadata.
- AWS SSM Patch Manager requires separate patch baselines for RHEL and Oracle Linux because it filters patches based on vendor-specific metadata prefixes (RHSA vs ELSA) and product names in updateinfo.xml.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| UEK (Unbreakable Enterprise Kernel) | An Oracle-built Linux kernel based on more recent mainline LTS releases, optimized for performance and stability on Oracle hardware and cloud infrastructure. |
| Ksplice | A zero-downtime patching technology that allows for kernel and user-space library updates without requiring a system reboot. |
| RHCK (Red Hat Compatible Kernel) | The standard kernel shipped with RHEL, also provided by Oracle Linux to ensure 100% binary compatibility for RHEL-certified applications. |
| updateinfo.xml | A metadata file used by package managers (yum/dnf) that contains information about security advisories, bug fixes, and enhancement updates. |

---

## Tensions & Tradeoffs

- The benefit of more modern kernels in UEK must be weighed against the operational overhead of managing non-standard kernel versions across a hybrid RHEL/OL fleet.
- The delay between RHSA and ELSA for RHCK patches on Oracle Linux creates a temporary security window that may not meet aggressive SLA requirements for Critical vulnerabilities.

---

## Open Questions

- What is the average statistical delay (in hours/days) between the release of an RHSA and its corresponding ELSA for RHCK on Oracle Linux 9?
- To what extent will RHEL 10's kpatch implementation bridge the gap with Ksplice regarding user-space library patching?

---

## Sources & References

- [Oracle Linux: Unbreakable Enterprise Kernel (UEK)](https://www.oracle.com/linux/unbreakable-enterprise-kernel/)
- [Red Hat Enterprise Linux 10 Release Notes](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/10)
- [AWS SSM Patch Manager: About Patch Baselines](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-how-it-works-baselines.html)
- [Oracle Ksplice: Zero-Downtime Patching](https://linux.oracle.com/ksplice/)
