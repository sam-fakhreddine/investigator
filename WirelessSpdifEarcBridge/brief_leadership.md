# Wireless S/PDIF to eARC Bridge — Hypothesis Verification — Engineering Leadership Brief

**Date:** 2026-03-13

---

## Headline

> The wireless S/PDIF-to-eARC bridge is technically feasible for Dolby Digital 5.1, but three hypothesis errors (non-existent IC, wrong VCXO parts, wrong package) must be corrected and full-rate DTS remains a high-risk bandwidth bet.

---

## So What

The architecture is sound — hardware S/PDIF decode (STM32F446), 2.4 GHz proprietary radio (nRF52840), VCXO clock recovery, and dedicated eARC IC are all verified as viable. However, the hypothesis named an IC that does not exist (IT6803), two components that are not VCXOs (TXC 7M, NDK NZ2520SDA), and one wrong package (PCM1808 SSOP-28 vs TSSOP-14). All corrections have known, available alternatives. The primary unresolved technical risk is DTS full-rate at 1509 Kbps consuming 89-116% of nRF52840 throughput.

---

## Key Points

- IT6803 does not exist — replace with IT6621 (ITE eARC TX) or Lattice SiI9438 before any schematic work
- TXC 7M (passive crystal) and NDK NZ2520SDA (fixed XO) are not VCXOs — use SiTime SiT3807 or Abracon ASVV for clock recovery
- PCM1808 is TSSOP-14 not SSOP-28 — PCB footprint must be corrected before layout
- DD5.1 at 640 Kbps fits nRF52840 with 40%+ margin (low risk); DTS at 1509 Kbps is marginal to infeasible (high risk)
- Marmitek Audio Anywhere 685 is prior art proving concept feasibility but is discontinued — confirms both the approach and the market gap

---

## Action Required

> Block PCB layout until IT6803 is replaced with IT6621 or SiI9438, VCXO selection is finalized (SiT3807 or ASVV), and PCM1808 footprint is corrected to TSSOP-14. Decide whether DTS is a hard requirement or stretch goal before committing RF protocol design.

---

*Full engineering investigation: [investigation.md](investigation.md)*
