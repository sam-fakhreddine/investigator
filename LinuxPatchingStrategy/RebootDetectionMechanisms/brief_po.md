# RHEL/Oracle Linux Reboot Detection Mechanisms — Product Brief

**Date:** 2024-05-23
**Risk Level:** MEDIUM

---

## What Is This?

> Patching systems without restarting them leaves them showing as 'broken' in AWS reports.

---

## What Does This Mean for Us?

Choosing to skip restarts to avoid downtime will cause our security reports to show systems as 'Non-Compliant,' even if the fixes are installed. This requires manual follow-up to update the reports.

---

## Key Points

- Security updates are not fully active until the system or specific services are restarted.
- Modern versions of Linux (RHEL 10) can restart much faster without a full 'off and on' cycle using 'soft-reboots'.
- Oracle Linux systems can apply critical updates without downtime via Ksplice, but standard monitoring tools will still report that a restart is 'needed' until confirmed otherwise by specialized commands.
- Using the 'NoReboot' option in AWS SSM leads to a persistent 'Pending Reboot' status that impacts compliance scores.

---

## Next Steps

**PO/EM Decision:**

> Decide if 'Non-Compliant' status in AWS is acceptable during critical production windows to avoid downtime.

**Engineering Work Items:**
- Evaluate RHEL 10 soft-reboot compatibility for internal applications to minimize maintenance windows.
- Review patching automation for Oracle Linux to properly leverage Ksplice and improve compliance reporting.

**Leadership Input Required:**

> Architects should weigh in on whether 'InstalledPendingReboot' should be treated as a hard compliance failure or an expected operational state.

---

## Open Questions

- Can we use RHEL 10's soft-reboot to reduce our patching downtime?
- How much effort is required to automate the 'Ksplice' check for our Oracle Linux instances?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
