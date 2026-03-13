# Validation Report — EarcHdmiOutput

**Date:** 2026-03-13
**Investigator output:** investigation.json
**Validator:** validator-earc

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge/EarcHdmiOutput
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           fd17b76711f9   fd17b76711f9
tensions             IN_SYNC        5            5            191bd1419d36   191bd1419d36
open_questions       IN_SYNC        5            5            ee46272358b0   ee46272358b0
sources              IN_SYNC        8            8            3607f7b57403   3607f7b57403
concepts             IN_SYNC        6            6            39a16c82329d   39a16c82329d
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source URL Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | ITE Tech Product Catalog — Video Link Category | https://www.ite.com.tw/en/product/cate1 | VERIFIED | Page loads, lists all HDMI products including IT6621, IT6622, IT6620BFN under eARC category. No IT6803 found. |
| 2 | ITE IT6621 Product Page — ARC/eARC Transmitter with Audio MUX | https://www.ite.com.tw/en/product/cate1/IT6621 | VERIFIED | Page loads with full product details: 32-pin QFN, 8x I2S + SPDIF input, 98.304 Mbps DMAC, eARC TX. |
| 3 | ITE IT6622 Product Page — HDMI 1.4 Tx with eARC RX and Embedded MCU | https://www.ite.com.tw/en/product/cate1/IT6622 | VERIFIED | Page loads with full product details: 56-pin QFN, HDMI 1.4 TX + eARC RX, embedded MCU and Flash. |
| 4 | HDMI.org — Enhanced Audio Return Channel (eARC) Specification Overview | https://www.hdmi.org/spec2sub/enhancedaudioreturnchannel | VERIFIED | Page loads. Now references "HDMI 2.2" (which supersedes 2.1 but retains eARC). Confirms high-bitrate audio support including DTS-HD MA, DTS:X, Dolby TrueHD, Dolby Atmos. |
| 5 | DPL Labs — HDMI eARC Detailed Technical Exploration | https://dpllabs.com/hdmis-enhanced-audio-return-channel-earc-detailed-technical-exploration/ | VERIFIED | Page loads with detailed technical content on HEAC pins 14/19, LVDS at 350 mVpp, CMDC independence from CEC, 37 Mbps bandwidth. |
| 6 | Granite River Labs — HDMI 2.1 eARC Compliance Testing | https://www.graniteriverlabs.com/en-us/technical-blog/hdmi-earc-compliance-test | VERIFIED | Page loads. Confirms DMAC (one-way audio TX→RX) and CMDC (bidirectional control) architecture, IEC 60958-1 encoding, CEC independence. |
| 7 | Lattice Semiconductor — HDMI 2.1 eARC Transmitter/Receiver Product Page | https://www.latticesemi.com/en/Products/ASSPs/HDMI21eARC | DEAD | Returns HTTP 403 Forbidden. However, the product is confirmed via Lattice data brief PDFs and press releases found through web search. |
| 8 | Dolby — HDMI 2.1 ARC and eARC Explained | https://www.dolby.com/experience/home-entertainment/articles/hdmi-2.1-arc-and-earc-explained | VERIFIED | Page loads (content rendered via JavaScript; title and structure confirmed). Dolby's authoritative source on eARC audio format support. |

---

## Finding Verification

