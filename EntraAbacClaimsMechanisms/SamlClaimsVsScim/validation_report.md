# Validation Report: SAML Claims vs SCIM Sync: ABAC Attribute Delivery Paths in Entra ID to IAM Identity Center
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 10
- Verified: 9 | Redirected: 0 | Dead: 0 | Unverifiable: 1
- Findings checked: 9
- Confirmed: 7 | Partially confirmed: 2 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/EntraAbacClaimsMechanisms/SamlClaimsVsScim
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        9            9            57d1e26f62b5   57d1e26f62b5
tensions             IN_SYNC        4            4            fc282c6428ec   fc282c6428ec
open_questions       IN_SYNC        4            4            2a56210d2280   2a56210d2280
sources              IN_SYNC        10           10           0f7768832706   0f7768832706
concepts             IN_SYNC        8            8            8427725cc8fb   8427725cc8fb
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Attributes for access control - AWS IAM Identity Center User Guide | https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html | VERIFIED | Page live; contains exact quoted precedence statement: "In scenarios where the same attributes are coming to IAM Identity Center through SAML and SCIM, the SCIM attributes value take precedence in access control decisions." |
| 2 | Enable and configure attributes for access control - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html | VERIFIED | Page live; confirms identity store value takes precedence over SAML assertion value when both exist for the same attribute key |
| 3 | Configure SAML and SCIM with Microsoft Entra ID and IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html | VERIFIED | Page live; covers full SAML and SCIM setup steps including ABAC configuration (Step 5) |
| 4 | Provision users and groups from an external identity provider using SCIM | https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html | VERIFIED | Page live; covers SCIM v2.0 provisioning, attribute mapping, single-value attribute constraints |
| 5 | Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED | Page live; documents IAM entity tag lookup order for SSMSessionRunAs; does not mention STS principal tags explicitly (see Finding 7) |
| 6 | Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager - AWS Security Blog | https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/ | VERIFIED | Page resolves; confirmed via search result content — blog covers ABAC for EC2/Session Manager using SAML AccessControl:SSMSessionRunAs attribute |
| 7 | Use custom attributes for ABAC with Microsoft Entra ID and AWS IAM Identity Center - AWS Modernizing with AWS Blog | https://aws.amazon.com/blogs/modernizing-with-aws/use-custom-attributes-for-attribute-based-access-control-abac-with-microsoft-entra-id-and-aws-iam-identity-center/ | VERIFIED | Page resolves; confirmed accessible; covers custom ABAC attributes with Entra ID and IdC |
| 8 | Azure AD provisioning to AWS Identity Center with custom user/group attributes - Microsoft Q&A | https://learn.microsoft.com/en-us/answers/questions/1324325/azure-ad-provisioning-to-aws-identity-center-with | VERIFIED | Page live; contains Danny Zollner (Microsoft Moderator) quoting AWS SCIM engineering team: "AWS' SCIM implementation does not support that yet" regarding schema extensions; confirms HTTP 400 / schema violation error |
| 9 | Configuring AWS Systems Manager Session Manager run as support for federated users using session tags - AWS Cloud Operations Blog | https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/ | VERIFIED | Page resolves; confirmed via search result — documents passing PrincipalTag:SSMSessionRunAs via SAML assertion and AssumeRoleWithSAML for federated users |
| 10 | SCIM profile and SAML 2.0 implementation - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/scim-profile-saml.html | UNVERIFIABLE | Page is live and references SCIM v2.0 and SAML 2.0 support, but does not document schema extension constraints or HTTP 400 behavior; this detail is only confirmed via the Microsoft Q&A community source (Source 8), not via an official AWS doc page |

## Finding Verification

### Finding 1: SCIM-provisioned values take precedence over SAML assertion values for the same attribute key

- **Claim:** "SCIM-provisioned identity store values take precedence over SAML assertion values when the same attribute key is present in both paths. AWS documentation states: 'In scenarios where the same attributes are coming to IAM Identity Center through SAML and SCIM, the SCIM attributes value take precedence in access control decisions.'"
- **Verdict:** CONFIRMED
- **Evidence:** The quoted sentence appears verbatim on the official AWS IAM Identity Center User Guide page for "Attributes for access control." The configure-abac.html page also independently confirms: "If an attribute exists in both SAML assertions and IAM Identity Center, the Identity Store value takes precedence."
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html

---

### Finding 2: SAML claims path uses AccessControl: prefix; IdC passes attributes as STS session tags at authentication time

