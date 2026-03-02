# Glossary — SAML Claims vs SCIM Sync: ABAC Attribute Delivery Paths in Entra ID to IAM Identity Center

Quick definitions of key terms and concepts referenced in this investigation.

---

## SAML Claims Path

Attributes delivered in the SAML 2.0 assertion emitted by the Entra enterprise app at user authentication. Configured in the Attributes and Claims section using the namespace https://aws.amazon.com/SAML/Attributes/AccessControl. IdC passes these attribute values to STS as session tags. Not stored in the IdC identity store and not visible in the IdC console.

## SCIM / Identity Store Path

Attributes continuously provisioned from Entra to the IAM Identity Center identity store via SCIM v2.0. Mapped to ABAC keys on the IAM Identity Center console Attributes for Access Control page. Limited to SCIM core and enterprise schema fields. When the same key exists in both SCIM and SAML, the identity store value takes precedence.

## Attributes for Access Control

IAM Identity Center feature that maps identity store attribute paths (e.g., ${path:enterprise.department}) to session tag keys. Configured in the IdC console Settings page. Attributes defined here override same-keyed SAML assertion attributes. Values here are drawn from SCIM-provisioned data.

## SSMSessionRunAs

A session tag and IAM entity tag consumed by SSM Session Manager to determine which OS-level user account starts a session on a managed Linux or macOS node. For federated IdC users, it is delivered as a SAML AccessControl attribute that becomes a PrincipalTag:SSMSessionRunAs STS session tag. Cannot be delivered via SCIM.

## AccessControl: SAML Attribute Prefix

The required SAML attribute namespace prefix https://aws.amazon.com/SAML/Attributes/AccessControl: used in Entra Attributes and Claims to signal that an attribute should be passed as an STS session tag. The key name follows the colon (e.g., AccessControl:SSMSessionRunAs).

## SCIM Schema Extension

SCIM v2.0 mechanism for adding custom attributes beyond the core and enterprise schema. AWS IAM Identity Center's SCIM endpoint does not support schema extensions, returning HTTP 400 for any attempt to provision extension attributes. This is the structural reason SSMSessionRunAs cannot be delivered via SCIM.

## STS Session Tag

A key-value tag attached to temporary security credentials issued by AWS STS via AssumeRoleWithSAML. Session tags are accessible in IAM policy conditions via aws:PrincipalTag/<key>. For IAM Identity Center ABAC, SAML AccessControl attributes become STS session tags at role assumption time.

## PrincipalTag:SSMSessionRunAs

The STS principal tag key that SSM Session Manager reads for federated sessions to determine the OS username. Populated via the SAML AccessControl:SSMSessionRunAs attribute. Referenced in CloudTrail as part of the principalTags object on the AssumeRoleWithSAML event.

---

*Back to: [investigation.md](investigation.md)*
