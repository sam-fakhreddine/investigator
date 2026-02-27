# Glossary — IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema and Configuration Surface

Quick definitions of key terms and concepts referenced in this investigation.

---

## InstanceAccessControlAttributeConfiguration

The singleton IAM Identity Center resource that enables ABAC and holds the list of identity store attribute-to-session-tag mappings. One per IdC instance. Managed via CreateInstanceAccessControlAttributeConfiguration, UpdateInstanceAccessControlAttributeConfiguration, and DescribeInstanceAccessControlAttributeConfiguration APIs.

## AccessControlAttribute

A single attribute mapping entry within InstanceAccessControlAttributeConfiguration. Contains a Key (the principal tag name that appears on the STS session) and a Value.Source (a single-item array with an identity store path expression or literal source token).

## path expression ${path:...}

Source value syntax for referencing SCIM-synced identity store attributes in an external IdP scenario (e.g. Entra ID with SCIM provisioning). Examples: ${path:userName}, ${path:enterprise.department}. Standard attributes use direct field names; enterprise extension attributes use the enterprise.* prefix shorthand consistent with the SCIM enterprise schema.

## AD source expression ${samaccountname}

Source value syntax for AWS Managed Microsoft AD-connected IdC instances. Uses flat dollar-brace syntax with the lowercase AD attribute name. Distinct from the ${path:} format used with external SCIM-provisioned IdPs and not valid in the SCIM path context.

## SSMSessionRunAs

The exact AccessControlAttribute Key value required for SSM RunAs integration. SSM Session Manager reads the principal tag named SSMSessionRunAs on the STS session to determine the OS user for a RunAs session. The string ssm:RunAsDefaultRunAs appears in SSM documentation but its status as a formally listed IAM condition key in the AWS Service Authorization Reference has not been confirmed.

## aws:PrincipalTag/<Key>

The IAM condition key format produced when an ABAC attribute is emitted on an STS session by IdC. If AccessControlAttribute Key = 'SSMSessionRunAs', the condition key is aws:PrincipalTag/SSMSessionRunAs. Used in permission set inline policies to enforce attribute-based access rules.

## CfnInstanceAccessControlAttributeConfiguration

The CDK L1 construct in aws-cdk-lib/aws-sso for this resource. Uses camelCase property names: instanceArn and accessControlAttributes. No L2 construct exists. The deprecated instanceAccessControlAttributeConfiguration property is present for backwards compatibility only.

## ABAC singleton create/update split

The API design constraint where CreateInstanceAccessControlAttributeConfiguration can only be called once per IdC instance to enable ABAC, and all subsequent attribute list changes must use UpdateInstanceAccessControlAttributeConfiguration. Calling create on an already-enabled instance returns ConflictException.

---

*Back to: [investigation.md](investigation.md)*
