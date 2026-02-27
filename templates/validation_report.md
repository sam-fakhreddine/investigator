# Validation Report: {INVESTIGATION TITLE}

**Date:** {YYYY-MM-DD}
**Validator:** Fact Validation Agent

---

## Summary

- Total sources checked: N
- Verified: N | Redirected: N | Dead: N | Unverifiable: N
- Findings checked: N
- Confirmed: N | Partially confirmed: N | Unverified: N | Contradicted: N
- JSON/MD sync issues: N
- Items requiring remediation: N

---

## JSON/MD Sync Check

```
[output of: python3 scripts/check_sync.py <investigation_dir>]
```
| key_findings | IN_SYNC / OUT_OF_SYNC | ... |
| sources | IN_SYNC / OUT_OF_SYNC | ... |
| concepts | IN_SYNC / OUT_OF_SYNC | ... |

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | ... | ... | VERIFIED / REDIRECT / DEAD / UNVERIFIABLE | ... |

---

## Finding Verification

### Finding: {brief label}

- **Claim:** {exact claim from investigation}
- **Verdict:** CONFIRMED / PARTIALLY CONFIRMED / UNVERIFIED / CONTRADICTED
- **Evidence:** {what was found to support or contradict the claim}
- **Source used:** {URL or search result}

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| ... | ... | ... |

---

## Overall Assessment

{Summary paragraph: what proportion of findings checked out, any material inaccuracies found, and whether the investigation can be trusted as a whole.}
