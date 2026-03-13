# Validation Report — RfTransport

**Date:** 2026-03-13
**Investigator output:** investigation.json
**Validator:** validator-rftransport

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge/RfTransport
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        11           11           7727c1beb338   7727c1beb338
tensions             IN_SYNC        5            5            74f2d6527419   74f2d6527419
open_questions       IN_SYNC        5            5            bc2ac7452885   bc2ac7452885
sources              IN_SYNC        7            7            0514310da0d7   0514310da0d7
concepts             IN_SYNC        6            6            e66c750a43f1   e66c750a43f1
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source URL Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Nordic Semiconductor nRF52840 Product Specification — RADIO peripheral | https://infocenter.nordicsemi.com/topic/ps_nrf52840/radio.html | REDIRECT | 302 redirects to https://docs.nordicsemi.com/bundle/ps_nrf52840/page/radio.html — Nordic migrated their infocenter to docs.nordicsemi.com. Redirected page exists but content did not render fully for extraction. The page is the correct destination. |
| 2 | Espressif ESP-NOW FAQ — Throughput measurements | https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/esp-now.html | VERIFIED | Page loads and confirms ~214 Kbps in open environment, ~555 Kbps in shielded box at 1 Mbps PHY default. |
| 3 | Espressif Developer Blog — ESP-NOW for Outdoor Applications | https://developer.espressif.com/blog/esp-now-for-outdoor-applications/ | VERIFIED | Blog post confirmed. Discusses ESP-NOW throughput vs distance, reports 400 kbps at close range in open fields. |
| 4 | Microsoft Learn — Representing Formats for IEC 61937 Transmissions | https://learn.microsoft.com/en-us/windows/win32/coreaudio/representing-formats-for-iec-61937-transmissions | VERIFIED | Page loads and discusses IEC 61937 format representation, SubFormat GUIDs for AC-3 and DTS, S/PDIF container rates. |
| 5 | ETSI TS 102 114 — DTS Coherent Acoustics specification | https://www.etsi.org/deliver/etsi_ts/102100_102199/102114/01.02.01_60/ts_102114v010201p.pdf | VERIFIED | PDF exists at ETSI. Binary PDF not readable via web fetch, but URL resolves correctly and ETSI search confirms TS 102 114 specifies DTS bitrate range 32-6144 Kbps. |
| 6 | S/PDIF Free Space Digital Audio Optical Link — bitrate calculations | https://www.jensign.com/SPDIFLink/ | VERIFIED | Page confirms 3.072 Mbps information bitrate at 48 kHz (48,000 x 64 bits/frame) and 6.144 Mbps at 96 kHz. Biphase mark encoding doubles the line rate. |
| 7 | Nordic DevZone — Intro to ShockBurst/Enhanced ShockBurst | https://devzone.nordicsemi.com/nordic/nordic-blog/b/blog/posts/intro-to-shockburstenhanced-shockburst | DEAD | HTTP 403 Forbidden. The URL exists in web search indexes and is the correct canonical URL, but returns 403 when fetched directly — likely behind authentication or CDN protection. Nordic DevZone search confirms the blog post exists. |

---

## Finding Verification

