# Glossary — eARC HDMI Output — IT6803 Claims and eARC Standard Verification

Quick definitions of key terms and concepts referenced in this investigation.

---

## eARC (Enhanced Audio Return Channel)

HDMI 2.1 feature providing 37 Mbps audio bandwidth from sink (TV) to source (AVR/soundbar), replacing legacy ARC's ~1 Mbps limit. Uses dedicated DMAC and CMDC channels independent of CEC.

## DMAC (Differential Mode Audio Channel)

The one-way audio data path in eARC, carrying audio from eARC TX (sink) to eARC RX (source) using LVDS at ~350 mVpp over the HEAC pin pair.

## CMDC (Common Mode Data Channel)

The bidirectional control channel in eARC used for discovery, capability exchange (E-EDID), heartbeat, and status — completely independent of CEC protocol.

## IT6621 (ITE eARC TX)

ITE Tech's standalone ARC/eARC transmitter IC in 32-pin QFN. Accepts 8x I2S + SPDIF input, supports 98.304 Mbps DMAC, includes embedded CEC PHY for legacy ARC fallback.

## IT6622 (ITE HDMI TX + eARC RX)

ITE Tech's combined HDMI 1.4 video transmitter and eARC receiver with embedded MCU and Flash. Outputs 4x I2S + SPDIF audio, handles HPD and CEC in hardware. Note: this is an eARC receiver, not transmitter.

## Lattice SiI9437/SiI9438

Lattice Semiconductor's dedicated eARC receiver (9437) and transmitter (9438) companion ICs in 32-pin QFN. Designed to pair with any HDMI TX/RX IC of any HDMI version, with I2C control interface.

---

*Back to: [investigation.md](investigation.md)*
