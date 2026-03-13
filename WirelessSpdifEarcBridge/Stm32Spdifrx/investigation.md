# Investigation: STM32F446 SPDIFRX Hardware Peripheral Capabilities and Availability

**Date:** 2026-03-13
**Status:** Complete

---

## Question

> Does the STM32F446 have a dedicated hardware SPDIFRX peripheral that handles biphase mark coding, synchronisation preamble detection, and symbol clock extraction in silicon -- and is this peripheral exclusive to the STM32 F4/F7/H7 series?

---

## Context

The Wireless S/PDIF eARC Bridge project requires receiving S/PDIF audio on a microcontroller. The STM32F446 is a candidate because it integrates a hardware SPDIFRX peripheral that could offload BMC decoding from firmware. This investigation verifies the peripheral's silicon-level capabilities, its availability across STM32 families, and the feasibility of running SPDIFRX alongside SAI output via DMA on a Nucleo-F446RE board.

---

## STM32F446 Audio Peripheral Summary

| Feature | Detail |
| --- | --- |
| SPDIFRX peripheral | 1x dedicated receiver, IEC-60958 and IEC-61937 compliant |
| BMC decode | Hardware — measures time intervals between transitions, not firmware |
| Preamble detection | Hardware — synchronisation state machine with free-running, sync, and locked states |
| Symbol clock output | spdifrx_symb_ck signal, routable to SAI or TIM for rate measurement (caveat: SAI routing via this path reported unreliable per ST community; treat as unverified) |
| SAI peripheral | 2x SAI blocks, full-duplex I2S/TDM, dedicated audio PLLs |
| DMA controllers | 2x (DMA1 + DMA2), each with 8 streams x 8 channels = 128 total configurations |
| SPDIFRX DMA | Two dedicated DMA requests: DMA_SPDIFRX_DT (data) and DMA_SPDIFRX_CS (channel status) |
| CPU | ARM Cortex-M4F, 180 MHz, FPU, DSP instructions |
| Families with SPDIFRX | STM32F4 (F446, F469, F479 within F4), F7 series, H7 series, MP1 series |

> Within the STM32F4 family, SPDIFRX is present on the F446, F469, and F479 lines (F469/F479 confirmed via RM0386); it is absent from the F401, F405, F407, F411, F412, F427, and F429.

---

## Key Findings

- The STM32F446 contains a dedicated hardware SPDIFRX peripheral that performs biphase mark code (BMC) decoding entirely in silicon by measuring time intervals between consecutive signal transitions -- no firmware-level bit-banging is required.
- The SPDIFRX peripheral implements a hardware synchronisation state machine that detects S/PDIF preambles (B, M, W) and locks to the incoming data stream, transitioning through free-running, sync, and locked states automatically.
- Symbol clock extraction is performed in hardware: the peripheral generates a spdifrx_symb_ck signal that can be routed internally to SAI or to a TIM input capture for precise sample-rate measurement. Note: ST community reports indicate that spdifrx_symb_ck routing to SAI as documented in RM0390 may contain errors and SAI synchronisation via this path is unreliable in practice -- this signal path should be treated as unverified until confirmed on hardware.
- The SPDIFRX is compliant with IEC-60958 (consumer/professional S/PDIF) and IEC-61937 (compressed multi-channel surround sound). The peripheral's spec covers 32 kHz to 192 kHz; on the STM32F446 specifically, 192 kHz reception may be limited by RCC clock constraints (requires a dedicated SPDIFRX clock of at least 135.2 MHz) -- confirmed for 44.1/48/96 kHz operation; 192 kHz support on F446 should be verified empirically.
- Within the STM32F4 family, SPDIFRX is present on the F446, F469, and F479 lines; it is absent from the F401, F405, F407, F411, F427, and F429. The F469/F479 inclusion is documented in RM0386. The STM32L476 Discovery, an L-series part, explicitly lacks hardware S/PDIF and requires a software decoder.
- The SPDIFRX peripheral is also present on STM32F7 series, STM32H7 series, and STM32MP1 series (confirmed via Linux kernel device tree bindings for st,stm32h7-spdifrx and ST MPU wiki documentation).
- ST Application Note AN5073 (Rev 2.0, September 2018) is titled 'Receiving S/PDIF audio stream with the STM32F4/F7/H7 Series' and covers electrical interfaces, S/PDIF background, and SPDIFRX peripheral configuration across all three families.
- The STM32F446 has two DMA controllers (DMA1 and DMA2) with 8 streams each. The SPDIFRX peripheral provides two dedicated DMA request lines -- DMA_SPDIFRX_DT for audio data and DMA_SPDIFRX_CS for channel status/user bits -- enabling zero-copy reception.
- The STM32F446 includes 2x SAI (Serial Audio Interface) blocks with full-duplex I2S and TDM support, plus 2 dedicated audio PLLs (PLLI2S and PLLSAI) for audio-class clock accuracy.
- The SPDIFRX and SAI peripherals use separate DMA streams on separate controllers, making simultaneous SPDIFRX reception and SAI I2S output via DMA feasible without stream conflicts.
- The NUCLEO-F446RE development board is in active production, widely available (approximately $15-33 USD), and provides Arduino Uno V3 plus ST Morpho headers that expose all STM32F446RE I/Os including SPDIFRX_IN and SAI pins.
- A key architectural tension exists: the SPDIFRX peripheral recovers the symbol rate but does not include a PLL-based clock recovery unit. The incoming S/PDIF clock domain is asynchronous to the MCU system clock, requiring either an ASRC algorithm in firmware or an external clock recovery IC (e.g., DIR9001, SRC4392) to avoid buffer under/overflows when bridging to SAI output.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SPDIFRX | Dedicated hardware peripheral on select STM32 MCUs that receives and decodes S/PDIF (IEC-60958/IEC-61937) digital audio streams. Performs BMC decoding, preamble detection, and data/channel-status separation in silicon. |
| Biphase Mark Coding (BMC) | The line encoding used by S/PDIF. Each bit period has a guaranteed transition at its start; a logic '1' has an additional mid-bit transition. The SPDIFRX hardware decodes BMC by measuring inter-transition time intervals. |
| SAI (Serial Audio Interface) | A flexible audio peripheral on STM32 MCUs supporting I2S, PCM, TDM, and AC'97 protocols. Each SAI contains two independent sub-blocks (A and B) that can operate as master or slave, transmitter or receiver. |
| spdifrx_symb_ck | An internally generated symbol clock output from the SPDIFRX peripheral. Represents the recovered symbol rate of the incoming S/PDIF stream and can be routed to SAI as a reference clock or to a TIM for frequency measurement. Caveat: ST community reports indicate the RM0390 documentation of this routing to SAI may be incorrect, and SAI synchronisation via spdifrx_symb_ck is unreliable in practice. |
| AN5073 | ST Microelectronics Application Note (Rev 2.0, September 2018) titled 'Receiving S/PDIF audio stream with the STM32F4/F7/H7 Series'. Covers electrical interface design, peripheral configuration, and DMA setup for SPDIFRX reception. |
| ASRC (Asynchronous Sample Rate Conversion) | An algorithm that converts audio between two clock domains running at independent rates. Required when bridging SPDIFRX input (source-clocked) to SAI output (locally-clocked) because the SPDIFRX peripheral lacks an integrated clock recovery PLL. |

