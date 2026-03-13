# Investigation: RF Transport Bandwidth Verification for Wireless S/PDIF Bridge

**Date:** 2026-03-13
**Status:** Complete

---

## Question

> Are the RF transport bandwidth claims in the wireless S/PDIF bridge hypothesis accurate — specifically the nRF52840 2 Mbps real-world throughput (~1.5 Mbps), the ESP32 ESP-NOW ~214 Kbps claim, and the IEC-61937 payload bandwidth figures for Dolby Digital 5.1 (~448 Kbps typical, 640 Kbps max) and DTS (up to ~1.5 Mbps)?

---

## Context

A proposed wireless S/PDIF-to-eARC bridge design relies on RF transport to carry compressed surround-sound payloads (Dolby Digital, DTS) extracted from a wired S/PDIF stream. The design claims the nRF52840 in proprietary 2 Mbps mode can carry DD5.1 comfortably and DTS marginally, while ESP-NOW is too slow. This investigation verifies the specific bandwidth numbers against primary sources and first-principles calculations.

---

## Bandwidth Budget Summary

| Parameter | Claimed Value | Verified Value | Verdict |
| --- | --- | --- | --- |
| Raw S/PDIF at 48 kHz | 3.072 Mbps | 3.072 Mbps (48k x 64 bits/frame) | Confirmed |
| nRF52840 2 Mbps proprietary real-world throughput | ~1.5 Mbps | ~1.3-1.7 Mbps (depends on protocol design) | Plausible but optimistic |
| ESP32 ESP-NOW throughput (open, default PHY) | ~214 Kbps | ~214 Kbps (Espressif FAQ, 1 Mbps PHY) | Confirmed |
| Dolby Digital 5.1 typical bitrate | ~448 Kbps | 448 Kbps (DVD-Video spec maximum) | Confirmed |
| Dolby Digital 5.1 maximum bitrate | 640 Kbps | 640 Kbps (AC-3 codec maximum) | Confirmed |
| DTS core maximum bitrate | ~1.5 Mbps | 1509.75 Kbps (DVD max at 48 kHz) | Confirmed |
| DD5.1 640 Kbps fits nRF52840 1.5 Mbps | Comfortable margin | Yes — 38-49% of available bandwidth | Confirmed |
| DTS 1.5 Mbps fits nRF52840 1.5 Mbps | Marginal | Marginal to infeasible without protocol optimization | Confirmed risk |

> nRF52840 throughput is highly sensitive to protocol design choices: unidirectional streaming without ACKs can approach ~1.7 Mbps, while ESB with ACKs drops to ~1 Mbps. DTS feasibility depends entirely on which end of this range the implementation achieves.

---

## Key Findings

- Raw S/PDIF at 48 kHz is exactly 3.072 Mbps (48,000 frames/s x 64 bits/frame per IEC 60958), confirming it cannot be transmitted as-is over any 2.4 GHz ISM radio examined here.
- The nRF52840 2 Mbps proprietary radio mode achieves ~1.0 Mbps with Enhanced ShockBurst (bidirectional with ACKs) per Nordic DevZone measurements, not 1.5 Mbps as claimed for a general case.
- Unidirectional nRF52840 streaming without ACKs can theoretically reach ~1.7 Mbps with max-size payloads (252 bytes), making the ~1.5 Mbps claim achievable only with a custom unidirectional protocol and minimal overhead.
- The 1.5 Mbps claim for nRF52840 is plausible but optimistic — it requires careful protocol engineering: no ACKs, maximum payload sizes, minimal inter-packet gaps, and favorable RF conditions.
- ESP-NOW at default 1 Mbps PHY rate achieves ~214 Kbps in open environments and ~555 Kbps in shielded conditions per Espressif's official FAQ, confirming the 214 Kbps claim exactly.
- ESP-NOW throughput can reach ~400 Kbps at close range with ESP32-C6 per Espressif developer testing, but even this is insufficient for DD5.1 at 640 Kbps, ruling out ESP-NOW for this application.
- Dolby Digital (AC-3) supports bitrates up to 640 Kbps per the codec specification, with 448 Kbps being the DVD-Video maximum — both figures are confirmed by Dolby's specification and industry documentation.
- DTS Digital Surround core at 48 kHz maxes out at 1509.75 Kbps on DVD, which fits within the S/PDIF 48 kHz stereo container of 1536 Kbps (IEC 60958) — confirming the ~1.5 Mbps claim.
- DD5.1 at 640 Kbps uses only 38-49% of the nRF52840's achievable throughput range (1.3-1.7 Mbps), confirming a comfortable margin for wireless transport.
- DTS core at 1509.75 Kbps consumes 89-116% of the nRF52840 throughput range, making it marginal at best and infeasible at the lower end — the original assessment of 'marginal' is confirmed but may understate the risk.
- The IEC 61937 transport adds a small framing overhead (preamble words per burst) but the payload bitrate remains the dominant factor — the compressed bitstream bitrate is the correct metric for sizing the RF link.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| IEC 60958 / S/PDIF | Consumer digital audio interface standard using biphase mark encoding. At 48 kHz stereo, each frame is 64 bits (two 32-bit subframes), yielding a 3.072 Mbps information bitrate. The physical line rate is double (6.144 MHz) due to biphase encoding. |
| IEC 61937 | Standard for transporting non-linear PCM (compressed audio like AC-3, DTS) over an IEC 60958 link. Adds burst preambles to identify codec type and frame boundaries. The compressed payload replaces PCM sample data within the same 3.072 Mbps container. |
| nRF52840 Proprietary Radio | Nordic Semiconductor's 2.4 GHz radio supporting 1 Mbps and 2 Mbps proprietary modes with configurable packet format (1B preamble, 1-5B address, payload up to 253B, 0-3B CRC). Lower overhead than BLE stack but still subject to ISM band contention. |
| Enhanced ShockBurst (ESB) | Nordic's lightweight proprietary protocol providing packet buffering, acknowledgment, and automatic retransmission. At 2 Mbps PHY, ESB achieves ~1 Mbps application throughput due to ACK overhead and turnaround times. |
| ESP-NOW | Espressif's connectionless Wi-Fi protocol for ESP32, using vendor-specific action frames with a maximum 250-byte payload. Default PHY is 1 Mbps, achieving ~214 Kbps in open environments due to CSMA/CA overhead and Wi-Fi framing. |
| AC-3 (Dolby Digital) | Perceptual audio codec supporting up to 5.1 channels. Maximum bitrate is 640 Kbps per the AC-3 specification. DVD-Video caps at 448 Kbps. Transported via IEC 61937-3 over S/PDIF. |

