# Investigation: Wireless Multichannel Audio Market Landscape: Projector-Soundbar Topology

**Date:** 2026-03-13
**Status:** Complete

---

## Question

> Is the hypothesis correct that no commercial product solves the projector-soundbar wireless multichannel audio problem -- transmitting a raw Dolby Digital 5.1/DTS bitstream wirelessly from a projector to a soundbar across the room -- and is there genuine unmet demand for such a solution?

---

## Context

Home theater projector setups frequently place the projector at the back or ceiling of the room with the soundbar at the front near the screen. Running cables across the room is cosmetically unacceptable for many users. This investigation examines whether any existing commercial product can wirelessly bridge a Dolby Digital 5.1 or DTS bitstream from a projector's TOSLINK/HDMI output to a soundbar's eARC or optical input, and whether real user demand for such a product exists.

---

## Quick Reference

| Solution | Supports Multichannel? | Projector Topology? | Notes |
| --- | --- | --- | --- |
| Wireless HDMI Kits (generic) | Stereo only (no ARC return) | No - assumes co-located source/display | Transmit HDMI forward only; no audio return path |
| WiSA SoundSend | Yes - up to 8ch uncompressed | No - requires WiSA-certified speakers | Cannot feed a standard soundbar's eARC/optical input |
| WiSA DS Soundbars | Yes - 4.1ch wireless to satellites | No - soundbar is the hub, not receiver | Only 3 certified soundbars exist; closed ecosystem |
| AirPlay 2 | Stereo PCM only | No | Downmixes all multichannel to 2.0 stereo |
| Chromecast Audio/Built-in Cast | Stereo PCM default; DD+ over HDMI | No | Defaults to stereo PCM over Wi-Fi; can pass DD+ over HDMI to compatible receiver |
| Bluetooth (SBC/aptX/LDAC) | Stereo only | Partial - can pair projector to speaker | 100-250ms latency causes lip-sync drift; stereo only |
| DLNA/UPnP | Theoretically multichannel | No - requires compatible renderer | Most implementations fall back to stereo PCM |
| Marmitek Audio Anywhere 685 | Yes - DD 5.1 and DTS passthrough | Yes - TOSLINK in/out wireless bridge | Discontinued/hard to find; 12ms latency; 2.4GHz only; no eARC |
| HDFury Arcana | Yes - full Atmos/TrueHD via eARC | Yes - inline HDMI splitter with eARC out | Wired solution only; requires HDMI cable run to soundbar |
| AWOL Vision ThunderBeat | Yes - 4.2.2 Dolby Atmos (5.2.2 with CenterSync on AWOL projectors) | No - proprietary system for AWOL projectors | CenterSync feature exclusive to AWOL UST projectors |
| Generic 2.4G HDMI ARC Transmitter (Amazon) | Unclear - marketed as ARC audio | Potentially | Unverified specs; no confirmed multichannel passthrough |

---

## Key Findings

