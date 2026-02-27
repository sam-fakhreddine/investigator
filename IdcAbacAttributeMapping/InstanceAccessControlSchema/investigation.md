# Investigation: IAM Identity Center InstanceAccessControlAttributeConfiguration — Schema and Configuration Surface

**Date:** 2026-02-27
**Status:** Complete

---

## Configuration Surface at a Glance

| Surface | Resource / Command | Key Property |
| --- | --- | --- |
| CloudFormation | AWS::SSO::InstanceAccessControlAttributeConfiguration | accessControlAttributes (array of Key + Value.Source) |
| CDK TypeScript L1 | aws-cdk-lib/aws-sso.CfnInstanceAccessControlAttributeConfiguration | accessControlAttributes (camelCase; no L2 exists) |
| CLI — create | aws sso-admin create-instance-access-control-attribute-configuration | --instance-access-control-attribute-configuration JSON |
| CLI — update | aws sso-admin update-instance-access-control-attribute-configuration | Same JSON shape as create; use when ABAC already enabled |
| Console | IdC > Settings > Attributes for access control | Enable button + attribute key/value form; SAML-only attrs not shown here |

> InstanceAccessControlAttributeConfiguration is a singleton per IdC instance — one configuration object exists per instance. The CLI create call returns ConflictException if ABAC is already enabled; use update instead. The InstanceArn is required on all surfaces and is obtained from the IdC console Settings page or via aws sso-admin list-instances.

---

## Question

> What is the high-level configuration surface of InstanceAccessControlAttributeConfiguration in IAM Identity Center for mapping a per-user SCIM-synced attribute (e.g. sAMAccountName or a custom extension attribute) to the ssm:RunAsDefaultRunAs session tag — as exposed via AWS CDK (TypeScript), CloudFormation, and AWS CLI?

---

## Context

IAM Identity Center's Attribute-Based Access Control (ABAC) feature allows user attributes stored in or synced to the IdC identity store to be passed as principal session tags into AWS. When a user assumes a permission set role, any configured attributes are emitted as aws:PrincipalTag/<Key> values on the STS session. SSM Session Manager's RunAs feature reads the SSMSessionRunAs session tag to determine which OS user to use for a session. Connecting these two surfaces — IdC ABAC attribute configuration and the SSM session tag — is the mechanism by which a SCIM-synced AD attribute (such as sAMAccountName or a custom extension attribute) can drive per-user OS login on managed instances without any per-user IAM configuration. The InstanceAccessControlAttributeConfiguration resource is the single control plane object that enables this pipeline.

---

## Key Findings

