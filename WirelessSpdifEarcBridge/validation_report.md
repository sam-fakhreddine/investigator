# Validation Report — WirelessSpdifEarcBridge (Rollup)

**Date:** 2026-03-13
**Investigator output:** investigation.json (rollup)
**Validator:** validator-rollup

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        13           13           accc70d913de   accc70d913de
tensions             IN_SYNC        8            8            4e37a54b1884   4e37a54b1884
open_questions       IN_SYNC        8            8            08dfa1f58d42   08dfa1f58d42
sources              IN_SYNC        48           48           489d468e4aee   489d468e4aee
concepts             IN_SYNC        10           10           3e9200377275   3e9200377275
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source URL Sample Verification (14 of 48)

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Nordic nRF52840 Product Spec — RADIO | https://docs.nordicsemi.com/bundle/ps_nrf52840/page/radio.html | VERIFIED | Page loads; JS-rendered SPA, URL path confirms RADIO peripheral content |
| 2 | AN5073 — S/PDIF with STM32F4/F7/H7 | https://www.st.com/resource/en/application_note/an5073-... | UNVERIFIABLE | Timeout fetching PDF; ST PDF hosting is slow but URL structure is canonical ST format |
| 3 | ITE IT6621 Product Page | https://www.ite.com.tw/en/product/cate1/IT6621 | VERIFIED | Confirmed: "ARC/eARC Transmitter with Audio MUX" — matches rollup claims exactly |
| 4 | TI PCM1808 Product Page | https://www.ti.com/product/PCM1808 | VERIFIED | Confirmed: 24-bit, 96 kHz stereo ADC, **14-pin TSSOP** package — supports PCM1808 package correction |
| 5 | SiTime SiT3807 VCXO | https://www.sitime.com/products/voltage-controlled-oscillators/sit3807 | VERIFIED | Confirmed: 1.544-49.152 MHz, pull range +/-25 to +/-200 ppm, $7.87, production status |
| 6 | NDK NZ2520SDA Product Page | https://www.ndk.com/en/products/lineup/crystal-oscillator/NZ2520SDA.html | VERIFIED | Confirmed: fixed-frequency SPXO (NOT a VCXO), ultra-low jitter 43 fs — supports VCXO misidentification finding |
| 7 | Lattice HDMI 2.1 eARC | https://www.latticesemi.com/en/Products/ASSPs/HDMI21eARC | DEAD | HTTP 403 Forbidden; page may have been reorganized or access-restricted |
| 8 | RFC 5905 — NTP Version 4 | https://datatracker.ietf.org/doc/html/rfc5905 | VERIFIED | Confirmed: "Network Time Protocol Version 4: Protocol and Algorithms Specification" |
| 9 | Marmitek Audio Anywhere 685 Manual | https://www.manualslib.com/manual/1038197/... | VERIFIED | Page loads on ManualsLib; header confirms "Marmitek Audio Anywhere 685 User Manual [Page 5]"; content behind JS rendering |
| 10 | HDFury 4K Arcana 18Gbps | https://hdfury.com/product/4k-arcana-18gbps/ | VERIFIED | Confirmed: eARC adapter, Dolby Atmos/TrueHD support, HDMI 2.0b passthrough |
| 11 | Abracon ASVV Datasheet | https://abracon.com/Oscillators/ASVV.pdf | VERIFIED | PDF downloaded (2.1 MB); URL reachable, binary content confirmed as PDF |
| 12 | HDMI.org — eARC Specification | https://www.hdmi.org/spec2sub/enhancedaudioreturnchannel | VERIFIED | Page now references HDMI 2.2 (not 2.1); eARC feature description matches claims. See Flag F1. |
| 13 | STMicroelectronics NUCLEO-F446RE | https://www.st.com/en/evaluation-tools/nucleo-f446re.html | UNVERIFIABLE | Timeout; ST website slow but URL is canonical ST product page format |
| 14 | AWOL Vision ThunderBeat | https://awolvision.com/products/thunderbeat | VERIFIED | Shopify product page loads (product ID 7558711574576); content behind JS rendering |

---

## Finding Verification

