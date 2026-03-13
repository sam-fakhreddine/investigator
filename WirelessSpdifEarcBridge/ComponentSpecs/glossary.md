# Glossary — Wireless S/PDIF-eARC Bridge — Component Specifications & BOM Validation

Quick definitions of key terms and concepts referenced in this investigation.

---

## VCXO (Voltage Controlled Crystal Oscillator)

An oscillator whose output frequency can be adjusted over a small range (typically +/-25 to +/-200 ppm) by varying a DC control voltage. Essential for clock recovery in S/PDIF receivers. Not to be confused with a passive crystal (no oscillation circuit) or a fixed XO (no voltage control).

## SPXO (Simple Packaged Crystal Oscillator)

A fixed-frequency crystal oscillator with no external frequency control input. The NDK NZ2520SDA is an SPXO — it outputs a stable clock but cannot be pulled by a control voltage for clock recovery.

## TSSOP-14 vs SSOP-28

TSSOP-14 is a Thin Shrink Small Outline Package with 14 pins and 0.65mm pitch. SSOP-28 has 28 pins and typically 0.65mm pitch. The PCM1808 uses TSSOP-14 — using an SSOP-28 footprint in a PCB design would be a layout-breaking error.

## Pull Range (VCXO)

The maximum frequency deviation achievable by varying the VCXO control voltage from minimum to maximum (typically 0V to 3.3V or 0.5V to 4.5V). Expressed in ppm. For S/PDIF clock recovery, +/-50 to +/-100 ppm is typically sufficient.

## Component Lifecycle Status

Indicates manufacturing status: ACTIVE (in production), NRND (not recommended for new designs), OBSOLETE (discontinued). The TORX173/TOTX173 modules are OBSOLETE, meaning supply may become scarce and alternatives should be evaluated for new designs.

## I2S (Inter-IC Sound)

A serial bus interface standard for connecting digital audio devices. Uses three lines: BCK (bit clock), LRCK (left/right clock), and DOUT (serial data). The PCM1808 supports both I2S and left-justified formats in master or slave mode.

## STM32 Timer Encoder Mode

A hardware peripheral mode on STM32 timers that automatically counts quadrature encoder pulses, detecting direction and position without software interrupt handling. Uses TI1/TI2 inputs on general-purpose timers (TIM2-TIM5, TIM1, TIM8).

---

*Back to: [investigation.md](investigation.md)*
