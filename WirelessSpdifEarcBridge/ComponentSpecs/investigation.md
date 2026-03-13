# Investigation: Wireless S/PDIF-eARC Bridge — Component Specifications & BOM Validation

**Date:** 2026-03-13
**Status:** Complete

---

## Question

> Are the component specifications and BOM cost estimates in the wireless S/PDIF bridge hypothesis accurate — specifically the PCM1808, EC11 encoder, VCXO parts (TXC 7M series, NDK NZ2520SDA), TOSLINK modules (TORX173/TOTX173), and the ~$67 core / ~$97-120 total cost estimate?

---

## Context

The wireless S/PDIF-to-eARC bridge hypothesis proposes a BOM with specific ICs and modules for audio ADC, TOSLINK I/O, wireless transport, user input, and clock recovery. This investigation cross-references each component against current datasheets and distributor pricing (DigiKey, Mouser, LCSC, AliExpress) to determine whether the specs cited in the hypothesis match reality and whether the cost estimates are plausible at hobby/prototype quantities.

---

## Component BOM Quick Reference

| Component | Claimed Spec | Verified Spec | Claimed Price | Verified Price | Status |
| --- | --- | --- | --- | --- | --- |
| PCM1808 (ADC) | 24-bit/96kHz, SSOP-28, I2S slave | 24-bit/96kHz, TSSOP-14, I2S master+slave | ~$2 | $0.32-1.50 | Spec error on package; price conservative |
| EC11 Encoder | 20 detents, quad A/B + push | 20 detents, quad A/B + push, 18deg step | ~$1 | $1.00-1.45 | Accurate |
| STM32 Timer Encoder Mode | HW quad decode, zero CPU | HW quad decode via TIMx, near-zero CPU | N/A | N/A | Accurate (minor overstatement on zero CPU) |
| TXC 7M VCXO | VCXO, 24.576MHz, +/-100-200ppm | 7M is a passive crystal, NOT a VCXO | ~$5 | N/A | INCORRECT — 7M is not a VCXO |
| NDK NZ2520SDA | VCXO, 24.576MHz, +/-100ppm | Fixed XO (SPXO), no voltage control | N/A | $5-10 (specialty) | INCORRECT — not a VCXO |
| TORX173 (RX) | TOSLINK RX module | TOSLINK RX, 6Mb/s, 5V, JEITA CP-1201 | ~$2 | $1-3 (obsolete) | Spec accurate; lifecycle risk |
| TOTX173 (TX) | TOSLINK TX module | TOSLINK TX, 6Mb/s, 5V, 660nm | ~$2 | $1-2 | Spec accurate; lifecycle risk |
| E73-2G4M08S1C (nRF52840) | BLE 5.0 module | nRF52840, BLE 5.0, 8dBm, SMD | ~$4 | $5.00-5.52 | Spec accurate; price ~38% higher |
| Nucleo-F446RE | STM32F446 dev board | STM32F446RET6, 180MHz, Arduino headers | ~$20 | $14.85 | Spec accurate; price 25% lower |
| Actual VCXO alternative | N/A | SiT3807 or Abracon ASVV, +/-50-200ppm | N/A | $5-10 | Viable replacements exist |

> Prices reflect single-unit or small-quantity orders from authorized distributors as of March 2026. LCSC prices tend lower; DigiKey/Mouser slightly higher.

---

## Key Findings

