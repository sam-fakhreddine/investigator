# Investigation: SAML Claims vs SCIM Sync: ABAC Attribute Delivery Paths in Entra ID to IAM Identity Center

**Date:** 2026-03-02
**Status:** Complete

---

## SAML Claims vs SCIM Sync: Attribute Delivery Comparison

| Dimension | SAML Claims Path | SCIM / Identity Store Path |
| --- | --- | --- |
| Trigger | At user authentication (per-login) | Continuous background provisioning |
| Configuration location | Entra enterprise app Attributes & Claims section | IdC console Attributes for Access Control page |
| Attribute prefix required | https://aws.amazon.com/SAML/Attributes/AccessControl:<key> | IAM Identity Center identity store field path (e.g. ${path:enterprise.department}) |
| Custom/arbitrary attributes | Yes — any Entra user property or extension attribute | No — limited to SCIM core and enterprise schema; AWS SCIM endpoint rejects schema extensions |
| SSMSessionRunAs supportable | Yes — configure as AccessControl:SSMSessionRunAs claim in Entra | No — not a SCIM-defined attribute; SCIM schema extension not supported by AWS endpoint |
| Precedence when same key in both | SCIM/identity store value wins and overrides SAML value | SCIM/identity store value wins (documented AWS behavior) |
| Visibility in IdC console | Not visible on Attributes for Access Control page | Visible — attributes are stored in identity store |
| Value freshness | Current Entra attribute value at login time | Value at last SCIM sync cycle (can lag) |

> Precedence rule source: AWS IAM Identity Center User Guide (attributesforaccesscontrol.html): 'In scenarios where the same attributes are coming to IAM Identity Center through SAML and SCIM, the SCIM attributes value take precedence in access control decisions.' For SSMSessionRunAs, use the SAML path exclusively — SCIM cannot carry this attribute.

---

## Question

> In the Entra ID to IAM Identity Center ABAC pipeline, what does the SAML claims path cover, how does it interact with SCIM sync when both specify the same attribute key, and what are the documented implications for SSMSessionRunAs attribute delivery?

---

## Context

Organizations federate Microsoft Entra ID to AWS IAM Identity Center (IdC) via SAML. IdC supports ABAC (Attributes for Access Control), which passes user attributes as STS session tags that condition IAM policy evaluation. The SSMSessionRunAs session tag controls which OS-level username SSM Session Manager uses when starting a session on a managed node. There are two distinct paths for delivering ABAC attributes to IdC: (1) SAML claims, emitted by the Entra enterprise app at authentication time using the https://aws.amazon.com/SAML/Attributes/AccessControl: prefix; and (2) the Attributes for Access Control configuration in the IdC console, which reads values from the IdC identity store populated by SCIM sync. Understanding which path wins, what each path can carry, and the structural difference for SSMSessionRunAs is essential to reliably routing the correct OS username into STS session tags.

---

## Key Findings

- SCIM-provisioned identity store values take precedence over SAML assertion values when the same attribute key is present in both paths. AWS documentation states: 'In scenarios where the same attributes are coming to IAM Identity Center through SAML and SCIM, the SCIM attributes value take precedence in access control decisions.'
- The SAML claims path uses the prefix https://aws.amazon.com/SAML/Attributes/AccessControl:<key> in the Entra Attributes and Claims section. IdC reads these at authentication time and passes them as STS session tags via AssumeRoleWithSAML without storing them in the identity store.
- The SCIM/identity store path is configured on the IAM Identity Center console Attributes for Access Control page. These values are read from the IdC identity store, populated by SCIM provisioning from Entra. The configured values replace matching SAML assertion values for the same key.
- SAML-sourced ABAC attributes are not visible on the IAM Identity Center Attributes for Access Control console page. Operators must know these attribute keys in advance to reference them in IAM policy conditions.
- AWS IAM Identity Center's SCIM endpoint does not support SCIM schema extensions. Arbitrary custom attributes, including SSMSessionRunAs, cannot be synced via SCIM. The endpoint returns HTTP 400 when schema extension attributes are submitted.
- SSMSessionRunAs must travel exclusively via the SAML claims path. The SAML attribute name is https://aws.amazon.com/SAML/Attributes/AccessControl:SSMSessionRunAs and the value maps to an OS-level username on the target managed node. SCIM cannot carry this attribute.
- Session Manager reads SSMSessionRunAs first as an IAM entity tag on the assumed role or user. For federated users, it reads the STS principal tag PrincipalTag:SSMSessionRunAs, which is set by the SAML session tag flowing through AssumeRoleWithSAML — as documented in the AWS Cloud Operations Blog; the official session preferences user guide does not describe the STS principal tag lookup path. SCIM provisioning does not populate this tag.
- The SCIM sync cycle introduces a lag between attribute changes in Entra and their availability in the IdC identity store. The SAML path reflects the current Entra attribute value at each login, making it more immediately consistent for per-user attributes that change frequently.
- Standard SCIM enterprise schema attributes — including department, title, employeeNumber, costCenter, and division — can be provisioned via SCIM and mapped to ABAC keys on the Attributes for Access Control page. These attributes then take precedence over any same-keyed SAML claim.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SAML Claims Path | Attributes delivered in the SAML 2.0 assertion emitted by the Entra enterprise app at user authentication. Configured in the Attributes and Claims section using the namespace https://aws.amazon.com/SAML/Attributes/AccessControl. IdC passes these attribute values to STS as session tags. Not stored in the IdC identity store and not visible in the IdC console. |
| SCIM / Identity Store Path | Attributes continuously provisioned from Entra to the IAM Identity Center identity store via SCIM v2.0. Mapped to ABAC keys on the IAM Identity Center console Attributes for Access Control page. Limited to SCIM core and enterprise schema fields. When the same key exists in both SCIM and SAML, the identity store value takes precedence. |
| Attributes for Access Control | IAM Identity Center feature that maps identity store attribute paths (e.g., ${path:enterprise.department}) to session tag keys. Configured in the IdC console Settings page. Attributes defined here override same-keyed SAML assertion attributes. Values here are drawn from SCIM-provisioned data. |
| SSMSessionRunAs | A session tag and IAM entity tag consumed by SSM Session Manager to determine which OS-level user account starts a session on a managed Linux or macOS node. For federated IdC users, it is delivered as a SAML AccessControl attribute that becomes a PrincipalTag:SSMSessionRunAs STS session tag. Cannot be delivered via SCIM. |
| AccessControl: SAML Attribute Prefix | The required SAML attribute namespace prefix https://aws.amazon.com/SAML/Attributes/AccessControl: used in Entra Attributes and Claims to signal that an attribute should be passed as an STS session tag. The key name follows the colon (e.g., AccessControl:SSMSessionRunAs). |
| SCIM Schema Extension | SCIM v2.0 mechanism for adding custom attributes beyond the core and enterprise schema. AWS IAM Identity Center's SCIM endpoint does not support schema extensions, returning HTTP 400 for any attempt to provision extension attributes. This is the structural reason SSMSessionRunAs cannot be delivered via SCIM. |
| STS Session Tag | A key-value tag attached to temporary security credentials issued by AWS STS via AssumeRoleWithSAML. Session tags are accessible in IAM policy conditions via aws:PrincipalTag/<key>. For IAM Identity Center ABAC, SAML AccessControl attributes become STS session tags at role assumption time. |
| PrincipalTag:SSMSessionRunAs | The STS principal tag key that SSM Session Manager reads for federated sessions to determine the OS username. Populated via the SAML AccessControl:SSMSessionRunAs attribute. Referenced in CloudTrail as part of the principalTags object on the AssumeRoleWithSAML event. |

