# Investigation: eARC HDMI Output — IT6803 Claims and eARC Standard Verification

**Date:** 2026-03-13
**Status:** Complete

---

## Question

> Is the IT6803 HDMI TX IC (ITE Tech) a real, available part that handles eARC negotiation in hardware, and does eARC support Dolby Digital 5.1 passthrough over HDMI without requiring the source to encode in a specific format?

---

## Context

The project hypothesizes using an IT6803 HDMI TX IC from ITE Tech to handle eARC output, offloading HDMI handshake complexity (HPD, DDC/EDID, CEC) from the MCU. This investigation verifies whether the IT6803 exists as a real product, what ITE Tech actually offers for eARC-capable HDMI transmission, and whether the eARC standard itself supports the intended Dolby Digital 5.1 passthrough use case.

---

## Quick Reference

| Claim | Verdict | Notes |
| --- | --- | --- |
| IT6803 is a real ITE Tech HDMI TX IC | NOT FOUND | No IT6803 in ITE product catalog; IT680x are HDMI receivers |
| IT6803 handles full HDMI handshake in HW | UNVERIFIABLE | Part does not appear to exist; ITE TX parts (IT6621/IT6622) do handle HPD/DDC/CEC in HW |
| IT6803 handles eARC via CEC in HW | INCORRECT PREMISE | eARC does not use CEC for negotiation; it has its own dedicated control channel (CMDC) |
| IT6803 presents I2S input to MCU | UNVERIFIABLE | Part not found; IT6621 does accept I2S input (up to 16-channel) |
| IT6803 eval boards exist | NOT FOUND | No eval boards found; IT6621/IT6622 are the real ITE eARC parts |
| eARC is part of HDMI 2.1 | CONFIRMED | eARC defined in HDMI 2.1 specification (2017+) |
| eARC supports lossless and DD 5.1 | CONFIRMED | eARC supports 37 Mbps bandwidth: DD, DD+, TrueHD, DTS-HD MA, Atmos, DTS:X |
| eARC uses CEC pins for negotiation | PARTIALLY CORRECT | eARC reuses HEAC+/HEAC- pins (14/19) but negotiation is via dedicated CMDC, not CEC protocol |
| HDMI HPD/DDC/CEC is non-trivial firmware | CONFIRMED | Multiple concurrent protocols with timing dependencies; dedicated ICs exist to abstract this |

> The IT6803 part number does not exist in ITE Tech's public product catalog. The correct ITE parts for eARC TX are IT6621 (standalone eARC TX) and IT6622 (HDMI 1.4 TX + eARC RX with embedded MCU). Alternative eARC ICs include Lattice SiI9437/SiI9438.

---

## Key Findings

- The IT6803 does not appear in ITE Tech's product catalog — ITE's IT680x series (IT6801, IT6802, IT6807) are HDMI receivers, not transmitters, and none support eARC.
- ITE Tech's actual eARC-capable transmitter parts are the IT6621 (ARC/eARC TX with Audio MUX, 32-pin QFN) and IT6622 (HDMI 1.4 TX with eARC RX and embedded MCU, 56-pin QFN).
- The IT6621 accepts eight I2S channels plus SPDIF input and handles eARC transmission with 98.304 Mbps DMAC bandwidth, supporting up to 8-channel 192 kHz audio — this is the closest match to the project's intended use case.
- The IT6622 combines an HDMI 1.4 video transmitter with an eARC receiver (not transmitter), includes an embedded MCU and Flash, and handles HPD detection and CEC via embedded hardware PHY.
- eARC negotiation does NOT use CEC — it has its own dedicated Common Mode Data Channel (CMDC) that operates independently of CEC, meaning full eARC interoperability works even when CEC is disabled or non-functional.
- eARC uses the HEAC differential pair (HDMI pins 14 and 19) for both the Differential Mode Audio Channel (DMAC) for one-way audio and the CMDC for bidirectional control — these are the same physical pins as legacy ARC but with a fundamentally different protocol.
- eARC supports all intended audio formats: Dolby Digital (AC-3) 5.1, Dolby Digital Plus (E-AC-3), Dolby TrueHD, Dolby Atmos, DTS, DTS-HD Master Audio, DTS:X, and uncompressed PCM up to 7.1 channels at 192 kHz/24-bit.
- eARC passthrough is format-agnostic — the transport does not require the source to re-encode audio; compressed bitstreams (DD 5.1, TrueHD) pass through untouched as IEC 61937 data packets.
- Lattice Semiconductor offers the SiI9437 (eARC RX) and SiI9438 (eARC TX) as dedicated 32-pin QFN eARC companion ICs that pair with any existing HDMI TX/RX IC, supporting both eARC and legacy ARC fallback.
- Implementing HDMI HPD, DDC/EDID, CEC, and eARC from firmware on a bare MCU is indeed non-trivial — multiple concurrent protocols with precise timing dependencies make dedicated silicon (IT6621, IT6622, or Lattice SiI943x) the standard industry approach.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| eARC (Enhanced Audio Return Channel) | HDMI 2.1 feature providing 37 Mbps audio bandwidth from sink (TV) to source (AVR/soundbar), replacing legacy ARC's ~1 Mbps limit. Uses dedicated DMAC and CMDC channels independent of CEC. |
| DMAC (Differential Mode Audio Channel) | The one-way audio data path in eARC, carrying audio from eARC TX (sink) to eARC RX (source) using LVDS at ~350 mVpp over the HEAC pin pair. |
| CMDC (Common Mode Data Channel) | The bidirectional control channel in eARC used for discovery, capability exchange (E-EDID), heartbeat, and status — completely independent of CEC protocol. |
| IT6621 (ITE eARC TX) | ITE Tech's standalone ARC/eARC transmitter IC in 32-pin QFN. Accepts 8x I2S + SPDIF input, supports 98.304 Mbps DMAC, includes embedded CEC PHY for legacy ARC fallback. |
| IT6622 (ITE HDMI TX + eARC RX) | ITE Tech's combined HDMI 1.4 video transmitter and eARC receiver with embedded MCU and Flash. Outputs 4x I2S + SPDIF audio, handles HPD and CEC in hardware. Note: this is an eARC receiver, not transmitter. |
| Lattice SiI9437/SiI9438 | Lattice Semiconductor's dedicated eARC receiver (9437) and transmitter (9438) companion ICs in 32-pin QFN. Designed to pair with any HDMI TX/RX IC of any HDMI version, with I2C control interface. |

