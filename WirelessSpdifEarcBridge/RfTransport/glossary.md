# Glossary — RF Transport Bandwidth Verification for Wireless S/PDIF Bridge

Quick definitions of key terms and concepts referenced in this investigation.

---

## IEC 60958 / S/PDIF

Consumer digital audio interface standard using biphase mark encoding. At 48 kHz stereo, each frame is 64 bits (two 32-bit subframes), yielding a 3.072 Mbps information bitrate. The physical line rate is double (6.144 MHz) due to biphase encoding.

## IEC 61937

Standard for transporting non-linear PCM (compressed audio like AC-3, DTS) over an IEC 60958 link. Adds burst preambles to identify codec type and frame boundaries. The compressed payload replaces PCM sample data within the same 3.072 Mbps container.

## nRF52840 Proprietary Radio

Nordic Semiconductor's 2.4 GHz radio supporting 1 Mbps and 2 Mbps proprietary modes with configurable packet format (1B preamble, 1-5B address, payload up to 253B, 0-3B CRC). Lower overhead than BLE stack but still subject to ISM band contention.

## Enhanced ShockBurst (ESB)

Nordic's lightweight proprietary protocol providing packet buffering, acknowledgment, and automatic retransmission. At 2 Mbps PHY, ESB achieves ~1 Mbps application throughput due to ACK overhead and turnaround times.

## ESP-NOW

Espressif's connectionless Wi-Fi protocol for ESP32, using vendor-specific action frames with a maximum 250-byte payload. Default PHY is 1 Mbps, achieving ~214 Kbps in open environments due to CSMA/CA overhead and Wi-Fi framing.

## AC-3 (Dolby Digital)

Perceptual audio codec supporting up to 5.1 channels. Maximum bitrate is 640 Kbps per the AC-3 specification. DVD-Video caps at 448 Kbps. Transported via IEC 61937-3 over S/PDIF.

---

*Back to: [investigation.md](investigation.md)*
