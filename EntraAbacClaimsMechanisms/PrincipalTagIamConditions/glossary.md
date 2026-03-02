# Glossary — aws:PrincipalTag Condition Keys — Scope, Capabilities, and SSMSessionRunAs Influence

Quick definitions of key terms and concepts referenced in this investigation.

---

## aws:PrincipalTag

A global IAM condition context key that exposes the tags on the calling principal (IAM user, IAM role, or federated session) at request time. For federated sessions via IAM Identity Center, this includes all STS session tags passed during AssumeRoleWithSAML. Used in Condition blocks of IAM policies to allow or deny API actions.

## STS Session Tag

A key-value pair attached to a federated or assumed-role session at the time of role assumption. Passed by the IdP via SAML attribute statements using the namespace https://aws.amazon.com/SAML/Attributes/PrincipalTag:{key}. Valid only for the life of the session and not written back to the IAM role resource itself.

## SSMSessionRunAs

A special tag key recognized by SSM Agent. When the calling principal carries a tag with this key, SSM Agent uses the tag value as the OS username for the session instead of the default ssm-user account. Can be set as a permanent IAM resource tag on a role or as a per-session STS session tag from an IdP.

## IAM Identity Center ABAC

A feature of IAM Identity Center (formerly AWS SSO) that allows user attributes from the connected identity store (including Entra ID via SAML) to be passed as STS session tags on sign-in. Enabled via the Attributes for access control page; the attribute key-value pairs then appear as aws:PrincipalTag/<key> in IAM policy evaluation.

## Permission Set

An IAM Identity Center construct that bundles AWS managed policies and inline IAM policies into a role that IAM Identity Center provisions in each assigned AWS account. Inline policies in permission sets can reference aws:PrincipalTag to build ABAC rules without referencing specific user identities.

## Session Manager Run As

A Session Manager feature that replaces the default ssm-user OS account with a specified OS username for session execution. Configured either via account-level Session Manager Preferences or per-principal via the SSMSessionRunAs tag. Applies only to Linux and macOS managed nodes; root is not supported.

## IAM Authorization Layer

The AWS evaluation engine that runs before any service API handler executes. It evaluates identity-based policies, resource-based policies, permission boundaries, and SCPs. aws:PrincipalTag conditions are evaluated at this layer — they can only produce Allow or Deny, not inject values into service-level behavior.

## ssm:resourceTag condition key

An SSM-specific condition key that matches tags on the target SSM resource (e.g., an EC2 instance or managed node) at the time of a StartSession call. Used in combination with aws:PrincipalTag to implement ABAC-style gating on which instances a federated user can start a session against.

---

*Back to: [investigation.md](investigation.md)*
