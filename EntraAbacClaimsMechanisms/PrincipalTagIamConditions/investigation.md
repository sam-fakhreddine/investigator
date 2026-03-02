# Investigation: aws:PrincipalTag Condition Keys — Scope, Capabilities, and SSMSessionRunAs Influence

**Date:** 2026-03-02
**Status:** Complete

---

## aws:PrincipalTag Control Surface vs SSMSessionRunAs Mechanism

| Mechanism | Layer | Can Influence SSMSessionRunAs? | Notes |
| --- | --- | --- | --- |
| aws:PrincipalTag in IAM policy Condition | IAM authorization (Allow/Deny API actions) | No — not directly | Controls whether StartSession is permitted; does not set the OS user |
| SSMSessionRunAs as IAM resource tag on role | IAM entity metadata (permanent) | Yes — but impractical for per-user mapping | One tag per role; everyone assuming that role gets the same OS user |
| SSMSessionRunAs as STS session tag | STS session context (per-session) | Yes — the primary per-user mechanism | Entra ID attribute mapped in IAM Identity Center flows as PrincipalTag; SSM reads it directly |
| Session Manager Preferences (account-level) | SSM configuration (fallback default) | Yes — as fallback only | Applies when no SSMSessionRunAs tag is present on the principal |

> SSMSessionRunAs and aws:PrincipalTag share the same STS session tag infrastructure. SSM reads SSMSessionRunAs directly from the principal tag context — not via an IAM policy Condition. aws:PrincipalTag in a policy Condition only gates the StartSession API call itself.

---

## Question

> In the Entra ID → IAM Identity Center ABAC pipeline, what can aws:PrincipalTag condition keys in permission set IAM policies control, and can they influence SSMSessionRunAs behavior or OS-level session identity?

---

## Context

Organizations federate Entra ID to AWS IAM Identity Center. SAML claims propagate as STS session tags accessible in IAM policies as aws:PrincipalTag/<key>. Permission sets include inline policies using these as condition keys. The question is what layer aws:PrincipalTag operates at, what resource-level or session-level control it enables, and specifically whether IAM policy conditions using aws:PrincipalTag can influence what OS user a federated user lands as in SSM Session Manager (SSMSessionRunAs).

---

## Key Findings

- aws:PrincipalTag condition keys operate exclusively at the IAM authorization layer — they allow or deny AWS API actions based on whether the principal's session tags match specified values; they do not inject data into service behavior or modify session parameters.
- When IAM Identity Center ABAC is enabled, user attributes configured on the Attributes for access control page are passed as STS session tags during AssumeRoleWithSAML; these tags are immediately available as aws:PrincipalTag/<key> in all downstream IAM policy evaluations for the session.
- A permission set inline policy using aws:PrincipalTag can gate ssm:StartSession access — for example, allowing StartSession only when ssm:resourceTag/Department matches aws:PrincipalTag/department — but this controls whether the session is permitted, not which OS user the session runs as.
- SSMSessionRunAs is resolved by SSM Agent reading the IAM principal's tag context directly: if the calling principal has a tag keyed SSMSessionRunAs, SSM uses that value as the target OS username; this happens outside IAM policy evaluation and cannot be expressed as an IAM Condition key. The primary SSM Run As documentation uses the term 'IAM entity tag' without explicitly distinguishing IAM resource tags from STS session tags; the equivalence for federated sessions is documented in AWS-authored blog posts rather than the primary user guide.
- Because IAM Identity Center session tags and aws:PrincipalTag share the same STS session tag infrastructure, an Entra ID attribute mapped as SSMSessionRunAs in IAM Identity Center flows end-to-end as a PrincipalTag and SSM Agent reads it — making per-user OS identity mapping possible without any IAM policy Condition on the permission set. This end-to-end flow is confirmed by AWS-authored blog posts; the primary SSM session preferences page does not enumerate STS session tags as an explicit input path.
- The SSMSessionRunAs resolution order is: (1) IAM principal tag SSMSessionRunAs wins if present; (2) Session Manager account-level preferences apply as fallback; (3) if neither is set and Run As is enabled, the session fails — there is no fallback to ssm-user once Run As is activated.
- IAM Identity Center automatically manages the trust policy of provisioned roles to permit sts:TagSession, which is required for SAML session tags (including SSMSessionRunAs) to be accepted; this is transparent to permission set authors.
- The ssm:StartSession action does not list aws:PrincipalTag as a supported condition key in the Service Authorization Reference; the condition keys it does support are ssm:SessionDocumentAccessCheck, ssm:resourceTag/${TagKey}, aws:ResourceTag/${TagKey}, and ssm:AccessRequestId — so aws:PrincipalTag can only condition the StartSession call indirectly by scoping on resource tags that the instance must also carry.
- Multi-valued session tags are not supported by AWS STS; an Entra ID user who maps to multiple SSMSessionRunAs values cannot be expressed in a single tag — this constrains designs where users need to assume different OS identities across instances.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| aws:PrincipalTag | A global IAM condition context key that exposes the tags on the calling principal (IAM user, IAM role, or federated session) at request time. For federated sessions via IAM Identity Center, this includes all STS session tags passed during AssumeRoleWithSAML. Used in Condition blocks of IAM policies to allow or deny API actions. |
| STS Session Tag | A key-value pair attached to a federated or assumed-role session at the time of role assumption. Passed by the IdP via SAML attribute statements using the namespace https://aws.amazon.com/SAML/Attributes/PrincipalTag:{key}. Valid only for the life of the session and not written back to the IAM role resource itself. |
| SSMSessionRunAs | A special tag key recognized by SSM Agent. When the calling principal carries a tag with this key, SSM Agent uses the tag value as the OS username for the session instead of the default ssm-user account. Can be set as a permanent IAM resource tag on a role or as a per-session STS session tag from an IdP. |
| IAM Identity Center ABAC | A feature of IAM Identity Center (formerly AWS SSO) that allows user attributes from the connected identity store (including Entra ID via SAML) to be passed as STS session tags on sign-in. Enabled via the Attributes for access control page; the attribute key-value pairs then appear as aws:PrincipalTag/<key> in IAM policy evaluation. |
| Permission Set | An IAM Identity Center construct that bundles AWS managed policies and inline IAM policies into a role that IAM Identity Center provisions in each assigned AWS account. Inline policies in permission sets can reference aws:PrincipalTag to build ABAC rules without referencing specific user identities. |
| Session Manager Run As | A Session Manager feature that replaces the default ssm-user OS account with a specified OS username for session execution. Configured either via account-level Session Manager Preferences or per-principal via the SSMSessionRunAs tag. Applies only to Linux and macOS managed nodes; root is not supported. |
| IAM Authorization Layer | The AWS evaluation engine that runs before any service API handler executes. It evaluates identity-based policies, resource-based policies, permission boundaries, and SCPs. aws:PrincipalTag conditions are evaluated at this layer — they can only produce Allow or Deny, not inject values into service-level behavior. |
| ssm:resourceTag condition key | An SSM-specific condition key that matches tags on the target SSM resource (e.g., an EC2 instance or managed node) at the time of a StartSession call. Used in combination with aws:PrincipalTag to implement ABAC-style gating on which instances a federated user can start a session against. |

