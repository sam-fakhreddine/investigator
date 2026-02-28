# Validation Report

**Investigation:** Per-Role Linux Identity Mapping via SSM Session Manager and IAM Identity Center
**Date:** 2026-02-28
**Validator:** rollup-validator
**Verdict:** PASS

---

## 1. JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/SsmRunAsPerRoleMapping
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        12           12           74b07870f622   74b07870f622
tensions             IN_SYNC        8            8            3643c40bfb52   3643c40bfb52
open_questions       IN_SYNC        7            7            93dfa3598799   93dfa3598799
sources              IN_SYNC        19           19           b00f9e853ce3   b00f9e853ce3
concepts             IN_SYNC        10           10           6a98b732b4f6   6a98b732b4f6
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## 2. Source Verification

| # | Source Title | URL | Tier | Status |
|---|-------------|-----|------|--------|
| 1 | Turn on Run As support for Linux and macOS managed nodes | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | official_doc | VERIFIED |
| 2 | Session document schema - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-schema.html | official_doc | VERIFIED |
| 3 | StartSession API Reference - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_StartSession.html | official_doc | VERIFIED |
| 4 | Actions, resources, and condition keys for AWS Systems Manager | https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html | official_doc | VERIFIED |
| 5 | Start a session with a document by specifying session documents in IAM policies | https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-specify-session-document.html | official_doc | VERIFIED |
| 6 | Create a Session Manager preferences document (command line) | https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-create-preferences-cli.html | official_doc | VERIFIED |
| 7 | Pass session tags in AWS STS | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html | official_doc | VERIFIED |
| 8 | Attribute-based access control - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html | official_doc | VERIFIED |
| 9 | Resolve the IAM error Cannot perform the operation on the protected role AWSReservedSSO | https://repost.aws/knowledge-center/identity-center-aws-reserved-sso | official_doc | VERIFIED (via web search; direct fetch returned 403 but URL resolves and content confirmed via search results and re:Post question threads) |
| 10 | ABAC checklist - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/abac-checklist.html | user_guide | VERIFIED |
| 11 | start-session CLI Reference - AWS Systems Manager | https://docs.aws.amazon.com/cli/latest/reference/ssm/start-session.html | official_doc | VERIFIED |
| 12 | Referencing permission sets in resource policies - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html | official_doc | VERIFIED |
| 13 | GetCallerIdentity API Reference - AWS STS | https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html | official_doc | VERIFIED |
| 14 | Logging AWS Systems Manager API calls with AWS CloudTrail | https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-cloudtrail-logs.html | official_doc | VERIFIED |
| 15 | AWS SSO and SSMSessionRunAs session tag - Hatem Mahmoud | https://mahmoudhatem.wordpress.com/2020/12/17/aws-sso-and-ssmsessionrunas-session-tag/ | blog | VERIFIED |
| 16 | Configuring AWS Systems Manager Session Manager run as support for federated users using session tags | https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/ | blog | VERIFIED |
| 17 | Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager | https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/ | blog | VERIFIED |
| 18 | aws-ssm-session - JavaScript library for SSM sessions | https://github.com/bertrandmartel/aws-ssm-session | community | VERIFIED |
| 19 | How to use AWS SSM Session Manager Plugin - DEV Community | https://dev.to/leimd/how-to-use-aws-ssm-session-manager-plugin-33hh | community | VERIFIED |

**Source summary:** 19/19 VERIFIED

---

## 3. Finding Verification