---

## Tensions & Tradeoffs

- The SPDIFRX peripheral decodes BMC and detects preambles in hardware, but it does not include a clock recovery PLL -- bridging to a locally-clocked SAI output requires either firmware ASRC or external clock recovery hardware, adding complexity.
- Within the STM32F4 family, SPDIFRX is present on the F446, F469, and F479 lines but absent from lower-cost F4 variants (F401, F405, F407, F411, F427, F429), limiting fallback options within F4 to these three lines.
- The Nucleo-F446RE board exposes all relevant pins via morpho headers, but the 64-pin LQFP package limits the number of simultaneously available peripheral I/Os compared to the 144-pin STM32F446ZE variant.
- Running SPDIFRX and SAI simultaneously via DMA is feasible from a stream-mapping perspective, but the asynchronous clock relationship between the two peripherals means naive circular-buffer approaches will eventually underflow or overflow without rate adaptation.

---

## Open Questions

- What is the exact DMA stream and channel mapping for SPDIFRX_DT and SPDIFRX_CS on the STM32F446, and do they conflict with any SAI DMA streams needed for I2S output?
- Is the spdifrx_symb_ck output accurate and stable enough to drive SAI directly as a master clock, or does jitter require an external VCXO or fractional-N PLL for clean I2S clocking? ST community reports indicate RM0390 documentation of this routing may be incorrect and SAI synchronisation via spdifrx_symb_ck is unreliable -- hardware verification is essential.
- What is the minimum viable ASRC implementation complexity on Cortex-M4F at 180 MHz, and can it sustain 96 kHz (and potentially 192 kHz, if RCC clock constraints permit) stereo 24-bit throughput in real time?
- Does the STM32F446 CubeMX/HAL have known bugs or limitations in its SPDIFRX driver, given community reports of configuration issues with CubeMX-generated SPDIFRX code?

---

## Sources & References

- [AN5073 - Receiving S/PDIF audio stream with the STM32F4/F7/H7 Series (ST Application Note, Rev 2.0)](https://www.st.com/resource/en/application_note/an5073-receiving-spdif-audio-stream-with-the-stm32f4f7h7-series-stmicroelectronics.pdf)
- [STM32F446xC/E Datasheet (DS10693, Rev 9)](https://www.st.com/resource/en/datasheet/stm32f446re.pdf)
- [RM0390 Reference Manual - STM32F446xx advanced ARM-based 32-bit MCUs](https://www.st.com/resource/en/reference_manual/dm00135183-stm32f446xx-advanced-arm-based-32-bit-mcus-stmicroelectronics.pdf)
- [SPDIFRX internal peripheral - STM32 MPU Wiki](https://wiki.st.com/stm32mpu/wiki/SPDIFRX_internal_peripheral)
- [Software STM32 S/PDIF decoder (jeddelog) - demonstrates L-series lacks hardware SPDIFRX](https://jeddelog.com/posts/soft-spdif/)
- [SPDIF RX async clocks question - EEVblog Forum (community experience with SPDIFRX clock domain challenges)](https://www.eevblog.com/forum/microcontrollers/spdif-rx-async-clocks-question-%28spdifrx-on-stm32-anyone-tried%29/)
- [RM0386 Reference Manual - STM32F469xx and STM32F479xx advanced ARM-based 32-bit MCUs](https://www.st.com/resource/en/reference_manual/dm00127514-stm32f469xx-and-stm32f479xx-advanced-arm-based-32-bit-mcus-stmicroelectronics.pdf)
- [F446 documentation: RCC frequency limit of dedicated SPDIF-RX clock - ST Community](https://community.st.com/t5/stm32-mcus-embedded-software/f446-documentation-rcc-frequency-limit-of-dedicated-spdif-rx/td-p/377718)
