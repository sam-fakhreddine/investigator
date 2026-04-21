# Glossary — RHEL/Oracle Linux Reboot Detection Mechanisms

Quick definitions of key terms and concepts referenced in this investigation.

---

## needs-restarting

A tool from yum-utils/dnf-utils that determines if a system or specific services need to be restarted after package updates by analyzing process memory maps.

## Ksplice

An Oracle Linux technology that allows for patching the kernel and key userspace libraries (glibc, openssl) without requiring a system reboot.

## systemd soft-reboot

A RHEL 10/systemd feature that restarts userspace without a full hardware/kernel reboot, reducing downtime for updates that do not affect the kernel.

## InstalledPendingReboot

An AWS SSM compliance status indicating that patches are installed but the instance requires a reboot to become 'Compliant' in the console.

---

*Back to: [investigation.md](investigation.md)*
