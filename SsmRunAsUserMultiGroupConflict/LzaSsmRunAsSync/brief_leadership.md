# LZA SSM RunAs Synchronization Across Member Accounts — Engineering Leadership Brief

**Date:** 2026-02-27

---

## Headline

> LZA has no native config surface for SSM RunAs enforcement — the correct path is a CloudFormation StackSet deployed via the customizations layer, protected by an SCP guardrail.

---

## So What

Without deliberate action, each member account's Session Manager RunAs setting is uncontrolled: LZA sets logging preferences but explicitly does not write RunAs values, and any engineer with sufficient IAM permissions in a member account can change or remove the setting. A StackSet carrying a Lambda that writes the runAsDefaultUser value to every account — combined with an SCP that blocks subsequent modification — is the durable enforcement pattern. New accounts are covered automatically via StackSet auto-deployment, eliminating the dependency on a pipeline run.

---

## Key Points

- LZA's global-config sessionManager block configures only logging destinations — it has zero surface for runAsEnabled or runAsDefaultUser; these fields must be managed outside LZA's standard config.
- LZA's ssmAutomation sharing mechanism cannot solve this: it shares a document reference, not a local copy, and SSM-SessionManagerRunShell must exist as a locally-owned document in each member account.
- LZA explicitly preserves existing runAsEnabled and runAsDefaultUser values when it updates the preferences document — this prevents pipeline regression but also means LZA can never be the enforcement agent for RunAs values.
- A service-managed CloudFormation StackSet (Root OU, auto-deployment on) carrying a Lambda custom resource is the LZA-native delivery mechanism; it is deployed in the CUSTOMIZATIONS pipeline stage and auto-deploys to new accounts via Organizations lifecycle events.
- An SCP denying ssm:UpdateDocument on SSM-SessionManagerRunShell to non-pipeline roles is required to prevent drift after the StackSet writes the value — without it, any account admin can undo the configuration.

---

## Action Required

> Engineering leadership must authorize two work items: (1) design and deploy a cloudFormationStackSets entry in customizations-config.yaml that delivers a Lambda-backed custom resource writing the desired runAsDefaultUser value to every member account, with auto-deployment enabled; and (2) add an SCP to the Root OU or relevant member OUs that denies ssm:UpdateDocument and related actions on SSM-SessionManagerRunShell for all principals except the StackSet service role and LZA pipeline role. Architects must decide the target OS username value and whether it should be uniform across all accounts or parameterized per-OU.

---

*Full engineering investigation: [investigation.md](investigation.md)*
