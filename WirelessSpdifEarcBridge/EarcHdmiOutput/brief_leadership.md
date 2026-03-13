# eARC HDMI Output — IT6803 Claims and eARC Standard Verification — Engineering Leadership Brief

**Date:** 2026-03-13

---

## Headline

> The IT6803 part does not exist — ITE's real eARC TX is the IT6621, and the eARC protocol is CEC-independent, which changes the firmware assumptions.

---

## So What

The design references a non-existent IC, requiring immediate part substitution before any PCB work proceeds. The correct ITE part (IT6621) or Lattice alternative (SiI9438) will handle eARC negotiation in hardware, but the eARC TX/RX role mapping needs careful review to ensure the design uses the right direction.

---

## Key Points

- IT6803 is not in ITE's product catalog — IT680x series are HDMI receivers, not transmitters; the eARC TX part is IT6621 (32-pin QFN, I2S input, 98 Mbps DMAC)
- eARC negotiation uses dedicated CMDC channel, not CEC — the original claim that CEC handles eARC handshake is incorrect, but dedicated ICs abstract CMDC entirely
- eARC supports all target audio formats (DD 5.1, TrueHD, Atmos) at 37 Mbps with format-agnostic passthrough — no re-encoding needed
- Lattice SiI9437/SiI9438 are viable alternatives with better public documentation and known distribution availability

---

## Action Required

> Correct the part number from IT6803 to IT6621 (or evaluate Lattice SiI9438) and clarify whether the design needs an eARC TX or RX role before proceeding with schematic.

---

*Full engineering investigation: [investigation.md](investigation.md)*
