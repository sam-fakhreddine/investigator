# Investigation: Entra ID to IAM Identity Center ABAC Pipeline — Attribute Delivery, PrincipalTag Scope, and SSMSessionRunAs

**Date:** 2026-03-02
**Status:** Complete

---

## Question

> In the Entra ID to IAM Identity Center ABAC pipeline, what are the documented mechanisms for delivering user attributes (SAML claims vs SCIM sync), how do they interact, what can aws:PrincipalTag condition keys control, and can any of these mechanisms influence SSMSessionRunAs OS-level session identity?

---

## Context

Organizations federate Microsoft Entra ID to AWS IAM Identity Center via SAML and SCIM. Two distinct pipelines deliver user attributes into the ABAC system: SAML claims emitted at authentication time and SCIM provisioning that continuously populates the IdC identity store. Once attributes reach STS as session tags, permission set IAM policies can reference them via aws:PrincipalTag condition keys. Separately, SSM Session Manager uses the SSMSessionRunAs tag to determine the OS-level username for sessions on managed Linux nodes. Understanding which attribute path controls what — and which path SSMSessionRunAs must exclusively use — is critical to reliable per-user OS identity mapping in federated environments.

---

## Entra ID ABAC Pipeline — Mechanism Comparison

| Mechanism | Layer | Carries Custom Attrs? | Carries SSMSessionRunAs? | Wins on Key Conflict? |
| --- | --- | --- | --- | --- |
| SAML Claims (Entra enterprise app) | STS session tags at login | Yes — any Entra user property | Yes — only viable path | No — SCIM overrides |
| SCIM + Identity Store (IdC console mapping) | STS session tags via identity store | No — core/enterprise schema only; extensions rejected with HTTP 400 | No — not a SCIM-defined attribute | Yes — always wins over SAML on same key |
| aws:PrincipalTag in IAM policy Condition | IAM authorization (Allow/Deny) | N/A — reads existing tags | No — cannot set or influence OS user | N/A — evaluates, does not produce tags |
| SSMSessionRunAs as STS session tag | SSM Agent tag read (outside IAM evaluation) | N/A — one specific key | Yes — primary per-user mechanism | N/A — SSM reads directly from principal context |

> SSMSessionRunAs must be delivered exclusively via the SAML claims path (AccessControl:SSMSessionRunAs attribute in Entra). SCIM cannot carry it. aws:PrincipalTag conditions gate StartSession API access but do not influence which OS user SSM uses — that is resolved by SSM Agent reading the tag context directly, outside IAM policy evaluation.

---

## Key Findings

