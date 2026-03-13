# Investigation: Clock Recovery Claims in Wireless S/PDIF Bridge

**Date:** 2026-03-13
**Status:** Complete

---

## Question

> Are the clock recovery claims in the wireless S/PDIF bridge hypothesis accurate -- specifically the 40 ppm crystal mismatch drift calculation, the unsuitability of ASRC for IEC-61937 bitstreams, and the proposed VCXO + Kalman filter approach for clock discipline?

---

## Context

A wireless S/PDIF-to-eARC bridge design proposes replacing the wired S/PDIF clock link with a wireless transport. Without a shared clock between transmitter and receiver, the design must recover timing from buffer fill level using a VCXO disciplined by a Kalman filter. The hypothesis makes specific claims about crystal drift rates, ASRC limitations on compressed audio, VCXO feasibility at 24.576 MHz, and convergence behavior modeled after NTP clock discipline.

---

## Claim Verification Summary

| Claim | Verdict | Notes |
| --- | --- | --- |
| Crystal pair mismatch up to 40 ppm | Confirmed | Standard crystals are +/-20 ppm; worst-case pair yields 40 ppm total |
| 40 ppm at 48 kHz = 1.92 Hz drift | Confirmed | 48000 x 40e-6 = 1.92 samples/second -- arithmetic is correct |
| ~19 samples in 10 seconds | Confirmed | 1.92 x 10 = 19.2 samples -- causes audible glitches without correction |
| ASRC cannot process IEC-61937 bitstreams | Confirmed | ASRC operates on PCM sample values; compressed bitstreams are data, not waveforms |
| VCXO at 24.576 MHz with +/-100-200 ppm range | Confirmed | SiTime SiT3807 offers +/-25 to +/-200 ppm pull range at 1.5-49.2 MHz |
| Kalman filter for clock rate estimation | Plausible with caveats | Kalman filter is proven for clock sync; may be over-engineered vs PI loop for this use case |
| Two-stage lock similar to NTP RFC 5905 | Confirmed | NTP uses a 5-state machine (NSET, FSET, FREQ, SPIK, SYNC) with 300s cold-start frequency acquisition |
| ~5 second initial lock convergence | Optimistic | NTP cold start takes 300s for freq; audio buffer loop likely 2-10s depending on buffer depth |
| Frame slip tolerated by AV receivers | Likely but unspecified | Consumer receivers handle clock drift via internal PLLs; occasional frame slip unlikely to cause failure |

> Verdicts are based on published specifications, standards documents, and engineering literature. 'Confirmed' means the claim matches primary sources; 'Plausible' means the approach is sound but details need qualification.

---

## Key Findings

- The 40 ppm worst-case crystal mismatch calculation is correct: standard quartz crystals specify +/-20 ppm frequency tolerance, and two independent crystals can diverge by up to 40 ppm in opposite directions.
- The drift arithmetic is verified: at 48 kHz sample rate, 40 ppm mismatch produces 1.92 samples/second of drift (48000 x 40e-6), accumulating ~19 samples in 10 seconds -- sufficient to cause audible clicks or gaps.
- ASRC fundamentally cannot process IEC-61937 compressed bitstreams because ASRC operates by interpolating between PCM sample values to reconstruct the analog waveform at a new rate. Compressed audio (Dolby Digital, DTS) encodes frequency-domain data where every bit is structurally significant -- interpolation would corrupt the codec bitstream, not resample it.
- VCXO oscillators at 24.576 MHz with +/-100 to +/-200 ppm pull range are commercially available from multiple vendors. The SiTime SiT3807 MEMS VCXO supports 1.544-49.152 MHz with configurable pull ranges of +/-25 to +/-200 ppm, confirming both the frequency and tuning range claims.
- Kalman filtering is a proven technique for clock synchronization, with IEEE literature demonstrating advantages over fixed-bandwidth PLLs in adaptive bandwidth and optimal state estimation. However, for a buffer-fill-level control loop with relatively benign noise characteristics, a well-tuned PI controller may achieve comparable performance with far less complexity.
- The NTP RFC 5905 clock discipline algorithm uses a documented 5-state machine (NSET, FSET, FREQ, SPIK, SYNC) with a two-stage approach: frequency acquisition followed by phase tracking. The 300-second cold-start frequency measurement period in NTP's FREQ state is specific to network timing; an audio buffer control loop would use a much shorter acquisition phase.
- The ~5 second convergence claim is optimistic but not implausible for audio clock recovery. NTP achieves initial offset estimates in ~10 seconds with iburst mode, and buffer-fill-based loops can converge faster due to higher measurement rates, but 2-10 seconds is a more realistic range depending on buffer depth and initial frequency offset.
- Consumer AV receivers and soundbars use internal PLLs to recover clock from the S/PDIF bitstream. They tolerate small frequency offsets inherently, but an abrupt frame slip (dropping or repeating one S/PDIF frame) would produce a transient glitch. Whether this is audible depends on content type: PCM would produce a click, while compressed bitstreams would likely cause a decoder error or mute.
- The buffer-fill-level approach to clock recovery is well-established in professional audio (Dante, AES67, AVB networks) where ASRC is avoided for latency and transparency reasons. Using buffer occupancy as the control variable for a VCXO is the standard technique in these systems.
- A critical tension exists between VCXO pull range and phase noise: wider pull ranges (+/-200 ppm) provide more headroom for frequency correction but increase oscillator phase noise, which appears as jitter on the recovered S/PDIF clock. For audio at 48 kHz, phase noise below 1 ns RMS is desirable.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| PPM (Parts Per Million) | Unit expressing crystal oscillator frequency accuracy. A +/-20 ppm crystal at 48 kHz can deviate by up to +/-0.96 Hz from nominal. Two independent crystals with +/-20 ppm specs can differ by up to 40 ppm from each other. |
| ASRC (Asynchronous Sample Rate Converter) | Hardware or software that converts PCM audio from one sample rate to another by interpolating between samples. Requires the input to be interpretable as a waveform -- cannot operate on compressed/encoded bitstreams like IEC-61937. |
| IEC-61937 | Standard for transporting non-linear (compressed) PCM audio over IEC-60958 (S/PDIF) interfaces. Wraps Dolby Digital, DTS, and other codec bitstreams in data bursts with a 64-bit preamble. Every bit in the payload is codec-significant. |
| VCXO (Voltage-Controlled Crystal Oscillator) | Crystal oscillator whose frequency can be adjusted over a narrow range (typically +/-25 to +/-200 ppm) by varying a control voltage. Used in clock recovery to discipline a local oscillator to match a remote reference. |
| Kalman Filter | Optimal recursive state estimator that combines noisy measurements with a dynamic model to estimate hidden state variables (here: clock frequency offset and drift rate). Offers adaptive bandwidth but adds computational complexity vs simpler PI loops. |
| Clock Discipline (NTP model) | Algorithm from RFC 5905 using a 5-state machine (NSET, FSET, FREQ, SPIK, SYNC) to first measure oscillator frequency error, then track phase offset. The two-stage acquisition/tracking pattern is applicable to audio clock recovery at compressed timescales. |

