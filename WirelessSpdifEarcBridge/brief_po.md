# Wireless S/PDIF to eARC Bridge — Hypothesis Verification — Product Brief

**Date:** 2026-03-13
**Risk Level:** MEDIUM

---

## What Is This?

> The wireless surround sound bridge plan mostly works, but three components need changing before ordering parts and one audio format may not be supported.

---

## What Does This Mean for Us?

The core idea — wirelessly sending surround sound from a projector to a soundbar — is technically viable and fills a real gap that no current product addresses. However, three specific parts listed in the original plan either do not exist or are the wrong type, and need to be swapped for correct alternatives at similar cost. The most common surround format (Dolby Digital 5.1) will work reliably, but full-quality DTS may push the wireless link to its limit.

---

## Key Points

- The main HDMI chip listed (IT6803) does not exist — real alternatives are available from ITE (IT6621) and Lattice (SiI9438) that do the same job
- Two clock components were the wrong type entirely (like specifying a lightbulb when you need a dimmer) — correct replacements exist at $5-10 each
- Dolby Digital 5.1 (Netflix, Disney+, broadcast TV, most DVDs) will work reliably with plenty of wireless headroom
- Full-rate DTS surround is at the edge of what the wireless chip can handle — half-rate DTS (most DTS DVDs) would work fine
- No competing product currently exists for this specific use case — the discontinued Marmitek Audio Anywhere 685 was the closest, confirming real but niche demand

---

## Next Steps

**PO/EM Decision:**

> Approve updated BOM with corrected components (IT6621 or SiI9438 for eARC, SiTime SiT3807 for clock, TSSOP-14 footprint for ADC) and decide whether full-rate DTS support is a launch requirement or post-launch stretch goal.

**Engineering Work Items:**
- Finalize eARC IC selection (IT6621 vs Lattice SiI9438) based on availability and documentation access
- Select and validate a 24.576 MHz VCXO with sufficient pull range for clock recovery
- Build nRF52840 unidirectional streaming prototype and measure real-world throughput to determine DTS feasibility
- Correct PCM1808 footprint to TSSOP-14 and identify in-production TOSLINK module replacements for obsolete TORX173/TOTX173

**Leadership Input Required:**

> Architecture decision needed on DTS support scope: full-rate (1509 Kbps, high risk) vs half-rate only (754 Kbps, comfortable margin), and whether a dual-radio or channel-bonding approach is justified for the added ~$5-10 BOM cost.

---

## Open Questions

- How long will it take to validate the replacement components and produce a corrected schematic?
- What percentage of real-world DTS content uses half-rate (754 Kbps) vs full-rate (1509 Kbps)?
- Can the device start playing audio immediately or will users experience a 2-10 second silence while the clock synchronization locks?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
