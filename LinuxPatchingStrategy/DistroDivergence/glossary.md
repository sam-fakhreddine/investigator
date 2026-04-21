# Glossary — RHEL vs Oracle Linux Patching and Kernel Divergence

Quick definitions of key terms and concepts referenced in this investigation.

---

## UEK (Unbreakable Enterprise Kernel)

An Oracle-built Linux kernel based on more recent mainline LTS releases, optimized for performance and stability on Oracle hardware and cloud infrastructure.

## Ksplice

A zero-downtime patching technology that allows for kernel and user-space library updates without requiring a system reboot.

## RHCK (Red Hat Compatible Kernel)

The standard kernel shipped with RHEL, also provided by Oracle Linux to ensure 100% binary compatibility for RHEL-certified applications.

## updateinfo.xml

A metadata file used by package managers (yum/dnf) that contains information about security advisories, bug fixes, and enhancement updates.

---

*Back to: [investigation.md](investigation.md)*
