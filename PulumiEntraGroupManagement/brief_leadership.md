# Pulumi @pulumi/azuread for Entra Group Management in IAM Identity Center Hybrid Environments — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> Pulumi @pulumi/azuread is a viable TypeScript-native replacement for Terraform azuread with near-identical capabilities for this use case, plus native multi-cloud stack support.

---

## So What

The team can replace Terraform HCL with Pulumi TypeScript and gain the ability to manage both Entra group membership and AWS IAM Identity Center assignments in a single program, with pulumi preview as the PR gate. The write-block on on-prem-synced groups is a Microsoft Graph API constraint that affects both tools equally; cloud-native groups or SOA-converted groups bypass this constraint. A 4-8 week version lag exists between the upstream Terraform provider and the Pulumi bridge release.

---

## Key Points

- azuread.Group and azuread.GroupMember cover cloud-native group management with full parity to Terraform's azuread_group and azuread_group_member for this use case
- A single Pulumi TypeScript stack can manage both the Entra group (via @pulumi/azuread) and the IAM Identity Center assignment (via @pulumi/aws ssoadmin) atomically — no separate Terraform stacks or cross-tool coordination needed
- pulumi preview posts to PR as a comment via the pulumi/actions GitHub Action, providing the same developer visibility as terraform plan
- SOA conversion (converting a synced group to cloud-managed) requires a one-time admin operation outside IaC; after conversion, Pulumi manages the group identically to a cloud-native group
- Pulumi Cloud backend is recommended over DIY S3/Azure Blob for teams running concurrent CI pipelines due to transactional state locking and team RBAC
- The 4-8 week lag between upstream terraform-provider-azuread releases and @pulumi/azuread releases is relevant only if new Graph API features are needed immediately

---

## Action Required

> Decide on state backend: Pulumi Cloud (managed, transactional) vs DIY S3 (data sovereignty, no transactional locking). This decision affects concurrent pipeline safety and compliance audit trail requirements.

---

*Full engineering investigation: [investigation.md](investigation.md)*