- The AccessControlAttribute structure has exactly two fields: Key (string, 1–128 chars) and Value.Source (single-item string array, 0–256 chars per item). Key is the name the attribute will carry as a principal tag. Value.Source contains a ${path:...} expression for SCIM-synced identity store attributes or a literal identity source token. The Key value becomes the principal tag key verbatim on the STS session.
- For SCIM-synced identity store attributes (external IdP + Entra SCIM), Source uses ${path:...} expressions: e.g. ${path:userName}, ${path:enterprise.department}, ${path:enterprise.employeeNumber}. For AWS Managed Microsoft AD-connected instances, Source uses flat dollar-brace syntax: ${samaccountname}, ${userprincipalname}, ${mail}. These two syntaxes are distinct and not interchangeable. The correct path for a sAMAccountName-derived attribute depends on where Entra places it in its SCIM payload — not on the AD attribute name itself.
- The AccessControlAttributes array is capped at 50 items and the entire configuration is a singleton per IdC instance. There is exactly one InstanceAccessControlAttributeConfiguration per instance. The list is replaced in full on every update — there is no per-attribute add/remove API. Omitting an existing attribute from an update call deletes it silently.
- Create vs Update: CreateInstanceAccessControlAttributeConfiguration enables ABAC and seeds the attribute list (call once per instance). UpdateInstanceAccessControlAttributeConfiguration replaces the attribute list on an already-enabled instance. Calling create on an instance where ABAC is already enabled returns ConflictException (HTTP 400). Calling update on an instance where ABAC has never been enabled returns ResourceNotFoundException. DescribeInstanceAccessControlAttributeConfiguration is the correct pre-check to determine which call to use.
- The CloudFormation resource has a deprecated top-level property InstanceAccessControlAttributeConfiguration; use the flat AccessControlAttributes property instead. CDK's L1 construct (CfnInstanceAccessControlAttributeConfiguration) exposes accessControlAttributes (flat array, current) and instanceAccessControlAttributeConfiguration (deprecated, backwards compat only). No L2 construct exists for this resource in aws-cdk-lib as of 2026.
- The attribute Key name set in AccessControlAttribute is the exact string that appears as aws:PrincipalTag/<Key> and as the SSM session tag name. For SSM RunAs: Key must be exactly 'SSMSessionRunAs' — SSM reads this tag name to select the OS user. Casing is significant. Note: the string ssm:RunAsDefaultRunAs appears in SSM user guide content and blog posts (e.g. in session preferences documentation) but has not been confirmed as a formally listed condition key in the AWS Service Authorization Reference condition key table for Systems Manager.
- The InstanceArn required on all surfaces is the ARN of the IAM Identity Center instance in the form arn:aws:sso:::instance/(sso)?ins-[a-zA-Z0-9-.]{16}. It is available in the IdC console under Settings or programmatically via aws sso-admin list-instances. It is not a Ref-able resource created in the same stack and must be passed as a parameter or resolved via CDK context.
- Console path for Attributes for access control: IAM Identity Center > Settings > Attributes for access control tab. Clicking Enable initializes ABAC. Attributes arriving only through SAML assertions (not stored in the IdC identity store) are not displayed in this console view even if they are active as session tags. The describe-instance-access-control-attribute-configuration CLI call is the authoritative check.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| InstanceAccessControlAttributeConfiguration | The singleton IAM Identity Center resource that enables ABAC and holds the list of identity store attribute-to-session-tag mappings. One per IdC instance. Managed via CreateInstanceAccessControlAttributeConfiguration, UpdateInstanceAccessControlAttributeConfiguration, and DescribeInstanceAccessControlAttributeConfiguration APIs. |
| AccessControlAttribute | A single attribute mapping entry within InstanceAccessControlAttributeConfiguration. Contains a Key (the principal tag name that appears on the STS session) and a Value.Source (a single-item array with an identity store path expression or literal source token). |
| path expression ${path:...} | Source value syntax for referencing SCIM-synced identity store attributes in an external IdP scenario (e.g. Entra ID with SCIM provisioning). Examples: ${path:userName}, ${path:enterprise.department}. Standard attributes use direct field names; enterprise extension attributes use the enterprise.* prefix shorthand consistent with the SCIM enterprise schema. |
| AD source expression ${samaccountname} | Source value syntax for AWS Managed Microsoft AD-connected IdC instances. Uses flat dollar-brace syntax with the lowercase AD attribute name. Distinct from the ${path:} format used with external SCIM-provisioned IdPs and not valid in the SCIM path context. |
| SSMSessionRunAs | The exact AccessControlAttribute Key value required for SSM RunAs integration. SSM Session Manager reads the principal tag named SSMSessionRunAs on the STS session to determine the OS user for a RunAs session. The string ssm:RunAsDefaultRunAs appears in SSM documentation but its status as a formally listed IAM condition key in the AWS Service Authorization Reference has not been confirmed. |
| aws:PrincipalTag/<Key> | The IAM condition key format produced when an ABAC attribute is emitted on an STS session by IdC. If AccessControlAttribute Key = 'SSMSessionRunAs', the condition key is aws:PrincipalTag/SSMSessionRunAs. Used in permission set inline policies to enforce attribute-based access rules. |
| CfnInstanceAccessControlAttributeConfiguration | The CDK L1 construct in aws-cdk-lib/aws-sso for this resource. Uses camelCase property names: instanceArn and accessControlAttributes. No L2 construct exists. The deprecated instanceAccessControlAttributeConfiguration property is present for backwards compatibility only. |
| ABAC singleton create/update split | The API design constraint where CreateInstanceAccessControlAttributeConfiguration can only be called once per IdC instance to enable ABAC, and all subsequent attribute list changes must use UpdateInstanceAccessControlAttributeConfiguration. Calling create on an already-enabled instance returns ConflictException. |

---

## Tensions & Tradeoffs

