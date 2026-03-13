# Clock Recovery Claims in Wireless S/PDIF Bridge — Product Brief

**Date:** 2026-03-13
**Risk Level:** MEDIUM

---

## What Is This?

> The proposed clock recovery approach for the wireless audio bridge is technically viable and uses proven components.

---

## What Does This Mean for Us?

The design correctly identifies that wireless audio transport needs active clock synchronization, and the chosen components (VCXO oscillator, buffer-based timing recovery) are standard industry practice. The main product risk is the initial sync time when the device powers on -- it may take several seconds before audio plays cleanly.

---

## Key Points

- The core technical claims about clock drift and component selection have been verified against manufacturer specs and standards.
- Users will experience a brief silence or glitch when the device first connects while the clock synchronization locks -- estimated 2-10 seconds.
- Compressed surround sound formats (Dolby, DTS) require bit-perfect transport, which the design correctly accounts for by avoiding sample rate conversion.

---

## Next Steps

**PO/EM Decision:**

> Define acceptable initial sync time for the user experience -- is 5-10 seconds of silence at power-on acceptable, or does the product need faster lock?

**Engineering Work Items:**
- Build a clock recovery prototype using PI controller and measure actual convergence time with wireless transport jitter.
- Test frame slip behavior on 3-5 popular AV receivers/soundbars to determine real-world tolerance for compressed audio.

**Leadership Input Required:**

> Decide whether Kalman filter complexity is justified given the cost/power constraints of the target hardware platform.

---

## Open Questions

- What is the actual measured lock time with realistic wireless channel conditions?
- How does the device behave during the initial sync period -- silence, noise, or muted output?
- What happens if the wireless link drops briefly -- does the clock recovery need to re-acquire from scratch?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