- The Marmitek Audio Anywhere 685 is the closest existing product to a wireless SPDIF bridge: it wirelessly transmits Dolby Digital 5.1 and DTS 6.1 bitstreams over TOSLINK/coaxial at 2.4GHz with 12ms latency. However, it appears discontinued or extremely hard to source, has no eARC output, and operates only at 2.4GHz with limited range through walls (10m).
- Wireless HDMI kits (2024-2025 models from various manufacturers) transmit video and audio forward from source to display only. They do not support HDMI ARC/eARC return, meaning they cannot extract audio from a projector and send it back to a soundbar. This confirms the topology gap.
- WiSA SoundSend decodes Dolby Digital, Dolby Digital+, and Dolby TrueHD and transmits up to 8 channels of uncompressed 24-bit audio -- but only to WiSA-certified speakers. It cannot output to a standard soundbar's optical or eARC input. Only three WiSA-certified soundbars exist (Harman Kardon Citation Bar, Citation MultiBeam 700, Savant Smart Audio 55), none of which are mainstream consumer products.
- AirPlay streams stereo PCM only. Apple TV always downmixes multichannel audio to 2-channel stereo over AirPlay, confirmed by multiple Apple Community threads and Roon Labs testing. Chromecast defaults to stereo PCM for broad compatibility and does not support raw IEC-61937 bitstream passthrough over Wi-Fi, though it can pass DD+ over HDMI to a compatible TV/receiver.
- Bluetooth is limited to stereo by all common codecs (SBC, aptX, aptX HD, LDAC, AAC). While AAC theoretically supports multichannel, no Bluetooth implementation passes 5.1 audio. Additionally, Bluetooth adds 100-250ms latency that causes visible lip-sync drift, a problem widely documented by BenQ, XGIMI, and ViewSonic in their projector support pages.
- DLNA/UPnP does not restrict multichannel audio at the protocol level, but most AVR and speaker implementations fall back to stereo PCM. Forum reports on AVS Forum and Roon Labs confirm that AC3 5.1 and TrueHD 5.1 content plays back as 2-channel stereo via DLNA in practice.
- Projector eARC/ARC support is growing but still uncommon. BenQ X3000i, Optoma UHZ45/UHZ50, and a few XGIMI models support eARC, but the majority of installed projectors lack it. Even with eARC, it provides a wired path to the soundbar -- solving format support but not the wireless requirement.
- The HDFury Arcana is the best wired solution: it sits inline between source and projector, extracting full eARC audio (up to Dolby Atmos over TrueHD) for a soundbar. But it requires a physical HDMI cable from projector location to soundbar, which is the exact cable run users want to avoid.
- Forum discussions on Tom's Guide, AVS Forum, Audioholics, and Home Theater Forum consistently show users asking how to wirelessly connect ceiling-mounted projectors to soundbars for surround sound. The universal answer is either 'use Bluetooth (stereo only)' or 'run a cable.' No wireless multichannel solution is ever recommended.
- AWOL Vision ThunderBeat (2024-2025) is a 4.2.2 wireless Dolby Atmos system, but it is designed exclusively for AWOL Vision UST projectors with CenterSync. It connects via eARC and is not a standalone wireless bridge for arbitrary projector-to-soundbar setups.
- A generic '2.4G HDMI Wireless ARC Audio Transmitter' appeared on Amazon (B0DC19ZCM2) claiming 50m wireless ARC transmission for projectors and soundbars, but product details are sparse, multichannel support is unverified, and no independent reviews confirm it passes anything beyond stereo.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| IEC 61937 Bitstream | The standard for conveying compressed multichannel audio (Dolby Digital, DTS) over S/PDIF and HDMI. A wireless bridge must pass this bitstream transparently without decoding it to PCM. |
| eARC (Enhanced Audio Return Channel) | HDMI 2.1 feature allowing a display to send high-bandwidth audio (Dolby TrueHD, Atmos) back to a soundbar or AVR over a single HDMI cable. Most projectors lack this feature. |
| WiSA (Wireless Speaker and Audio) | Industry standard for wireless multichannel audio using 5GHz unlicensed band. Delivers uncompressed 24-bit/96kHz audio to certified speakers. Closed ecosystem -- both transmitter and speakers must be WiSA-certified. |
| Projector Topology Problem | In projector setups, the display (projector) is ceiling/rear-mounted while audio equipment (soundbar) sits at the front near the screen. This physical separation -- typically 3-10 meters with no cable path -- creates the wireless audio gap that no mainstream product addresses. |
| TOSLINK/S/PDIF | Optical or coaxial digital audio interface supporting 2-channel PCM and compressed Dolby Digital 5.1/DTS. Present on most projectors and soundbars. Bandwidth-limited: cannot carry uncompressed multichannel PCM or lossless codecs (TrueHD, DTS-HD MA). |
| Lip-Sync Drift | Visible mismatch between video and audio caused by wireless transmission latency. Bluetooth adds 100-250ms; thresholds above 40-80ms are perceptible. A critical quality metric for any wireless audio bridge solution. |