- PCM1808 is correctly identified as a 24-bit/96kHz stereo ADC with I2S output, but the hypothesis incorrectly states SSOP-28 package — the actual package is TSSOP-14 (14 pins, not 28). This is a significant PCB footprint error that would affect board layout.
- PCM1808 pricing is conservative at ~$2 — LCSC lists the PCM1808PWR at $0.32 per unit, and DigiKey stocks it around $1.50 in single quantities. The part is actively manufactured by TI with an ACTIVE lifecycle status.
- The EC11 rotary encoder claim of 20 detents with quadrature A/B output and push switch is fully accurate. Pricing at ~$1 is confirmed across LCSC ($1.08) and other distributors.
- STM32 timer encoder mode does support hardware quadrature decoding — TIM2-TIM5 and TIM1/TIM8 on the F446 all have this mode. The claim of 'zero CPU overhead' is slightly overstated: the CPU must still read the counter register, but the actual edge counting and direction detection are fully hardware-driven.
- The TXC 7M series is NOT a VCXO — it is a passive quartz crystal (no oscillator circuit, no voltage control pin). The hypothesis fundamentally misidentifies this component. A VCXO requires an active oscillator with voltage control input.
- The NDK NZ2520SDA is NOT a VCXO — it is a fixed-frequency SPXO (crystal oscillator) with ultra-low phase noise (43fs jitter typical). It has no voltage control input and no tuning range. Its frequency tolerance is +/-50ppm fixed, not tuneable.
- Both TORX173 and TOTX173 TOSLINK modules have correct specifications (6Mb/s, 5V, JEITA CP-1201 compliant) and pricing (~$1-3). However, both carry an OBSOLETE lifecycle status from Toshiba, creating supply chain risk for a new design.
- The Ebyte E73-2G4M08S1C nRF52840 module is correctly specified but priced ~38% higher than claimed: LCSC lists it at $5.52 versus the hypothesized ~$4. It remains in active production with stock available.
- The Nucleo-F446RE is accurately specified and actually cheaper than estimated — DigiKey lists it at $14.85 versus the hypothesized ~$20, saving ~$5 per unit.
- Viable 24.576MHz VCXO alternatives exist: the SiTime SiT3807 MEMS VCXO offers +/-25 to +/-200ppm pull range in multiple packages (2520-7050), and the Abracon ASVV series provides +/-50ppm pull range in a 7050 package. Both are actively produced and stocked at major distributors.
- The core BOM estimate of ~$67 needs revision: correcting the nRF52840 price upward (+$1.50), the Nucleo price downward (-$5), adding a proper VCXO (~$5-10 depending on source), and accounting for the TOSLINK obsolescence risk, the adjusted core BOM is likely in the $60-75 range — broadly consistent with the original estimate.
- The total BOM estimate of $97-120 including passives and test equipment remains plausible. Passive components (decoupling caps, resistors, connectors) typically add $10-20, and basic test equipment (logic analyzer, scope probes) can range from $20-50 for hobby-grade tools.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| VCXO (Voltage Controlled Crystal Oscillator) | An oscillator whose output frequency can be adjusted over a small range (typically +/-25 to +/-200 ppm) by varying a DC control voltage. Essential for clock recovery in S/PDIF receivers. Not to be confused with a passive crystal (no oscillation circuit) or a fixed XO (no voltage control). |
| SPXO (Simple Packaged Crystal Oscillator) | A fixed-frequency crystal oscillator with no external frequency control input. The NDK NZ2520SDA is an SPXO — it outputs a stable clock but cannot be pulled by a control voltage for clock recovery. |
| TSSOP-14 vs SSOP-28 | TSSOP-14 is a Thin Shrink Small Outline Package with 14 pins and 0.65mm pitch. SSOP-28 has 28 pins and typically 0.65mm pitch. The PCM1808 uses TSSOP-14 — using an SSOP-28 footprint in a PCB design would be a layout-breaking error. |
| Pull Range (VCXO) | The maximum frequency deviation achievable by varying the VCXO control voltage from minimum to maximum (typically 0V to 3.3V or 0.5V to 4.5V). Expressed in ppm. For S/PDIF clock recovery, +/-50 to +/-100 ppm is typically sufficient. |
| Component Lifecycle Status | Indicates manufacturing status: ACTIVE (in production), NRND (not recommended for new designs), OBSOLETE (discontinued). The TORX173/TOTX173 modules are OBSOLETE, meaning supply may become scarce and alternatives should be evaluated for new designs. |
| I2S (Inter-IC Sound) | A serial bus interface standard for connecting digital audio devices. Uses three lines: BCK (bit clock), LRCK (left/right clock), and DOUT (serial data). The PCM1808 supports both I2S and left-justified formats in master or slave mode. |
| STM32 Timer Encoder Mode | A hardware peripheral mode on STM32 timers that automatically counts quadrature encoder pulses, detecting direction and position without software interrupt handling. Uses TI1/TI2 inputs on general-purpose timers (TIM2-TIM5, TIM1, TIM8). |

