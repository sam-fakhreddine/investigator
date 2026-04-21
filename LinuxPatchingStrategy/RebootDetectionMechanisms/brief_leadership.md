# RHEL/Oracle Linux Reboot Detection Mechanisms — Engineering Leadership Brief

**Date:** 2024-05-23

---

## Headline

> Reboot detection shifts from static lists to metadata-driven automation in RHEL 10.

---

## So What

Inconsistent reboot handling across RHEL and Oracle Linux, combined with SSM 'NoReboot' policies, creates compliance reporting gaps that require manual intervention or Ksplice-aware automation.

---

## Key Points

- RHEL 10's DNF5 improves detection speed and adds JSON support for better integration with automation pipelines.
- Oracle Linux Ksplice reduces reboot frequency, but standard tools like `needs-restarting -r` are NOT natively aware of in-memory patches and will report a required reboot if a newer kernel package is detected on disk.
- SSM 'NoReboot' policies lock instances into 'Non-Compliant' status despite patches being applied, potentially triggering false security alarms.

---

## Action Required

> Standardize on DNF5-compatible automation for RHEL 10 and ensure Oracle Linux monitoring uses `uptrack-show` or `ksplice-show` for accurate reboot reporting.

---

*Full engineering investigation: [investigation.md](investigation.md)*