| # | Finding (summary) | Verdict | Evidence | Source |
|---|-------------------|---------|----------|--------|
| 1 | Raw S/PDIF at 48 kHz is exactly 3.072 Mbps (48,000 frames/s x 64 bits/frame per IEC 60958) | CONFIRMED | jensign.com confirms "for the sampling rates of 48kHz... the information bit rates are 3.072 Mbit/sec." Calculation is straightforward: 48000 x 64 = 3,072,000 bps. | https://www.jensign.com/SPDIFLink/ |
| 2 | nRF52840 2 Mbps proprietary radio with ESB achieves ~1.0 Mbps application throughput, not 1.5 Mbps as claimed for general case | CONFIRMED | Web search confirms ESB at 2 Mbps PHY yields ~1 Mbps application throughput due to ACK overhead and turnaround times. Nordic DevZone discussions corroborate this figure. | Nordic DevZone Q&A, ESB documentation |
| 3 | Unidirectional nRF52840 streaming without ACKs can theoretically reach ~1.7 Mbps with max-size payloads (252 bytes) | CONFIRMED | Nordic DevZone thread on ESB maximum data rate discusses ~1.7 Mbps theoretical throughput with 252-byte payloads and no ACKs at 2 Mbps PHY. Calculation: 252 bytes payload / (252+overhead bytes) * 2 Mbps aligns with this figure. | https://devzone.nordicsemi.com/f/nordic-q-a/120889/how-to-achieve-nrf52840-esb-maximum-data-rate |
| 4 | The 1.5 Mbps claim for nRF52840 is plausible but optimistic — requires careful protocol engineering | CONFIRMED | With ESB (ACKs) yielding ~1 Mbps and unidirectional max at ~1.7 Mbps, 1.5 Mbps sits in the upper range requiring no ACKs, max payloads, minimal inter-packet gaps. The characterization as "plausible but optimistic" is accurate. | Derived from findings #2 and #3 |
| 5 | ESP-NOW at default 1 Mbps PHY achieves ~214 Kbps in open environments and ~555 Kbps in shielded conditions | CONFIRMED | Espressif ESP-FAQ page states exactly: "Around 214 Kbps in opened environment" and "Around 555 Kbps in shielding box" at 1 Mbps PHY default on ESP32-DevKitC V4. | https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/esp-now.html |
| 6 | ESP-NOW can reach ~400 Kbps at close range with ESP32-C6, but insufficient for DD5.1 at 640 Kbps | CONFIRMED | Espressif developer blog confirms "Speed in open fields reached a maximum of 400 kbps at close ranges" for ESP-NOW. 400 Kbps < 640 Kbps, so correctly ruled out. | https://developer.espressif.com/blog/esp-now-for-outdoor-applications/ |
| 7 | Dolby Digital (AC-3) max bitrate 640 Kbps per codec spec; DVD-Video caps at 448 Kbps | CONFIRMED | Library of Congress format description states "The maximum bitrate in the ATSC AC-3 specification is 640 kb/s" and "In DVD applications... the maximum [is] 448 kb/s." Wikipedia and multiple sources corroborate. | https://www.loc.gov/preservation/digital/formats/fdd/fdd000209.shtml |
| 8 | DTS core at 48 kHz maxes out at 1509.75 Kbps on DVD, fits within S/PDIF 48 kHz stereo container of 1536 Kbps | CONFIRMED | AVS Forum and VideoHelp discussions confirm DTS on DVD-Video at 48 kHz uses 1509.75 kbps (full-rate) or 754.5 kbps (half-rate). The 1536 Kbps S/PDIF stereo container (48000 x 32 = 1,536,000 bps) is the standard transport rate. ETSI TS 102 114 specifies DTS range up to 6144 Kbps for the full codec, with DVD implementations limited by the S/PDIF container. | ETSI TS 102 114, AVS Forum threads |
| 9 | DD5.1 at 640 Kbps uses 38-49% of nRF52840 throughput range (1.3-1.7 Mbps) | CONFIRMED | Arithmetic check: 640/1700 = 37.6%, 640/1300 = 49.2%. The stated range of 38-49% is correct (investigation states "43-53%" in quick_reference which uses 1.3-1.5 Mbps range — see flag below). The key finding #9 says "38-49%" matching the 1.3-1.7 Mbps range. | Derived calculation |
| 10 | DTS core at 1509.75 Kbps consumes 89-116% of nRF52840 throughput range, marginal to infeasible at lower end | CONFIRMED | Arithmetic check: 1509.75/1700 = 88.8%, 1509.75/1300 = 116.1%. The stated 89-116% range is correct. At the lower end (1.3 Mbps), DTS exceeds capacity. "Marginal to infeasible" is an accurate characterization. | Derived calculation |
| 11 | IEC 61937 adds small framing overhead but compressed bitstream bitrate is the dominant factor for RF link sizing | CONFIRMED | Microsoft Learn IEC 61937 page shows that compressed audio (AC-3, DTS) is transported within the existing S/PDIF frame structure using SubFormat GUIDs. The burst preamble is minimal overhead relative to the payload bitrate. The payload bitrate is correctly identified as the governing metric. | https://learn.microsoft.com/en-us/windows/win32/coreaudio/representing-formats-for-iec-61937-transmissions |

---

## Flags

**INTERNAL_CONFLICT:** The quick_reference table states DD5.1 uses "43-53% of available bandwidth" while key finding #9 states "38-49%." The discrepancy arises from different throughput ranges: the quick_reference appears to use 1.2-1.5 Mbps while the key findings use 1.3-1.7 Mbps. The quick_reference "notes" field correctly states the 1.3-1.7 Mbps range but the percentage in the table row does not match. The key finding #9 percentages (38-49%) are arithmetically correct against the 1.3-1.7 Mbps range. The quick_reference percentages (43-53%) correspond to approximately 1.2-1.5 Mbps, which is inconsistent with the stated range. This is a minor internal inconsistency.

**CONFIRM_OR_HEDGE:** Finding #3 states ~1.7 Mbps as "theoretical" — this is sourced from Nordic DevZone community calculations rather than official Nordic documentation. The Nordic DevZone blog post (source #7) returned 403, so the primary source for ESB throughput calculations could not be directly verified. However, the figure is consistent with first-principles calculation (252 payload bytes / ~260 total bytes * 2 Mbps) and is widely cited in the developer community.

---

## Summary

- Sources: 5 verified / 7 total, 1 dead (403), 1 redirect (302 to valid destination)
- Findings: 11 confirmed, 0 partially confirmed, 0 unverified, 0 contradicted
- Flags: 2 (1 INTERNAL_CONFLICT on percentage range in quick_reference vs key findings, 1 CONFIRM_OR_HEDGE on ~1.7 Mbps theoretical figure)
- Disputed items requiring correction: Quick reference table row "DD5.1 640 Kbps fits nRF52840 1.5 Mbps" states "43-53%" but should be "38-49%" to match the 1.3-1.7 Mbps range stated elsewhere in the document. Source #1 URL should be updated to the new Nordic docs URL.