---

## Tensions & Tradeoffs

- The IT6803 part number referenced in the project design does not exist in ITE's catalog — the project must either correct the part number to IT6621 (eARC TX) or evaluate alternative ICs, which may require PCB redesign.
- The IT6621 is an eARC transmitter (sends audio FROM a sink device like a TV), but the project needs to transmit audio TO a TV/AVR — the eARC TX/RX role naming is counterintuitive because 'TX' means the device sending audio back, not the one outputting HDMI.
- eARC's independence from CEC is an advantage for reliability but means the project cannot rely on simple CEC-based negotiation — it must support the full CMDC protocol, which dedicated ICs like IT6621 or SiI9438 handle internally.
- The Lattice SiI9438 eARC TX is a companion IC that requires pairing with a separate HDMI TX IC, adding BOM complexity, whereas the ITE IT6622 integrates HDMI TX and eARC RX in one chip but serves the opposite eARC role (receiver, not transmitter).
- No public datasheets or eval board documentation were found for the IT6621 or IT6622 — ITE Tech appears to require NDA for detailed specifications, which creates procurement and design risk for a small-scale project.

---

## Open Questions

- Which specific ITE part should replace the IT6803 in the design — IT6621 (standalone eARC TX) or IT6622 (HDMI TX + eARC RX) — given the project's audio-only use case?
- Does the project need an eARC TX (sending audio back from a sink) or an eARC RX (receiving audio on a source device)? The TX/RX naming in eARC follows the audio direction, which is the reverse of the HDMI video direction.
- Are ITE's IT6621/IT6622 available through standard distribution channels (Mouser, DigiKey, LCSC) at prototype quantities, or do they require direct engagement with ITE?
- Should the Lattice SiI9438 (eARC TX) + a standard HDMI TX IC be considered as an alternative to an ITE single-chip solution, given Lattice's better-documented eARC ecosystem?
- What is the minimum viable firmware required when using IT6621 or SiI9438 — do these ICs handle the full eARC CMDC protocol autonomously, or does the host MCU need to participate in capability exchange?

---

## Sources & References

- [ITE Tech Product Catalog — Video Link Category](https://www.ite.com.tw/en/product/cate1)
- [ITE IT6621 Product Page — ARC/eARC Transmitter with Audio MUX](https://www.ite.com.tw/en/product/cate1/IT6621)
- [ITE IT6622 Product Page — HDMI 1.4 Tx with eARC RX and Embedded MCU](https://www.ite.com.tw/en/product/cate1/IT6622)
- [HDMI.org — Enhanced Audio Return Channel (eARC) Specification Overview](https://www.hdmi.org/spec2sub/enhancedaudioreturnchannel)
- [DPL Labs — HDMI eARC Detailed Technical Exploration (Physical Layer, CMDC, DMAC)](https://dpllabs.com/hdmis-enhanced-audio-return-channel-earc-detailed-technical-exploration/)
- [Granite River Labs — HDMI 2.1 eARC Compliance Testing: Channel Architecture and Encoding](https://www.graniteriverlabs.com/en-us/technical-blog/hdmi-earc-compliance-test)
- [Lattice Semiconductor — HDMI 2.1 eARC Transmitter/Receiver Product Page](https://www.latticesemi.com/en/Products/ASSPs/HDMI21eARC)
- [Dolby — HDMI 2.1 ARC and eARC Explained (Audio Format Support)](https://www.dolby.com/experience/home-entertainment/articles/hdmi-2.1-arc-and-earc-explained)
