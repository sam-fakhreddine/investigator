# SSM RunAs Sync Pipeline — Entra ID, IAM Identity Center, and LZA — Engineering Leadership Brief

**Date:** 2026-02-27

---

## Headline

> The SSMSessionRunAs pipeline spans three layers — Entra ID, IAM Identity Center ABAC, and per-account SSM preferences — and LZA owns only the middle layer partially; the ABAC configuration and RunAs enforcement both require tooling outside LZA's scope.

---

## So What

Engineers hitting SSM session failures or incorrect OS username assignment are encountering a multi-layer configuration gap. The root cause (group-derived SSMSessionRunAs) causes hard sign-in rejections from IAM Identity Center. The fix requires three coordinated changes: (1) move SSMSessionRunAs to a per-user Entra attribute synced via SCIM, (2) configure IdC ABAC attribute mapping outside LZA (confirmed LZA gap), and (3) deploy a CloudFormation StackSet via LZA customizations to enforce runAsDefaultUser in every member account with an SCP guardrail. No single tool handles all three layers — this is a deliberate cross-team configuration problem.

---

## Key Points

- Group-derived SSMSessionRunAs causes hard sign-in rejection by IdC ABAC — not silent misbehavior — when a user belongs to more than one qualifying group. The fix is architectural: move to a per-user Entra extension attribute or sAMAccountName synced via SCIM.
- AWSReservedSSO_ roles cannot be tagged by customers. The only path to pass SSMSessionRunAs for IdC-federated users is via SAML assertion or ABAC user-profile attribute — a static role tag is not possible.
- LZA has no configuration surface for IdC ABAC attribute mapping (InstanceAccessControlAttributeConfiguration). This is a confirmed gap across all LZA versions. A supplemental IaC resource (Terraform aws_ssoadmin_instance_access_control_attributes or CloudFormation AWS::SSO::InstanceAccessControlAttributeConfiguration) must own this or it exists only in the IdC console with no version history or drift detection.
- LZA explicitly preserves but never writes runAsEnabled or runAsDefaultUser values. A service-managed CloudFormation StackSet in customizations-config.yaml (Root OU, auto-deployment on) with a Lambda custom resource is the correct LZA-native enforcement path. An SCP denying ssm:UpdateDocument on SSM-SessionManagerRunShell is required to prevent post-deployment drift.
- OU-scoped LZA assignments cover direct child accounts only — nested OUs are silently excluded (GitHub #220). Management account assignment failures have occurred in v1.7.0+ (GitHub #215, #496). Both gaps require explicit verification against the deployed LZA version and account hierarchy.
- Active IAM role sessions are not invalidated by permission set updates — in-flight credentials remain valid until session duration expires, up to 12 hours.

---

## Action Required

> Engineering leadership must authorize and sequence three work streams: (1) Identity/Entra team to move SSMSessionRunAs sourcing to a per-user attribute in Entra ID and configure SCIM sync to propagate it to the IAM Identity Center identity store; (2) Platform/IaC team to bring IdC ABAC attribute configuration (InstanceAccessControlAttributeConfiguration) under version-controlled IaC — either Terraform or a supplemental CloudFormation stack — separate from the LZA config repo; (3) Platform team to design, test, and deploy a cloudFormationStackSets entry in customizations-config.yaml that enforces runAsDefaultUser org-wide with auto-deployment, paired with an SCP guardrail on the Root OU. Architects must decide whether runAsDefaultUser is uniform across all accounts or parameterized per-OU before work stream 3 can be scoped.

---

*Full engineering investigation: [investigation.md](investigation.md)*
