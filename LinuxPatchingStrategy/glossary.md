# Glossary — Optimal Weekly Patching Strategy for RHEL and Oracle Linux on EC2

Quick definitions of key terms and concepts referenced in this investigation.

---

## InstalledPendingReboot

An SSM metadata property indicating patches are installed on-disk but the system requires a reboot to activate them and return to a 'Compliant' state.

## kpatch

Red Hat's implementation of kernel live patching using ftrace-based function redirection to apply security fixes without downtime.

## Ksplice

Oracle Linux technology for zero-downtime patching of the kernel and critical userspace libraries like glibc and OpenSSL at the object-code level.

## Reboot Debt

The accumulation of unapplied updates and configuration changes that can only be cleared by a system restart, increasing operational risk over time.

## systemd soft-reboot

A RHEL 10 feature that restarts the userspace environment without a full hardware or kernel reboot, significantly reducing maintenance downtime.

## UEK (Unbreakable Enterprise Kernel)

An Oracle-built Linux kernel based on modern mainline LTS releases, optimized for performance and stability on cloud infrastructure.

---

*Back to: [investigation.md](investigation.md)*