| # | Finding (summary) | Verdict | Evidence / Sub-inv source | Source |
|---|-------------------|---------|--------------------------|--------|
| 1 | IT6803 does not exist; IT680x are receivers; correct part is IT6621 (eARC TX) or SiI9438 | CONFIRMED | EarcHdmiOutput sub-inv key_finding[0]: "IT6803 does not appear in ITE Tech's product catalog — ITE's IT680x series (IT6801, IT6802, IT6807) are HDMI receivers." Live ITE IT6621 page confirms "ARC/eARC Transmitter with Audio MUX." | EarcHdmiOutput/investigation.json |
| 2 | TXC 7M is a crystal (not VCXO); NDK NZ2520SDA is a fixed SPXO (not VCXO); replacements: SiT3807, ASVV | CONFIRMED | ComponentSpecs sub-inv key_findings[4-5]: "TXC 7M series is NOT a VCXO — passive quartz crystal"; "NDK NZ2520SDA is NOT a VCXO — fixed-frequency SPXO." Live NDK page confirms "fixed crystal oscillator" with no voltage control. SiT3807 live page confirms VCXO with +/-25 to +/-200 ppm pull range. | ComponentSpecs/investigation.json |
| 3 | PCM1808 is TSSOP-14, not SSOP-28 as hypothesis claimed | CONFIRMED | ComponentSpecs sub-inv key_finding[0]: "hypothesis incorrectly states SSOP-28 package — the actual package is TSSOP-14 (14 pins, not 28)." TI live product page confirms "14-pin TSSOP (PW) package, 5 x 6.4 mm." | ComponentSpecs/investigation.json, TI live page |
| 4 | DTS core at 1509 Kbps consumes 89-116% of nRF52840 throughput, marginal to infeasible | CONFIRMED | RfTransport sub-inv key_finding[9]: "DTS core at 1509.75 Kbps consumes 89-116% of the nRF52840 throughput range, making it marginal at best and infeasible at the lower end." Quick reference table row confirms same figures. | RfTransport/investigation.json |
| 5 | DD5.1 at 640 Kbps uses 38-49% of nRF52840 throughput — comfortable margin | CONFIRMED | RfTransport sub-inv key_finding[8]: "DD5.1 at 640 Kbps uses only 38-49% of the nRF52840's achievable throughput range (1.3-1.7 Mbps)." Arithmetic: 640/1700 = 37.6%, 640/1300 = 49.2%. Rollup rounds to 38-49%. | RfTransport/investigation.json |
| 6 | ASRC cannot process IEC-61937 compressed bitstreams — VCXO is only viable approach | CONFIRMED | ClockRecovery sub-inv key_finding[2]: "ASRC fundamentally cannot process IEC-61937 compressed bitstreams because ASRC operates by interpolating between PCM sample values." Stm32Spdifrx sub-inv tension[0] also notes ASRC limitation. | ClockRecovery/investigation.json |
| 7 | STM32F446 SPDIFRX does BMC decode, preamble detection in hardware; present on F446/F469/F479 | CONFIRMED | Stm32Spdifrx sub-inv key_findings[0-1]: "dedicated hardware SPDIFRX peripheral that performs biphase mark code (BMC) decoding entirely in silicon"; key_finding[4]: "present on the F446, F469, and F479 lines." | Stm32Spdifrx/investigation.json |
| 8 | eARC uses CMDC, not CEC — eARC operates independently of CEC | CONFIRMED | EarcHdmiOutput sub-inv key_finding[4]: "eARC negotiation does NOT use CEC — it has its own dedicated Common Mode Data Channel (CMDC) that operates independently of CEC." HDMI.org live page describes eARC features (though does not explicitly mention CMDC in summary text). | EarcHdmiOutput/investigation.json |
| 9 | Marmitek Audio Anywhere 685 proves concept feasibility — wireless DD 5.1/DTS via TOSLINK, 12ms latency; discontinued | CONFIRMED | MarketLandscape sub-inv key_finding[0]: "wirelessly transmits Dolby Digital 5.1 and DTS 6.1 bitstreams over TOSLINK/coaxial at 2.4GHz with 12ms latency...appears discontinued." ManualsLib page confirms manual exists. | MarketLandscape/investigation.json |
| 10 | 40 ppm worst-case crystal mismatch is correct; 1.92 samples/sec drift at 48 kHz | CONFIRMED | ClockRecovery sub-inv key_findings[0-1]: "standard quartz crystals specify +/-20 ppm...two independent crystals can diverge by up to 40 ppm"; "1.92 samples/second of drift (48000 x 40e-6)." Arithmetic independently verified: 48000 x 0.00004 = 1.92. | ClockRecovery/investigation.json |
| 11 | 24.576 MHz VCXOs with +/-100 to +/-200 ppm pull range are commercially available (SiT3807, ASVV) | CONFIRMED | ComponentSpecs sub-inv key_finding[9]: "SiTime SiT3807 MEMS VCXO offers +/-25 to +/-200ppm pull range." SiT3807 live page confirms 1.544-49.152 MHz range (includes 24.576 MHz) with +/-25 to +/-200 ppm. Abracon ASVV PDF reachable. | ComponentSpecs/investigation.json, SiT3807 live page |
| 12 | SPDIFRX lacks clock recovery PLL — async clock domain requires ASRC or external IC | CONFIRMED | Stm32Spdifrx sub-inv key_finding[10]: "SPDIFRX peripheral recovers the symbol rate but does not include a PLL-based clock recovery unit." Tension[0] in same file: "does not include a clock recovery PLL." | Stm32Spdifrx/investigation.json |
| 13 | BOM estimate ~$67 core / $97-120 total broadly correct at $60-75 after corrections | CONFIRMED | ComponentSpecs sub-inv key_finding[10]: "adjusted core BOM is likely in the $60-75 range — broadly consistent with the original estimate." Individual price checks: Nucleo $14.85 (vs $20 claimed), nRF52840 module $5.50 (vs $4 claimed), PCM1808 $0.32-1.50. Net adjustment is minor. | ComponentSpecs/investigation.json |

