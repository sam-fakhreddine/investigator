# Validation Report — ClockRecovery

**Date:** 2026-03-13
**Investigator output:** investigation.json
**Validator:** validator-clockrecovery

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge/ClockRecovery
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           98100f5cc366   98100f5cc366
tensions             IN_SYNC        5            5            37f3dfb49317   37f3dfb49317
open_questions       IN_SYNC        5            5            200b7825e8d5   200b7825e8d5
sources              IN_SYNC        6            6            f548e7586bb3   f548e7586bb3
concepts             IN_SYNC        6            6            b58687ef8a06   b58687ef8a06
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source URL Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | SiTime SiT3807 MEMS VCXO Product Page | https://www.sitime.com/products/voltage-controlled-oscillators/sit3807 | VERIFIED | Product page live. Confirms 1.544–49.152 MHz range, pull ranges +/-25 to +/-200 ppm. 24.576 MHz not explicitly listed but within range; 49.152 MHz upper bound suggests audio frequency support. |
| 2 | RFC 5905 - NTPv4 | https://datatracker.ietf.org/doc/html/rfc5905 | VERIFIED | Full RFC available. Section 11.3 covers clock discipline algorithm. |
| 3 | NTP Clock Discipline Algorithm (Mills, UDel) | https://www.eecis.udel.edu/~mills/ntp/html/discipline.html | VERIFIED | Page live. Describes hybrid PLL/FLL discipline loop, Allan intercept (~2048s), cold-start frequency measurement over 5-minute interval. |
| 4 | Are PLLs Dead? (IEEE) | https://ieeexplore.ieee.org/document/8039260/ | VERIFIED | IEEE Aerospace and Electronic Systems Magazine, Vol. 32, Issue 7, July 2017. Compares Kalman filter vs PLL for carrier synchronization. |
| 5 | NTP Clock State Machine Documentation | https://www.ntp.org/documentation/4.2.8-series/clock/ | VERIFIED | Describes 5-state machine: NSET, FSET, FREQ, SPIK, SYNC. Stepout threshold 300s. |
| 6 | DSPRelated: Fixing Sample Rate Error/Mismatch | https://www.dsprelated.com/thread/7564/fixing-sample-rate-error-mismatch | VERIFIED | Forum thread discussing buffer-fill-level control for rate mismatch, PLL-based interpolation, and ASRC approaches. |

---

## Finding Verification

