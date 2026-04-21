# SSM Patch Manager Baselines for RHEL and Oracle Linux — Engineering Leadership Brief

**Date:** 2026-04-21

---

## Headline

> SSM Patch Manager enables automated, classification-driven patching for RHEL and Oracle Linux with integrated compliance reporting.

---

## So What

Staged patching (NoReboot) maintains uptime but triggers Non-Compliant alerts, requiring operational coordination to bridge the gap between on-disk and effective states.

---

## Key Points

- Implement a tiered auto-approval strategy (7/14/30 days) to balance security and stability.
- Explicitly include kpatch-patch or Ksplice in custom baselines to leverage live-patching capabilities.
- Distinguish between RebootIfNeeded and NoReboot runbooks based on workload sensitivity.
- Acknowledge that InstalledPendingReboot status is an expected intermediate SSM metadata state for staged patching.

---

## Action Required

> Define and document the maintenance window strategy (Staged vs. Auto-Reboot) for each application tier.

---

*Full engineering investigation: [investigation.md](investigation.md)*
