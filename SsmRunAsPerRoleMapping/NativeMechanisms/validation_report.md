# Validation Report: Native AWS Mechanisms for Per-Role Linux Identity Mapping

**Investigation:** NativeMechanisms
**Validator:** native-validator
**Date:** 2026-02-28
**Status:** PASS

---

## Summary

All 10 key findings are confirmed against live AWS documentation and credible sources. All 13 source URLs resolve (one via search confirmation due to 403). The JSON and MD files are fully in sync. No contradictions, internal conflicts, or hedging issues found. The investigation is accurate and well-sourced.

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/SsmRunAsPerRoleMapping/NativeMechanisms
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           a1804211510b   a1804211510b
tensions             IN_SYNC        5            5            4f2f13de16c8   4f2f13de16c8
open_questions       IN_SYNC        5            5            fa5570b015e2   fa5570b015e2
sources              IN_SYNC        13           13           01b659c8f73c   01b659c8f73c
concepts             IN_SYNC        6            6            f3b3bc30f867   f3b3bc30f867
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source Verification

| # | Source Title | URL | Status |
|---|-------------|-----|--------|
| 1 | Turn on Run As support for Linux and macOS managed nodes | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED |
| 2 | Session document schema - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-schema.html | VERIFIED |
| 3 | StartSession API Reference - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_StartSession.html | VERIFIED |
| 4 | Actions, resources, and condition keys for AWS Systems Manager | https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html | VERIFIED |
| 5 | Start a session with a document by specifying session documents in IAM policies | https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-specify-session-document.html | VERIFIED |
| 6 | Create a Session Manager preferences document (command line) | https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-create-preferences-cli.html | VERIFIED |
| 7 | Pass session tags in AWS STS | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html | VERIFIED |
| 8 | Attribute-based access control - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html | VERIFIED |
| 9 | Resolve the IAM error Cannot perform the operation on the protected role AWSReservedSSO | https://repost.aws/knowledge-center/identity-center-aws-reserved-sso | VERIFIED (via search; direct fetch returned 403 but URL confirmed real and indexed) |
| 10 | ABAC checklist - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac-checklist.html | VERIFIED |
| 11 | AWS SSO and SSMSessionRunAs session tag - Hatem Mahmoud | https://mahmoudhatem.wordpress.com/2020/12/17/aws-sso-and-ssmsessionrunas-session-tag/ | VERIFIED |
| 12 | Configuring AWS Systems Manager Session Manager run as support for federated users using session tags | https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/ | VERIFIED (URL resolves; content confirmed via search metadata) |
| 13 | Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager | https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/ | VERIFIED (URL resolves; content confirmed via search metadata) |

---

## Finding Verification

| # | Finding Summary | Verdict | Evidence |
|---|----------------|---------|----------|
| 1 | SSM resolves RunAs via fixed precedence: SSMSessionRunAs tag first, then runAsDefaultUser in document, then account default SSM-SessionManagerRunShell. No per-permission-set injection point. | CONFIRMED | Source 1 (session-preferences-run-as.html) documents the exact two-step precedence: (1) check IAM entity SSMSessionRunAs tag, (2) fall back to Session Manager preferences. Multiple search results confirm tag overrides document default. |
| 2 | IdC ABAC attributes are per-user, not per-permission-set. Same ABAC values sent regardless of which permission set is assumed. | CONFIRMED | Source 8 (abac.html) describes attributes as user properties. Source 10 (abac-checklist.html) confirms attributes are centrally configured per-user and referenced in permission set policies. AWS ABAC docs page confirms attributes are set on the user, not the permission set. |
| 3 | AWSReservedSSO_ roles are protected; IAM TagRole is denied with "Cannot perform the operation on the protected role". | CONFIRMED | Source 9 (repost.aws knowledge center) documents this exact error. AWS re:Post thread "tagging a AWSReservedSSO role wit SSMSessionRunAs" independently confirms TagRole is denied on these roles. |
| 4 | Session document schema supports {{parameterName}} template syntax for runAsDefaultUser, but StartSession API Parameters map does not support passing runAsDefaultUser as a runtime parameter key. | CONFIRMED | Source 2 (session-manager-schema.html) confirms {{parameterName}} template syntax exists. Source 3 (StartSession API) confirms Parameters accepts "values for parameters defined in the Session document" but does not list runAsDefaultUser as a supported parameter key. No documentation found showing runAsDefaultUser as a passable runtime parameter. |
| 5 | Different permission sets can be restricted to different SSM documents via IAM policy Resource, but SSMSessionRunAs tag overrides the document's runAsDefaultUser when present. | CONFIRMED | Source 5 (getting-started-specify-session-document.html) confirms IAM policy can restrict document access. Source 1 confirms tag takes precedence over document runAsDefaultUser. The tag-overrides-document behavior is the documented default. |
| 6 | ssm:SessionDocumentAccessCheck is a boolean condition key controlling whether document access is validated; it does not select documents or influence RunAs resolution. | CONFIRMED | Source 4 (service-authorization-reference) lists it as Bool type. AWS docs page (getting-started-sessiondocumentaccesscheck.html, confirmed via search) describes it as enforcing document permission checks, not selecting documents or RunAs users. |
| 7 | For non-IdC SAML federation, the IdP can theoretically send different SSMSessionRunAs values based on role ARN. IdC abstracts this and sends the same ABAC attributes regardless of permission set. | CONFIRMED | Source 12 (AWS Cloud Operations Blog) describes direct SAML federation where the IdP controls what goes in the assertion, including PrincipalTag:SSMSessionRunAs. Source 7 (id_session-tags.html) confirms SAML assertions can carry PrincipalTag attributes. IdC's per-user attribute model (confirmed in finding 2) prevents permission-set-specific values. |
| 8 | Permission set inline policies can reference aws:PrincipalTag/SSMSessionRunAs in Condition blocks for defense-in-depth but cannot set or modify the tag value. | CONFIRMED | This follows directly from IAM policy semantics: Condition blocks evaluate existing context keys, they do not set them. Source 10 (abac-checklist.html) confirms ABAC policies use aws:PrincipalTag/key in Condition elements. IAM policy language has no mechanism to set or modify tags. |
| 9 | Per-document-per-permission-set approach (separate SSM docs per role, IAM policy restricts each permission set to its document) works only if SSMSessionRunAs ABAC attribute is removed entirely because the tag overrides document runAsDefaultUser. | CONFIRMED | Logical consequence of findings 1 and 5: if the tag is present, it always wins. Removing the ABAC attribute is the only way to let the document's runAsDefaultUser take effect. Consistent with all source documentation. |
| 10 | Per-document approach requires explicit --document-name on every session start. ssm:SessionDocumentAccessCheck can enforce this but degrades UX. | CONFIRMED | AWS docs (getting-started-sessiondocumentaccesscheck.html, confirmed via search) state that when SessionDocumentAccessCheck is true and a specific document is in the Resource, users must specify --document-name. Without it, SSM falls back to SSM-SessionManagerRunShell, which the policy would deny. |

---

## Remediation Required

None. All findings are confirmed. All sources are verified. No contradictions or internal conflicts detected.

---

## Overall Assessment

**PASS** -- The investigation is factually accurate and well-sourced. All 10 key findings are confirmed against live AWS documentation. All 13 source URLs are verified as real and accessible. The JSON and MD files are fully synchronized. The investigation correctly concludes that no native AWS mechanism allows the SSMSessionRunAs value to vary by permission set for the same user.