---

## Tensions & Tradeoffs

- The hypothesis names two VCXO parts (TXC 7M, NDK NZ2520SDA) that are not VCXOs at all — this is a fundamental component selection error that must be corrected before prototyping, as clock recovery requires a true VCXO.
- TORX173/TOTX173 TOSLINK modules are functionally correct and cheap but carry OBSOLETE status — designing around discontinued parts risks supply chain disruption; alternatives should be sourced now.
- The PCM1808 package error (SSOP-28 vs actual TSSOP-14) would cause a PCB layout failure if not caught before fabrication — fewer pins also means fewer configuration options than might be expected.
- The nRF52840 module price is ~38% higher than estimated ($5.50 vs $4), which is small per-unit but compounds across a two-board design (TX + RX) and prototype iterations.
- VCXO availability at 24.576MHz with sufficient pull range (+/-100ppm+) at hobby quantities is limited — MEMS VCXOs (SiTime SiT3807) offer the best specs but may cost $7-10, while quartz VCXOs (Abracon ASVV) are cheaper but only offer +/-50ppm pull range.

---

## Open Questions

- What specific VCXO will replace the incorrectly specified TXC 7M / NDK NZ2520SDA? The SiTime SiT3807 at 24.576MHz with +/-100ppm pull range is the strongest candidate but pricing needs confirmation at single-unit quantities.
- Are there currently-in-production TOSLINK RX/TX modules that can directly replace the obsolete TORX173/TOTX173 without PCB footprint changes?
- Does the +/-50ppm pull range of the Abracon ASVV provide sufficient tuning margin for S/PDIF clock recovery, or is the +/-100ppm or higher range of the SiT3807 required?
- Should the BOM account for a second VCXO at 22.5792MHz to support 44.1kHz-family sample rates (44.1k, 88.2k), or will a single 24.576MHz VCXO with fractional-N PLL suffice?

---

## Sources & References

- [TI PCM1808 Product Page — 24-bit 96kHz Stereo ADC](https://www.ti.com/product/PCM1808)
- [PCM1808 Datasheet (TI SLES167)](https://www.ti.com/lit/gpn/PCM1808)
- [NDK NZ2520SDA Crystal Oscillator Product Page](https://www.ndk.com/en/products/lineup/crystal-oscillator/NZ2520SDA.html)
- [SiTime SiT3807 MEMS VCXO Product Page](https://www.sitime.com/products/mhz-oscillators/voltage-controlled-oscillators/sit3807)
- [Abracon ASVV Series VCXO Datasheet](https://abracon.com/Oscillators/ASVV.pdf)
- [STM32 Timer Encoder Mode — DeepBlue Embedded Tutorial](https://deepbluembedded.com/stm32-timer-encoder-mode-stm32-rotary-encoder-interfacing/)
- [LCSC PCM1808PWR Listing (C55513) — Pricing and Stock](https://www.lcsc.com/product-detail/C55513.html)
- [LCSC E73-2G4M08S1C Listing (C356849) — Pricing and Stock](https://www.lcsc.com/product-detail/C356849.html)
- [Ebyte E73-2G4M08S1C nRF52840 Module Product Page](https://www.cdebyte.com/products/E73-2G4M08S1C)
- [STMicroelectronics NUCLEO-F446RE Product Page](https://www.st.com/en/evaluation-tools/nucleo-f446re.html)
