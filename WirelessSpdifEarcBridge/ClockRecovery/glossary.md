# Glossary — Clock Recovery Claims in Wireless S/PDIF Bridge

Quick definitions of key terms and concepts referenced in this investigation.

---

## PPM (Parts Per Million)

Unit expressing crystal oscillator frequency accuracy. A +/-20 ppm crystal at 48 kHz can deviate by up to +/-0.96 Hz from nominal. Two independent crystals with +/-20 ppm specs can differ by up to 40 ppm from each other.

## ASRC (Asynchronous Sample Rate Converter)

Hardware or software that converts PCM audio from one sample rate to another by interpolating between samples. Requires the input to be interpretable as a waveform -- cannot operate on compressed/encoded bitstreams like IEC-61937.

## IEC-61937

Standard for transporting non-linear (compressed) PCM audio over IEC-60958 (S/PDIF) interfaces. Wraps Dolby Digital, DTS, and other codec bitstreams in data bursts with a 64-bit preamble. Every bit in the payload is codec-significant.

## VCXO (Voltage-Controlled Crystal Oscillator)

Crystal oscillator whose frequency can be adjusted over a narrow range (typically +/-25 to +/-200 ppm) by varying a control voltage. Used in clock recovery to discipline a local oscillator to match a remote reference.

## Kalman Filter

Optimal recursive state estimator that combines noisy measurements with a dynamic model to estimate hidden state variables (here: clock frequency offset and drift rate). Offers adaptive bandwidth but adds computational complexity vs simpler PI loops.

## Clock Discipline (NTP model)

Algorithm from RFC 5905 using a 5-state machine (NSET, FSET, FREQ, SPIK, SYNC) to first measure oscillator frequency error, then track phase offset. The two-stage acquisition/tracking pattern is applicable to audio clock recovery at compressed timescales.

---

*Back to: [investigation.md](investigation.md)*
