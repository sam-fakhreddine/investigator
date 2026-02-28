# Glossary — Lambda-Based Session Broker for SSM Per-Role Linux Identity

Quick definitions of key terms and concepts referenced in this investigation.

---

## StartSession API

SSM API operation (POST to AmazonSSM.StartSession) that initiates a Session Manager session. Accepts Target (instance ID), optional DocumentName, Parameters, and Reason. Returns SessionId, StreamUrl (WebSocket endpoint), and TokenValue (encrypted auth token).

## Session Document (Standard_Stream)

An SSM document of type Session that defines session preferences. Key inputs include runAsEnabled (boolean), runAsDefaultUser (OS username), idleSessionTimeout, and maxSessionDuration. The document name is passed via the DocumentName parameter of StartSession.

## session-manager-plugin

AWS-provided binary that establishes the WebSocket connection to the SSM data channel. Invoked with six positional arguments: StartSession response JSON, region, 'StartSession', profile name, request parameters JSON, and SSM endpoint URL.

## AWSReservedSSO_ Role Naming

IAM Identity Center creates roles named AWSReservedSSO_<PermissionSetName>_<uniqueSuffix> in each member account when a permission set is assigned. The permission set name is extractable from the role ARN via string parsing.

## SSM Binary WebSocket Protocol

After the initial JSON authentication handshake (sending TokenValue), SSM sessions switch to a custom binary framing protocol with fixed-width header fields. This protocol is implemented by the session-manager-plugin and the SSM Agent.

## CloudTrail Attribution Gap

When a Lambda function calls StartSession, CloudTrail records the Lambda execution role as the caller. The original user identity is not propagated to the SSM session audit trail, creating an attribution gap that must be addressed with compensating controls.

---

*Back to: [investigation.md](investigation.md)*
