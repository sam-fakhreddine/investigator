# Validation Report — MarketLandscape

**Date:** 2026-03-13
**Investigator output:** investigation.json
**Validator:** validator-market

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/WirelessSpdifEarcBridge/MarketLandscape
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        11           11           4f608254998e   4f608254998e
tensions             IN_SYNC        5            5            ee218d9172f9   ee218d9172f9
open_questions       IN_SYNC        5            5            dbbff0534472   dbbff0534472
sources              IN_SYNC        11           11           c0e4031c6070   c0e4031c6070
concepts             IN_SYNC        6            6            ce798d07a2d2   ce798d07a2d2

Result: IN_SYNC
```

---

## Source URL Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | WiSA SoundSend - Official Product Page | https://www.wisatechnologies.com/soundsend | VERIFIED | Page confirms SoundSend transmits up to 8ch uncompressed 24-bit audio to WiSA speakers; decodes Dolby Digital, DD+, TrueHD, Atmos |
| 2 | WiSA-Certified Soundbars - Official Listing | https://www.wisatechnologies.com/soundbars | VERIFIED | Lists exactly 3 soundbars: Harman Kardon Citation Bar, Citation MultiBeam 700, Savant Smart Audio WiSA Soundbar 55 |
| 3 | HDMI eARC Specification - HDMI.org | https://www.hdmi.org/spec2sub/enhancedaudioreturnchannel | VERIFIED | Page live; describes eARC with Dolby TrueHD, Atmos, DTS-HD MA, DTS:X support. Note: page now references HDMI 2.2 carrying eARC, but eARC was originally introduced with HDMI 2.1 (2017) |
| 4 | HDFury 4K Arcana 18Gbps - Official Product Page | https://hdfury.com/product/4k-arcana-18gbps/ | VERIFIED | Confirms "world's first eARC adapter" extracting full Dolby Atmos/TrueHD; wired HDMI solution with 1 HDMI In, 1 HDMI Out, 1 eARC Out |
| 5 | Marmitek Audio Anywhere 685 User Manual - ManualsLib | https://www.manualslib.com/manual/1038197/Marmitek-Audio-Anywhere-685.html?page=5 | VERIFIED | URL resolves; manual content confirmed via icecat.biz and manualzz.com mirror sources showing DD 5.1, DTS 6.1, 2.4GHz, 12ms latency specs. Page itself rendered mostly CSS/JS but manual exists at this location |
| 6 | 20+ Projectors With HDMI ARC/eARC - PointerClicker | https://pointerclicker.com/do-projectors-have-earc/ | VERIFIED | Lists 20+ projectors with ARC/eARC; confirms BenQ X3000i and Optoma UHZ45/UHZ50 with eARC. XGIMI models not found on this specific page |
| 7 | Wireless Audio Solution for Ceiling Mounted Projector - Tom's Guide | https://forums.tomsguide.com/threads/wireless-audio-solution-for-ceiling-mounted-projector.424743/ | VERIFIED | Forum thread matches description: user asks about wireless audio for ceiling-mounted BenQ projector; recommended solutions are Bluetooth (stereo) or wired. No wireless multichannel solution recommended |
| 8 | AirPlay Surround or Multichannel Audio - Apple Community | https://discussions.apple.com/thread/253723517 | VERIFIED | Thread exists; user reports Apple TV sends stereo only over AirPlay to multichannel Denon amplifier. Thread implies but does not explicitly state "stereo PCM only" as a protocol spec |
| 9 | AWOL Vision ThunderBeat - Official Product Page | https://awolvision.com/products/thunderbeat | VERIFIED | Page exists but rendered mostly as JS; Amazon listing and Best Buy confirm 4.2.2 configuration with Dolby Atmos/DTS:X support and CenterSync feature |
| 10 | Can Bluetooth Transmit Surround Sound? - TheTechyLife | https://thetechylife.com/can-bluetooth-transmit-surround-sound/ | VERIFIED | Article discusses Bluetooth surround limitations; confirms SBC/AAC not designed for multichannel; mentions aptX, LDAC. Does not provide specific 100-250ms latency figures |
| 11 | BenQ ARC and eARC Projector Audio Feature Guide | https://www.benq.com/en-us/campaign/gaming-projector/resources/arc-and-earc-the-audio-feature-that-enhances-your-home-theater-experience.html | VERIFIED | BenQ page confirming ARC/eARC on gaming projectors; lists X3000i, X3100i, X500i, X300G with eARC and Dolby Atmos support. Confirms eARC implements HDMI 2.1 specs |

---

## Finding Verification

| # | Finding (summary) | Verdict | Evidence | Source |
|---|-------------------|---------|----------|--------|
| 1 | Marmitek Audio Anywhere 685 wirelessly transmits DD 5.1 / DTS 6.1 over TOSLINK/coax at 2.4GHz with 12ms latency; appears discontinued; no eARC; 10m through walls | CONFIRMED | icecat.biz specs confirm DD 5.1, DTS 6.1, 2.4GHz (2400-2483.5 MHz), 12ms latency, 40m free-field / 10m through walls, TOSLINK+coax I/O. Product not listed on current Marmitek website (which sells Audio Anywhere 625/630 only). Amazon UK listing exists but availability unclear. | icecat.biz product specs; Marmitek official site; Amazon UK B011RE4HU6 |
| 2 | Wireless HDMI kits do not support ARC/eARC return; cannot extract audio from projector to soundbar | CONFIRMED | Web search confirms wireless HDMI transmitters "likely will not support ARC or eARC." AVForums and AVS Forum discussions confirm no wireless HDMI product supports ARC return path. Market offers only wired HDBaseT extenders with eARC. | AVForums thread "Wireless HDMI Exclusively for ARC"; AVS Forum thread on wireless HDMI for audio codecs |
| 3 | WiSA SoundSend: up to 8ch uncompressed 24-bit; decodes DD/DD+/TrueHD; only outputs to WiSA-certified speakers; only 3 certified soundbars (HK Citation Bar, Citation MultiBeam 700, Savant Smart Audio 55) | CONFIRMED | WiSA official pages confirm all claims exactly. SoundSend page lists 8ch uncompressed 24-bit 48/96kHz; soundbars page lists exactly 3 models matching the investigation. | wisatechnologies.com/soundsend; wisatechnologies.com/soundbars |
| 4 | AirPlay streams stereo PCM only; Apple TV downmixes multichannel to 2ch stereo over AirPlay | CONFIRMED | Apple Community thread confirms user's multichannel Denon receiver receives only stereo via AirPlay from Apple TV. Roon Labs community confirms AirPlay multichannel streaming produces 2-channel output. Sonos community corroborates. Multiple Apple Community threads document this limitation. | Apple Community thread/253723517; Roon Labs community; Sonos community |
| 5 | Chromecast outputs stereo PCM when casting; 5.1 content downmixed to 2.0 | PARTIALLY CONFIRMED | The situation is more nuanced than stated. Chromecast can pass DD+ to compatible devices via HDMI, but when the connected device lacks DD+ support, it falls back to stereo PCM (not DD 5.1). The core claim that many users experience stereo-only output is valid, but it is caused by codec compatibility fallback, not an inherent protocol limitation. The investigation's framing of "stereo PCM only" overstates the constraint. | Android Central, AVForums, Sonos Community, Hardware Canucks forum threads on Chromecast 5.1 |
| 6 | Bluetooth limited to stereo by SBC/aptX/LDAC/AAC; 100-250ms latency causes lip-sync drift | CONFIRMED | Multiple sources confirm BT codecs are stereo-only for practical purposes. Latency figures confirmed: SBC 150-220ms, aptX 100-200ms, LDAC 150ms+. Typical system-level range is 150-300ms, which encompasses and slightly exceeds the investigation's 100-250ms range. Lip-sync threshold is ~80-120ms for perceptibility. BenQ/XGIMI projector support pages reference BT latency as a known issue. | TREBLAB latency guide; Avantree latency guide; RTINGS BT tests; ArmorSound 2026 guide |
| 7 | DLNA/UPnP: most implementations fall back to stereo PCM despite protocol supporting multichannel | CONFIRMED | Investigation correctly hedges with "most implementations fall back to stereo PCM." Roon Labs and AVS Forum discussions confirm AC3 5.1 via DLNA often plays as 2ch stereo. The protocol itself does not restrict multichannel, but renderer implementation is the bottleneck. | Roon Labs community; AVS Forum DLNA discussions |
| 8 | Projector eARC/ARC growing but still uncommon; BenQ X3000i, Optoma UHZ45/UHZ50 support eARC; majority lack it | CONFIRMED | BenQ official page lists X3000i, X3100i, X500i, X300G with eARC (7.1ch + Atmos). PointerClicker lists 20+ models with ARC/eARC including Optoma UHZ45/UHZ50. eARC remains limited to mid/high-end projectors; budget and older models lack it. | BenQ eARC guide; PointerClicker projector list |
| 9 | HDFury Arcana: best wired solution; extracts full eARC audio (Atmos/TrueHD); requires physical HDMI cable | CONFIRMED | HDFury product page confirms "world's first eARC adapter" with full Dolby Atmos over TrueHD extraction. Entirely wired with HDMI In/Out/eARC Out. | hdfury.com/product/4k-arcana-18gbps/ |
| 10 | Forum discussions consistently show users asking for wireless projector-to-soundbar surround; answers are "Bluetooth (stereo)" or "run a cable" | CONFIRMED | Tom's Guide thread validated: ceiling-mounted projector user gets only Bluetooth or wired recommendations. AVForums and AVS Forum threads corroborate this pattern. No wireless multichannel solution is ever recommended in the threads found. | Tom's Guide thread/424743; AVForums wireless HDMI ARC thread |
| 11 | AWOL Vision ThunderBeat: wireless Dolby Atmos; designed for AWOL UST projectors with CenterSync; not a standalone bridge | PARTIALLY CONFIRMED | ThunderBeat is confirmed as 4.2.2 (not "5.2.2" as stated in quick_reference table). CenterSync creates a 5.2.2 config by using the AWOL projector as center channel. Product connects via eARC. Best Buy Q&A confirms CenterSync is specific to AWOL projectors. However, the investigation's key finding correctly says "4.2.2" while the quick_reference table row says "5.2.2 Dolby Atmos" -- this is an internal inconsistency. The key finding text also says "4.2.2 wireless Dolby Atmos system" which is correct, but the same finding says CenterSync creates 5.2.2, which is also correct. The quick_reference should say "4.2.2 (5.2.2 with CenterSync)" for clarity. | Amazon B0DKJZ69DT; Best Buy ThunderBeat listing; AWOL Vision official page |

---

## Flags

1. **INTERNAL_CONFLICT — AWOL ThunderBeat channel count:** The quick_reference table (row 10) states "5.2.2 Dolby Atmos" but key finding #10 correctly identifies it as "4.2.2 wireless Dolby Atmos system" that becomes 5.2.2 with CenterSync. The quick_reference should note the base config is 4.2.2.

2. **CONFIRM_OR_HEDGE — Chromecast stereo limitation:** Key finding #4 states Chromecast "outputs stereo PCM when casting, with users on Sonos and AVS Forums confirming 5.1 content is downmixed to 2.0." This is true in many common setups but is caused by DD+ incompatibility fallback, not an inherent casting protocol limitation. Chromecast can pass multichannel DD+ over HDMI to compatible devices. The finding should hedge: "Chromecast frequently falls back to stereo PCM when the receiving device does not support Dolby Digital Plus."

3. **CONFIRM_OR_HEDGE — eARC HDMI version:** The concepts section states eARC is an "HDMI 2.1 feature." This is historically accurate (eARC was introduced with HDMI 2.1 in 2017), but the current HDMI.org page now describes eARC under HDMI 2.2. The claim as stated is not wrong, but could be more precise: "introduced with HDMI 2.1."

4. **NEEDS_PRIMARY_SOURCE — Marmitek discontinuation:** The investigation states the Marmitek 685 "appears discontinued or extremely hard to source." No official discontinuation announcement was found. The product is absent from Marmitek's current product lineup (they sell Audio Anywhere 625/630 models), and Amazon UK has the listing but availability is unclear. The claim is reasonable but lacks a primary source confirming discontinuation.

---

## Summary

- Sources: **11 verified / 11 total**, 0 dead, 0 unverifiable
- Findings: **9 confirmed**, **2 partially confirmed**, 0 unverified, 0 contradicted
- Flags: **4** (1 INTERNAL_CONFLICT, 2 CONFIRM_OR_HEDGE, 1 NEEDS_PRIMARY_SOURCE)
- Disputed items requiring correction:
  - **Quick reference table row 10 (AWOL ThunderBeat):** Change "5.2.2 Dolby Atmos" to "4.2.2 (5.2.2 with CenterSync) Dolby Atmos" to match key finding #10 and avoid internal inconsistency
