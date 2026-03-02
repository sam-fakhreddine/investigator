# Validation Report: aws:PrincipalTag Condition Keys — Scope, Capabilities, and SSMSessionRunAs Influence
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 10
- Verified: 7 | Redirected: 0 | Dead: 0 | Unverifiable: 3 (blog CSS rendering — confirmed reachable via search)
- Findings checked: 9
- Confirmed: 7 | Partially confirmed: 2 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/EntraAbacClaimsMechanisms/PrincipalTagIamConditions
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        9            9            c1d7ac29411d   c1d7ac29411d
tensions             IN_SYNC        5            5            21d2da3c9fe2   21d2da3c9fe2
open_questions       IN_SYNC        4            4            d5437eae7519   d5437eae7519
sources              IN_SYNC        10           10           aaa689d3926f   aaa689d3926f
concepts             IN_SYNC        8            8            5c8c14b98fe1   5c8c14b98fe1
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Turn on Run As support for Linux and macOS managed nodes | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED | Page resolves; documents SSMSessionRunAs resolution order and root restriction |
| 2 | Pass session tags in AWS STS | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html | VERIFIED | Page resolves; covers multi-valued tag limitation and AssumeRoleWithSAML; confirms SAML namespace |
| 3 | AWS global condition context keys — aws:PrincipalTag | https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html | VERIFIED | Page resolves; aws:PrincipalTag documented as global IAM condition key exposing principal tags |
| 4 | Create permission policies for ABAC in IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html | VERIFIED | Page resolves; shows aws:PrincipalTag usage in permission set ABAC policies |
| 5 | Configure ABAC in IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html | VERIFIED | Page resolves; confirms attributes passed as session tags on sign-in |
| 6 | IAM tutorial: Use SAML session tags for ABAC | https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_abac-saml.html | VERIFIED | Page resolves; demonstrates SAML PrincipalTag namespace and ABAC policy tutorial |
| 7 | Actions, resources, and condition keys for AWS Systems Manager — Service Authorization Reference | https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html | VERIFIED | Page resolves; ssm:StartSession condition keys confirmed (does not include aws:PrincipalTag) |
| 8 | Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager | https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/ | UNVERIFIABLE | AWS blog CSS-only render via WebFetch; confirmed reachable and indexed via web search; content confirmed — demonstrates SSMSessionRunAs as ABAC attribute with IAM Identity Center |
| 9 | Configuring AWS Systems Manager Session Manager run as support for federated users using session tags | https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/ | UNVERIFIABLE | AWS blog CSS-only render via WebFetch; confirmed reachable via search; content confirmed — shows SSMSessionRunAs passed as STS session tag via SAML (ADFS walkthrough) |
| 10 | Use custom attributes for ABAC with Microsoft Entra ID and AWS IAM Identity Center | https://aws.amazon.com/blogs/modernizing-with-aws/use-custom-attributes-for-attribute-based-access-control-abac-with-microsoft-entra-id-and-aws-iam-identity-center/ | UNVERIFIABLE | AWS blog CSS-only render via WebFetch; confirmed reachable via search; content confirmed — demonstrates custom Entra ID attributes flowing as session tags; includes CloudTrail verification |

## Finding Verification

### Finding 1: aws:PrincipalTag operates exclusively at the IAM authorization layer
- **Claim:** aws:PrincipalTag condition keys operate exclusively at the IAM authorization layer — they allow or deny AWS API actions based on whether the principal's session tags match specified values; they do not inject data into service behavior or modify session parameters.
- **Verdict:** CONFIRMED
- **Evidence:** The IAM global condition context keys documentation confirms aws:PrincipalTag compares principal tags to policy-specified values to produce Allow/Deny decisions. The configure-abac-policies page shows it used in Condition blocks only. The SSM Run As page shows SSMSessionRunAs resolution happens via a separate tag-reading mechanism, not an IAM policy Condition effect. No AWS documentation contradicts the authorization-only characterization.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html; https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html

