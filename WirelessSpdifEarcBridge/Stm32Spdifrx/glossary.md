# Glossary — STM32F446 SPDIFRX Hardware Peripheral Capabilities and Availability

Quick definitions of key terms and concepts referenced in this investigation.

---

## SPDIFRX

Dedicated hardware peripheral on select STM32 MCUs that receives and decodes S/PDIF (IEC-60958/IEC-61937) digital audio streams. Performs BMC decoding, preamble detection, and data/channel-status separation in silicon.

## Biphase Mark Coding (BMC)

The line encoding used by S/PDIF. Each bit period has a guaranteed transition at its start; a logic '1' has an additional mid-bit transition. The SPDIFRX hardware decodes BMC by measuring inter-transition time intervals.

## SAI (Serial Audio Interface)

A flexible audio peripheral on STM32 MCUs supporting I2S, PCM, TDM, and AC'97 protocols. Each SAI contains two independent sub-blocks (A and B) that can operate as master or slave, transmitter or receiver.

## spdifrx_symb_ck

An internally generated symbol clock output from the SPDIFRX peripheral. Represents the recovered symbol rate of the incoming S/PDIF stream and can be routed to SAI as a reference clock or to a TIM for frequency measurement. Caveat: ST community reports indicate the RM0390 documentation of this routing to SAI may be incorrect, and SAI synchronisation via spdifrx_symb_ck is unreliable in practice.

## AN5073

ST Microelectronics Application Note (Rev 2.0, September 2018) titled 'Receiving S/PDIF audio stream with the STM32F4/F7/H7 Series'. Covers electrical interface design, peripheral configuration, and DMA setup for SPDIFRX reception.

## ASRC (Asynchronous Sample Rate Conversion)

An algorithm that converts audio between two clock domains running at independent rates. Required when bridging SPDIFRX input (source-clocked) to SAI output (locally-clocked) because the SPDIFRX peripheral lacks an integrated clock recovery PLL.

---

*Back to: [investigation.md](investigation.md)*