- SAML claims and SCIM provisioning are parallel, independent attribute delivery pipelines into IAM Identity Center ABAC. SAML emits attribute values at each login via the Entra enterprise app; SCIM continuously populates the IdC identity store in the background. Both can contribute to the STS session tags that appear as aws:PrincipalTag in IAM policy evaluation.
- When the same attribute key is present in both pipelines, SCIM/identity store values win unconditionally. AWS documents this explicitly: 'In scenarios where the same attributes are coming to IAM Identity Center through SAML and SCIM, the SCIM attributes value take precedence in access control decisions.' This override is silent — no alert, no console indicator — and is not configurable.
- SCIM's schema is structurally limited to SCIM core and enterprise schema fields. The AWS IAM Identity Center SCIM endpoint rejects schema extension attributes — confirmed via an AWS engineering contact cited in a community thread; the specific HTTP 400 response code is community-sourced only and not documented in AWS primary documentation. Arbitrary custom attributes, including SSMSessionRunAs, cannot be delivered via SCIM regardless of how the Entra provisioning connector is configured.
- SSMSessionRunAs must travel exclusively via the SAML claims path. It is configured in the Entra enterprise app Attributes and Claims section as the attribute https://aws.amazon.com/SAML/Attributes/AccessControl:SSMSessionRunAs. At login, IdC passes it to STS as a session tag; SSM Agent reads PrincipalTag:SSMSessionRunAs from the principal's tag context to determine the OS username for the session.
- aws:PrincipalTag condition keys in permission set IAM policies operate at the IAM authorization layer — they allow or deny AWS API calls (such as ssm:StartSession) based on whether session tag values match specified criteria. They do not inject data into service-level behavior and cannot set or modify the OS user for a session.
- SSMSessionRunAs resolution by SSM Agent is a direct tag read that occurs outside IAM policy evaluation. The resolution order is: (1) the calling principal's tag SSMSessionRunAs wins if present; (2) account-level Session Manager Preferences apply as fallback; (3) if neither is set and Run As is enabled, the session fails — there is no ssm-user fallback once Run As is activated.
- The SCIM-wins-over-SAML precedence rule creates a structurally asymmetric system: SAML has broader attribute coverage but loses on any key that SCIM also carries. Operators who configure the same attribute key in both paths without awareness of this rule will find SAML values silently suppressed, including for attributes they intended to control via SAML.
- IAM Identity Center is documented in AWS blog posts as automatically managing sts:TagSession permission in provisioned role trust policies, enabling SAML session tags (including SSMSessionRunAs) to pass through without manual trust policy changes; primary AWS documentation pages do not explicitly confirm this automatic management. SAML-delivered attributes are not visible in the IdC console — operators must know the configured Entra attribute names to audit them.
- The ssm:StartSession action does not list aws:PrincipalTag as a supported condition key in the Service Authorization Reference. ABAC enforcement on StartSession must be routed through ssm:resourceTag conditions on the target managed node, which requires instance-side tagging to align with principal session tag values.
- Multi-valued session tags are not supported by STS. A user who needs to operate as different OS usernames on different instances cannot express this in a single SSMSessionRunAs tag — multiple role assumptions or a broker are the only architectural paths to multi-value OS identity mapping.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SAML Claims Path | Attributes delivered in the SAML 2.0 assertion emitted by the Entra enterprise app at user authentication. Configured in the Entra Attributes and Claims section using the namespace https://aws.amazon.com/SAML/Attributes/AccessControl. IAM Identity Center reads these at login and passes them to STS as session tags via AssumeRoleWithSAML. Not stored in the IdC identity store; not visible in the IdC console. |
| SCIM / Identity Store Path | Attributes continuously provisioned from Entra to the IAM Identity Center identity store via SCIM v2.0. Mapped to ABAC session tag keys on the IAM Identity Center Attributes for Access Control console page. Limited to SCIM core and enterprise schema fields. When the same key is present in both SCIM and SAML, the identity store value takes precedence — unconditionally and silently. |
| SCIM-Wins Precedence Rule | AWS-documented behavior in IAM Identity Center: when the same attribute key arrives through both SAML assertion and SCIM provisioning, the identity store (SCIM) value overrides the SAML assertion value for access control decisions. The precedence is not configurable and produces no console alert or log entry visible to operators. |
| SSMSessionRunAs | A tag key recognized by SSM Agent. When the calling principal carries a tag with this key, SSM Agent uses the tag value as the OS username for the session instead of the default ssm-user account. For federated IAM Identity Center users, it must be delivered via the SAML claims path as AccessControl:SSMSessionRunAs. Cannot be delivered via SCIM. Resolved by SSM Agent outside IAM policy evaluation. |
| aws:PrincipalTag | A global IAM condition context key that exposes the tags on the calling principal at request time. For federated sessions via IAM Identity Center, includes all STS session tags from AssumeRoleWithSAML. Used in IAM policy Condition blocks to allow or deny API actions. Operates at the IAM authorization layer — cannot set values, modify session parameters, or influence OS-level behavior. |
| Attributes for Access Control | IAM Identity Center console feature that maps identity store attribute paths (e.g., ${path:enterprise.department}) to ABAC session tag keys. Attributes defined here override same-keyed SAML assertion values. Values are drawn exclusively from SCIM-provisioned identity store data. |
| STS Session Tag | A key-value pair attached to a federated or assumed-role session at role assumption time. Passed by the IdP via SAML attribute statements under the AccessControl namespace. Accessible in IAM policy evaluation as aws:PrincipalTag/<key>. Valid only for the life of the session. SSMSessionRunAs travels as a session tag and is read directly by SSM Agent from the principal tag context. |
| IAM Authorization Layer | The AWS evaluation engine that runs before any service API handler executes. Evaluates identity-based policies, resource-based policies, permission boundaries, and SCPs against the principal's session context including PrincipalTag values. aws:PrincipalTag conditions operate here — they produce Allow or Deny on API actions, not injected values in service behavior. |
| SCIM Schema Extension | SCIM v2.0 mechanism for adding custom attributes beyond the core and enterprise schema. The AWS IAM Identity Center SCIM endpoint does not support schema extensions, returning HTTP 400 for any attempt to provision extension attributes. This is the structural reason SSMSessionRunAs cannot be delivered via SCIM. |
| ssm:resourceTag Condition Key | An SSM-specific condition key that matches tags on the target managed node at the time of a StartSession call. Because aws:PrincipalTag is not listed as a supported condition key for ssm:StartSession, ABAC enforcement on StartSession must be expressed by matching the principal's session tag values against resource tags on the EC2 instance — requiring instance-side tagging to be maintained. |

