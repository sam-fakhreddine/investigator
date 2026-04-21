# Kernel Live Patching Safety and Consistency Models — Product Brief

**Date:** 2026-04-21
**Risk Level:** LOW

---

## What Is This?

> Live patching allows for critical security updates without interrupting running applications or requiring server reboots.

---

## What Does This Mean for Us?

This technology enables 100% uptime for security compliance, though some complex updates may still require a standard maintenance window.

---

## Key Points

- Updates are applied 'in the background' while the system is running.
- The system ensures that no program gets 'confused' by seeing half of an update.
- In rare cases where an update gets stuck, it can be safely cancelled without crashing the system.

---

## Next Steps

**PO/EM Decision:**

> Define the policy for when to use live patches versus scheduled reboots for security compliance.

**Engineering Work Items:**
- Audit existing infrastructure for CONFIG_LIVEPATCH compatibility.
- Establish monitoring for livepatch transition states in the fleet.

---

## Open Questions

- Which of our current server architectures support reliable stack checking for live patches?
- What is our standard procedure if a patch transition stalls due to a blocked task?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
