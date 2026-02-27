# Glossary — IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema, Configuration Surface, Drift, and Idempotency

Quick definitions of key terms and concepts referenced in this investigation.

---

## InstanceAccessControlAttributeConfiguration

The singleton IAM Identity Center resource (CloudFormation type AWS::SSO::InstanceAccessControlAttributeConfiguration) that enables ABAC and holds the list of identity store attribute-to-session-tag mappings. Exactly one exists per IdC instance. Managed via Create, Update, Delete, and Describe sso-admin API operations.

## AccessControlAttribute

A single attribute mapping entry within InstanceAccessControlAttributeConfiguration. Contains a Key (the principal tag name that appears on the STS session) and a Value.Source (a single-item array with an identity store path expression or literal source token). The full array is replaced on every update — no partial-update API exists.

## path expression ${path:...}

Source value syntax for referencing SCIM-synced identity store attributes in an external IdP scenario (e.g. Entra ID with SCIM provisioning). Examples: ${path:userName}, ${path:enterprise.department}. Standard attributes use direct field names; enterprise extension attributes use the enterprise.* prefix.

## AD source expression ${samaccountname}

Source value syntax for AWS Managed Microsoft AD-connected IdC instances. Uses flat dollar-brace syntax with the lowercase AD attribute name. Distinct from the ${path:} format used with external SCIM-provisioned IdPs and not valid in the SCIM path context.

## SSMSessionRunAs

The exact AccessControlAttribute Key value required for SSM RunAs integration. SSM Session Manager reads the principal tag named SSMSessionRunAs on the STS session to determine the OS user for a RunAs session. Casing is significant. The string ssm:RunAsDefaultRunAs appears in SSM documentation but its status as a formally listed IAM condition key in the AWS Service Authorization Reference has not been confirmed.

## aws:PrincipalTag/<Key>

The IAM condition key format produced when an ABAC attribute is emitted on an STS session by IdC. If AccessControlAttribute Key = 'SSMSessionRunAs', the condition key is aws:PrincipalTag/SSMSessionRunAs. ABAC-dependent permission set policies that reference this key stop matching immediately when ABAC is deleted.

## ABAC singleton create/update split

The API design constraint where CreateInstanceAccessControlAttributeConfiguration enables ABAC once per IdC instance, and all subsequent attribute list changes must use UpdateInstanceAccessControlAttributeConfiguration. CloudFormation abstracts this split, but the distinction surfaces as a ConflictException if the resource already exists when the stack is first deployed.

## DeleteInstanceAccessControlAttributeConfiguration

The sso-admin API call that fully disables ABAC and removes all attribute mappings for an IdC instance. Called by the CloudFormation delete handler when the resource is removed from a stack or the stack is deleted. Immediately stops attribute propagation — ABAC-dependent policies become non-matching with no grace period.

## DescribeInstanceAccessControlAttributeConfiguration

The sso-admin read-side API that returns the current ABAC status (ENABLED, CREATION_IN_PROGRESS, or CREATION_FAILED) and the configured attribute list for an IdC instance. Used by the CloudFormation resource provider to assess current state. Believed to return ResourceNotFoundException for instances with no ABAC configuration, though this is not explicitly documented.

## NOT_CHECKED drift status

The CloudFormation drift status assigned to resource types that do not support drift detection. AWS::SSO::InstanceAccessControlAttributeConfiguration receives this status permanently. Changes made outside of CloudFormation are invisible to IaC tooling.

## DeletionPolicy / UpdateReplacePolicy

CloudFormation resource attributes that control what happens when a resource is deleted from a stack or replaced during an update. Setting DeletionPolicy: Retain prevents DeleteInstanceAccessControlAttributeConfiguration from being called when the stack is deleted. In CDK, set via applyRemovalPolicy() on the L1 construct's cfnOptions.

## CfnInstanceAccessControlAttributeConfiguration

The CDK L1 construct in aws-cdk-lib/aws-sso for this resource. Uses camelCase property names: instanceArn and accessControlAttributes (current). No L2 construct exists. The deprecated instanceAccessControlAttributeConfiguration nested property is present for backwards compatibility only.

## ConflictException

An sso-admin API error returned when CreateInstanceAccessControlAttributeConfiguration is called on an instance where ABAC is already enabled. This is the expected failure mode when IaC is deployed against a console-pre-configured instance or when two stacks declare this resource against the same InstanceArn.

---

*Back to: [investigation.md](investigation.md)*