---

## Tensions & Tradeoffs

- SCIM has unconditional precedence over SAML on shared keys, yet SCIM has narrower attribute coverage. The path with broader expressiveness (SAML) loses to the path with structural constraints (SCIM) on any key they share. This asymmetry is not surfaced in the IdC console and creates silent suppression of SAML-intended values.
- SAML is the only delivery path for custom and non-standard attributes like SSMSessionRunAs, yet SAML-delivered attributes are invisible in the IdC console. Operators cannot inspect, audit, or confirm SAML attribute values from the AWS side — troubleshooting requires knowledge of what was configured in the Entra enterprise app.
- SCIM sync lag means the winning (SCIM) value may be stale relative to what Entra would emit in a fresh SAML assertion. An attribute change in Entra takes effect immediately in SAML but only after the next SCIM sync cycle in the identity store — yet the potentially stale SCIM value overrides the current SAML value.
- aws:PrincipalTag in IAM policy Conditions and SSMSessionRunAs as a tag read by SSM Agent share the same STS session tag infrastructure but operate at entirely different layers. They appear interchangeable to operators not familiar with the distinction — one gates API calls, the other selects an OS user — and cannot substitute for each other.
- The absence of aws:PrincipalTag as a supported condition key for ssm:StartSession forces ABAC enforcement on session access to depend on EC2 instance resource tags. This adds an operational tagging requirement on the managed-node side that must be maintained in sync with the ABAC attribute scheme — a second configuration surface with its own drift risk.
- Per-user OS identity via SSMSessionRunAs requires Linux usernames to be pre-provisioned on every managed instance the user may access. The tag flow from Entra to SSM Agent is well-defined, but the prerequisite OS-level account provisioning at scale is outside the scope of the IAM/IdC configuration and requires a separate operational pipeline.

---

## Open Questions

- Whether the SCIM-wins-over-SAML precedence rule applies only when an IdC Attributes for Access Control mapping exists for the key, or also when an attribute arrives purely via SAML with no console configuration, is not explicitly clarified in the official documentation.
- When an Attributes for Access Control mapping references an identity store field that has no provisioned value for a given user, whether the system falls back to the SAML assertion value or emits no session tag for that key is not documented.
- Whether AWS plans to support SCIM schema extensions in the IAM Identity Center SCIM endpoint is not on any confirmed public roadmap. Community reports cite an AWS engineering contact confirming absence of extension support as of 2023.
- When Entra ID passes SSMSessionRunAs via a direct SAML assertion without a corresponding Attributes for Access Control mapping in the IdC console, whether IAM Identity Center forwards it faithfully as a session tag or strips it is not definitively documented in the primary user guide — blog posts confirm the flow but the official page does not.
- The interaction between a SAML-delivered SSMSessionRunAs tag and an account-level Session Manager Preferences default OS user setting when both are present is only partially documented — the primary lookup order is described in the user guide but the exact fallback behavior at each step in the absence of a tag value is not fully specified.
- IAM Identity Center automatically includes sts:TagSession in provisioned role trust policies for standard ABAC attribute mappings; whether this automatic permission covers all SAML session tags or only those mapped through the Attributes for Access Control console page is not explicitly stated.
- Multi-valued OS user assignments — a user needing different OS identities on different instances — are not expressible in a single STS session tag. Whether a future STS update could support multi-valued session tags, or whether a Lambda broker remains the only path, is an open architectural constraint.

---

## Sources & References

- [Attributes for access control - AWS IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html)
- [Enable and configure attributes for access control - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html)
- [Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html)
- [Provision users and groups from an external identity provider using SCIM - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html)
- [SCIM profile and SAML 2.0 implementation - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/scim-profile-saml.html)
- [Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Pass session tags in AWS STS - AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html)
- [AWS global condition context keys — aws:PrincipalTag](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
- [Create permission policies for ABAC in IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html)
- [Actions, resources, and condition keys for AWS Systems Manager - Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html)
- [Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [Configuring AWS Systems Manager Session Manager run as support for federated users using session tags](https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/)
- [Use custom attributes for ABAC with Microsoft Entra ID and AWS IAM Identity Center](https://aws.amazon.com/blogs/modernizing-with-aws/use-custom-attributes-for-attribute-based-access-control-abac-with-microsoft-entra-id-and-aws-iam-identity-center/)
- [Azure AD provisioning to AWS Identity Center with custom user/group attributes - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1324325/azure-ad-provisioning-to-aws-identity-center-with)
