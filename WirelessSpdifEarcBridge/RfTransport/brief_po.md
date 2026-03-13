# RF Transport Bandwidth Verification for Wireless S/PDIF Bridge — Product Brief

**Date:** 2026-03-13
**Risk Level:** MEDIUM

---

## What Is This?

> The wireless bridge can reliably carry Dolby Digital surround sound, but DTS support is technically risky and may need to be a stretch goal.

---

## What Does This Mean for Us?

Most surround-sound content (Dolby Digital 5.1, the dominant format in streaming, broadcast, and DVD) will work over the proposed wireless link with good margin. Full-quality DTS, used mainly on some Blu-rays and older DVDs, pushes the wireless link to its absolute limit and may not work reliably in real homes with Wi-Fi interference.

---

## Key Points

- Dolby Digital 5.1 (the most common surround format) works with plenty of headroom — this covers Netflix, Disney+, broadcast TV, and most DVDs.
- Full-rate DTS (1509 Kbps) is right at the edge of what the wireless chip can handle — it may work in a lab but drop out in a busy Wi-Fi environment.
- Half-rate DTS (754 Kbps), used on most DTS DVDs, would work fine — consider targeting this as the supported DTS tier.

---

## Next Steps

**PO/EM Decision:**

> Define whether DTS support is a launch requirement or a post-launch enhancement, and whether half-rate DTS (754 Kbps) coverage is acceptable.

**Engineering Work Items:**
- Build nRF52840 unidirectional streaming prototype and measure real-world throughput in home environment with active Wi-Fi
- Test with actual DTS and DD5.1 content to validate end-to-end audio quality

**Leadership Input Required:**

> Architects should evaluate whether a dual-radio or channel-bonding approach could provide the 3+ Mbps needed for comfortable full-rate DTS, and whether the added complexity is justified.

---

## Open Questions

- What percentage of real-world DTS content is encoded at 754.5 Kbps (half-rate) vs 1509.75 Kbps (full-rate)?
- Can we implement graceful degradation — attempt DTS transport and fall back to re-encoding if packet loss exceeds a threshold?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