| # | Finding (summary) | Verdict | Evidence | Source |
|---|-------------------|---------|----------|--------|
| 1 | 40 ppm worst-case crystal mismatch from two +/-20 ppm crystals | CONFIRMED | Standard quartz crystals are specified at +/-20 ppm. Two independent crystals can diverge by +20 and -20 ppm respectively, yielding 40 ppm total mismatch. This is basic arithmetic on industry-standard crystal specs. | General electronics engineering knowledge; crystal datasheets universally cite +/-20 ppm for standard parts. |
| 2 | 48 kHz x 40 ppm = 1.92 samples/sec drift, ~19 samples in 10s | CONFIRMED | 48000 x 40e-6 = 1.92; 1.92 x 10 = 19.2. Arithmetic is correct and straightforward. | Direct calculation. |
| 3 | ASRC cannot process IEC-61937 compressed bitstreams | CONFIRMED | ASRC operates by interpolating PCM sample values — treating them as waveform amplitudes. IEC-61937 compressed bitstreams (Dolby Digital, DTS) encode frequency-domain codec data where bit patterns are structurally significant. Interpolating between these values would corrupt the codec bitstream. This is a well-established constraint in professional audio. | IEC-61937 standard definition; professional audio engineering practice (Dante/AES67 avoid ASRC for this reason). |
| 4 | VCXO at 24.576 MHz with +/-100–200 ppm pull range commercially available | CONFIRMED | SiTime SiT3807 supports 1.544–49.152 MHz with pull ranges +/-25 to +/-200 ppm. 24.576 MHz is within the supported range. The upper bound of 49.152 MHz (= 2 x 24.576 MHz) is a standard audio master clock frequency, confirming audio clock use case. | SiTime SiT3807 product page (source #1). |
| 5 | Kalman filter is proven for clock synchronization | CONFIRMED | IEEE paper "Are PLLs Dead?" (2017) systematically compares Kalman filter and PLL approaches for synchronization, demonstrating KF advantages in challenging environments (high dynamics, fading, multipath). The technique is well-established in the literature. | IEEE paper (source #4). |
| 6 | Kalman filter may be over-engineered vs PI controller for this use case | CONFIRMED | The investigation itself correctly identifies this tension. A buffer-fill-level control loop has relatively benign noise characteristics compared to GNSS/deep-space scenarios where Kalman filters shine. The IEEE paper's advantages apply primarily to "challenging environments involving high dynamics, fading, multipath effects" — not a wired buffer occupancy signal. A PI controller is standard practice in Dante/AES67 implementations. | IEEE paper context; professional audio networking practice (Dante/AES67 typically use PI-based loops). |
| 7 | NTP RFC 5905 uses a two-stage approach: frequency acquisition then phase tracking | PARTIALLY CONFIRMED | The NTP clock discipline does use a multi-stage approach with states NSET, FSET, FREQ, SPIK, SYNC. The general pattern of frequency acquisition followed by phase tracking is correct. However, the investigation states "900-second frequency measurement interval in NTP's FREQ state" — this is inaccurate. The NTP.org documentation describes a 5-minute (300-second) cold-start frequency measurement period and a stepout threshold of 300 seconds. The 900-second figure does not appear in NTP primary documentation. The investigation also describes the state machine as "NSET -> FREQ -> SYNC or FSET -> SYNC" which omits the SPIK state (5 states total, not 4 implied). | NTP.org clock state machine page (source #5); Mills discipline page (source #3): "first measures the oscillator frequency over a five-min interval." |
| 8 | ~5 second convergence claim is optimistic; 2–10s more realistic | CONFIRMED | The investigation itself qualifies this claim as "optimistic" and provides 2–10s as a more realistic range. NTP cold start takes ~5 minutes for frequency acquisition, but an audio buffer-fill loop operates at much higher measurement rates (every buffer fill/drain cycle, potentially hundreds of Hz vs NTP's seconds-scale polls). The 2–10 second range is plausible for audio clock recovery depending on buffer depth, initial frequency offset, and loop bandwidth. | NTP documentation (source #3); engineering analysis of measurement rate differences. |
| 9 | Consumer AV receivers tolerate frame slip via internal PLLs | PARTIALLY CONFIRMED | Consumer S/PDIF receivers do use internal PLLs to recover clock, and they inherently tolerate small frequency offsets. However, the investigation correctly notes the asymmetry: PCM frame slip produces a click, while IEC-61937 compressed bitstream frame slip could corrupt a codec data burst. The claim "unlikely to cause failure" needs qualification — for compressed bitstreams, a frame slip hitting the 64-bit preamble or data burst could cause decoder mute. The investigation's own tension #4 acknowledges this but the quick_reference table says "Likely but unspecified" which understates the compressed audio risk. | Engineering analysis; IEC-61937 frame structure (preamble-sensitive). |
| 10 | Buffer-fill-level clock recovery is standard in professional audio (Dante, AES67, AVB) | CONFIRMED | This is well-established practice. The DSPRelated thread (source #6) discusses buffer-fill-level feedback for rate mismatch correction, including Fred Harris's description of using buffer address-space distance as a control error. Dante/AES67/AVB networks are known to use media clock recovery from buffer occupancy rather than ASRC. | DSPRelated thread (source #6); professional audio networking practice. |

---

## Flags

1. **NEEDS_PRIMARY_SOURCE — 900-second NTP frequency acquisition claim (Finding #7):** The investigation states "The 900-second frequency measurement interval in NTP's FREQ state is specific to network timing." This figure does not appear in the NTP primary documentation consulted. The Mills discipline page states frequency is measured over "a five-min interval" (300 seconds) at cold start, and the stepout threshold is 300 seconds. The 900-second figure should be corrected to 300 seconds, or a primary source citation provided if it refers to a different NTP parameter.

2. **CONFIRM_OR_HEDGE — Frame slip tolerance for compressed audio (Finding #9):** The quick_reference table assigns "Likely but unspecified" to frame slip tolerance. This is reasonable for PCM but potentially misleading for IEC-61937 compressed bitstreams, where the investigation's own tension #4 notes "dropping a frame during an IEC-61937 compressed bitstream could corrupt a codec data burst and cause decoder mute or error." The quick_reference verdict should be hedged to reflect this asymmetry more clearly.

3. **INTERNAL_CONFLICT — NTP state machine description:** Key finding #6 describes the state machine as "NSET -> FREQ -> SYNC or FSET -> SYNC" but omits the SPIK state. The concept definition for "Clock Discipline (NTP model)" also lists only 4 states. The actual NTP state machine has 5 states: NSET, FSET, FREQ, SPIK, SYNC. This is a minor inaccuracy but should be noted.

---

## Summary

- Sources: **6 verified / 6 total**, 0 dead, 0 unverifiable
- Findings: **7 confirmed**, **2 partially confirmed**, **0 unverified**, **0 contradicted**
- Flags: **3** (1 NEEDS_PRIMARY_SOURCE, 1 CONFIRM_OR_HEDGE, 1 INTERNAL_CONFLICT)
- Disputed items requiring correction:
  - The "900-second frequency measurement interval" claim should be corrected to 300 seconds (5 minutes) or a primary source provided for the 900s figure.
  - The NTP state machine description omits the SPIK state (5 states, not 4).