---

## Tensions & Tradeoffs

- aws:PrincipalTag in a permission set policy Condition gates API access (Allow/Deny), but SSMSessionRunAs tag is resolved by SSM Agent outside IAM policy evaluation — these are distinct mechanisms that can appear interchangeable but operate at different layers and cannot substitute for each other.
- For SSMSessionRunAs to work per-user via IAM Identity Center, the SSMSessionRunAs attribute must be mapped in the Attributes for access control page — not just passed through a SAML assertion claim that bypasses IAM Identity Center's controlled attribute set. Attributes sent directly by the external IdP without being mapped through IAM Identity Center's ABAC configuration may still pass as session tags, but their provenance and enforcement guarantees differ.
- IAM resource tags on a permission set's provisioned role are shared across all users who assume that role; they cannot encode per-user identity. This means SSMSessionRunAs as an IAM resource tag on the role assigns the same OS user to everyone — which is useful for shared service accounts but defeats per-user OS identity. STS session tags are the only mechanism for per-user mapping.
- The absence of aws:PrincipalTag in the list of supported condition keys for ssm:StartSession means developers cannot write a Condition that directly matches the principal's tag against a session parameter — they must route ABAC enforcement through resource tags on the managed node, adding an operational tagging requirement on the EC2/managed-instance side.
- STS does not support multi-valued session tags, so a user who legitimately needs to run as different OS users on different instances cannot express this in a single SSMSessionRunAs tag — multiple role assumptions or a Lambda broker are the only paths to multi-value mapping.

---

## Open Questions

- Does IAM Identity Center's automatic trust policy management for provisioned roles always include sts:TagSession, or does this require explicit configuration when custom session tags beyond standard ABAC attributes are used?
- When Entra ID passes SSMSessionRunAs via a direct SAML assertion (not via IAM Identity Center's Attributes for access control page), does IAM Identity Center forward it faithfully as a session tag, or does it strip attributes not mapped through its ABAC configuration?
- Is there a documented maximum length constraint on SSMSessionRunAs tag values that aligns with Linux username length limits, given that IAM Identity Center attribute values have their own length constraints?
- Can aws:PrincipalTag conditions in an IAM Identity Center permission set inline policy be used to restrict which SSM Session documents (DocumentName) a user may invoke, providing a second ABAC enforcement point without depending on instance-side resource tags?

---

## Sources & References

- [Turn on Run As support for Linux and macOS managed nodes — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Pass session tags in AWS STS — AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html)
- [AWS global condition context keys — aws:PrincipalTag](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
- [Create permission policies for ABAC in IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html)
- [Configure ABAC in IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html)
- [IAM tutorial: Use SAML session tags for ABAC](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_abac-saml.html)
- [Actions, resources, and condition keys for AWS Systems Manager — Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html)
- [Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [Configuring AWS Systems Manager Session Manager run as support for federated users using session tags](https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/)
- [Use custom attributes for ABAC with Microsoft Entra ID and AWS IAM Identity Center](https://aws.amazon.com/blogs/modernizing-with-aws/use-custom-attributes-for-attribute-based-access-control-abac-with-microsoft-entra-id-and-aws-iam-identity-center/)