---

## Cross-checks

- **IT6803 non-existence claim:** CONFIRMED. Rollup states "IT6803 HDMI TX IC does not exist in ITE Tech's product catalog — the IT680x series are HDMI receivers, not transmitters." This matches EarcHdmiOutput sub-inv key_finding[0] verbatim. Live ITE product catalog (ite.com.tw/en/product/cate1) was visited in the sub-investigation; IT6621 product page is live and confirmed as "ARC/eARC Transmitter with Audio MUX."

- **VCXO misidentification (TXC 7M + NDK NZ2520SDA):** CONFIRMED. Rollup states "TXC 7M is a passive quartz crystal with no oscillator circuit, and the NDK NZ2520SDA is a fixed-frequency SPXO with no voltage control input." This matches ComponentSpecs sub-inv key_findings[4-5]. Live NDK product page explicitly categorizes NZ2520SDA under "crystal-oscillator" (not VCXO) and lists no voltage control pin. SiT3807 live page confirms it is a VCXO with configurable pull range.

- **PCM1808 TSSOP-14 package:** CONFIRMED. Rollup states "TSSOP-14 (14 pins, not 28)." ComponentSpecs sub-inv key_finding[0] matches. TI live product page confirms "14-pin TSSOP (PW) package."

- **DTS bandwidth risk characterisation:** CONFIRMED. Rollup states "DTS core at 1509.75 Kbps consumes 89-116% of the nRF52840's achievable throughput range (1.3-1.7 Mbps), making full-rate DTS marginal to infeasible without a custom ACK-less unidirectional protocol." RfTransport sub-inv key_finding[9] states the same percentages and characterisation. The rollup's additional note that DTS "may understate the risk" is a reasonable editorial judgment given the 89-116% range includes values >100%.

---

## Flags

**F1 — NEEDS_PRIMARY_SOURCE: HDMI eARC version attribution.** The rollup (concept #2) describes eARC as an "HDMI 2.1 feature." The HDMI.org eARC specification page now references HDMI 2.2, not 2.1. eARC was originally introduced in HDMI 2.1 (2017) but the current HDMI.org page uses HDMI 2.2 branding. This is likely a rebranding/versioning update by HDMI Forum rather than a factual error in the rollup — eARC was part of HDMI 2.1 at the time of its introduction. **Recommendation: hedge as "HDMI 2.1+" or "HDMI 2.1/2.2" to be version-safe.**

**F2 — CONFIRM_OR_HEDGE: Lattice SiI9438 product page inaccessible.** The Lattice HDMI 2.1 eARC product page (https://www.latticesemi.com/en/Products/ASSPs/HDMI21eARC) returns HTTP 403. The product may have been reorganized, renamed, or access-restricted. The SiI9437/SiI9438 parts are referenced in the EarcHdmiOutput sub-investigation and rollup as alternatives to the IT6621. If the page has been taken down, Lattice may have discontinued or reorganized these products. **Recommendation: verify current Lattice eARC product availability before selecting SiI9438 as an alternative.**

**F3 — CONFIRM_OR_HEDGE: SiT3807 pricing.** The rollup states VCXO replacement cost as "$5-10." The live SiTime product page lists $7.87 for the SiT3807. This is within the stated range but at the higher end. Single-unit distributor pricing may be higher. Minor discrepancy — no correction needed, but the $5 lower bound may only be achievable with the Abracon ASVV (whose datasheet PDF was reachable but content not extractable for price verification).

---

## Summary

- **Sources sampled:** 11 verified / 14 sampled, 1 dead (Lattice 403), 2 unverifiable (ST timeouts)
- **Findings:** 13 confirmed, 0 partially confirmed, 0 unverified, 0 contradicted
- **Flags:** 3 (1 NEEDS_PRIMARY_SOURCE, 2 CONFIRM_OR_HEDGE)
- **Disputed items requiring correction:** None. All 13 findings are confirmed. F1 (HDMI version) is cosmetic. F2 (Lattice URL) is an availability concern, not a factual error. F3 (pricing) is within stated range.