| # | Finding (summary) | Verdict | Evidence | Source |
|---|-------------------|---------|----------|--------|
| 1 | IT6803 does not appear in ITE Tech's product catalog — IT680x series are HDMI receivers, not transmitters, none support eARC | CONFIRMED | ITE product catalog lists IT6801FN, IT68013FN, IT6802E, IT6807, IT68071 as receivers. No IT6803 exists. Web search for "IT6803" returns no results from ITE or any datasheet aggregator. | ITE product catalog (Source #1), web search |
| 2 | ITE Tech's actual eARC-capable TX parts are IT6621 (ARC/eARC TX, 32-pin QFN) and IT6622 (HDMI 1.4 TX + eARC RX, 56-pin QFN) | CONFIRMED | ITE product page confirms IT6621 as "ARC/eARC Transmitter with Audio MUX" in 32-pin QFN (4x4mm), and IT6622 as "HDMI 1.4 Tx with eARC RX and Embedded MCU" in 56-pin QFN (7x7mm). | Sources #2, #3 |
| 3 | IT6621 accepts 8x I2S + SPDIF, handles eARC with 98.304 Mbps DMAC, supports up to 8ch 192kHz audio | CONFIRMED | ITE product page states: "Eight I2S signals for multi-channel L-PCM audio with maximum 16-channel," SPDIF input, 98.304 Mbps DMAC bandwidth, 8ch 192kHz in eARC mode. | Source #2 |
| 4 | IT6622 combines HDMI 1.4 video TX with eARC receiver (not transmitter), includes embedded MCU and Flash, handles HPD and CEC via embedded HW PHY | CONFIRMED | ITE product page confirms: HDMI 1.4b TX (3 Gbps/channel), eARC RX function, embedded MCU with Flash, HDCP 1.4 HW engines, CEC PHY, HPD/termination detection. | Source #3 |
| 5 | eARC negotiation does NOT use CEC — uses dedicated CMDC, operates independently even when CEC is disabled | CONFIRMED | DPL Labs article explicitly states eARC uses "eARC Data Channel" for link management "independently of CEC" and "full eARC interoperability...even in systems where CEC is disabled." Granite River Labs confirms CMDC provides bidirectional control "without CEC dependency." | Sources #5, #6 |
| 6 | eARC uses HEAC differential pair (HDMI pins 14 and 19) for both DMAC (one-way audio) and CMDC (bidirectional control) | CONFIRMED | DPL Labs article confirms: "HEAC differential pair (pins 14 and 19)" with "LVDS at approximately 350 mVpp differential swing centered around 1.8V common mode." Granite River Labs confirms DMAC is one-way from eARC TX (Sink) to eARC RX (Source), CMDC is bidirectional. | Sources #5, #6 |
| 7 | eARC supports DD 5.1, DD+, TrueHD, Atmos, DTS, DTS-HD MA, DTS:X, and uncompressed PCM up to 7.1ch 192kHz/24-bit | CONFIRMED | HDMI.org page confirms: "high-bitrate audio formats up to 192kHz, 24-bit, and uncompressed 5.1 and 7.1, and 32-channel uncompressed audio" plus "DTS-HD Master Audio, DTS:X, Dolby TrueHD, Dolby Atmos." Multiple web sources confirm 37-38 Mbps bandwidth supports all these formats. | Source #4, web search results |
| 8 | eARC passthrough is format-agnostic — compressed bitstreams pass through untouched as IEC 61937 data packets | CONFIRMED | Granite River Labs confirms IEC 60958-1 standard structure for audio data encoding. The eARC transport carries both compressed and uncompressed audio without re-encoding. Note: investigation says "IEC 61937" while GRL says "IEC 60958-1" — both are correct as IEC 61937 defines compressed audio framing within the IEC 60958 transport. | Source #6 |
| 9 | Lattice SiI9437 (eARC RX) and SiI9438 (eARC TX) are dedicated 32-pin QFN eARC companion ICs that pair with any HDMI TX/RX, support eARC and legacy ARC fallback | CONFIRMED | Lattice data brief and press releases confirm: SiI9437 (RX) and SiI9438 (TX), 32-pin 4x4mm QFN, designed to work with "existing HDMI transmitter or receiver ICs using any version of HDMI," automatic ARC fallback, I2C control. Pioneer+Onkyo selected SiI9437 for eARC in their AVRs. Product page itself returns 403 but product is well-documented elsewhere. | Lattice data briefs, Business Wire press release, Mouser product listing |
| 10 | HDMI HPD/DDC/CEC and eARC from firmware on bare MCU is non-trivial — dedicated silicon is the standard approach | CONFIRMED | ITE and Lattice both market dedicated ICs specifically because these protocols require precise timing and multiple concurrent state machines. IT6621/IT6622 handle CEC PHY, HPD detection, and eARC CMDC in hardware. The existence of these specialized ICs from multiple vendors confirms the complexity claim. | Sources #2, #3, Lattice ecosystem |

---

## Flags

### CONFIRM_OR_HEDGE: eARC bandwidth figure

The investigation states eARC has "37 Mbps bandwidth" in the concepts section. Some sources report "37 Mbps" (DPL Labs), others "38 Mbps" (What Hi-Fi). The HDMI.org page does not specify an exact number. This is a minor discrepancy — the investigation's 37 Mbps figure is sourced from DPL Labs and is within the commonly cited range. No correction needed, but the figure could be stated as "~37 Mbps" for precision.

### CONFIRM_OR_HEDGE: HDMI version for eARC

The investigation states "eARC defined in HDMI 2.1 specification (2017+)." This is correct — eARC was introduced in HDMI 2.1 (November 2017). However, the HDMI.org page now references "HDMI 2.2" which is the current latest version that also includes eARC. The investigation's claim is historically accurate; eARC originated in 2.1.

### NEEDS_PRIMARY_SOURCE: IT6621/IT6622 availability and eval boards

Finding in tension #5 states "No public datasheets or eval board documentation were found for the IT6621 or IT6622 — ITE Tech appears to require NDA." This is plausible (product pages show feature summaries but not full datasheets), but the investigation does not provide evidence of an NDA requirement — this is inferred. The claim is reasonable but unverified against a primary source.

---

## Summary

- **Sources:** 7 verified / 8 total, 1 dead (Lattice product page returns 403, but product confirmed via alternative sources), 0 unverifiable
- **Findings:** 10 confirmed, 0 partially confirmed, 0 unverified, 0 contradicted
- **Flags:** 3 (2 CONFIRM_OR_HEDGE, 1 NEEDS_PRIMARY_SOURCE)
- **Disputed items requiring correction:** None
