# Optimal Weekly Patching Strategy for RHEL and Oracle Linux on EC2 — Product Brief

**Date:** 2024-05-24
**Risk Level:** MEDIUM

---

## What Is This?

> We can automate most security updates for Linux servers, but some will still require scheduled restarts to stay fully compliant.

---

## What Does This Mean for Us?

Skipping restarts keeps systems running but causes them to show as 'Non-Compliant' in AWS security reports, which may require manual explanation during audits.

---

## Key Points

- Security fixes are applied automatically after 7 days; non-security bug fixes wait for 14 days to ensure stability.
- Live patching allows us to fix the core of the system without turning it off, but this is a temporary bridge rather than a permanent substitute for restarts.
- Oracle Linux systems can stay running longer without restarts than Red Hat systems, but they require a higher-tier subscription for this feature.
- The most reliable way to keep systems healthy is to replace them with fresh, updated versions (AMI swaps) rather than patching them in place.

---

## Next Steps

**PO/EM Decision:**

> Determine if the organization accepts 'InstalledPendingReboot' status in AWS during peak production months to avoid maintenance downtime.

**Engineering Work Items:**
- Configure separate SSM Patch Baselines for RHEL and Oracle Linux in all AWS environments.
- Implement maintenance windows with RebootIfNeeded for non-critical application tiers.
- Verify the cost vs. benefit of Oracle Premier Support for zero-downtime glibc/openssl patching.

**Leadership Input Required:**

> Confirm if the 6-to-12 month RHEL reboot window aligns with the organizational security compliance policy.

---

## Open Questions

- How often are we currently performing full reboots versus live patching across our fleet?
- Do our security scanners recognize live patches, or do we have a reporting gap we need to address?
- Are we using immutable node replacement for our EKS clusters to prevent drift?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
