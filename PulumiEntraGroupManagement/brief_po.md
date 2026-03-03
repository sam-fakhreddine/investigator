# Pulumi @pulumi/azuread for Entra Group Management in IAM Identity Center Hybrid Environments — Product Brief

**Date:** 2026-03-02
**Risk Level:** LOW

---

## What Is This?

> Developers can manage AWS access by editing TypeScript files in a PR — no Windows AD admin involvement for cloud-native or SOA-converted groups.

---

## What Does This Mean for Us?

The Pulumi toolchain enables the developer-managed PR workflow the team wants. Pulumi @pulumi/azuread handles Entra group membership; @pulumi/aws handles the AWS side. Both live in one TypeScript program. A PR triggers a preview showing exactly what access will change; merge triggers the actual change. This replaces the current Terraform HCL workflow with TypeScript and gains cross-cloud atomicity.

---

## Key Points

- Developers write TypeScript, open a PR, see an access-change preview in the PR comment, and merge to apply — no Windows admin required for cloud-native or converted groups
- The same tool and the same PR handle both the Entra group change and the AWS permission assignment — no separate processes or ticketing
- On-prem-synced groups remain write-blocked by Microsoft; this is unchanged whether the team uses Terraform or Pulumi — only cloud-native or SOA-converted groups are developer-manageable
- SOA conversion is a one-time, admin-executed step per group; after conversion, developers own the group via IaC
- Pulumi Cloud provides an audit log of who ran each deployment and what changed, relevant for compliance

---

## Next Steps

**PO/EM Decision:**

> Confirm with Architects and Windows/infra team which existing synced groups need SOA conversion and who will perform the one-time admin conversion step before developer IaC ownership begins.

**Engineering Work Items:**
- Architects: design the Pulumi stack structure (separate stacks per environment vs. one stack with per-env configs) and select the state backend (Pulumi Cloud vs S3)
- Developers: prototype a single TypeScript stack managing one cloud-native Entra group and one aws.ssoadmin.AccountAssignment to validate the cross-provider output reference pattern
- Windows/infra team: perform SOA conversion for any existing synced groups the developers need to take ownership of, and grant Group-OnPremisesSyncBehavior.ReadWrite.All to the service principal used for the one-time conversion

**Leadership Input Required:**

> Approval needed on Pulumi Cloud vs DIY state backend — Pulumi Cloud has a per-user cost and involves Pulumi SaaS; DIY S3 requires engineering effort to manage state safety for concurrent pipelines.

---

## Open Questions

- Which groups are currently synced from on-prem and which are already cloud-native? How many SOA conversions are needed?
- Does the team's compliance posture require state and audit logs to stay within the company's own cloud accounts, or is Pulumi Cloud acceptable?
- How is the Identity Store group GUID resolved for groups federated from Entra — is there an existing lookup mechanism or does the stack need to perform a live aws.identitystore.getGroup call on each run?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