---

## Tensions & Tradeoffs

- nRF52840 throughput is highly protocol-dependent: using ESB with ACKs gives reliability but halves throughput (~1 Mbps); removing ACKs doubles throughput but sacrifices error recovery — the DTS use case demands the higher end.
- DTS core at 1509.75 Kbps sits right at the boundary of nRF52840 capability, creating a binary pass/fail situation — unlike DD5.1 which has 40%+ margin, DTS has essentially zero margin in realistic conditions.
- The 2.4 GHz ISM band is shared with Wi-Fi, Bluetooth, and microwave ovens — real-world throughput can drop 20-40% below lab measurements, which would push even DD5.1 at 640 Kbps closer to the margin on a bad day.
- ESP-NOW's higher-PHY-rate modes (up to 54 Mbps Wi-Fi rates) can theoretically boost throughput to ~4.4 Mbps but suffer extreme packet loss at high rates, making the default 1 Mbps/214 Kbps the only reliable configuration.
- Removing ACKs from the nRF52840 protocol improves throughput but means any packet loss directly causes audio glitches — for real-time audio, FEC or redundancy must replace ACK-based reliability, consuming some of the throughput gained.

---

## Open Questions

- What is the measured nRF52840 unidirectional streaming throughput with 252-byte payloads and no ACKs in a typical home environment with active Wi-Fi?
- Can lightweight FEC (e.g., Reed-Solomon or XOR parity) protect DTS streams within the remaining ~200 Kbps margin above 1509.75 Kbps, or does FEC overhead push total required bandwidth beyond what nRF52840 can deliver?
- Would frequency hopping across the 2.4 GHz band (as BLE does) improve or hurt sustained throughput for continuous audio streaming on nRF52840 proprietary mode?
- Is there a practical path to use nRF52840's multi-channel radio capability to bond two channels for ~3 Mbps aggregate throughput, enabling comfortable DTS transport?
- For the common case where DTS content is encoded at 754.5 Kbps (half-rate, most DVD movies), does the design work comfortably — and should the system target half-rate DTS as the primary use case rather than full-rate?

---

## Sources & References

- [Nordic Semiconductor nRF52840 Product Specification — RADIO peripheral](https://docs.nordicsemi.com/bundle/ps_nrf52840/page/radio.html)
- [Espressif ESP-NOW FAQ — Throughput measurements](https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/esp-now.html)
- [Espressif Developer Blog — ESP-NOW for Outdoor Applications (throughput vs distance)](https://developer.espressif.com/blog/esp-now-for-outdoor-applications/)
- [Microsoft Learn — Representing Formats for IEC 61937 Transmissions (S/PDIF container rates)](https://learn.microsoft.com/en-us/windows/win32/coreaudio/representing-formats-for-iec-61937-transmissions)
- [ETSI TS 102 114 — DTS Coherent Acoustics specification (bitrate range 32-6144 Kbps)](https://www.etsi.org/deliver/etsi_ts/102100_102199/102114/01.02.01_60/ts_102114v010201p.pdf)
- [S/PDIF Free Space Digital Audio Optical Link — bitrate calculations at 48 kHz](https://www.jensign.com/SPDIFLink/)
- [Nordic DevZone — Intro to ShockBurst/Enhanced ShockBurst (ESB throughput calculations)](https://devzone.nordicsemi.com/nordic/nordic-blog/b/blog/posts/intro-to-shockburstenhanced-shockburst)
