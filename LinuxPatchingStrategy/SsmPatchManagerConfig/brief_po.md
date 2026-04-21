# SSM Patch Manager Baselines for RHEL and Oracle Linux — Product Brief

**Date:** 2026-04-21
**Risk Level:** MEDIUM

---

## What Is This?

> Security updates for Linux servers can be automated to happen weekly without immediate reboots.

---

## What Does This Mean for Us?

This allows for critical security fixes to be applied without disrupting users, though a scheduled restart will eventually be needed to fully complete the update.

---

## Key Points

- Critical security fixes are applied after 7 days, while non-critical bugs wait 14 days.
- New features are delayed or held for manual review to prevent unexpected changes to the system.
- Servers will show a Non-Compliant warning after patching if they haven't been restarted yet.
- The Live Patching feature can be used to apply some updates without any downtime at all.

---

## Next Steps

**PO/EM Decision:**

> Review the proposed auto-approval delays (7/14/30 days) with stakeholders to ensure they align with business risk tolerance.

**Engineering Work Items:**
- Configure custom SSM patch baselines for RHEL and Oracle Linux tiers.
- Implement maintenance windows with NoReboot parameters for high-availability clusters.
- Set up monitoring alerts that distinguish InstalledPendingReboot from actual patching failures.

---

## Open Questions

- Which server tiers require NoReboot staged patching versus automatic restarts?
- How will we track when a server is Pending Reboot to ensure we don't stay in that state indefinitely?
- Are all our RHEL and Oracle Linux versions currently compatible with Live Patching?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