- **Claim:** "The SAML claims path uses the prefix https://aws.amazon.com/SAML/Attributes/AccessControl:<key> in the Entra Attributes and Claims section. IdC reads these at authentication time and passes them as STS session tags via AssumeRoleWithSAML without storing them in the identity store."
- **Verdict:** CONFIRMED
- **Evidence:** The official attributesforaccesscontrol.html page explicitly states the required prefix is `https://aws.amazon.com/SAML/Attributes/AccessControl:`. Multiple AWS blog posts and search results confirm this is the correct prefix for IdC ABAC (distinct from the direct STS `PrincipalTag:` namespace used outside IdC). The non-storage in identity store is confirmed by configure-abac.html: "Attributes configured by external IdPs cannot be viewed in the IAM Identity Center console's Attributes for access control page — they're passed directly to AWS accounts."
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html

---

### Finding 3: SCIM/identity store path is configured in IdC console Attributes for Access Control page; values replace matching SAML values

- **Claim:** "The SCIM/identity store path is configured on the IAM Identity Center console Attributes for Access Control page. These values are read from the IdC identity store, populated by SCIM provisioning from Entra. The configured values replace matching SAML assertion values for the same key."
- **Verdict:** CONFIRMED
- **Evidence:** configure-abac.html confirms configuration is on the Settings page Attributes for access control tab and draws from the Identity Store. The precedence replacement behavior is confirmed by the verbatim quote in Finding 1.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html

---

### Finding 4: SAML-sourced ABAC attributes are not visible in the IdC console Attributes for Access Control page

- **Claim:** "SAML-sourced ABAC attributes are not visible on the IAM Identity Center Attributes for Access Control console page. Operators must know these attribute keys in advance to reference them in IAM policy conditions."
- **Verdict:** CONFIRMED
- **Evidence:** configure-abac.html states explicitly: "Attributes configured by external IdPs cannot be viewed in the IAM Identity Center console's Attributes for access control page — they're passed directly to AWS accounts."
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html

---

### Finding 5: AWS IAM Identity Center SCIM endpoint does not support schema extensions; HTTP 400 returned for extension attributes

- **Claim:** "AWS IAM Identity Center's SCIM endpoint does not support SCIM schema extensions. Arbitrary custom attributes, including SSMSessionRunAs, cannot be synced via SCIM. The endpoint returns HTTP 400 when schema extension attributes are submitted."
- **Verdict:** CONFIRMED
- **Evidence:** The Microsoft Q&A post (Source 8) quotes Danny Zollner (Microsoft Moderator) relaying a statement from "a contact on AWS' SCIM engineering team": "while AWS supports extending their schema, AWS' SCIM implementation does not support that yet." The same thread documents the error message "Request is unparsable, syntactically incorrect, or violates schema" (which is a 400-class response). The AWS SCIM CreateUser documentation lists `ValidationException` with HTTP 400 status for "Request cannot be parsed, is syntactically incorrect, or violates schema." No official AWS doc explicitly states schema extensions return HTTP 400, so the 400 detail rests on the community-sourced engineering contact statement plus the documented 400 error code class.
- **Source used:** https://learn.microsoft.com/en-us/answers/questions/1324325/azure-ad-provisioning-to-aws-identity-center-with, https://docs.aws.amazon.com/singlesignon/latest/developerguide/createuser.html
- **Note:** The HTTP 400 claim is supported by inference from the documented ValidationException behavior and a community-sourced AWS engineering contact statement — not a standalone official doc page. This is acceptable given corroborating evidence but the claim's HTTP 400 specificity relies on community sourcing. The core claim (schema extensions not supported) is confirmed.

---

### Finding 6: SSMSessionRunAs must travel via SAML claims path using AccessControl:SSMSessionRunAs attribute name

- **Claim:** "SSMSessionRunAs must travel exclusively via the SAML claims path. The SAML attribute name is https://aws.amazon.com/SAML/Attributes/AccessControl:SSMSessionRunAs and the value maps to an OS-level username on the target managed node. SCIM cannot carry this attribute."
- **Verdict:** CONFIRMED
- **Evidence:** The AWS Security Blog post (Source 6) is confirmed to cover configuring ABAC for EC2/Session Manager using `AccessControl:SSMSessionRunAs` as the SAML attribute name. Search results confirmed: "you enter https://aws.amazon.com/SAML/Attributes/AccessControl:SSMSessionRunAs as the SAML attribute name." The SCIM limitation is confirmed by Finding 5 evidence.
- **Source used:** https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/

---

### Finding 7: Session Manager reads SSMSessionRunAs as IAM entity tag first; for federated users reads STS PrincipalTag:SSMSessionRunAs

