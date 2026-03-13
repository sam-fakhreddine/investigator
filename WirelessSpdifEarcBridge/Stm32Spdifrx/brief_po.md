# STM32F446 SPDIFRX Hardware Peripheral Capabilities and Availability — Product Brief

**Date:** 2026-03-13
**Risk Level:** LOW

---

## What Is This?

> The chip we selected has a built-in circuit that automatically reads digital audio signals, saving significant development time and reducing firmware risk.

---

## What Does This Mean for Us?

This means the hardest part of receiving S/PDIF audio is handled by the chip itself, not by custom software. The remaining challenge is synchronising the audio clock between input and output, which requires either additional firmware work or a small extra component on the board.

---

## Key Points

- The STM32F446 chip has a dedicated hardware block for receiving S/PDIF audio -- this is confirmed by ST's official documentation and application note AN5073.
- This hardware block is only available on certain premium STM32 chips (F446, F469, F479 within the F4 family, plus F7, H7 series), not on cheaper models -- so the chip selection is locked to this tier.
- A low-cost development board (NUCLEO-F446RE, ~$15-33) is readily available for prototyping.
- One engineering challenge remains: synchronising the audio timing between input and output, which will require additional firmware or a small extra chip.

---

## Next Steps

**PO/EM Decision:**

> Approve the STM32F446 as the target MCU for the S/PDIF receive path and confirm whether BOM cost constraints allow an external clock recovery IC or if firmware-only ASRC is required.

**Engineering Work Items:**
- Prototype SPDIFRX reception on NUCLEO-F446RE using CubeMX/HAL with DMA, verify basic S/PDIF lock and data capture.
- Evaluate ASRC firmware feasibility on Cortex-M4F at 180 MHz for target sample rates (44.1/48/96 kHz; 192 kHz on F446 requires empirical verification due to RCC clock constraints).
- If ASRC is too complex, evaluate BOM impact of adding DIR9001 or SRC4392 for external clock recovery.

**Leadership Input Required:**

> Architecture decision needed on clock domain strategy: firmware ASRC vs external clock recovery IC, considering BOM cost, firmware complexity, and audio quality targets.

---

## Open Questions

- How much firmware effort is the ASRC implementation, and does our 180 MHz Cortex-M4 have enough headroom for it at 96 kHz (and can the F446 RCC even supply the required 135.2 MHz SPDIFRX clock for 192 kHz)?
- Are there known CubeMX or HAL bugs with SPDIFRX that could delay prototyping?
- What is the additional BOM cost if we add an external clock recovery chip instead of doing ASRC in firmware?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
