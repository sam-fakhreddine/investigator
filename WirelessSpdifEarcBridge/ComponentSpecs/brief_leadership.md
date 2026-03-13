# Wireless S/PDIF-eARC Bridge — Component Specifications & BOM Validation — Engineering Leadership Brief

**Date:** 2026-03-13

---

## Headline

> Two of ten BOM components are fundamentally misidentified — the named VCXO parts are not VCXOs — requiring substitution before any PCB layout work begins.

---

## So What

The VCXO misidentification (TXC 7M is a crystal, NDK NZ2520SDA is a fixed XO) means clock recovery cannot work as described without component substitution. The PCM1808 package error (SSOP-28 cited vs actual TSSOP-14) would produce an incorrect PCB footprint. Both errors are correctable with off-the-shelf alternatives.

---

## Key Points

- PCM1808 ADC specs are correct but package is TSSOP-14 not SSOP-28 — PCB footprint must be corrected before layout
- Neither the TXC 7M nor NDK NZ2520SDA is a VCXO — SiTime SiT3807 or Abracon ASVV are viable drop-in replacements at $5-10
- TORX173/TOTX173 TOSLINK modules are OBSOLETE — functional for prototyping but need replacement strategy for any production run
- Overall BOM cost estimate of ~$67 core is broadly correct (adjusted range: $60-75) after fixing component selections and updated pricing

---

## Action Required

> Block PCB layout until VCXO selection is finalized and PCM1808 footprint is corrected to TSSOP-14.

---

*Full engineering investigation: [investigation.md](investigation.md)*
