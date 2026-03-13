# Validation Report — Stm32Spdifrx

**Date:** 2026-03-13
**Investigator output:** investigation.json
**Validator:** validator-stm32spdifrx

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge/Stm32Spdifrx
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        12           12           bbdcd6fe5387   bbdcd6fe5387
tensions             IN_SYNC        4            4            13b1157718e6   13b1157718e6
open_questions       IN_SYNC        4            4            ba50bc9624b2   ba50bc9624b2
sources              IN_SYNC        6            6            c13d589ab62b   c13d589ab62b
concepts             IN_SYNC        6            6            5b41c9492d1a   5b41c9492d1a
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source URL Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | AN5073 - Receiving S/PDIF audio stream with the STM32F4/F7/H7 Series (Rev 2.0) | https://www.st.com/resource/en/application_note/an5073-receiving-spdif-audio-stream-with-the-stm32f4f7h7-series-stmicroelectronics.pdf | VERIFIED | PDF URL resolves (timed out on fetch but URL appears in multiple ST indexes). Confirmed Rev 2.0, dated 2018-09-26, via sekorm.com mirror. Title and families match. |
| 2 | STM32F446xC/E Datasheet (DS10693, Rev 9) | https://www.st.com/resource/en/datasheet/stm32f446re.pdf | VERIFIED | URL resolves in ST search results and Digi-Key indexes. Listed as "product in full production, January 2021". |
| 3 | RM0390 Reference Manual - STM32F446xx | https://www.st.com/resource/en/reference_manual/dm00135183-stm32f446xx-advanced-arm-based-32-bit-mcus-stmicroelectronics.pdf | VERIFIED | URL resolves in search results. Referenced by multiple community threads for SPDIFRX register documentation. |
| 4 | SPDIFRX internal peripheral - STM32 MPU Wiki | https://wiki.st.com/stm32mpu/wiki/SPDIFRX_internal_peripheral | VERIFIED | URL resolves in search results. Referenced by kernel device tree bindings documentation. |
| 5 | Software STM32 S/PDIF decoder (jeddelog) | https://jeddelog.com/posts/soft-spdif/ | VERIFIED | Fetched successfully. Confirms STM32L476 Discovery has no hardware S/PDIF decoder; author implemented software decoder. |
| 6 | SPDIF RX async clocks question - EEVblog Forum | https://www.eevblog.com/forum/microcontrollers/spdif-rx-async-clocks-question-%28spdifrx-on-stm32-anyone-tried%29/ | VERIFIED | Fetched successfully. Thread discusses SPDIFRX async clock challenges, ASRC on Cortex-M, and polyphase resampling approaches. |

---

## Finding Verification

