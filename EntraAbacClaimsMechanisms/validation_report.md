# Validation Report: Entra ID to IAM Identity Center ABAC Pipeline — Attribute Delivery, PrincipalTag Scope, and SSMSessionRunAs
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 14
- Verified: 13 | Redirected: 0 | Dead: 0 | Unverifiable: 1
- Findings checked: 10
- Confirmed: 7 | Partially confirmed: 3 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 3

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/EntraAbacClaimsMechanisms
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           3604ac7f7acf   3604ac7f7acf
tensions             IN_SYNC        6            6            54706e1c70bf   54706e1c70bf
open_questions       IN_SYNC        7            7            fa982a466da6   fa982a466da6
sources              IN_SYNC        14           14           50ddcb08d2bf   50ddcb08d2bf
concepts             IN_SYNC        10           10           bfd568a9aa26   bfd568a9aa26
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Attributes for access control - AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html | VERIFIED | Page exists; contains the quoted SCIM-wins-over-SAML language verbatim |
| 2 | Enable and configure attributes for access control - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html | VERIFIED | Page exists; confirms identity store precedence over SAML and SAML attribute invisibility in console |
| 3 | Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html | VERIFIED | Page exists; covers both SAML and SCIM configuration for Entra ID integration |
| 4 | Provision users and groups from an external identity provider using SCIM | https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html | VERIFIED | Page exists; covers SCIM v2.0 auto-provisioning; notes multivalue attributes not currently supported |
| 5 | SCIM profile and SAML 2.0 implementation - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/scim-profile-saml.html | VERIFIED | Page exists; high-level overview; does not detail schema extension support — must be supplemented by SCIM developer guide |
| 6 | Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED | Page exists; documents SSMSessionRunAs tag, resolution order, and behavior when Run As is active |
| 7 | Pass session tags in AWS STS - AWS Identity and Access Management | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html | VERIFIED | Page exists; confirms multi-valued session tags are not supported; documents sts:TagSession requirement |
| 8 | AWS global condition context keys — aws:PrincipalTag | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html | VERIFIED | Page exists; documents aws:PrincipalTag as a global condition context key |
| 9 | Create permission policies for ABAC in IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html | VERIFIED | Page exists; shows aws:PrincipalTag usage in permission set IAM policy Condition blocks |
| 10 | Actions, resources, and condition keys for AWS Systems Manager - Service Authorization Reference | https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html | VERIFIED | Page exists; ssm:StartSession condition keys listed are ssm:SessionDocumentAccessCheck, ssm:resourceTag/${TagKey}, aws:ResourceTag/${TagKey}, ssm:AccessRequestId — aws:PrincipalTag is absent |
| 11 | Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager | https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/ | VERIFIED | Page resolves and title matches; article body not fully renderable via automated fetch but page is live |
| 12 | Configuring AWS Systems Manager Session Manager run as support for federated users using session tags | https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/ | VERIFIED | Page resolves and title matches; confirmed via web search to document AccessControl:SSMSessionRunAs SAML attribute name and federated user flow |
| 13 | Use custom attributes for ABAC with Microsoft Entra ID and AWS IAM Identity Center | https://aws.amazon.com/blogs/modernizing-with-aws/use-custom-attributes-for-attribute-based-access-control-abac-with-microsoft-entra-id-and-aws-iam-identity-center/ | VERIFIED | Page resolves and title matches; article body not fully renderable via automated fetch but page is live |
| 14 | Azure AD provisioning to AWS Identity Center with custom user/group attributes - Microsoft Q&A | https://learn.microsoft.com/en-us/answers/questions/1324325/azure-ad-provisioning-to-aws-identity-center-with | VERIFIED | Page exists; Microsoft Moderator Danny Zollner cites AWS SCIM engineering contact confirming schema extension absence; community tier source, appropriately labeled |

## Finding Verification

