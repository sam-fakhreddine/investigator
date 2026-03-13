# STM32F446 SPDIFRX Hardware Peripheral Capabilities and Availability — Engineering Leadership Brief

**Date:** 2026-03-13

---

## Headline

> The STM32F446 SPDIFRX peripheral handles BMC decode and preamble detection in silicon, eliminating the need for firmware bit-banging, but clock domain bridging to SAI output remains an open firmware challenge.

---

## So What

Using the STM32F446 de-risks the S/PDIF receive path -- the hardest part of decode is in hardware. However, the lack of integrated clock recovery means the team must budget effort for ASRC firmware or an external clock recovery IC, which directly impacts BOM cost and firmware complexity.

---

## Key Points

- SPDIFRX hardware handles BMC decode, preamble detection, and symbol clock extraction -- no firmware bit-banging needed for the receive path.
- Within the F4 family, SPDIFRX is present on the F446, F469, and F479 lines (also on F7, H7, MP1) -- cheaper F4 variants without SPDIFRX cannot be used as fallbacks.
- Two dedicated DMA channels for SPDIFRX (data + channel status) allow zero-copy reception alongside SAI output on separate DMA streams.
- The async clock domain between SPDIFRX and SAI is the primary integration risk -- ASRC or external PLL required to prevent audio artifacts.

---

## Action Required

> Allocate firmware engineering effort for ASRC implementation or evaluate external clock recovery ICs (DIR9001, SRC4392) as an alternative before finalising the hardware design.

---

*Full engineering investigation: [investigation.md](investigation.md)*
