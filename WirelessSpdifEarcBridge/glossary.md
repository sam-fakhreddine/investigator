# Glossary — Wireless S/PDIF to eARC Bridge — Hypothesis Verification

Quick definitions of key terms and concepts referenced in this investigation.

---

## IEC 61937 Bitstream Transport

Standard for conveying compressed multichannel audio (Dolby Digital, DTS) over IEC 60958 (S/PDIF) and HDMI interfaces. Every bit in the payload is codec-significant — the bitstream must pass through untouched without PCM-style interpolation or sample rate conversion.

## eARC (Enhanced Audio Return Channel)

HDMI 2.1 feature providing 37 Mbps audio bandwidth from sink to source using dedicated DMAC and CMDC channels independent of CEC. Supports DD, DD+, TrueHD, Atmos, DTS-HD MA, and uncompressed PCM up to 7.1ch/192kHz.

## SPDIFRX Hardware Peripheral

Dedicated receiver on select STM32 MCUs (F446, F469, F479, F7, H7, MP1) that decodes biphase mark coding, detects preambles, and separates audio data from channel status in silicon. Does not include a clock recovery PLL.

## VCXO (Voltage-Controlled Crystal Oscillator)

Oscillator whose frequency is adjustable over a narrow range (+/-25 to +/-200 ppm) via a DC control voltage. Essential for clock recovery when bridging asynchronous audio domains. Not to be confused with passive crystals (no oscillator) or fixed XOs (no voltage control).

## nRF52840 Proprietary Radio

Nordic Semiconductor's 2.4 GHz radio supporting 2 Mbps proprietary mode with configurable packet format. Achieves ~1.0 Mbps with ESB (ACKs) or ~1.7 Mbps unidirectional with max payloads — protocol design determines whether DTS fits.

## ASRC (Asynchronous Sample Rate Conversion)

Converts PCM audio between independent clock domains by interpolating sample values. Cannot operate on IEC-61937 compressed bitstreams where bits encode frequency-domain codec data rather than waveform amplitudes.

## Projector Topology Problem

Physical separation of ceiling/rear-mounted projector from front-mounted soundbar (3-10m) with no cable path. No mainstream wireless product bridges this gap with multichannel audio — mainstream solutions are stereo-only (Bluetooth, AirPlay) or closed-ecosystem (WiSA).

## CMDC (Common Mode Data Channel)

Bidirectional control channel in eARC for discovery, capability exchange, and heartbeat. Operates independently of CEC on the HEAC pin pair (HDMI pins 14/19). Dedicated eARC ICs handle CMDC autonomously.

## Clock Discipline (Buffer-Fill VCXO Loop)

Technique from professional audio networking (Dante, AES67) where buffer occupancy drives a VCXO control voltage to match remote clock rate. Avoids ASRC latency and preserves bit-perfect compressed audio transport. A PI controller may suffice over a Kalman filter for this use case.

## Enhanced ShockBurst (ESB)

Nordic's lightweight proprietary protocol providing packet buffering, ACK, and retransmission. At 2 Mbps PHY, ESB achieves ~1 Mbps application throughput due to ACK overhead — removing ACKs doubles throughput but sacrifices error recovery.

---

*Back to: [investigation.md](investigation.md)*