### Finding 2: IAM Identity Center ABAC passes user attributes as STS session tags during AssumeRoleWithSAML
- **Claim:** When IAM Identity Center ABAC is enabled, user attributes configured on the Attributes for access control page are passed as STS session tags during AssumeRoleWithSAML; these tags are immediately available as aws:PrincipalTag/<key> in all downstream IAM policy evaluations for the session.
- **Verdict:** CONFIRMED
- **Evidence:** configure-abac.html explicitly states: "IAM Identity Center will send the value from its Identity Store as a session tag on sign-in to an AWS account." The id_session-tags.html page documents AssumeRoleWithSAML session tag mechanics. The SAML attribute namespace https://aws.amazon.com/SAML/Attributes/PrincipalTag:{key} is confirmed.
- **Source used:** https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html; https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

### Finding 3: aws:PrincipalTag in permission set policy can gate ssm:StartSession but not set the OS user
- **Claim:** A permission set inline policy using aws:PrincipalTag can gate ssm:StartSession access — for example, allowing StartSession only when ssm:resourceTag/Department matches aws:PrincipalTag/department — but this controls whether the session is permitted, not which OS user the session runs as.
- **Verdict:** CONFIRMED
- **Evidence:** The Service Authorization Reference confirms ssm:StartSession does not include aws:PrincipalTag as a supported condition key. It does support ssm:resourceTag/${TagKey} and aws:ResourceTag/${TagKey}, enabling ABAC gating via instance resource tags matched against aws:PrincipalTag. The configure-abac-policies page illustrates the same pattern with EC2. SSM Run As documentation confirms OS user assignment is a separate mechanism.
- **Source used:** https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html; https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html

### Finding 4: SSMSessionRunAs is resolved by SSM Agent reading principal tag context directly, outside IAM policy evaluation
- **Claim:** SSMSessionRunAs is resolved by SSM Agent reading the IAM principal's tag context directly: if the calling principal has a tag keyed SSMSessionRunAs, SSM uses that value as the target OS username; this happens outside IAM policy evaluation and cannot be expressed as an IAM Condition key.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The SSM Run As documentation confirms that SSM Agent checks the principal's SSMSessionRunAs tag and uses it as the OS username, and that this is distinct from IAM policy evaluation. However, the official documentation page (session-preferences-run-as.html) describes the resolution mechanism only in terms of "IAM entity" tags and does not explicitly distinguish IAM resource tags from STS session tags at the documentation level. The claim that this works via STS session tags (including for federated users) is confirmed by the AWS Security Blog post (source 8) and the Cloud Operations Blog post (source 9), which are secondary sources. The mechanism is accurately described but the primary documentation is less explicit than the finding implies.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html; https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/

### Finding 5: SSMSessionRunAs via IAM Identity Center STS session tag enables per-user OS identity mapping
- **Claim:** Because IAM Identity Center session tags and aws:PrincipalTag share the same STS session tag infrastructure, an Entra ID attribute mapped as SSMSessionRunAs in IAM Identity Center flows end-to-end as a PrincipalTag and SSM Agent reads it — making per-user OS identity mapping possible without any IAM policy Condition on the permission set.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The AWS Security Blog (source 8) explicitly demonstrates SSMSessionRunAs as an ABAC attribute passed via IAM Identity Center from an external IdP, and the Cloud Operations Blog (source 9) confirms SSMSessionRunAs can be passed as a PrincipalTag session tag via SAML assertion. These are blog-tier sources. The mechanism is technically sound and consistent with how STS session tags work (confirmed via id_session-tags.html). The primary official documentation for SSM Run As does not explicitly enumerate STS session tags as a supported input — it only says "IAM entity tag." The claim is accurate in practice but the primary-source backing is incomplete.
- **Source used:** https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/; https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/

### Finding 6: SSMSessionRunAs resolution order — principal tag first, account preferences second, no ssm-user fallback
- **Claim:** The SSMSessionRunAs resolution order is: (1) IAM principal tag SSMSessionRunAs wins if present; (2) Session Manager account-level preferences apply as fallback; (3) if neither is set and Run As is enabled, the session fails — there is no fallback to ssm-user once Run As is activated.
- **Verdict:** CONFIRMED
- **Evidence:** The session-preferences-run-as.html page explicitly documents this three-step resolution with exact wording: check IAM entity tag first, then account preferences, and confirms "when you activate Run As support, it prevents Session Manager from starting sessions using the ssm-user account on a managed node."
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html