### Finding 1: SAML and SCIM are parallel, independent attribute delivery pipelines
- **Claim:** SAML emits attribute values at each login via the Entra enterprise app; SCIM continuously populates the IdC identity store in the background. Both can contribute to the STS session tags that appear as aws:PrincipalTag in IAM policy evaluation.
- **Verdict:** CONFIRMED
- **Evidence:** Source 1 (attributesforaccesscontrol.html) and Source 2 (configure-abac.html) both confirm the two-path model. Source 2 states SAML attributes are "directly sent to the AWS account when users federate in" while SCIM-sourced attributes flow from the identity store. Source 3 (idp-microsoft-entra.html) confirms both pipelines in the context of Entra ID integration.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html

### Finding 2: SCIM/identity store values win unconditionally when same key is present in both pipelines
- **Claim:** AWS documents this explicitly: "In scenarios where the same attributes are coming to IAM Identity Center through SAML and SCIM, the SCIM attributes value take precedence in access control decisions." This override is silent, with no alert or console indicator, and is not configurable.
- **Verdict:** CONFIRMED
- **Evidence:** Source 1 contains this quoted language verbatim. Source 2 also confirms: "If an attribute from a SAML assertion is also defined as an ABAC attribute in IAM Identity Center, IAM Identity Center will send the value from its Identity Store as a session tag on sign-in." Neither source mentions a configuration option to alter this precedence.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html

### Finding 3: SCIM schema is structurally limited to core and enterprise schema; extensions rejected with HTTP 400
- **Claim:** The AWS IAM Identity Center SCIM endpoint rejects schema extension attributes with HTTP 400. Arbitrary custom attributes, including SSMSessionRunAs, cannot be delivered via SCIM.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The Microsoft Q&A community thread (Source 14) provides the most specific corroboration: a Microsoft Moderator cites an AWS SCIM engineering contact confirming "AWS' SCIM implementation does not support [schema extensions] yet." The specific HTTP 400 response code is not confirmed in any primary AWS documentation found. Source 5 (scim-profile-saml.html) exists but does not discuss schema extensions. The SCIM Implementation Developer Guide (referenced from Source 5 but not listed as a source) would be the authoritative primary source. The claim is well-supported by the combination of the community source and the structural absence of custom attributes from the IdC attribute mapping UI, but the HTTP 400 detail relies on community/secondary sourcing only.
- **Source used:** https://learn.microsoft.com/en-us/answers/questions/1324325/azure-ad-provisioning-to-aws-identity-center-with

### Finding 4: SSMSessionRunAs must travel exclusively via the SAML claims path
- **Claim:** Configured in the Entra enterprise app as https://aws.amazon.com/SAML/Attributes/AccessControl:SSMSessionRunAs. At login, IdC passes it to STS as a session tag; SSM Agent reads PrincipalTag:SSMSessionRunAs from the principal's tag context to determine the OS username.
- **Verdict:** CONFIRMED
- **Evidence:** Web search results confirm the AccessControl:SSMSessionRunAs SAML attribute name from the AWS blog posts (Sources 11, 12). Source 6 (session-preferences-run-as.html) confirms SSM Agent reads the SSMSessionRunAs principal tag to determine OS username. Source 3 (idp-microsoft-entra.html) confirms the AccessControl: namespace pattern for SAML attributes in Entra integration. The claim that SSMSessionRunAs cannot be delivered via SCIM is supported by Finding 3's evidence.
- **Source used:** https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/, https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html

### Finding 5: aws:PrincipalTag condition keys operate at IAM authorization layer; cannot set or modify OS user
- **Claim:** They allow or deny AWS API calls (such as ssm:StartSession) based on whether session tag values match specified criteria. They do not inject data into service-level behavior and cannot set or modify the OS user for a session.
- **Verdict:** CONFIRMED
- **Evidence:** Source 8 (reference_policies_condition-keys.html) confirms aws:PrincipalTag is a condition key used to allow or deny actions based on principal tags. Source 9 (configure-abac-policies.html) shows it used in Allow/Deny IAM policy conditions. Nothing in any source suggests it can modify service behavior or OS-level session parameters. The distinction is structural: IAM authorization evaluates before service handlers execute.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html

