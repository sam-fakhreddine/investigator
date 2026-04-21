# Investigation: SSM Patch Manager Baselines for RHEL and Oracle Linux

**Date:** 2026-04-21
**Status:** Complete

---

## Question

> What is the recommended design for SSM Patch Manager baselines for RHEL (8/9/10) and Oracle Linux (8/9 equivalents)? Include advisory classification (Security, Bugfix, Enhancement) strategies for weekly automated runs vs manual approval, inclusion of kpatch-patch/Ksplice packages, maintenance window design for no-reboot vs reboot runbooks, and compliance state behavior when NoReboot is used (i.e., how SSM reports on effective vs on-disk patch state).

---

## Context

SSM Patch Manager uses repository metadata to classify and approve patches. For RHEL and Oracle Linux, this involves mapping vendor-specific advisory prefixes to SSM internal classification system.

---

## Patching Strategy Overview

| Category | Strategy | Impact/Action |
| --- | --- | --- |
| Advisory Classification | 7-day delay (Security), 14-day delay (Bugfix), 30-day/Manual (Enhancement) | Automates regular patching while minimizing instability. |
| Live Patching | Explicitly add 'kpatch-patch' or 'ksplice/uptrack' to Approved Patches | Enables kernel updates without downtime. |
| Maintenance Windows | NoReboot (Staged) vs RebootIfNeeded (Auto) | Staged patching allows for traffic draining and manual verification. |
| Compliance State | InstalledPendingReboot SSM metadata property | Reports non-compliant until reboot; indicates on-disk vs effective state mismatch via SSM metadata. |

> RHEL/OL use specific advisory prefixes (RHSA/ELSA, RHBA/ELBA, RHEA/ELEA) which SSM parses from repo metadata.

---

## Key Findings

- Recommended strategy: Auto-approve Security (Critical/Important) after 7 days and Bugfix after 14 days for automated weekly runs.
- Enhancement updates should have a 30-day delay or require manual approval to avoid unexpected feature changes.
- Live-patching packages like kpatch-patch (RHEL/AL2) and ksplice/uptrack (Oracle) must be explicitly added to a Custom Patch Baseline Approved patches list.
- Two primary runbook patterns: RebootIfNeeded for automated end-to-end patching and NoReboot for staged patching in high-availability environments.
- When NoReboot is used, SSM reports a compliance status of Non-Compliant with a specific patch state of InstalledPendingReboot.
- A reboot and a subsequent Scan operation are required to transition to Compliant after a NoReboot patch installation.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| InstalledPendingReboot | An SSM metadata property (not an RPM state) indicating patches are on-disk but not active in memory. |
| Advisory Prefixes | Vendor-specific naming (e.g., RHSA/ELSA) used to classify patch types. |
| Live Patching | Technology allowing kernel updates without a system reboot (kpatch/Ksplice). |

---

## Tensions & Tradeoffs

- Compliance vs. Availability: Using NoReboot maintains availability but results in a Non-Compliant status in SSM until a reboot occurs.
- Automation vs. Stability: Auto-approving enhancements can lead to unexpected system behavior changes, favoring a manual approval or longer delay for these updates.

---

## Open Questions

- What are the specific RHEL 10 advisory metadata classification prefixes once it is GA?
- Does SSM provide native support for Oracle Ksplice 'uptrack-upgrade' for non-kernel user-space live patching?

---

## Sources & References

- [How patch baselines work](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-how-it-works-baselines.html)
- [About patch compliance](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-compliance-about.html)
- [Organizing patches into groups (Tiered Strategy)](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-organizing-patch-groups.html)
- [SSM Agent requirements for Patch Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-ssm-agent-requirements.html)