| # | Finding (abbreviated) | Verdict | Evidence |
|---|----------------------|---------|----------|
| 1 | SSM RunAs resolution precedence: (1) SSMSessionRunAs tag, (2) runAsDefaultUser in specified document, (3) runAsDefaultUser in SSM-SessionManagerRunShell | CONFIRMED | Source 1 documents the two-step precedence (tag on principal, then account preferences). Source 2 confirms runAsDefaultUser in session documents. Source 6 confirms SSM-SessionManagerRunShell as the default document name. Consistent with NativeMechanisms finding 1. |
| 2 | IdC ABAC attributes are per-user, not per-permission-set; same values sent regardless of permission set | CONFIRMED | Source 8 describes ABAC attributes as per-user properties sent as session tags. Source 10 (ABAC checklist) shows attributes are configured on user objects. No mechanism exists to scope attributes per-permission-set. Consistent with NativeMechanisms finding 2. |
| 3 | AWSReservedSSO_ roles are protected; TagRole operations denied | CONFIRMED | Source 9 (re:Post) explicitly confirms the "Cannot perform the operation on the protected role" error. Web search confirms TagRole is denied on these roles. A dedicated re:Post question about tagging AWSReservedSSO roles with SSMSessionRunAs confirms this. Consistent with NativeMechanisms finding 3. |
| 4 | Per-document workaround: separate SSM documents per role, restricted by IAM policy; only works if SSMSessionRunAs tag is removed | CONFIRMED | Source 1 confirms tag overrides document runAsDefaultUser. Source 5 describes restricting documents via IAM policy. The logical conclusion that the tag must be absent for document RunAs to take effect follows directly. Consistent with NativeMechanisms finding 9. |
| 5 | Per-document workaround degrades UX: users must specify --document-name; ssm:SessionDocumentAccessCheck can enforce it | CONFIRMED | Source 11 (CLI reference) shows --document-name is optional and defaults to shell. Source 4 confirms ssm:SessionDocumentAccessCheck as a boolean condition key. Consistent with NativeMechanisms finding 10. |
| 6 | Permission set inline policies can reference aws:PrincipalTag/SSMSessionRunAs for defense-in-depth but cannot set/override the tag | CONFIRMED | Source 7 confirms session tags become aws:PrincipalTag values. IAM Condition blocks can only evaluate, not modify, tag values -- this is fundamental IAM behavior. Consistent with NativeMechanisms finding 8. |
| 7 | Lambda broker can achieve per-role mapping by parsing AWSReservedSSO_ role ARN via GetCallerIdentity and calling StartSession with per-role document | CONFIRMED | Source 12 documents the AWSReservedSSO_<PermSetName>_<suffix> naming convention, confirming permission set name is extractable. Source 13 confirms GetCallerIdentity requires no permissions and returns caller ARN. Source 3 confirms StartSession accepts DocumentName. Consistent with LambdaSessionBroker findings 1, 4. |
| 8 | Broker only handles control plane; WebSocket data channel flows directly between plugin and SSM Agent | CONFIRMED | Source 3 confirms StartSession returns StreamUrl (WebSocket endpoint). Source 18 (aws-ssm-session library) and Source 19 (DEV article) confirm the plugin connects directly to the WebSocket. Consistent with LambdaSessionBroker finding 6. |
| 9 | StartSession returns SessionId, StreamUrl, TokenValue; session-manager-plugin accepts these as first argument | CONFIRMED | Source 3 explicitly documents all three return values. Source 19 (DEV article) confirms the plugin's six positional arguments with the StartSession response JSON as the first. Consistent with LambdaSessionBroker findings 2, 3. |
| 10 | CloudTrail attributes StartSession to Lambda execution role, not original caller; compensating logging required | CONFIRMED | Source 14 confirms StartSession generates CloudTrail entries attributed to the calling principal. When Lambda calls StartSession, the calling principal is the Lambda execution role. This is standard CloudTrail behavior. Consistent with LambdaSessionBroker finding 5. |
| 11 | Per-role session documents must be deployed to every member account; IAM policy conditions provide defense-in-depth | CONFIRMED | Source 5 describes IAM policy restrictions on session documents. Per-account document deployment follows from SSM's account-scoped document model. Consistent with LambdaSessionBroker finding 8. |
| 12 | session-manager-plugin uses custom binary framing protocol over WebSocket; proxying through API Gateway would require reimplementation | CONFIRMED | Source 18 (aws-ssm-session library) documents the binary frame structure: HeaderLength (4 bytes), MessageType (32 bytes), SchemaVersion (4 bytes), CreatedDate (8 bytes), SequenceNumber (8 bytes), Flags (8 bytes). The protocol is custom, not standard WebSocket text/binary frames. Consistent with LambdaSessionBroker finding 7. |

**Finding summary:** 12/12 CONFIRMED

---

## 4. Cross-Check: Rollup vs Sub-Investigations

| Check | Result |
|-------|--------|
| Rollup findings 1-6 accurately represent NativeMechanisms findings | CONSISTENT -- rollup findings on RunAs precedence, ABAC per-user nature, protected roles, per-document workaround, document UX degradation, and defense-in-depth policy all match NativeMechanisms findings 1-3, 5, 8-10 |
| Rollup findings 7-12 accurately represent LambdaSessionBroker findings | CONSISTENT -- rollup findings on broker architecture, control-plane-only design, StartSession response handoff, CloudTrail attribution gap, StackSet deployment, and binary protocol all match LambdaSessionBroker findings 1-8 |
| Rollup quick_reference table consistent with sub-investigations | CONSISTENT -- all five rows reflect conclusions documented in sub-investigations |
| Rollup tensions consistent with sub-investigation tensions | CONSISTENT -- all 8 tensions are either direct carries or logical merges from the 5 NativeMechanisms tensions + 5 LambdaSessionBroker tensions |
| Rollup open questions consistent with sub-investigations | CONSISTENT -- all 7 open questions appear in or are derived from sub-investigation open questions |
| Rollup sources are superset of sub-investigation sources | CONSISTENT -- NativeMechanisms has 13 sources, LambdaSessionBroker has 10 sources, rollup has 19 sources (union with duplicates removed) |
| No contradictions between rollup and sub-investigations | NONE FOUND |

---

## 5. Additional Checks

| Check | Result |
|-------|--------|
| INTERNAL_CONFLICT | NONE -- findings are internally consistent; no finding contradicts another |
| NEEDS_PRIMARY_SOURCE | NONE -- all findings cite official AWS documentation or verifiable community sources |
| CONFIRM_OR_HEDGE | NONE -- findings use appropriate confidence levels; open questions are clearly separated |

---

## 6. Verdict

**PASS**

- Sync check: IN_SYNC
- Sources: 19/19 VERIFIED
- Findings: 12/12 CONFIRMED
- Cross-check with sub-investigations: CONSISTENT, no contradictions
- No internal conflicts, no unverifiable claims
