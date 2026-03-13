# Wireless S/PDIF-eARC Bridge — Component Specifications & BOM Validation — Product Brief

**Date:** 2026-03-13
**Risk Level:** MEDIUM

---

## What Is This?

> The parts list for the wireless audio bridge has two wrong components that need swapping, but the overall cost estimate is still in the right ballpark.

---

## What Does This Mean for Us?

Two clock components were misidentified and cannot do what the design requires. Correct replacements exist at similar cost. The total estimated cost of $97-120 remains realistic after corrections. Some parts are discontinued, which could delay sourcing.

---

## Key Points

- Two out of ten key components were wrong type (clock parts that cannot be tuned) — replacements are available at similar price
- One chip has the wrong physical size listed, which would cause a circuit board error if not caught
- Some optical connector parts are discontinued by the manufacturer — need to find alternatives before production
- The $97-120 total cost estimate holds after corrections, possibly even slightly lower at $90-115

---

## Next Steps

**PO/EM Decision:**

> Approve engineering time to finalize VCXO selection and identify in-production TOSLINK module alternatives before committing to PCB layout.

**Engineering Work Items:**
- Select and validate a 24.576MHz VCXO (SiTime SiT3807 or Abracon ASVV) with sufficient pull range for clock recovery
- Identify in-production TOSLINK RX/TX modules to replace obsolete TORX173/TOTX173
- Update PCB footprint library to use TSSOP-14 for PCM1808 instead of SSOP-28

---

## Open Questions

- How long will it take to validate a replacement VCXO and update the schematic?
- Is the TOSLINK obsolescence a blocker for prototyping, or can we use remaining stock for initial builds?
- Does the corrected BOM still fit within the target retail price point?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
