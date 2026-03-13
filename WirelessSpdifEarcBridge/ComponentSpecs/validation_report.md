# Validation Report — ComponentSpecs

**Date:** 2026-03-13
**Investigator output:** investigation.json
**Validator:** validator-componentspecs

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge/ComponentSpecs
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        12           12           9b59abf1745f   9b59abf1745f
tensions             IN_SYNC        5            5            982e51e772c6   982e51e772c6
open_questions       IN_SYNC        4            4            06412daeeb19   06412daeeb19
sources              IN_SYNC        10           10           e8b0f1dab08c   e8b0f1dab08c
concepts             IN_SYNC        7            7            06e9234e74e9   06e9234e74e9
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source URL Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | TI PCM1808 Product Page | https://www.ti.com/product/PCM1808 | VERIFIED | Returns full product page; confirms 24-bit/96kHz stereo ADC, TSSOP-14, ACTIVE status |
| 2 | PCM1808 Datasheet (TI SLES167) | https://www.ti.com/lit/gpn/PCM1808 | VERIFIED | Returns PDF binary (638KB); datasheet accessible |
| 3 | NDK NZ2520SDA Product Page | https://www.ndk.com/en/products/lineup/crystal-oscillator/NZ2520SDA.html | VERIFIED | Returns product page confirming fixed SPXO, 20-54 MHz range, 43fs jitter |
| 4 | SiTime SiT3807 Product Page | https://www.sitime.com/products/mhz-oscillators/voltage-controlled-oscillators/sit3807 | VERIFIED | Returns full product page; confirms MEMS VCXO, +/-25 to +/-200 ppm pull range, production status |
| 5 | Abracon ASVV Datasheet | https://abracon.com/Oscillators/ASVV.pdf | VERIFIED | Returns PDF binary (2.1MB); datasheet accessible from Abracon site |
| 6 | STM32 Timer Encoder Mode Tutorial | https://deepbluembedded.com/stm32-timer-encoder-mode-stm32-rotary-encoder-interfacing/ | VERIFIED | Page exists (JS-heavy, content not extractable via fetch); confirmed via search results that content covers STM32 timer encoder mode |
| 7 | LCSC PCM1808PWR (C55513) | https://www.lcsc.com/product-detail/C55513.html | VERIFIED | Returns product listing: PCM1808PWR, TSSOP-14, $0.3351/unit, 372 in stock |
| 8 | LCSC E73-2G4M08S1C (C356849) | https://www.lcsc.com/product-detail/C356849.html | VERIFIED | Returns product listing: E73-2G4M08S1C nRF52840, $5.5188/unit, 1236 in stock |
| 9 | Ebyte E73-2G4M08S1C Product Page | https://www.cdebyte.com/products/E73-2G4M08S1C | VERIFIED | Returns product page confirming nRF52840, BLE 4.2/5.0, SMD, 8dBm TX power |
| 10 | STMicroelectronics NUCLEO-F446RE | https://www.st.com/en/evaluation-tools/nucleo-f446re.html | UNVERIFIABLE | Page timed out on fetch; however, URL confirmed valid via multiple search results referencing it |

---

## Finding Verification

