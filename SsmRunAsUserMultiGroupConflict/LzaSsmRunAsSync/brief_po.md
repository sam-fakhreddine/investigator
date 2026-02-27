# LZA SSM RunAs Synchronization Across Member Accounts — Product Brief

**Date:** 2026-02-27
**Risk Level:** HIGH

---

## What Is This?

> AWS servers (EC2 instances) in all team accounts need a consistent login-user setting that LZA does not apply automatically — a one-time engineering deployment is required to set and lock that configuration across all accounts.

---

## What Does This Mean for Us?

When engineers use AWS Session Manager (the AWS-native terminal access tool) to connect to servers, a setting in each AWS account determines which server user they connect as. That setting is not automatically synced by the Landing Zone Accelerator (LZA — the tool that manages all AWS accounts). Without a deliberate deployment, each account has its own independent copy of this setting that can be missing, incorrect, or changed by an account administrator — causing engineers to get access as the wrong user or be blocked entirely.

---

## Key Points

- LZA, the tool used to govern all AWS accounts, does not write the server-login-user setting (called RunAs) — it only manages session logging. This is a documented gap, not a bug.
- Each AWS member account has its own independent copy of this setting. There is no automatic sync mechanism — each account must be configured individually, either manually or via an automated deployment.
- The engineering fix is a CloudFormation StackSet (a multi-account automation tool built into AWS) that automatically configures this setting in every account, including accounts created in the future.
- Without a guardrail (called an SCP — a policy that blocks account admins from changing the setting), any account administrator could revert the configuration, causing a silent drift that only surfaces when an engineer tries to start a session.
- New AWS accounts created through LZA will have this setting deployed automatically once the StackSet is in place — no manual steps are needed per new account.

---

## Next Steps

**PO/EM Decision:**

> PO/EM to schedule a design session with the platform/infrastructure team to decide: (A) what OS username should be set as the default RunAs user in all accounts, and (B) whether different OUs or account types need different values. Once decided, assign the StackSet build and SCP deployment as tracked engineering work.

**Engineering Work Items:**
- Add a cloudFormationStackSets entry to customizations-config.yaml targeting Root OU with auto-deployment enabled, carrying a Lambda custom resource that writes the agreed runAsDefaultUser value to SSM-SessionManagerRunShell in each member account.
- Write and deploy an SCP to the Root OU (or relevant member-account OUs) that denies ssm:UpdateDocument, ssm:CreateDocument, and ssm:DeleteDocument on SSM-SessionManagerRunShell for all principals except the StackSet service role and LZA pipeline role.
- Validate the deployment in a non-production OU first: verify the Lambda runs successfully in a test member account, the correct runAsDefaultUser value is set, and an attempt to modify the document from within the account is denied by the SCP.
- Document the SCP exception list (which roles are permitted to modify the document) and add it to the platform runbook.
- Identify and validate the current RunAs state across all existing member accounts — accounts that were vended before this StackSet existed may have the default (unconfigured) document and should be remediated by the initial StackSet pipeline run.

**Leadership Input Required:**

> Architects and senior ICs must determine: (1) whether a single shared OS username is acceptable for all accounts (simpler) or per-OU parameterization is needed (more complex StackSet logic), and (2) whether the SCP exception list for the StackSet service role and LZA pipeline role is consistent with the organization's existing SCP strategy for protecting baseline settings.

---

## Open Questions

- Has the team confirmed which specific OS username should be set as the default RunAs user, and does that user exist on all managed EC2 instances across all accounts?
- Are there any existing member accounts where SSM-SessionManagerRunShell has already been manually configured, and would the StackSet deployment overwrite those values — or should those accounts be excluded?
- How long does it currently take for a new AWS account to go from creation to fully configured via the LZA pipeline — and during that window, can engineers successfully start Session Manager sessions, and as which user?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