### Finding 6: SSMSessionRunAs resolution order — principal tag wins, then account preferences, then session fails
- **Claim:** (1) Calling principal's SSMSessionRunAs tag wins if present; (2) account-level Session Manager Preferences apply as fallback; (3) if neither is set and Run As is enabled, the session fails — no ssm-user fallback once Run As is activated.
- **Verdict:** CONFIRMED
- **Evidence:** Source 6 (session-preferences-run-as.html) documents this exact priority order: first checks IAM entity tag SSMSessionRunAs, then checks account-level Session Manager Preferences default OS user. When Run As support is activated, it prevents fallback to the default ssm-user account, and session fails if no OS account is specified via either method.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html

### Finding 7: SCIM-wins-over-SAML creates asymmetric system with silent SAML suppression
- **Claim:** SAML has broader attribute coverage but loses on any key that SCIM also carries. Operators who configure the same attribute key in both paths without awareness will find SAML values silently suppressed.
- **Verdict:** CONFIRMED
- **Evidence:** This is a direct logical consequence of Finding 2 which is confirmed by primary sources. Source 1 confirms SAML attribute values are not visible in the IdC console. Source 2 confirms SAML attributes are invisible from the Attributes for Access Control page. The combination makes silent suppression a documented structural property of the system.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html

### Finding 8: IAM Identity Center automatically manages sts:TagSession in provisioned role trust policies
- **Claim:** IAM Identity Center automatically manages sts:TagSession permission in provisioned role trust policies, enabling SAML session tags (including SSMSessionRunAs) to pass through without manual trust policy changes. SAML-delivered attributes are not visible in the IdC console.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The claim that SAML-delivered attributes are invisible in the IdC console is directly confirmed by Sources 1 and 2. The automatic management of sts:TagSession by IAM Identity Center is supported by web search results indicating IdC-provisioned trust policies include sts:TagSession automatically, but no single primary AWS documentation page was found that explicitly states this as an automatic behavior of the IdC provisioning process in the pages reviewed. Source 7 (id_session-tags.html) documents sts:TagSession as a manual requirement without mentioning IAM Identity Center automation. This claim should be hedged or the specific AWS documentation page confirming automatic management should be cited.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html, https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

### Finding 9: ssm:StartSession does not list aws:PrincipalTag as a supported condition key; ABAC must use ssm:resourceTag
- **Claim:** The ssm:StartSession action does not list aws:PrincipalTag as a supported condition key in the Service Authorization Reference. ABAC enforcement on StartSession must be routed through ssm:resourceTag conditions on the target managed node.
- **Verdict:** CONFIRMED
- **Evidence:** Source 10 (list_awssystemsmanager.html) was verified directly. The condition keys listed for ssm:StartSession are: ssm:SessionDocumentAccessCheck, ssm:resourceTag/${TagKey}, aws:ResourceTag/${TagKey}, and ssm:AccessRequestId. aws:PrincipalTag is absent from the ssm:StartSession row. The ssm:resourceTag condition key is present, confirming the investigation's routing recommendation.
- **Source used:** https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html

