# SSM RunAs Sync Pipeline — Entra ID, IAM Identity Center, and LZA — Product Brief

**Date:** 2026-02-27
**Risk Level:** HIGH

---

## What Is This?

> Engineers using AWS terminal access (SSM Session Manager) may be failing to connect or connecting as the wrong server user — fixing this requires coordinated changes across three systems: Entra ID (Azure AD), AWS Identity Center, and the AWS account configuration layer.

---

## What Does This Mean for Us?

When engineers access AWS servers through Session Manager, a chain of three settings must be correctly configured and in sync: (1) Entra ID must store and send each engineer's server login name as a per-user property — not derived from group membership; (2) AWS Identity Center must be configured to read that property and pass it into each session; (3) each AWS account must have a consistent fallback login-user setting. The Landing Zone Accelerator (LZA — the tool governing all AWS accounts) handles part of layer 2 but leaves confirmed gaps at both the attribute-mapping configuration and the per-account SSM settings. No single tool currently closes all three layers without deliberate engineering work.

---

## Key Points

- Engineers whose Entra ID groups each try to specify a different server login name will have their AWS sign-in hard-rejected by AWS Identity Center — they cannot open any Session Manager terminal until the Entra ID configuration is corrected.
- The per-user server login name must be stored directly on the user's Entra profile (like an employee ID), not derived from group membership. This requires an Entra ID admin change and a SCIM sync update.
- The AWS Identity Center setting that reads that attribute and passes it into each session (called ABAC attribute configuration) is not managed by LZA. If it was configured manually in the AWS console, there is no version history and no automated drift detection.
- Every AWS member account has its own independent copy of the server-access fallback setting. LZA does not write this setting — it must be deployed separately via a CloudFormation StackSet. Without it, new accounts have an unconfigured default.
- A policy guardrail (SCP) must be applied to prevent account administrators from changing or removing the per-account setting after it is deployed. Without this, the configuration will silently drift.
- New AWS accounts created through LZA will automatically receive the correct settings once the StackSet is in place — no manual steps are needed per new account after the one-time engineering deployment.

---

## Next Steps

**PO/EM Decision:**

> PO/EM to facilitate a cross-team coordination session with the Identity team (Entra ID / Azure AD owners), the Platform/IaC team (LZA config repo owners), and the Security team (SCP governance). Three work streams must be scoped and sequenced: (1) Entra ID attribute sourcing change, (2) AWS Identity Center ABAC configuration brought under version-controlled IaC, (3) CloudFormation StackSet deployment for per-account SSM settings with SCP guardrail. Escalate to Engineering Leadership if resource allocation across the three teams is unclear.

**Engineering Work Items:**
- Entra ID team: audit current group-to-attribute mappings for SSMSessionRunAs; determine whether sAMAccountName or a custom extension attribute is the correct per-user source; update the Entra enterprise application configuration and SCIM sync settings to propagate the chosen attribute to the AWS Identity Center identity store.
- Platform/IaC team: identify whether any IaC tool currently owns the AWS Identity Center ABAC attribute configuration (InstanceAccessControlAttributeConfiguration); if not, create a tracked IaC resource (Terraform or CloudFormation) and add it to the version-controlled config pipeline.
- Platform/IaC team: add a cloudFormationStackSets entry to customizations-config.yaml targeting Root OU with auto-deployment enabled, carrying a Lambda function that writes the agreed runAsDefaultUser value to SSM-SessionManagerRunShell in each member account.
- Security/Platform team: write and deploy an SCP to the Root OU denying ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument on SSM-SessionManagerRunShell for all principals except the StackSet service role and LZA pipeline role.
- Platform team: validate the full pipeline end-to-end in a non-production account — confirm a test user with correct Entra attribute gets the right OS username in a Session Manager session, and confirm the SCP blocks unauthorized modification of the SSM document.
- Platform team: audit existing member accounts for their current SSM-SessionManagerRunShell state; accounts vended before the StackSet existed may need remediation in the initial StackSet pipeline run.

**Leadership Input Required:**

> Architects and senior ICs must decide: (1) whether a single shared OS username is the correct default across all accounts (simpler) or whether different account types or OUs should have different default users (more complex StackSet parameterization); (2) which IaC tool takes ownership of the IdC ABAC attribute configuration — Terraform or CloudFormation — and how that integrates with the existing LZA config repo operational model; (3) whether the SCP exception list for the StackSet and LZA pipeline roles is consistent with the organization's existing SCP governance strategy.

---

## Open Questions

- Are there engineers today who are failing to start SSM sessions or connecting as the wrong server user — and have we confirmed that misconfigured Entra group attributes or missing SSM-SessionManagerRunShell settings are the cause?
- Does any IaC tool currently own the AWS Identity Center ABAC attribute configuration, or was it set manually in the console with no version history?
- Has the per-account SSM-SessionManagerRunShell document been audited across all member accounts — do we know which accounts have RunAs enabled, and with what username?
- If we change the Entra ID attribute source for SSMSessionRunAs, how quickly does that change propagate to active engineer sessions — and will engineers need to log out and back in to pick up the new attribute value?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
