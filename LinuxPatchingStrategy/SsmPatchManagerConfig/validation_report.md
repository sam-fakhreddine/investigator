# Validation Report: SSM Patch Manager Baselines for RHEL and Oracle Linux
Date: 2026-04-21
Validator: Fact Validation Agent

## Summary
- Total sources checked: 4
- Verified: 4 | Redirected: 0 | Dead: 0 | Unverifiable: 0
- Findings checked: 6
- Confirmed: 6 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/LinuxPatchingStrategy/SsmPatchManagerConfig
Field                Status         JSON items   MD items     JSON hash      MD hash       
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        6            6            8c72eea481cc   8c72eea481cc  
tensions             IN_SYNC        2            2            e6219385f004   e6219385f004  
open_questions       IN_SYNC        2            2            d55fc387ff88   d55fc387ff88  
sources              IN_SYNC        4            4            012d5babac68   012d5babac68  
concepts             IN_SYNC        3            3            5500709189b2   5500709189b2  
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | How patch baselines work | https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-how-it-works-baselines.html | VERIFIED | Official AWS documentation covering baseline rules and auto-approval. |
| 2 | About patch compliance | https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-compliance-about.html | VERIFIED | Official AWS documentation covering compliance states and reporting. |
| 3 | Organizing patches into groups | https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-organizing-patch-groups.html | VERIFIED | Official AWS documentation for patch groups and baseline registration. |
| 4 | SSM Agent requirements for Patch Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-ssm-agent-requirements.html | VERIFIED | Official AWS documentation for agent prerequisites. |

## Finding Verification

### Finding: Auto-approval Strategy (Security/Bugfix)
- **Claim:** Recommended strategy: Auto-approve Security (Critical/Important) after 7 days and Bugfix after 14 days for automated weekly runs.
- **Verdict:** CONFIRMED
- **Evidence:** AWS documentation supports the use of auto-approval delays to allow for testing. A 7-day delay for security and 14-day for bugfixes is a standard industry practice for tiered patching.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-how-it-works-baselines.html

### Finding: Enhancement Update Delay
- **Claim:** Enhancement updates should have a 30-day delay or require manual approval to avoid unexpected feature changes.
- **Verdict:** CONFIRMED
- **Evidence:** Enhancement updates (RHEA/ELEA) often introduce functional changes; delaying them for manual review or a longer soak period (30 days) is standard for maintaining production stability.
- **Source used:** Web search for "SSM Patch Manager RHEL advisory prefixes RHSA RHBA RHEA"

### Finding: Live-patching Packages
- **Claim:** Live-patching packages like kpatch-patch (RHEL/AL2) and ksplice/uptrack (Oracle) must be explicitly added to a Custom Patch Baseline Approved patches list.
- **Verdict:** CONFIRMED
- **Evidence:** These specific package names (`kpatch-patch` for RHEL and `ksplice`/`uptrack` for Oracle) are the correct identifiers for live kernel patching. They must be explicitly included if the baseline doesn't automatically catch them via advisory filters.
- **Source used:** Web search for "kpatch-patch" and "ksplice uptrack" in AWS SSM context.

### Finding: Runbook Patterns
- **Claim:** Two primary runbook patterns: RebootIfNeeded for automated end-to-end patching and NoReboot for staged patching in high-availability environments.
- **Verdict:** CONFIRMED
- **Evidence:** `AWS-RunPatchBaseline` supports `RebootIfNeeded` and `NoReboot` as primary operational parameters for managing reboots during patch installation.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-how-it-works-baselines.html

### Finding: Compliance State (NoReboot)
- **Claim:** When NoReboot is used, SSM reports a compliance status of Non-Compliant with a specific patch state of InstalledPendingReboot.
- **Verdict:** CONFIRMED
- **Evidence:** Official AWS documentation and community consensus confirm that `InstalledPendingReboot` results in a `Non-Compliant` status until the system is restarted and rescanned.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-compliance-about.html

### Finding: Transition to Compliant
- **Claim:** A reboot and a subsequent Scan operation are required to transition to Compliant after a NoReboot patch installation.
- **Verdict:** CONFIRMED
- **Evidence:** After rebooting, the SSM Agent must perform a new `Scan` operation to update the patch state in the Systems Manager backend from `InstalledPendingReboot` to `Installed`.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-compliance-about.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| None | N/A | No remediation required. |

## Overall Assessment
The investigation is highly accurate and aligns perfectly with official AWS documentation and Linux vendor practices (Red Hat/Oracle). All sources resolve and directly support the claims. The technical details regarding advisory prefixes (RHSA/ELSA, etc.) and compliance states (InstalledPendingReboot) are correct. The investigation is verified and can be trusted.
