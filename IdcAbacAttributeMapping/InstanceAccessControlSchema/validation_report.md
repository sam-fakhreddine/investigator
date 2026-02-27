# Validation Report: IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema and Configuration Surface — Cycle 1 Re-check
Date: 2026-02-27
Validator: Fact Validation Agent (cycle 1 re-check)

## Summary
- Total sources checked: 14 (carried forward; no new sources verified in this cycle)
- Verified: 13 | Redirected: 0 | Dead: 0 | Unverifiable: 1 | Carried forward: 14
- Findings checked: 1 (KF6 re-check only)
- Confirmed: 1 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/IdcAbacAttributeMapping/InstanceAccessControlSchema
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        8            8            afa33f36b14e   afa33f36b14e
tensions             IN_SYNC        4            4            85273affb2c9   85273affb2c9
open_questions       IN_SYNC        6            6            54136082d762   54136082d762
sources              IN_SYNC        14           14           6ac4d4170ab9   6ac4d4170ab9
concepts             IN_SYNC        8            8            63a285290b30   63a285290b30
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Finding Verification (Cycle 1 Re-check)

### KF6: SSMSessionRunAs as the exact tag Key

**Verdict: CONFIRMED**

**Claim 1 — `SSMSessionRunAs` is the exact required Key string.**

Confirmed directly against the AWS Systems Manager user guide page "Turn on Run As support for Linux and macOS managed nodes" (https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html). The page states verbatim: "Enter `SSMSessionRunAs` for the key name. Enter the name of an OS user account for the key value." The documentation prescribes this exact string with no variation offered. Casing significance is implicitly confirmed by the explicit, case-specific instruction.

**Claim 2 — `ssm:RunAsDefaultRunAs` appears in SSM user guide content or blog posts but is NOT listed in the formal AWS Service Authorization Reference condition key table for Systems Manager.**

Confirmed on both halves:

- The string `ssm:RunAsDefaultRunAs` does appear in SSM user guide content (session preferences documentation) and in blog posts such as "How to automate Session Manager preferences across your organization" (https://aws.amazon.com/blogs/security/how-to-automate-session-manager-preferences-across-your-organization/). Its informal presence in AWS-authored documentation is confirmed.
- The AWS Service Authorization Reference for Systems Manager (https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html) was fetched and reviewed. The complete condition key list for Systems Manager contains 20 entries. `ssm:RunAsDefaultRunAs` does not appear among them. Its absence from the formal condition key table is confirmed.

The corrected KF6 accurately represents both the operational requirement (`SSMSessionRunAs` is the exact required key name, casing is significant) and the status of `ssm:RunAsDefaultRunAs` (present in informal SSM documentation contexts, not formally listed in the Service Authorization Reference condition key table). The prior PARTIALLY CONFIRMED verdict was based on a version of KF6 that made a stronger, unverified claim; the corrected text accurately qualifies the claim and is now fully supportable.

**Sources used:** SSM user guide session-preferences-run-as.html; AWS Service Authorization Reference list_awssystemsmanager.html; AWS Security Blog automating Session Manager preferences post.

## Carried Forward (Prior Validation)

| Finding | Prior Verdict | Note |
|---------|---------------|------|
| KF1: AccessControlAttribute schema (Key + Value.Source structure and constraints) | CONFIRMED | No change |
| KF2: Source path syntax differs by identity source (${path:...} vs flat ${samaccountname}) | CONFIRMED | No change |
| KF3: 50-attribute cap, singleton resource, full-replace update semantics | CONFIRMED | No change |
| KF4: Create vs Update API split; ConflictException and ResourceNotFoundException behavior | PARTIALLY CONFIRMED | Framing issue only — exception type confirmed; AWS describes ConflictException as general write-conflict rather than explicitly "ABAC already enabled"; not a factual error for operational purposes |
| KF5: Only L1 CDK construct exists; deprecated nested property | CONFIRMED | No change |
| KF7: InstanceArn format and retrieval method | CONFIRMED | No change |
| KF8: Console path and SAML attribute visibility | CONFIRMED | No change |
| Sources (14 total) | 13 VERIFIED, 1 UNVERIFIABLE | UNVERIFIABLE: AWS Security Blog body (Source 12) not accessible via WebFetch; title and topic confirmed via search; the claim it supports is corroborated by other verified sources |

## Remediation Required

No remediation required.

## Overall Assessment

KF6 has been re-verified against live AWS documentation. The corrected text — stating that `SSMSessionRunAs` is the exact required key and that `ssm:RunAsDefaultRunAs` appears in informal AWS documentation but is not in the formal Service Authorization Reference condition key table — is fully confirmed. All other findings carry forward from the prior validation cycle unchanged. The investigation is complete, sync is clean, and no further remediation is needed.
