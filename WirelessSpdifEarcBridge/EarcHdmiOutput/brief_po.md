# eARC HDMI Output — IT6803 Claims and eARC Standard Verification — Product Brief

**Date:** 2026-03-13
**Risk Level:** MEDIUM

---

## What Is This?

> The specific chip referenced in the design does not exist, but equivalent parts are available that fully support the intended audio passthrough feature.

---

## What Does This Mean for Us?

This is a design-phase correction, not a show-stopper. The audio features we want (surround sound passthrough including Dolby Digital 5.1 and higher-quality formats) are fully supported by the eARC standard and by real, available chips from ITE and Lattice.

---

## Key Points

- The IT6803 chip name needs to be corrected — real alternatives exist from ITE (IT6621) and Lattice (SiI9438) that do the same job
- All target audio formats (Dolby Digital 5.1, Dolby Atmos, DTS surround) are confirmed supported by the eARC standard with plenty of bandwidth headroom
- The core architecture concept is sound — using a dedicated chip to handle HDMI complexity is the industry-standard approach used by Pioneer, Onkyo, and other AV manufacturers

---

## Next Steps

**PO/EM Decision:**

> Approve updated BOM with corrected part number (IT6621 or Lattice SiI9438) and confirm eARC direction (TX vs RX) with engineering.

**Engineering Work Items:**
- Engineering to evaluate IT6621 vs Lattice SiI9438 for availability, documentation quality, and I2S interface compatibility with the STM32
- Engineering to clarify eARC TX/RX role requirement and update schematic accordingly

---

## Open Questions

- Is the IT6621 or Lattice SiI9438 available at prototype quantities without an NDA, and what is the lead time?
- Does correcting the part number require a PCB redesign or just a BOM swap, given the different pin counts (32-pin vs 56-pin)?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
