# Glossary — Per-Role Linux Identity Mapping via SSM Session Manager and IAM Identity Center

Quick definitions of key terms and concepts referenced in this investigation.

---

## SSMSessionRunAs Tag

An IAM tag with key SSMSessionRunAs whose value specifies the OS user account for SSM sessions. SSM checks for this tag on the calling IAM principal (user, role, or STS session). When present, it overrides the runAsDefaultUser in the session preferences document.

## IdC ABAC Attributes

User attributes configured in IAM Identity Center's 'Attributes for access control' settings. These are sourced from the IdC identity store and passed as STS session tags (aws:PrincipalTag) when a user assumes any permission set. Attributes are per-user, not per-permission-set.

## RunAs Resolution Precedence

The order in which SSM determines the OS user for a session: (1) SSMSessionRunAs tag on the calling principal, (2) runAsDefaultUser in the document specified by DocumentName, (3) runAsDefaultUser in the account default SSM-SessionManagerRunShell document. The tag always wins when present.

## AWSReservedSSO_ Protected Roles

IAM roles created by IAM Identity Center in member accounts with names following AWSReservedSSO_<PermissionSetName>_<uniqueSuffix>. These roles are protected by AWS and cannot be tagged or modified by customers, but the permission set name is extractable from the role ARN.

## Session Document (Standard_Stream)

An SSM document of type Session that defines session preferences including runAsEnabled, runAsDefaultUser, idleSessionTimeout, and maxSessionDuration. Per-role documents can specify different RunAs users and be restricted to specific permission sets via IAM policy.

## ssm:SessionDocumentAccessCheck

A boolean condition key for ssm:StartSession that controls whether SSM validates the caller's permission to use the specified session document. Gates document access enforcement but does not influence RunAs user resolution or document selection.

## StartSession API

SSM API operation that initiates a Session Manager session. Accepts Target, optional DocumentName, Parameters, and Reason. Returns SessionId, StreamUrl (WebSocket endpoint), and TokenValue (encrypted auth token) needed by session-manager-plugin.

## session-manager-plugin

AWS-provided binary that establishes the WebSocket connection to the SSM data channel. Accepts six positional arguments: StartSession response JSON, region, 'StartSession', profile name, request parameters JSON, and SSM endpoint URL.

## CloudTrail Attribution Gap

When a Lambda function calls StartSession, CloudTrail records the Lambda execution role as the caller, not the original user. The broker must implement compensating logging to maintain audit traceability.

## SSM Binary WebSocket Protocol

After the initial JSON authentication handshake, SSM sessions use a custom binary framing protocol over WebSocket. This protocol is implemented by session-manager-plugin and the SSM Agent, making data-plane proxying impractical.

---

*Back to: [investigation.md](investigation.md)*
