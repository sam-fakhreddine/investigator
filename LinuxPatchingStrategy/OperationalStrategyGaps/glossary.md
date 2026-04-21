# Glossary — Tiered Linux Patching Strategy on EC2

Quick definitions of key terms and concepts referenced in this investigation.

---

## Reboot Debt

The accumulation of unapplied updates and configuration changes that can only be cleared by a system restart, increasing the risk of failure during the eventual reboot.

## kpatch

The Red Hat implementation of kernel live patching that allows applying security fixes without stopping the kernel.

## Ksplice

Oracle Linux technology for zero-downtime patching of the kernel and critical userspace libraries like glibc and OpenSSL.

## RHUI

Red Hat Update Infrastructure, a service provided by AWS to allow RHEL instances to access updates without a direct Red Hat subscription.

---

*Back to: [investigation.md](investigation.md)*
