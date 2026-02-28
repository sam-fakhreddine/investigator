# Validation Report: Lambda-Based Session Broker for SSM Per-Role Linux Identity

**Investigation:** LambdaSessionBroker
**Date validated:** 2026-02-28
**Validator:** claude-opus-4-6

---

## Summary

All 10 source URLs are live and accessible. All 10 key findings are confirmed against official AWS documentation and community sources. JSON and MD are in sync. No remediation required.

**Overall verdict: PASS**

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/SsmRunAsPerRoleMapping/LambdaSessionBroker
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           857d701549c6   857d701549c6
tensions             IN_SYNC        5            5            b195d26018db   b195d26018db
open_questions       IN_SYNC        5            5            8ed003f5b508   8ed003f5b508
sources              IN_SYNC        10           10           5051223b3b9d   5051223b3b9d
concepts             IN_SYNC        6            6            171275f1cc62   171275f1cc62
brief_leadership.md  IN_SYNC

Result: IN_SYNC
```

---

## Source Verification

| # | Source Title | URL | Status |
|---|-------------|-----|--------|
| 1 | StartSession API Reference - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_StartSession.html | VERIFIED |
| 2 | Session document schema - AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-schema.html | VERIFIED |
| 3 | Turn on Run As support for Linux and macOS managed nodes | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED |
| 4 | start-session CLI Reference - AWS Systems Manager | https://docs.aws.amazon.com/cli/latest/reference/ssm/start-session.html | VERIFIED |
| 5 | Referencing permission sets in resource policies - AWS IAM Identity Center | https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html | VERIFIED |
| 6 | Start a session with a document by specifying session documents in IAM policies | https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-specify-session-document.html | VERIFIED |
| 7 | aws-ssm-session - JavaScript library for SSM sessions | https://github.com/bertrandmartel/aws-ssm-session | VERIFIED |
| 8 | How to use AWS SSM Session Manager Plugin - DEV Community | https://dev.to/leimd/how-to-use-aws-ssm-session-manager-plugin-33hh | VERIFIED |
| 9 | GetCallerIdentity API Reference - AWS STS | https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html | VERIFIED |
| 10 | Logging AWS Systems Manager API calls with AWS CloudTrail | https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-cloudtrail-logs.html | VERIFIED |

---

## Finding Verification

| # | Finding (abbreviated) | Verdict | Evidence |
|---|----------------------|---------|----------|
| 1 | StartSession API accepts DocumentName parameter; each document can set runAsEnabled/runAsDefaultUser for programmatic control of Linux user | CONFIRMED | StartSession API reference confirms DocumentName is an optional parameter. Session document schema confirms runAsEnabled (boolean, required) and runAsDefaultUser (string) as inputs for Standard_Stream documents. |
| 2 | StartSession returns SessionId, StreamUrl (WebSocket to ssmmessages.\<region\>.amazonaws.com), and TokenValue (encrypted short-lived auth token) | CONFIRMED | API reference confirms all three return values. Example response shows StreamUrl format as `wss://ssmmessages.{region}.amazonaws.com/v1/data-channel/{session-id}?role=publish_subscribe`. TokenValue described as 0-300 character encrypted token valid only for connection establishment. |
| 3 | session-manager-plugin accepts StartSession response JSON as first arg, followed by region, literal "StartSession", CLI profile name (can be empty), request parameters JSON, and SSM endpoint URL | CONFIRMED | DEV Community article and session-manager-plugin GitHub repo confirm six positional arguments in exactly this order: (1) StartSession response JSON, (2) region, (3) "StartSession", (4) profile name, (5) parameters JSON, (6) SSM endpoint URL. |
| 4 | IAM Identity Center creates roles named AWSReservedSSO\_\<PermissionSetName\>\_\<uniqueSuffix\>; Lambda can parse permission set name from caller ARN via STS GetCallerIdentity (requires no IAM permissions) | CONFIRMED | IAM Identity Center documentation confirms role naming format `AWSReservedSSO_permission-set-name_unique-suffix`. STS GetCallerIdentity documentation explicitly states "No permissions are required to perform this operation" and confirms it returns the assumed role ARN. |
| 5 | When Lambda calls StartSession, CloudTrail attributes event to Lambda execution role, not original caller; compensating controls needed | CONFIRMED | CloudTrail userIdentity documentation confirms that API calls made by a Lambda function are attributed to the Lambda execution role. The original invoker's identity is recorded via sourceIdentity/sourceArn context fields but is not the primary caller identity in the SSM event. Compensating logging is the standard mitigation. |
| 6 | WebSocket data channel flows directly between session-manager-plugin and SSM Agent; Lambda broker not in data path after session creation | CONFIRMED | StartSession API returns a StreamUrl (WebSocket URL) that the client plugin connects to directly. The broker pattern only calls the StartSession API (control plane). The data channel is a direct WebSocket between client plugin and SSM Agent via ssmmessages endpoint. No proxy intermediary is described in any documentation. |
| 7 | session-manager-plugin binary protocol uses custom binary framing with HeaderLength (4 bytes), MessageType (32 bytes), SchemaVersion (4 bytes), CreatedDate (8 bytes), SequenceNumber (8 bytes), and Flags (8 bytes) | CONFIRMED | The aws-ssm-session JavaScript library (bertrandmartel/aws-ssm-session) documents the binary message format. Web search results confirm header fields including headerLength (4 bytes), MessageType (32 bytes UTF-8), SchemaVersion (4 bytes), createdDate (8 bytes), sequenceNumber (8 bytes long integer), flags (8 bytes), plus additional fields (messageId 16 bytes, payloadDigest 32 bytes, payloadType 4 bytes, payloadLength 4 bytes). |
| 8 | Alternative of modifying shared SSM-SessionManagerRunShell per-request creates race conditions; separate named documents per role are safer | CONFIRMED | SSM-SessionManagerRunShell is confirmed as the shared preferences document used by all sessions when no DocumentName is specified. Modifying it per-request for concurrent users would indeed create race conditions. The StartSession API accepts DocumentName for specifying custom session documents, confirming that separate per-role documents are the correct approach. |
| 9 | IAM policy conditions can restrict which session documents a role can use via ssm:SessionDocumentAccessCheck condition key | CONFIRMED | AWS documentation page "Enforce a session document permission check for the AWS CLI" confirms the `ssm:SessionDocumentAccessCheck` condition key exists and is used with `BoolIfExists`. When set to true, users must specify `--document-name` and have explicit IAM access to that document. This provides the defense-in-depth described in the finding. |
| 10 | session-manager-plugin must be installed on client; no AWS-provided mechanism to establish SSM session purely via API without plugin (or reimplementation like aws-ssm-session JS library) | CONFIRMED | All AWS documentation for Session Manager requires the session-manager-plugin for interactive sessions. The StartSession API alone only provides the WebSocket URL and token; establishing the actual terminal session requires implementing the binary protocol. The aws-ssm-session library (bertrandmartel/aws-ssm-session) is confirmed as a community reimplementation of this protocol for browser/NodeJS. |

---

## Remediation Required

None. All findings are confirmed. All sources are live. JSON and MD are in sync.

---

## Overall Assessment

**PASS** -- The investigation is factually accurate. All 10 key findings are confirmed against primary AWS documentation and verified community sources. All 10 source URLs resolve correctly. No internal conflicts, missing primary sources, or hedging issues were identified. The concepts, tensions, and open questions are consistent with the verified findings.
