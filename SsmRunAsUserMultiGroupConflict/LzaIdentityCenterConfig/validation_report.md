# Validation Report: LZA identityCenter Config Block — Declarative Surface, Limits, and ABAC Gap
Date: 2026-02-27
Validator: Fact Validation Agent (cycle 2 — final re-check)

## Summary
- Total sources checked: 25 (carried forward from cycle 1; only re-checked items re-verified below)
- Findings checked: 1 (Finding 9 — the only corrected finding; all other findings unchanged from cycle 1)
- Confirmed: 1 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

Cycle 1 verdicts for Findings 1–8, 10–11 are unchanged and carry forward as CONFIRMED. This cycle re-checks Finding 9 only, per the remediation instruction.

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/LzaIdentityCenterConfig
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        11           11           a04a5dfffb9a   a04a5dfffb9a
tensions             IN_SYNC        5            5            22a020433c36   22a020433c36
open_questions       IN_SYNC        6            6            f7fc8aaafe97   f7fc8aaafe97
sources              IN_SYNC        25           25           3151a543ddd9   3151a543ddd9
concepts             IN_SYNC        11           11           71fd482f1d48   71fd482f1d48
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

All fields and brief files are IN_SYNC. No markdown regeneration required.

---

## Finding Re-verification

### Finding 9: ABAC attribute precedence — two confirmed two-way relationships

**Corrected claim (paraphrase):** AWS documentation confirms two specific precedence relationships: (a) console-configured attributes (InstanceAccessControlAttributeConfiguration) override SAML assertion values for the same key; and (b) SCIM-synchronized attributes take precedence over SAML assertion values for the same key. Both relationships are explicitly documented. The relative ordering between console-configured attributes and SCIM-synchronized attributes is not documented by AWS — treating this as a confirmed three-tier linear hierarchy (console > SCIM > SAML) goes beyond what the source material states and is an inference. The practical implication: both the console configuration and the SCIM sync are confirmed to override SAML claims, so either source could be the effective value when debugging unexpected SSMSessionRunAs values; but which of those two sources wins when both specify the same key cannot be determined from AWS documentation alone.

**Verdict: CONFIRMED**

**Evidence:**

**(a) Console-configured attributes override SAML assertions — CONFIRMED.**
The AWS "Attributes for access control" documentation page (https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html) states verbatim: "The attributes values that you choose here replace the values for any matching attributes that come from an IdP through an assertion." "Here" refers to the console "Attributes for access control" page (the InstanceAccessControlAttributeConfiguration resource). "Through an assertion" is SAML-specific language. This directly and explicitly confirms the claim.

**(b) SCIM-synchronized attributes override SAML assertions — CONFIRMED.**
The same page states verbatim: "In scenarios where the same attributes are coming to IAM Identity Center through SAML and SCIM, the SCIM attributes value take precedence in access control decisions." This directly and explicitly confirms the claim.

**(c) Console-configured vs. SCIM ordering — correctly stated as undocumented.**
The corrected finding explicitly states that the relative ordering between console-configured attributes and SCIM-synchronized attributes is not documented by AWS, and that treating console > SCIM > SAML as a confirmed three-tier linear hierarchy "goes beyond what the source material states and is an inference." This is accurate. The AWS page examined does not contain any sentence establishing the relative position of console-configured attributes versus SCIM-synchronized attributes. The corrected finding appropriately moves this question to open_questions.

The `SCIM attribute precedence` concept entry has been corrected in parallel and states the same two confirmed relationships while explicitly flagging the console-vs-SCIM ordering as undocumented. Consistent with the finding.

**Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html — VERIFIED (live, returns AWS documentation content as of 2026-02-27)

---

## Remediation Assessment

The cycle 1 re-check required the following correction to Finding 9:

> Narrow the claim to only what AWS documentation explicitly supports. Retain: (1) SCIM takes precedence over SAML, and (2) console-configured attributes replace SAML assertion values. The claim that console-configured attributes override SCIM-synchronized values must be downgraded to an inference or open question. The SCIM attribute precedence concept description must be narrowed to match.

The corrected investigation.json satisfies all three requirements:
- SCIM > SAML: retained as confirmed.
- Console-configured > SAML: retained as confirmed.
- Console > SCIM: explicitly labeled as an inference / open question; moved to open_questions (question 6 of 6).

No further remediation is required.

---

## Overall Assessment

**The investigation is ready to close.**

Finding 9 has been corrected in full compliance with the cycle 1 remediation instruction. The corrected claim is accurate, is supported by the live AWS source, and does not overstate what the documentation confirms. All other findings (1–8, 10–11) were CONFIRMED in cycle 1 and are unchanged.

The investigation's primary outputs — the LZA ABAC gap (Finding 8), the confirmed SCIM > SAML and console-configured > SAML precedence relationships (Finding 9), the OU-scoping limitation (Finding 6), and the ProvisionPermissionSet session non-invalidation behavior (Finding 4) — are all validated against primary AWS documentation and LZA source material. The quick_reference table and audience briefs accurately reflect these findings.

The investigation is internally consistent, JSON/MD sync is confirmed, and no CONTRADICTED or material UNVERIFIED claims remain.

**Final status: CLOSED — no outstanding remediation items.**