| # | Finding (summary) | Verdict | Evidence | Source |
|---|-------------------|---------|----------|--------|
| 1 | PCM1808 is 24-bit/96kHz stereo ADC with I2S, but package is TSSOP-14 not SSOP-28 | CONFIRMED | TI product page explicitly states "TSSOP (14)" package, 5x6.4mm. LCSC lists PCM1808PWR as TSSOP-14. Multiple datasheet references confirm 14 pins. The hypothesis citing SSOP-28 is indeed incorrect. | TI product page, LCSC C55513, datasheet search results |
| 2 | PCM1808 pricing conservative at ~$2; LCSC $0.32, DigiKey ~$1.50 | CONFIRMED | LCSC lists PCM1808PWR at $0.3351/unit (372 in stock). Investigation's claim of "$0.32" is very close to verified $0.3351. DigiKey pricing not directly verified but TI product page confirms ACTIVE status, consistent with broad availability. | LCSC C55513 listing |
| 3 | EC11 rotary encoder: 20 detents, quad A/B, push switch, ~$1 | UNVERIFIED | No source URL provided for EC11 specifically. The investigation does not include an EC11 datasheet or distributor link. The EC11 is a well-known Alps/generic encoder and the specs are consistent with common knowledge, but no primary source was cited or verified. | No primary source in investigation |
| 4 | STM32 timer encoder mode: HW quad decode, near-zero CPU | CONFIRMED | Multiple STM32 community posts and tutorials confirm TIM2-TIM5, TIM1, TIM8 support hardware encoder mode on STM32F446. ST community thread specifically discusses STM32F446 + quadrature encoder. Hardware handles edge counting/direction; CPU only reads counter register. "Zero CPU" is slightly overstated (investigation correctly notes this). | ST community forum, DeepBlue Embedded tutorial, EmbeddedExpertIO |
| 5 | TXC 7M series is NOT a VCXO — it is a passive quartz crystal | CONFIRMED | Amazon and Newark listings explicitly describe TXC 7M-24.576MEEQ-T as "QUARTZ CRYSTAL, 24.576 MHz, 10 pF, SMD" — a passive crystal, not an oscillator. TXC's own product page separates crystals from VCXOs. The investigation correctly identifies the hypothesis error. | Amazon, Newark (86R1541), TXC product pages |
| 6 | NDK NZ2520SDA is NOT a VCXO — it is a fixed SPXO with no voltage control | CONFIRMED | NDK product page confirms fixed-frequency crystal oscillator (SPXO), 20-54 MHz range, ultra-low phase jitter (43fs typical). No mention of voltage control pin or tuning range. Described as "crystal oscillator" not "voltage controlled." | NDK NZ2520SDA product page (direct fetch) |
| 7 | TORX173 and TOTX173 are OBSOLETE lifecycle | CONFIRMED | Octopart listings and web search results confirm both TORX173 and TOTX173 carry OBSOLETE lifecycle status. Datasheets date from 2001. Multiple sources describe availability as limited to surplus channels. | Octopart (blocked but confirmed via search snippets), AllDatasheet, DigChip |
| 8 | E73-2G4M08S1C nRF52840 module: correctly specified but ~25% higher price ($5.52 vs $4) | CONFIRMED | LCSC lists at $5.5188/unit (1236 in stock). Ebyte product page confirms nRF52840, BLE 4.2/5.0, SMD, 8dBm TX power, 13x18mm. Price delta vs claimed $4 is confirmed at ~38% higher ($5.52), actually larger than the "~25%" stated in the investigation. | LCSC C356849, Ebyte product page |
| 9 | Nucleo-F446RE accurately specified, cheaper than estimated ($14.85 vs ~$20) | PARTIALLY CONFIRMED | Multiple search results reference the NUCLEO-F446RE at DigiKey. Web search snippet confirms $14.85 pricing. STM32F446RET6 with 180MHz and Arduino headers confirmed. ST product page timed out but URL is valid. Price of $14.85 confirmed via search. | DigiKey search results, Amazon listings, ST product page (via search) |
| 10 | SiTime SiT3807 and Abracon ASVV are viable 24.576MHz VCXO alternatives | CONFIRMED | SiT3807 confirmed as production MEMS VCXO with pull ranges +/-25 to +/-200 ppm, 1.544-49.152 MHz range (24.576 MHz within range), 4 package options (2520-7050), priced at ~$7.87. Abracon ASVV confirmed as VCXO series; ASVV-24.576MHZ-L50-N102-T exists on DigiKey with +/-50 ppm pull range (L50 designation), 7050 package. Both are actively produced. | SiTime product page (direct fetch), DigiKey ASVV listing (search), Abracon VCXO page |
| 11 | Adjusted core BOM ~$60-75, broadly consistent with original ~$67 estimate | PARTIALLY CONFIRMED | Individual component prices verified (PCM1808 $0.33-1.50, E73 $5.52, Nucleo $14.85, VCXO $3-8). The directional adjustments are correct (nRF52840 up, Nucleo down, VCXO added). However, not all BOM line items were individually priced, so the $60-75 range is a reasonable estimate but not independently totaled. | Aggregation of individual component verifications |
| 12 | Total BOM $97-120 including passives and test equipment remains plausible | UNVERIFIED | No specific pricing was provided for passive components or test equipment. The claim that passives add $10-20 and test equipment $20-50 is stated as general knowledge without source citations. Plausible but not independently verified against any specific BOM or distributor quote. | No primary source |

---

## Flags

| # | Finding | Flag | Detail |
|---|---------|------|--------|
| 1 | Finding #8 — nRF52840 price delta | NEEDS_PRIMARY_SOURCE | Investigation states "~25% higher" ($5.52 vs $4) but the actual delta is ~38%. The percentage claim should be corrected. |
| 2 | Finding #3 — EC11 encoder | NEEDS_PRIMARY_SOURCE | No source URL for EC11 encoder specs or pricing was included in the investigation sources list. Should cite LCSC, DigiKey, or Alps datasheet. |
| 3 | Finding #10 — SiT3807 pricing | CONFIRM_OR_HEDGE | Investigation claims "$3-8" for VCXO alternatives, but SiT3807 verified at ~$7.87. Low end of $3 not substantiated for SiT3807; may apply only to Abracon ASVV (not directly price-verified). The range should be hedged to "$4-10" or a specific price cited per part. |
| 4 | Finding #12 — Total BOM estimate | NEEDS_PRIMARY_SOURCE | No itemized passive BOM or test equipment list was provided. The $97-120 range is plausible but unsubstantiated. |

---

## Summary

- Sources: 9 verified / 10 total, 0 dead, 1 unverifiable (ST product page timeout, but URL confirmed valid via search)
- Findings: 7 confirmed, 2 partially confirmed, 2 unverified, 0 contradicted
- Flags: 4
- Disputed items requiring correction:
  - **nRF52840 price delta**: Investigation states "~25% higher" but actual delta is ~38% ($5.52 vs $4). Should be corrected to "~38% higher" or the text adjusted.
  - **VCXO price range**: "$3-8" is optimistic; SiT3807 verified at ~$7.87 and Abracon ASVV price not confirmed at the low end. Consider adjusting to "$5-10" or citing per-part pricing.
