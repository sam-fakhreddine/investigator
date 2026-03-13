# Validation Report (Cycle 1 Re-check) — Stm32Spdifrx

**Date:** 2026-03-13
**Investigator output:** investigation.json
**Validator:** validator-stm32spdifrx-c1
**Scope:** Targeted re-validation of 3 corrected items from cycle 0 validation

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge/Stm32Spdifrx
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        12           12           9356b073f319   9356b073f319
tensions             IN_SYNC        4            4            3319cab1eaf0   3319cab1eaf0
open_questions       IN_SYNC        4            4            605d75ba2068   605d75ba2068
sources              IN_SYNC        8            8            b6934c3c5a6a   b6934c3c5a6a
concepts             IN_SYNC        6            6            20dfe27b82cc   20dfe27b82cc
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Corrected Item Verification

### Item 1: F4 Family SPDIFRX Availability (was CONTRADICTED)

**Original issue:** Investigation claimed SPDIFRX was exclusive to STM32F446 within the F4 family.

**Correction applied:** Investigation now states SPDIFRX is present on F446, F469, and F479 within F4 (with F469/F479 confirmed via RM0386).

**Verification:** The correction is accurate and consistent across all locations:
- `quick_reference.rows` — "STM32F4 (F446, F469, F479 within F4), F7 series, H7 series, MP1 series"
- `quick_reference.notes` — "Within the STM32F4 family, SPDIFRX is present on the F446, F469, and F479 lines (F469/F479 confirmed via RM0386)"
- `key_findings[4]` — "Within the STM32F4 family, SPDIFRX is present on the F446, F469, and F479 lines"
- `tensions[1]` — "SPDIFRX is present on the F446, F469, and F479 lines but absent from lower-cost F4 variants (F401, F405, F407, F411, F427, F429)"
- Leadership brief bullets — "F446, F469, and F479 lines"
- PO brief bullets — "F446, F469, F479 within the F4 family"

RM0386 (STM32F469xx/F479xx reference manual) is now listed as source #7, providing proper provenance. The F469/F479 are higher-end F4 parts (with DSI display controller), so the corrected tension ("limiting fallback options within F4 to these three lines") remains valid.

**Verdict: CONFIRMED** — correction is accurate and consistently applied.

---

### Item 2: 192 kHz Support on F446 (was PARTIALLY CONFIRMED)

**Original issue:** Investigation claimed 32 kHz to 192 kHz support without qualification; ST community thread indicates F446 RCC cannot supply the required 135.2 MHz dedicated SPDIFRX clock for 192 kHz.

**Correction applied:** Investigation now hedges: "on the STM32F446 specifically, 192 kHz reception may be limited by RCC clock constraints (requires a dedicated SPDIFRX clock of at least 135.2 MHz) -- confirmed for 44.1/48/96 kHz operation; 192 kHz support on F446 should be verified empirically."

**Verification:** The hedge is appropriate and well-sourced:
- The 135.2 MHz figure matches the ST community thread (source #8: "F446 documentation: RCC frequency limit of dedicated SPDIF-RX clock")
- The caveat appears in `key_findings[3]`, `open_questions[2]`, PO brief `work_to_assign`, and PO `questions_to_ask_engineering`
- The wording correctly distinguishes between the peripheral's spec (32-192 kHz per IEC-60958) and the F446-specific RCC limitation
- Recommending empirical verification is the right call since the community thread raises the concern but the exact achievable clock rate depends on PLL configuration

**Verdict: CONFIRMED** — hedge is accurate, well-sourced, and consistently applied.

---

### Item 3: spdifrx_symb_ck SAI Routing Reliability (was PARTIALLY CONFIRMED)

**Original issue:** Investigation presented spdifrx_symb_ck routing to SAI as straightforward; ST community reports indicate RM0390 documentation of this feature contains errors and practical synchronization is unreliable.

**Correction applied:** Investigation now includes caveats throughout:
- `quick_reference` symbol clock row: "caveat: SAI routing via this path reported unreliable per ST community; treat as unverified"
- `key_findings[2]`: "ST community reports indicate that spdifrx_symb_ck routing to SAI as documented in RM0390 may contain errors and SAI synchronisation via this path is unreliable in practice -- this signal path should be treated as unverified until confirmed on hardware"
- `concepts` spdifrx_symb_ck entry: "RM0390 documentation of this routing to SAI may be incorrect, and SAI synchronisation via spdifrx_symb_ck is unreliable in practice"
- `open_questions[1]`: "ST community reports indicate RM0390 documentation of this routing may be incorrect and SAI synchronisation via spdifrx_symb_ck is unreliable -- hardware verification is essential"

**Verification:** The caveats accurately reflect the ST community evidence cited in source #6 (EEVblog forum) and community reports about RM0390 errors. The TIM input capture path (TIM11_CH1 via TIM11_OR.TI1_RMP) is kept as the alternative, which is correct. The investigation correctly recommends hardware verification before relying on this signal path.

**Verdict: CONFIRMED** — caveat is accurate, well-sourced, and consistently applied across all relevant locations.

---

## Spot-Check of Uncorrected Findings

| # | Finding (summary) | Status |
|---|-------------------|--------|
| 1 | STM32F446 has dedicated hardware SPDIFRX for BMC decoding | Unchanged from cycle 0 — still CONFIRMED |
| 7 | AN5073 Rev 2.0 (September 2018) covers STM32F4/F7/H7 | Unchanged from cycle 0 — still CONFIRMED |
| 8 | Two DMA controllers, 8 streams each; SPDIFRX has DT and CS DMA requests | Unchanged from cycle 0 — still CONFIRMED |
| 12 | SPDIFRX lacks clock recovery PLL; ASRC or external IC needed | Unchanged from cycle 0 — still CONFIRMED |

**Sources:** Now 8 sources (up from 6 in cycle 0). Two additions:
- RM0386 (STM32F469xx/F479xx reference manual) — supports correction #1
- ST Community thread on RCC clock limits — supports correction #2

Both are legitimate additions providing provenance for the corrections. No sources were removed. No unintended changes detected in uncorrected findings.

---

## Summary

- **Sync status:** IN_SYNC (all fields)
- **Corrected items:** 3/3 CONFIRMED as accurate after correction
- **Unintended changes:** None detected
- **Disputed items remaining:** 0

| Corrected Item | Cycle 0 Verdict | Cycle 1 Verdict |
|----------------|-----------------|-----------------|
| F4 family SPDIFRX availability (F446 + F469 + F479) | CONTRADICTED | CONFIRMED |
| 192 kHz support hedge (RCC clock constraint caveat) | PARTIALLY CONFIRMED | CONFIRMED |
| spdifrx_symb_ck SAI routing caveat (RM0390 doc issues) | PARTIALLY CONFIRMED | CONFIRMED |

All three corrections have been accurately applied and are consistent across investigation.json, investigation.md, quick_reference, audience briefs, tensions, open_questions, and concepts. No further correction cycles are needed.