---

## Tensions & Tradeoffs

- The Marmitek Audio Anywhere 685 proves the concept is technically feasible (wireless SPDIF with DD 5.1/DTS passthrough), but its discontinuation and lack of eARC output suggest the market was too small to sustain the product commercially.
- Users overwhelmingly want wireless convenience but multichannel audio standards (Dolby Digital, DTS, Atmos) were designed for wired interconnects (HDMI, TOSLINK). No wireless standard natively supports raw bitstream passthrough -- WiFi audio protocols (AirPlay, Cast, DLNA) decode to PCM first.
- The projector eARC adoption trend could eventually eliminate the need for a separate wireless bridge if projectors gain eARC and users accept running one HDMI cable to the soundbar. But this requires both hardware upgrades and still leaves the cable problem for ceiling-mounted setups.
- WiSA solves wireless multichannel audio at the speaker level but is a closed ecosystem. Users with existing soundbars (Sonos Arc, Samsung, Bose, etc.) cannot use WiSA without replacing their entire audio system.
- The market for this niche product is real but small: it requires a projector owner with a soundbar across the room who cares about multichannel audio and refuses to run a cable. This specificity may explain why no major manufacturer has built a dedicated solution.

---

## Open Questions

- Is the Marmitek Audio Anywhere 685 truly discontinued, or is it still available in some markets? If discontinued, what was the stated reason -- lack of demand or technical obsolescence?
- Does the generic Amazon '2.4G HDMI Wireless ARC Audio Transmitter' (B0DC19ZCM2) actually pass Dolby Digital 5.1 bitstreams, or is it stereo-only despite ARC branding? Independent testing would be needed.
- Could a wireless HDMI extender with an HDMI audio extractor at the receiver end solve the topology -- source to wireless TX, wireless RX to projector + audio extractor to soundbar? This would require the extractor to output via TOSLINK or eARC.
- How large is the addressable market? Projector sales are approximately 10 million units/year globally, but what fraction are ceiling-mounted with a soundbar setup where users would pay for a wireless bridge?
- Will HDMI 2.1 eARC becoming standard on projectors (BenQ, Optoma, XGIMI are leading) eventually make a wireless bridge less necessary, or does the physical separation still mandate a wireless solution?

---

## Sources & References

- [WiSA SoundSend Wireless Audio Transmitter - Official Product Page](https://www.wisatechnologies.com/soundsend)
- [WiSA-Certified Soundbars - Official Product Listing](https://www.wisatechnologies.com/soundbars)
- [HDMI eARC Specification - HDMI.org](https://www.hdmi.org/spec2sub/enhancedaudioreturnchannel)
- [HDFury 4K Arcana 18Gbps - Official Product Page](https://hdfury.com/product/4k-arcana-18gbps/)
- [Marmitek Audio Anywhere 685 User Manual - ManualsLib](https://www.manualslib.com/manual/1038197/Marmitek-Audio-Anywhere-685.html?page=5)
- [20+ Projectors With HDMI ARC/eARC - PointerClicker](https://pointerclicker.com/do-projectors-have-earc/)
- [Wireless Audio Solution for Ceiling Mounted Projector - Tom's Guide Forum](https://forums.tomsguide.com/threads/wireless-audio-solution-for-ceiling-mounted-projector.424743/)
- [AirPlay Surround or Multichannel Audio - Apple Community Discussion](https://discussions.apple.com/thread/253723517)
- [AWOL Vision ThunderBeat Wireless Surround Sound System - Official Product Page](https://awolvision.com/products/thunderbeat)
- [Can Bluetooth Transmit Surround Sound? - TheTechyLife Analysis](https://thetechylife.com/can-bluetooth-transmit-surround-sound/)
- [BenQ ARC and eARC Projector Audio Feature Guide](https://www.benq.com/en-us/campaign/gaming-projector/resources/arc-and-earc-the-audio-feature-that-enhances-your-home-theater-experience.html)