---

## Tensions & Tradeoffs

- VCXO pull range vs phase noise: wider tuning range enables correction of larger frequency offsets but degrades oscillator phase noise (jitter), directly impacting S/PDIF clock quality.
- Kalman filter optimality vs implementation complexity: Kalman filtering provides theoretically optimal state estimation, but a well-tuned PI controller may be sufficient for the relatively benign noise environment of a buffer-fill control loop, at a fraction of the computational cost.
- Convergence speed vs stability: faster acquisition requires wider loop bandwidth, which admits more noise into the frequency estimate and risks oscillation. The ~5 second claim may require aggressive initial bandwidth that compromises steady-state tracking.
- Frame slip tolerance for PCM vs compressed bitstreams: dropping a single S/PDIF frame during PCM playback produces a minor click, but dropping a frame during an IEC-61937 compressed bitstream could corrupt a codec data burst and cause decoder mute or error -- the consequences are asymmetric.
- Buffer depth vs latency: deeper buffers provide more time for the clock recovery loop to converge and absorb jitter, but add audio-video synchronization latency. The wireless transport already adds latency from RF processing.

---

## Open Questions

- What is the actual phase noise specification of available 24.576 MHz VCXOs at +/-100 ppm pull range, and does it meet the jitter requirements of consumer S/PDIF receivers (typically < 50 ns UI-referenced jitter tolerance)?
- Has anyone implemented Kalman-filter-based clock recovery specifically for S/PDIF or IEC-61937 bitstream transport, as opposed to PCM audio networking (Dante/AES67)? The compressed bitstream case adds the constraint that frame slip is more destructive.
- What is the measured convergence time for a buffer-fill-level VCXO discipline loop with realistic wireless transport jitter, and how does it compare to the ~5 second claim?
- How do consumer AV receivers actually handle a single dropped or repeated S/PDIF frame during IEC-61937 compressed playback -- do they mute, glitch, or silently resync?
- Would a hybrid approach (PI controller for steady-state, Kalman filter only during acquisition) provide the best tradeoff between convergence speed and implementation simplicity?

---

## Sources & References

- [SiTime SiT3807 MEMS VCXO Product Page](https://www.sitime.com/products/voltage-controlled-oscillators/sit3807)
- [RFC 5905 - Network Time Protocol Version 4: Protocol and Algorithms Specification](https://datatracker.ietf.org/doc/html/rfc5905)
- [NTP Clock Discipline Algorithm (Mills, University of Delaware)](https://www.eecis.udel.edu/~mills/ntp/html/discipline.html)
- [Are PLLs Dead? Kalman Filter-Based Techniques for Digital Carrier Synchronization (IEEE)](https://ieeexplore.ieee.org/document/8039260/)
- [NTP Clock State Machine Documentation](https://www.ntp.org/documentation/4.2.8-series/clock/)
- [DSPRelated: Fixing Sample Rate Error/Mismatch (Buffer-Fill Clock Recovery Discussion)](https://www.dsprelated.com/thread/7564/fixing-sample-rate-error-mismatch)