---

## Tensions & Tradeoffs

- SCIM values take precedence over SAML values for the same key, but SCIM is limited to a fixed attribute schema. This creates an asymmetric system: the path with broader coverage (SAML) loses to the path with narrower coverage (SCIM) on any key they share. Operators who configure the same attribute key in both paths without awareness of this rule will find SAML values silently suppressed.
- The SAML path is the only mechanism for custom or non-standard attributes like SSMSessionRunAs, yet SAML attributes are not visible in the IdC console. This creates an observability gap: operators cannot inspect or audit SAML-delivered ABAC attributes from the IdC interface, which complicates troubleshooting.
- SCIM sync is continuous but introduces lag, while SAML delivers current attribute values at login time. For attributes that change in Entra (e.g., department reassignment), the SCIM value in the identity store may be stale relative to what Entra would emit in a SAML assertion — yet the stale SCIM value wins.
- The Entra SCIM provisioning connector does not remove attribute values from IdC when an attribute is cleared in Entra; it only syncs non-empty changes. This means SCIM-provisioned ABAC values can persist in the identity store after the source value is removed, causing access decisions to reflect outdated data.

---

## Open Questions

- Whether AWS plans to support SCIM schema extensions in the IAM Identity Center SCIM endpoint is not publicly documented on any confirmed roadmap. Community reports cite an AWS engineering contact confirming absence of extension support as of 2023.
- The exact behavior when an Attributes for Access Control mapping references an identity store field that has no value for a given user (e.g., SCIM never provisioned a value) is not fully documented — whether it falls back to the SAML assertion value or emits no session tag for that key.
- Whether the SCIM-wins-over-SAML precedence rule applies only when an IdC Attributes for Access Control mapping exists for the key, or also when the attribute arrives purely via SAML with no console configuration, is not explicitly clarified in the official documentation.
- The interaction between the SAML-delivered SSMSessionRunAs tag and a per-document Session Manager preferences default OS user setting (the account-level fallback) when both are present has not been publicly documented beyond the basic lookup order described in the Session Manager user guide.

---

## Sources & References

- [Attributes for access control - AWS IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html)
- [Enable and configure attributes for access control - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html)
- [Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html)
- [Provision users and groups from an external identity provider using SCIM - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html)
- [Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager - AWS Security Blog](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [Use custom attributes for ABAC with Microsoft Entra ID and AWS IAM Identity Center - AWS Modernizing with AWS Blog](https://aws.amazon.com/blogs/modernizing-with-aws/use-custom-attributes-for-attribute-based-access-control-abac-with-microsoft-entra-id-and-aws-iam-identity-center/)
- [Azure AD provisioning to AWS Identity Center with custom user/group attributes - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1324325/azure-ad-provisioning-to-aws-identity-center-with)
- [Configuring AWS Systems Manager Session Manager run as support for federated users using session tags - AWS Cloud Operations Blog](https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/)
- [SCIM profile and SAML 2.0 implementation - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/scim-profile-saml.html)