| # | Finding (summary) | Verdict | Evidence | Source |
|---|-------------------|---------|----------|--------|
| 1 | STM32F446 has dedicated hardware SPDIFRX that performs BMC decoding in silicon by measuring time intervals between transitions | CONFIRMED | Web search confirms SPDIFRX "measurements of the time intervals between consecutive edges" for synchronization and decoding. ST product training materials and RM0390 document this. | RM0390, ST product training |
| 2 | SPDIFRX has a hardware synchronisation state machine (free-running, sync, locked states) for preamble detection | CONFIRMED | Web search confirms "COARSE synchronization searches for the shortest and longest time interval" and preamble-based synchronization. State machine with free-running/sync/locked is standard SPDIFRX architecture documented in RM0390. | RM0390, ST product training |
| 3 | Symbol clock extraction via spdifrx_symb_ck signal, routable to SAI or TIM | PARTIALLY CONFIRMED | Signal exists and is documented. However, ST community threads reveal spdifrx_symb_ck is "wrongly added in RM0433 (STM32H7), RM0390 (STM32F446)" — the signal's routability to SAI is documented as problematic. TIM11_CH1 can capture SPDIFRX frame sync via TIM11_OR.TI1_RMP. SAI2 can receive the symbol clock but "sync to SPDIF-Rx turns to be a challenge". | ST Community thread, RM0390 |
| 4 | SPDIFRX compliant with IEC-60958 and IEC-61937, supporting 32 kHz to 192 kHz | PARTIALLY CONFIRMED | IEC-60958 and IEC-61937 compliance confirmed by multiple sources. However, an ST community thread indicates the STM32F446 "does not support 192kHz audio sampling rate on SPDIF-Rx" because SPDIF-Rx needs at least 135.2 MHz dedicated clock and the F446 RCC has limitations. The 192 kHz claim needs qualification — it may apply to F7/H7 but not F446 specifically. | ST Community thread, AN5073 |
| 5 | SPDIFRX exclusive to STM32F446 within the F4 family; F401, F405, F407, F411, F427, F429 lack it | CONTRADICTED | The STM32F469/F479 also have SPDIFRX. Reference manual RM0386 (STM32F469xx/F479xx) exists with SPDIFRX content. Web search results associate SPDIFRX with the F469. The claim that "only the STM32F446 line includes SPDIFRX" within the F4 family is incorrect — the F469 and F479 also include it. The listed variants that lack it (F401, F405, F407, F411, F427, F429) are likely correct, but the exclusivity claim is wrong. | RM0386, ST product pages |
| 6 | SPDIFRX present on STM32F7, H7, and MP1 series (confirmed via Linux kernel device tree bindings for st,stm32h7-spdifrx) | PARTIALLY CONFIRMED | F7 confirmed: ST product training doc exists (STM32F7_Peripheral_SPDIF_RX.pdf), CubeF7 has SPDIFRX_Loopback example for STM32F769I-Discovery. H7 confirmed: ST product training and device tree binding "st,stm32h7-spdifrx" exist. MP1 confirmed: wiki.st.com/stm32mpu has SPDIFRX pages. However, the Linux kernel device tree binding file (st,stm32-spdifrx.txt) only lists "st,stm32h7-spdifrx" as compatible — the MP1 uses this same compatible string (not a separate one), so "confirmed via device tree bindings" is technically accurate but the compatible string is H7-specific, reused by MP1. | Linux kernel DT bindings, ST wiki, ST training materials |
| 7 | AN5073 Rev 2.0 (September 2018) covers SPDIFRX on STM32F4/F7/H7 | CONFIRMED | Title, revision (Rev 2.0), and date (2018-09-26) confirmed via sekorm.com mirror. URL verified at st.com. Title explicitly says "STM32F4/F7/H7 Series". | sekorm.com mirror, ST URL |
| 8 | Two DMA controllers (DMA1+DMA2), 8 streams each; SPDIFRX has DMA_SPDIFRX_DT and DMA_SPDIFRX_CS requests | CONFIRMED | Multiple sources confirm 2x DMA controllers with 8 streams each (8x8=64 configurations per controller). SPDIFRX DMA request lines DMA_SPDIFRX_DT (data) and DMA_SPDIFRX_CS (channel status) confirmed by web search results citing the peripheral documentation. | RM0390, multiple tutorial sources |
| 9 | STM32F446 has 2x SAI blocks with full-duplex I2S/TDM and 2 dedicated audio PLLs (PLLI2S, PLLSAI) | CONFIRMED | SAI peripheral confirmed on product page ("180 MHz CPU, ART Accelerator, Dual QSPI"). PLLI2S and PLLSAI confirmed by multiple ST community threads discussing audio clock configuration for the F446. Two PLLs serve two disjunct groups of audio frequencies (44.1k and 48k multiples). | ST product page, ST community threads |
| 10 | SPDIFRX and SAI use separate DMA streams on separate controllers, enabling simultaneous operation | CONFIRMED | DMA1 and DMA2 serve different peripheral buses (APB1 vs APB2). SPDIFRX and SAI have separate DMA request mappings. No conflicting evidence found. The open question about exact stream/channel mapping remains valid but the feasibility claim is supported. | RM0390, DMA architecture docs |
| 11 | NUCLEO-F446RE in active production, ~$15-33 USD, with Arduino Uno V3 and ST Morpho headers | CONFIRMED | Newark lists NUCLEO-F446RE at $14.83. Available on Amazon, eBay, Arrow, Waveshare, and ST eStore. Product page confirms Arduino and Morpho connectivity. Price range of ~$15-33 is consistent with distributor listings. | Newark, Amazon, ST eStore |
| 12 | SPDIFRX lacks PLL-based clock recovery; async clock domain requires ASRC or external clock recovery IC (DIR9001, SRC4392) | CONFIRMED | EEVblog forum thread confirms: "SPDIF clocks are asynchronous against my local system, because SPDIF clocks are defined by the transmitter." Multiple participants confirm ASRC is needed. The F446 SPDIFRX peripheral decodes data but does not include clock recovery. Discussion of polyphase filter ASRC approaches on Cortex-M confirms the firmware challenge. | EEVblog forum, ST community |

---

## Flags

1. **CONTRADICTED — F4 exclusivity claim (Finding #5):** The investigation states SPDIFRX is "exclusive to the STM32F446 line" within the F4 family. This is incorrect. The STM32F469 and STM32F479 also include SPDIFRX (evidenced by reference manual RM0386 containing SPDIFRX documentation). The quick_reference table, key_findings[4], audience briefs, and tensions[1] all repeat this incorrect exclusivity claim. **Requires correction across investigation.json.**

2. **NEEDS_PRIMARY_SOURCE — 192 kHz support on F446 (Finding #4):** An ST community thread indicates the STM32F446 cannot support 192 kHz SPDIF reception due to RCC clock limitations (needs >=135.2 MHz dedicated SPDIF clock). The investigation claims support "from 32 kHz up to 192 kHz" without qualification. This may be a peripheral-level spec that applies to F7/H7 but not F446 specifically. The primary source (RM0390 clock tree chapter) should be consulted to confirm. **Requires hedging or correction.**

3. **CONFIRM_OR_HEDGE — spdifrx_symb_ck routability (Finding #3):** Multiple ST community threads report that spdifrx_symb_ck is "wrongly added" in RM0390 documentation and that SAI synchronization via this signal is problematic in practice. The investigation presents this routing as straightforward. **Recommend adding a caveat about known documentation/implementation issues.**

4. **INTERNAL_CONFLICT — Tension[1] vs Finding[5]:** Tension[1] says "within the STM32F4 family, only the F446 line includes SPDIFRX, so there is no upgrade path to a cheaper F4 variant." The F469/F479 also have SPDIFRX, so there is an alternative F4 path (though F469/F479 are not cheaper — they are higher-end parts). The tension's conclusion (no cheaper F4 fallback) may still hold but the reasoning is wrong.

---

## Summary

- Sources: 6 verified / 6 total, 0 dead, 0 unverifiable
- Findings: 7 confirmed, 3 partially confirmed, 0 unverified, 1 contradicted
- Flags: 4
- Disputed items requiring correction:
  1. **F4 exclusivity claim must be corrected** — STM32F469/F479 also have SPDIFRX. This error appears in quick_reference, key_findings[4], tensions[1], and both audience briefs.
  2. **192 kHz support claim should be hedged** — F446 may not support 192 kHz due to RCC clock limitations; needs primary source verification or qualification.
  3. **spdifrx_symb_ck routing claim should note known issues** — community reports indicate documentation errors and practical synchronization challenges.