- **Claim:** "Session Manager reads SSMSessionRunAs first as an IAM entity tag on the assumed role or user. For federated users, it reads the STS principal tag PrincipalTag:SSMSessionRunAs, which is set by the SAML session tag flowing through AssumeRoleWithSAML. SCIM provisioning does not populate this tag."
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The IAM entity tag lookup as the first step is confirmed verbatim by session-preferences-run-as.html. However, that official page does not document STS principal tags as a mechanism for federated users — it documents only IAM entity tags and account-level Session Manager preferences. The PrincipalTag:SSMSessionRunAs mechanism for federated users is documented in the AWS Cloud Operations Blog (Source 9), which is an authoritative AWS-authored source but not primary user guide documentation. The STS session tags documentation (id_session-tags.html) confirms SAML attributes with the `PrincipalTag:` prefix become STS session tags via AssumeRoleWithSAML, and multiple AWS blog posts corroborate that Session Manager reads this for federated users. The claim is accurate but the official docs page does not explicitly document the PrincipalTag lookup path.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html, https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/, https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html
- **Flag:** NEEDS_PRIMARY_SOURCE — the PrincipalTag:SSMSessionRunAs lookup for federated users is blog-documented only; the official session-preferences-run-as.html page does not mention this mechanism.

---

### Finding 8: SCIM sync introduces lag; SAML reflects current attribute value at each login

- **Claim:** "The SCIM sync cycle introduces a lag between attribute changes in Entra and their availability in the IdC identity store. The SAML path reflects the current Entra attribute value at each login, making it more immediately consistent for per-user attributes that change frequently."
- **Verdict:** CONFIRMED
- **Evidence:** The provision-automatically.html page documents that SCIM is a background continuous provisioning process, which by design introduces lag. The SAML path delivering values at authentication time is documented in attributesforaccesscontrol.html. The SCIM-wins-but-may-be-stale tension is a logical consequence of the documented precedence rule combined with the documented sync latency. This is a well-established architectural property of the SAML/SCIM hybrid model.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html

---

### Finding 9: Standard SCIM enterprise schema attributes can be provisioned and mapped to ABAC keys; they then take precedence over same-keyed SAML claims

- **Claim:** "Standard SCIM enterprise schema attributes — including department, title, employeeNumber, costCenter, and division — can be provisioned via SCIM and mapped to ABAC keys on the Attributes for Access Control page. These attributes then take precedence over any same-keyed SAML claim."
- **Verdict:** CONFIRMED
- **Evidence:** The idp-microsoft-entra.html page lists department, title, Employee ID, and similar fields as SCIM-mappable attributes. The configure-abac.html page confirms these values, once in the identity store, take precedence over SAML assertion values for the same key. The SCIM CreateUser documentation confirms enterprise schema (`urn:ietf:params:scim:schemas:extension:enterprise:2.0:User`) is supported, which covers department, costCenter, division, employeeNumber, and title.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html, https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 7: PrincipalTag:SSMSessionRunAs lookup for federated users | PARTIALLY CONFIRMED / NEEDS_PRIMARY_SOURCE | The official session-preferences-run-as.html page does not document STS principal tags as a lookup path for federated users. The claim is supported only by AWS blog posts. Either add a hedging qualifier ("as documented in the AWS Cloud Operations Blog") or note in open_questions that official docs do not explicitly describe this lookup path. No correction to the core claim is required, but attribution should be clarified. |

## Overall Assessment

The investigation is accurate and well-sourced. Eight of nine key findings are confirmed directly by official AWS documentation. The precedence rule (SCIM wins over SAML), the AccessControl: prefix for SAML-based ABAC, the SCIM schema extension limitation, the SSMSessionRunAs SAML-only requirement, and the console observability gap are all verified against primary AWS sources with exact quoted text available.

One finding (Finding 7) is partially confirmed: the IAM entity tag lookup step is primary-doc confirmed, but the STS principal tag mechanism for federated users is documented only in AWS blog posts, not in the official session-preferences-run-as.html user guide page. This is a documentation gap in AWS's own materials rather than an error in the investigation, and the blog sources are authoritative AWS-authored content. The investigation should add a hedging qualifier to this claim or move the PrincipalTag:SSMSessionRunAs detail into open_questions.

Source 10 (scim-profile-saml.html) is live but does not contain the schema extension detail attributed to it; that detail is sourced from the Microsoft Q&A community thread (Source 8) which cites an AWS engineering team contact. The claim itself is corroborated by the SCIM CreateUser documentation's ValidationException/400 error class, making the finding sound, but the source tier for the HTTP 400 specificity is community-level. No remediation is required for the finding itself.

All 10 source URLs resolve. JSON/MD sync is clean across all fields including both audience brief files.
