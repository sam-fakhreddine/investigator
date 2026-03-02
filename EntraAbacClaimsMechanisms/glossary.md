# Glossary — Entra ID to IAM Identity Center ABAC Pipeline — Attribute Delivery, PrincipalTag Scope, and SSMSessionRunAs

Quick definitions of key terms and concepts referenced in this investigation.

---

## SAML Claims Path

Attributes delivered in the SAML 2.0 assertion emitted by the Entra enterprise app at user authentication. Configured in the Entra Attributes and Claims section using the namespace https://aws.amazon.com/SAML/Attributes/AccessControl. IAM Identity Center reads these at login and passes them to STS as session tags via AssumeRoleWithSAML. Not stored in the IdC identity store; not visible in the IdC console.

## SCIM / Identity Store Path

Attributes continuously provisioned from Entra to the IAM Identity Center identity store via SCIM v2.0. Mapped to ABAC session tag keys on the IAM Identity Center Attributes for Access Control console page. Limited to SCIM core and enterprise schema fields. When the same key is present in both SCIM and SAML, the identity store value takes precedence — unconditionally and silently.

## SCIM-Wins Precedence Rule

AWS-documented behavior in IAM Identity Center: when the same attribute key arrives through both SAML assertion and SCIM provisioning, the identity store (SCIM) value overrides the SAML assertion value for access control decisions. The precedence is not configurable and produces no console alert or log entry visible to operators.

## SSMSessionRunAs

A tag key recognized by SSM Agent. When the calling principal carries a tag with this key, SSM Agent uses the tag value as the OS username for the session instead of the default ssm-user account. For federated IAM Identity Center users, it must be delivered via the SAML claims path as AccessControl:SSMSessionRunAs. Cannot be delivered via SCIM. Resolved by SSM Agent outside IAM policy evaluation.

## aws:PrincipalTag

A global IAM condition context key that exposes the tags on the calling principal at request time. For federated sessions via IAM Identity Center, includes all STS session tags from AssumeRoleWithSAML. Used in IAM policy Condition blocks to allow or deny API actions. Operates at the IAM authorization layer — cannot set values, modify session parameters, or influence OS-level behavior.

## Attributes for Access Control

IAM Identity Center console feature that maps identity store attribute paths (e.g., ${path:enterprise.department}) to ABAC session tag keys. Attributes defined here override same-keyed SAML assertion values. Values are drawn exclusively from SCIM-provisioned identity store data.

## STS Session Tag

A key-value pair attached to a federated or assumed-role session at role assumption time. Passed by the IdP via SAML attribute statements under the AccessControl namespace. Accessible in IAM policy evaluation as aws:PrincipalTag/<key>. Valid only for the life of the session. SSMSessionRunAs travels as a session tag and is read directly by SSM Agent from the principal tag context.

## IAM Authorization Layer

The AWS evaluation engine that runs before any service API handler executes. Evaluates identity-based policies, resource-based policies, permission boundaries, and SCPs against the principal's session context including PrincipalTag values. aws:PrincipalTag conditions operate here — they produce Allow or Deny on API actions, not injected values in service behavior.

## SCIM Schema Extension

SCIM v2.0 mechanism for adding custom attributes beyond the core and enterprise schema. The AWS IAM Identity Center SCIM endpoint does not support schema extensions, returning HTTP 400 for any attempt to provision extension attributes. This is the structural reason SSMSessionRunAs cannot be delivered via SCIM.

## ssm:resourceTag Condition Key

An SSM-specific condition key that matches tags on the target managed node at the time of a StartSession call. Because aws:PrincipalTag is not listed as a supported condition key for ssm:StartSession, ABAC enforcement on StartSession must be expressed by matching the principal's session tag values against resource tags on the EC2 instance — requiring instance-side tagging to be maintained.

---

*Back to: [investigation.md](investigation.md)*
