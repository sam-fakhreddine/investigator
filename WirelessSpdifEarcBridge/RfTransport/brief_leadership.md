# RF Transport Bandwidth Verification for Wireless S/PDIF Bridge — Engineering Leadership Brief

**Date:** 2026-03-13

---

## Headline

> Dolby Digital 5.1 is safely transportable over nRF52840, but full-rate DTS at 1509 Kbps is a high-risk bet requiring custom protocol work with uncertain outcome.

---

## So What

The wireless bridge design works for the most common surround format (DD5.1 at up to 640 Kbps) with ~40% bandwidth headroom. However, full-rate DTS at 1509.75 Kbps pushes the nRF52840 to its absolute limit with zero margin for error correction or RF interference — this is a design risk that should be scoped explicitly before committing.

---

## Key Points

- DD5.1 at 640 Kbps fits within nRF52840 throughput (1.3-1.7 Mbps) with 40-60% margin — low risk.
- DTS core at 1509.75 Kbps consumes 89-116% of achievable throughput — marginal to infeasible without ACK-less unidirectional protocol.
- ESP-NOW at ~214 Kbps is confirmed too slow even for DD5.1 — correctly eliminated in the original design.

---

## Action Required

> Decide whether DTS support is a hard requirement or a stretch goal. If required, allocate engineering time for nRF52840 custom protocol development and real-world throughput testing before committing to the RF transport architecture.

---

*Full engineering investigation: [investigation.md](investigation.md)*
