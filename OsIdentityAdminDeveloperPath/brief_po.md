# OS Identity Admin Surface for Developer-Run AWS EC2 Access via SSMSessionRunAs — Product Brief

**Date:** 2026-03-02
**Risk Level:** MEDIUM

---

## What Is This?

> Every new developer getting access to EC2 instances currently touches two admin queues — a Windows AD admin for group membership and possibly a Linux admin for OS accounts. There is a documented architecture that eliminates both, but it requires license investment and one-time infrastructure work.

---

## What Does This Mean for Us?

Right now, developers who need EC2 access via Session Manager depend on a Windows AD admin to manage their group membership (which controls AWS permission set assignment) and potentially a Linux sysadmin to create OS user accounts on the instances. This creates access latency and admin bottlenecks that slow the team. The investigation identifies a path that removes both dependencies — but it is not zero-cost to set up.

---

## Key Points

- The root cause of the Windows AD admin dependency: on-prem Active Directory groups cannot be managed from the cloud by developers using any tool. Only a Windows AD admin with on-prem access can add or remove members from these groups.
- The cloud-side solution: create new cloud-native Entra security groups (not synced from AD), enable group writeback so they appear in AD, and let developers manage membership via Terraform pull requests or the Entra self-service portal. This requires Entra ID P1 license minimum.
- The Linux OS account dependency is eliminated entirely when EC2 instances are SSSD domain-joined — the developer's AD user account satisfies the Session Manager check without any local account creation. Without SSSD, Architects or Infra engineers must provision OS accounts (via AMI rebuild, cloud-init, or Run Command) whenever the user set changes.
- The self-service path for group membership (Entra My Groups portal) requires Entra ID P1. Just-in-time group access with approval and time limits (PIM for Groups) requires Entra ID P2. Automated access lifecycle with workflows (Entitlement Management) requires Entra ID Governance. These are different license tiers with different costs.
- The Terraform IaC path (azuread_group_member resource in a PR pipeline) requires no extra license beyond the developer toolchain and a service principal — it is the most cost-effective self-service option for teams already using Terraform.

---

## Next Steps

**PO/EM Decision:**

> PO/EM should determine current Entra ID license tier and whether SSSD domain join is planned for EC2 instances, then bring those two data points to Architects for architecture decision.

**Engineering Work Items:**
- Architects: assess whether existing developer AD accounts are on-prem-synced (a requirement for group writeback membership) or cloud-only, and determine Entra license tier in the tenant
- Architects: design the cloud-native Entra group + group writeback configuration to replace or supplement on-prem AD groups used for IdC permission set assignment
- Infra/platform team: evaluate SSSD domain join for new EC2 Linux instances as the mechanism to eliminate OS user provisioning (see SssdEntraLinuxEntitlements investigation for mechanics)
- Infra/platform team: build the Terraform azuread_group_member pipeline (service principal, azuread provider configuration, group membership resources in version control) as the developer-managed group membership path
- Windows/AD admin: perform the one-time group writeback configuration in Entra Cloud Sync provisioning agent — this is the prerequisite for cloud-side group management

**Leadership Input Required:**

> Leadership needs to approve the Entra license tier needed for self-service (at minimum P1; P2 if PIM for Groups is desired for just-in-time access). This is the gating decision for the self-service architecture.

---

## Open Questions

- Are developer Entra accounts on-prem-synced from AD or cloud-only? (If cloud-only, group writeback membership constraints require a different solution path.)
- What Entra ID license is currently in the tenant — Free, P1, P2, or ID Governance?
- Is SSSD domain join on the roadmap for EC2 Linux instances, or are instances running without domain membership today?
- Is there an existing Terraform pipeline for AWS infrastructure that could be extended to manage Entra group membership, or would that be a new pipeline?
- Who currently owns the Windows AD admin function — is there a team or individual whose involvement can be scoped to the one-time group writeback setup?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
