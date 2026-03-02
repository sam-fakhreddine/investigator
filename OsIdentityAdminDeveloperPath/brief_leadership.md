# OS Identity Admin Surface for Developer-Run AWS EC2 Access via SSMSessionRunAs — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> Developer teams can eliminate both Windows AD admin dependency and Linux sysadmin dependency for EC2 access, but only if two one-time architecture investments are made: SSSD domain join and cloud-native Entra group infrastructure.

---

## So What

Without these investments, every new developer getting EC2 access via SSMSessionRunAs requires a Windows AD admin to modify group membership and potentially a Linux admin to create an OS account. The two investments flip this to a developer-self-service model with no recurring admin involvement — but they require license and infrastructure commitments that engineering leadership must decide.

---

## Key Points

- On-prem AD groups (synced via Entra Connect) cannot be managed from the cloud by any tool — Graph API, Terraform, PIM, or self-service portals all fail for these groups. A Windows AD admin is the only path for synced groups.
- Cloud-native Entra security groups with group writeback are the prerequisite for developer self-service group management — via Terraform azuread IaC, Entra My Groups portal, PIM for Groups, or Entitlement Management access packages. Each requires different license tiers (P1 through ID Governance).
- SSSD domain join (investigated separately in SssdEntraLinuxEntitlements) is the only pattern that fully eliminates Linux OS user provisioning — the named domain user satisfies the SSMSessionRunAs check without any local account. AMI baking and cloud-init are partial solutions; Run Command requires an explicit trigger per fleet event.
- The combined architecture — SSSD domain join + cloud-native Entra groups managed by developers via Terraform or self-service — removes both admin dependencies after a one-time setup. The team must evaluate whether Entra ID P1 (minimum for self-service) or P2/ID Governance (for PIM or Entitlement Management) licenses are available or will be procured.
- Terraform azuread IaC is the most developer-natural pattern: group membership changes go through a PR, get reviewed, and apply via CI. This requires a service principal with Group Member role and a pipeline — no Entra admin portal involvement after initial setup.

---

## Action Required

> Decide on Entra license tier (P1 for self-service, P2/ID Governance for PIM or Entitlement Management) and whether SSSD domain join is the target for new EC2 Linux instances. Both decisions gate the self-service architecture.

---

*Full engineering investigation: [investigation.md](investigation.md)*