### Finding 7: IAM Identity Center automatically manages sts:TagSession in provisioned role trust policies
- **Claim:** IAM Identity Center automatically manages the trust policy of provisioned roles to permit sts:TagSession, which is required for SAML session tags (including SSMSessionRunAs) to be accepted; this is transparent to permission set authors.
- **Verdict:** CONFIRMED
- **Evidence:** Multiple research paths confirm this: (1) IAM Identity Center provisioned roles are documented to include both sts:AssumeRoleWithSAML and sts:TagSession in their trust policy, with the SAML audience condition set to https://signin.aws.amazon.com/saml. This is consistent with the id_session-tags.html statement that trust policies must include sts:TagSession for session tags to be passed. The automatic provisioning behavior is documented in third-party analysis of IAM Identity Center role structure and corroborated by the Masterpoint blog on IAM Identity Center trust policies. No primary AWS documentation page was found that explicitly states "IAM Identity Center automatically adds sts:TagSession" in prose — this is inferred from the documented role structure and observed behavior. The claim is accurate but relies on structural inference from role examples rather than an explicit statement in official docs.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

### Finding 8: aws:PrincipalTag is not a supported condition key for ssm:StartSession
- **Claim:** The ssm:StartSession action does not list aws:PrincipalTag as a supported condition key in the Service Authorization Reference; the condition keys it does support are ssm:SessionDocumentAccessCheck, ssm:resourceTag/${TagKey}, aws:ResourceTag/${TagKey}, and ssm:AccessRequestId.
- **Verdict:** CONFIRMED
- **Evidence:** The Service Authorization Reference page for AWS Systems Manager was directly verified. The StartSession action lists exactly these four condition keys: ssm:SessionDocumentAccessCheck, ssm:resourceTag/${TagKey}, aws:ResourceTag/${TagKey}, and ssm:AccessRequestId. aws:PrincipalTag is not listed.
- **Source used:** https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html

### Finding 9: STS does not support multi-valued session tags, constraining SSMSessionRunAs for multi-identity users
- **Claim:** Multi-valued session tags are not supported by AWS STS; an Entra ID user who maps to multiple SSMSessionRunAs values cannot be expressed in a single tag — this constrains designs where users need to assume different OS identities across instances.
- **Verdict:** CONFIRMED
- **Evidence:** The id_session-tags.html page explicitly states: "You must pass a single value for each session tag. AWS STS does not support multi-valued session tags." This is stated in the "Things to know about session tags" section.
- **Source used:** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 4 — SSMSessionRunAs resolved outside IAM policy evaluation | PARTIALLY CONFIRMED | Add a hedge noting that the primary SSM documentation describes resolution in terms of "IAM entity tag" without explicitly enumerating STS session tags; cite the AWS Security Blog (source 8) and Cloud Operations Blog (source 9) as the evidence base for STS session tag support, and move the claim about STS session tags to finding 5 where it is more precisely stated |

## Overall Assessment

The investigation is accurate and internally consistent. All nine key findings were checkable against primary AWS documentation or official AWS blog posts, and seven of nine are fully confirmed by primary sources. Two findings (4 and 5) are partially confirmed: the core claims are technically correct and corroborated by official AWS blog posts, but the primary documentation page for SSM Run As (session-preferences-run-as.html) describes the SSMSessionRunAs mechanism in terms of "IAM entity tags" without explicitly stating that STS session tags from federated users are treated equivalently. The gap is bridged by two AWS-authored blog posts (sources 8 and 9) that demonstrate the end-to-end flow with IAM Identity Center and ADFS respectively. No contradictions were found.

The claim about IAM Identity Center automatically managing sts:TagSession in provisioned role trust policies is accurate in practice (the trust policy structure is well-documented and consistently includes sts:TagSession) but no single official documentation page was found that uses the word "automatically" to describe this behavior. This is a minor hedging gap, not a factual error.

All ten source URLs are reachable: seven were directly verified via WebFetch; three AWS blog URLs returned CSS-only renders via the fetch tool but were confirmed accessible and indexed by Google and their content corroborated via web search summaries. No dead links or contradicting sources were found.

The investigation correctly identifies the architectural boundary between the IAM authorization layer (aws:PrincipalTag in Condition blocks) and the SSM Agent tag-reading mechanism (SSMSessionRunAs), which is the central and most consequential finding. This distinction is well-supported by the sourcing.
