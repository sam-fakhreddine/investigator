# Clock Recovery Claims in Wireless S/PDIF Bridge — Engineering Leadership Brief

**Date:** 2026-03-13

---

## Headline

> The clock recovery design is technically sound in its core claims but the ~5 second convergence time and Kalman filter choice need qualification.

---

## So What

The fundamental physics (40 ppm drift, ASRC incompatibility with compressed audio, VCXO feasibility) are all verified against primary sources. The main risk is over-engineering: a Kalman filter adds complexity where a PI controller may suffice, and the convergence time claim needs empirical validation with realistic wireless jitter.

---

## Key Points

- Crystal drift math is correct: 40 ppm worst-case produces 1.92 samples/second drift at 48 kHz, requiring active clock recovery.
- ASRC cannot be used on IEC-61937 compressed bitstreams -- VCXO-based clock recovery is the correct architectural choice.
- 24.576 MHz VCXOs with +/-100-200 ppm pull range are commercially available (SiTime SiT3807), confirming hardware feasibility.
- Kalman filter is proven for clock sync but may be over-engineered for this application vs a simpler PI controller.
- The ~5 second lock time is optimistic; budget 2-10 seconds depending on buffer depth and initial frequency offset.

---

## Action Required

> Prototype the clock recovery loop with a PI controller first and benchmark against Kalman filter to determine if the added complexity is justified.

---

*Full engineering investigation: [investigation.md](investigation.md)*