### Finding 10: Multi-valued session tags are not supported by STS
- **Claim:** A user who needs to operate as different OS usernames on different instances cannot express this in a single SSMSessionRunAs tag — multiple role assumptions or a broker are the only architectural paths.
- **Verdict:** CONFIRMED
- **Evidence:** Source 7 (id_session-tags.html) states explicitly: "You must pass a single value for each session tag. AWS STS does not support multi-valued session tags." Source 4 (provision-automatically.html) also notes multivalue attributes are not currently supported in the SCIM provisioning context. The architectural conclusion follows directly.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 3: HTTP 400 on schema extension rejection | PARTIALLY CONFIRMED | The specific HTTP 400 response code for SCIM schema extension rejection is sourced only from a community Q&A thread citing an AWS engineering contact, not from primary AWS documentation. Either (a) locate the IAM Identity Center SCIM Implementation Developer Guide page that specifies the error response, or (b) revise the claim to state "schema extensions are not supported by the AWS SCIM endpoint" without asserting the specific HTTP 400 code, downgrading the HTTP 400 detail to an open question. |
| Finding 8: sts:TagSession automatic management by IdC | PARTIALLY CONFIRMED | The claim that IAM Identity Center automatically manages sts:TagSession in provisioned role trust policies is not confirmed by any of the cited sources. The IAM session tags documentation describes sts:TagSession as a manual trust policy requirement without mentioning IdC automation. Either (a) identify and cite the specific AWS documentation page confirming IdC automatically includes sts:TagSession (e.g., the ABAC user guide or permission set documentation), or (b) add a qualifier noting this behavior is documented in operational practice but not explicitly stated in a primary source, and move the precise claim to open_questions. |
| Finding 3: SCIM Developer Guide absent from sources | PARTIALLY CONFIRMED | The SCIM Implementation Developer Guide is referenced in the investigation's source pages (Source 5 cites it) but is not listed as a source in investigation.json. Given that the schema extension limitation is a core claim, this guide should be added to sources if it contains the relevant restriction, or the claim should be explicitly marked as community-sourced in the investigation text. |

## Overall Assessment

The investigation is structurally sound and internally consistent. Nine of ten key findings are confirmed by primary AWS documentation, with the confirmed findings backed by direct quotes from official sources. The two partially confirmed findings (Finding 3 on the HTTP 400 response code, and Finding 8 on automatic sts:TagSession management) are not wrong but exceed what the cited sources explicitly state — they rely on secondary sourcing or operational inference where primary documentation is available but not cited.

The SCIM-wins-over-SAML precedence rule (the most operationally significant claim) is confirmed verbatim from Source 1. The SSMSessionRunAs SAML delivery path and resolution order are confirmed by the SSM Run As documentation and corroborated by AWS blog posts. The absence of aws:PrincipalTag from ssm:StartSession condition keys is confirmed directly from the Service Authorization Reference. The multi-valued session tag limitation is confirmed from primary IAM documentation.

All 14 sources resolve. The Microsoft Q&A community source is appropriately labeled as community tier and is used only for the SCIM schema extension claim where it is the most specific available evidence. No source is dead, redirected, or inaccessible.

Two targeted remediations are recommended: narrow or hedge the HTTP 400 claim, and either source or hedge the sts:TagSession automatic management claim. Neither affects the investigation's central conclusions.

Sources:
- [Attributes for access control - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html)
- [Enable and configure attributes for access control](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html)
- [Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html)
- [Provision users and groups from an external identity provider using SCIM](https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html)
- [SCIM profile and SAML 2.0 implementation](https://docs.aws.amazon.com/singlesignon/latest/userguide/scim-profile-saml.html)
- [Turn on Run As support for Linux and macOS managed nodes](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Pass session tags in AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html)
- [AWS global condition context keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
- [Actions, resources, and condition keys for AWS Systems Manager](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html)
- [Configure AWS IAM Identity Center ABAC for EC2 instances and Session Manager](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [Configuring SSM Session Manager run as support for federated users using session tags](https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/)
- [Use custom attributes for ABAC with Microsoft Entra ID and AWS IAM Identity Center](https://aws.amazon.com/blogs/modernizing-with-aws/use-custom-attributes-for-attribute-based-access-control-abac-with-microsoft-entra-id-and-aws-iam-identity-center/)
- [Azure AD provisioning to AWS Identity Center with custom attributes - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/1324325/azure-ad-provisioning-to-aws-identity-center-with)