- The Source path for a sAMAccountName-derived attribute is not simply ${path:samaccountname} — the correct path depends on how Entra ID maps the AD attribute into its SCIM payload before syncing to IdC. If sAMAccountName is mapped to a custom enterprise extension field, the path would be ${path:enterprise.<customFieldName>}. This dependency is controlled by Entra provisioning attribute mapping configuration and must be confirmed before the Source value can be written.
- UpdateInstanceAccessControlAttributeConfiguration replaces the entire AccessControlAttributes list, creating a coordination hazard in shared IdC instances. Concurrent deployments from multiple stacks or teams risk silently overwriting each other's attributes. There is no merge or partial-update API surface.
- If ABAC was previously enabled manually in the IdC console, a CloudFormation or CDK stack deploying this resource will fail with ConflictException because the create call conflicts with the existing singleton. The resource must be imported into the stack before IaC management can proceed — a non-trivial remediation in LZA-managed environments.
- Attributes delivered purely via SAML assertions — not stored in the IdC identity store and not configured in AccessControlAttributeConfiguration — are functional as session tags but invisible in the Attributes for access control console view. This creates a discoverability gap where a working configuration appears incomplete or absent in the console.

---

## Open Questions

- What is the exact Entra ID SCIM provisioning mapping for sAMAccountName — which SCIM schema field does Entra write sAMAccountName into when provisioning users to IdC? This determines the correct ${path:...} Source value.
- Does LZA's IdC configuration surface expose any mechanism to manage InstanceAccessControlAttributeConfiguration, or must this resource always be deployed outside of the LZA customizations pipeline?
- What is the behavior when a user's identity store attribute referenced in a Source path is null or empty — does IdC emit an empty tag, omit the tag entirely, or block session issuance?
- Are there documented quota increase paths for the 50-attribute limit, or is 50 a hard service ceiling?
- Does the CloudFormation resource type support stack import for environments where ABAC was manually enabled prior to IaC adoption?
- Is ssm:RunAsDefaultRunAs a formally listed IAM condition key in the AWS Service Authorization Reference condition key table for Systems Manager? The string appears in SSM user guide content and blog posts but was not found in the SAR condition key list during validation. Its exact role — whether it is a valid IAM condition key usable in permission set policies, a documentation label only, or something else — is unconfirmed.

---

## Sources & References

- [AWS CloudFormation — AWS::SSO::InstanceAccessControlAttributeConfiguration resource reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html)
- [AWS CloudFormation — AccessControlAttribute property type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattribute.html)
- [AWS CloudFormation — AccessControlAttributeValue property type](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattributevalue.html)
- [IAM Identity Center API Reference — CreateInstanceAccessControlAttributeConfiguration](https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_CreateInstanceAccessControlAttributeConfiguration.html)
- [IAM Identity Center API Reference — UpdateInstanceAccessControlAttributeConfiguration](https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_UpdateInstanceAccessControlAttributeConfiguration.html)
- [IAM Identity Center API Reference — InstanceAccessControlAttributeConfiguration data type](https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_InstanceAccessControlAttributeConfiguration.html)
- [AWS CLI reference — create-instance-access-control-attribute-configuration](https://docs.aws.amazon.com/cli/latest/reference/sso-admin/create-instance-access-control-attribute-configuration.html)
- [AWS CLI reference — update-instance-access-control-attribute-configuration](https://docs.aws.amazon.com/cli/latest/reference/sso-admin/update-instance-access-control-attribute-configuration.html)
- [AWS CDK v2 — CfnInstanceAccessControlAttributeConfiguration construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_sso.CfnInstanceAccessControlAttributeConfiguration.html)
- [IAM Identity Center User Guide — Attributes for access control](https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html)
- [IAM Identity Center User Guide — Attribute mappings concept](https://docs.aws.amazon.com/singlesignon/latest/userguide/attributemappingsconcept.html)
- [AWS Security Blog — Configure AWS IAM Identity Center ABAC for EC2 and Systems Manager Session Manager](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [AWS MT Blog — Configure Session Manager access for federated users using SAML session tags](https://aws.amazon.com/blogs/mt/configure-session-manager-access-for-federated-users-using-saml-session-tags/)
- [IAM Identity Center User Guide — Enable and configure attributes for access control](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html)
