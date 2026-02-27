# LZA identityCenter Config Block — Declarative Surface, Limits, and ABAC Gap — Product Brief

**Date:** 2026-02-27
**Risk Level:** MEDIUM

---

## What Is This?

> AWS Landing Zone Accelerator (LZA) — the tool that manages our cloud account permissions — controls most access configuration, but there is one important gap: the setting that links user profile data (like an employee's Linux login name) to their AWS sessions is not controlled by LZA and has no version-controlled owner.

---

## What Does This Mean for Us?

LZA handles who can log into which AWS account and with what permissions. But the feature that passes a user's Linux username into each session — the piece that makes SSM server access work per-user — is configured separately in AWS and is not tracked by the LZA configuration files. If someone changes it by hand, there is no automated way to detect or reverse that change.

---

## Key Points

- LZA handles permission sets (what access someone gets) and assignments (who gets access to which accounts) — those are working and version-controlled.
- LZA does not handle ABAC (Attribute-Based Access Control), which is the setting that passes an engineer's Linux username into each server session for SSM access. This must be configured separately, and today it has no automated owner.
- If the ABAC setting is changed or deleted in the AWS console, LZA will not detect or restore it — it will simply be gone until someone manually fixes it.
- Permission changes (such as removing a policy from a permission set) take effect on new sessions only; an engineer already logged in continues to have the old permissions until their session expires, which can be up to 12 hours.
- Entra ID groups assigned to permission sets must already exist in AWS before LZA runs — LZA cannot create those groups. This is a dependency that SCIM (the sync tool from Entra ID to AWS) must satisfy first.

---

## Next Steps

**PO/EM Decision:**

> PO/EM to raise with the Identity/Platform team: does any IaC tool currently own the AWS Identity Center ABAC attribute configuration? If not, a work item is needed to bring it under version control (Terraform or CloudFormation) before it becomes a drift or incident risk.

**Engineering Work Items:**
- Audit the current IdC 'Attributes for Access Control' configuration in the AWS console and document which attributes are mapped and what values they reference.
- Determine which IaC tool (Terraform or CloudFormation) will own the aws_ssoadmin_instance_access_control_attributes or AWS::SSO::InstanceAccessControlAttributeConfiguration resource and create a tracked resource for it.
- Verify that all Entra ID groups referenced in identityCenterAssignments exist in the IdC identity store before relying on LZA to create those assignments.
- Review the OU hierarchy against identityCenterAssignments deploymentTargets to confirm that nested OUs whose accounts need assignments are explicitly listed.

**Leadership Input Required:**

> Architects must weigh in on which IaC tool takes ownership of the IdC ABAC configuration — LZA (CDK/CloudFormation) cannot be extended to do this without upstream contribution, so the choice is between a Terraform sidecar or a supplemental CloudFormation stack. That decision affects the operational model for the team managing the identity pipeline.

---

## Open Questions

- Is the ABAC attribute configuration in AWS Identity Center currently documented anywhere, and what would happen if it were accidentally changed or deleted?
- Have we verified that every Entra ID group referenced in our LZA assignment config is present in AWS Identity Center before the LZA pipeline runs?
- When we update a permission set in LZA (e.g., add or remove a policy), how long does it take before all engineers see the change — and is there a way to force active sessions to pick up the new permissions sooner?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
