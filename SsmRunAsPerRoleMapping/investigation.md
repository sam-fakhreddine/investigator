# Investigation: Per-Role Linux Identity Mapping via SSM Session Manager and IAM Identity Center

**Date:** 2026-02-28
**Status:** Complete

---

## Per-Role RunAs Mapping: Native vs Custom Approaches

| Approach | Feasibility | Complexity | Key Trade-off |
| --- | --- | --- | --- |
| IdC ABAC SSMSessionRunAs tag | Not feasible | None (current state) | Tag is per-user, not per-permission-set; same value sent for all role assumptions |
| Direct tagging of AWSReservedSSO_ roles | Blocked | None (cannot implement) | AWS protects these roles; TagRole is denied |
| Per-document RunAs without ABAC tag | Fragile workaround | Medium | Requires removing ABAC tag entirely; users must specify --document-name on every session |
| Permission set IAM policy (defense-in-depth) | Supplementary only | Low | Can deny mismatched sessions but cannot set or override the RunAs value |
| Lambda session broker | Feasible | High | Solves per-role mapping but introduces audit attribution gap, client workflow change, and new availability dependency |

> No native AWS mechanism allows SSMSessionRunAs to vary by permission set. The Lambda broker is the only architecture that achieves true per-role mapping, at the cost of additional infrastructure and operational complexity.

---

## Question

> Can AWS SSM Session Manager map different Linux usernames based on which IAM Identity Center permission set (role) the user selects, and if not natively, what does a custom broker architecture involve?

---

## Context

The current PoC uses Entra ID extensionAttribute1 mapped through SCIM to IdC ABAC SSMSessionRunAs tags, achieving per-user Linux identity mapping. However, per-user mapping means a user always lands as the same OS user regardless of which permission set they select -- if Alice has SSMSessionRunAs=alice, she is 'alice' whether she picks Admin or Developer. Per-role mapping is needed so that the Linux session identity reflects the access level chosen, enabling least-privilege OS-level separation and cleaner audit trails tied to role context rather than just personal identity.

---

## Key Findings

- SSM Session Manager resolves the RunAs user through a fixed precedence chain: (1) SSMSessionRunAs tag on the calling IAM principal, (2) runAsDefaultUser in the specified session document, (3) runAsDefaultUser in the account default SSM-SessionManagerRunShell document. No native mechanism allows injecting a per-permission-set value into this chain.
- IAM Identity Center ABAC attributes are fundamentally per-user, not per-permission-set. When a user assumes any permission set, IdC sends the same ABAC attribute values as STS session tags. The permission set selection does not influence which attribute values are sent, so SSMSessionRunAs always resolves to the same value for a given user.
- AWSReservedSSO_ roles created by IAM Identity Center are protected resources. AWS denies IAM TagRole operations on these roles, closing off the most direct native approach of tagging each permission set's role with a different SSMSessionRunAs value.
- A per-document workaround exists: separate SSM session documents per role (e.g., SSMRunAs-Admin-Session with runAsDefaultUser=admin), each restricted via IAM policy to the corresponding permission set. This only works if the SSMSessionRunAs ABAC tag is removed entirely, because the tag overrides any document-level runAsDefaultUser setting.
- The per-document workaround degrades user experience: users must specify --document-name on every session start. Without it, SSM falls back to SSM-SessionManagerRunShell. The ssm:SessionDocumentAccessCheck condition key can enforce document specification, but at the cost of usability.
- Permission set inline policies can reference aws:PrincipalTag/SSMSessionRunAs in Condition blocks for defense-in-depth (e.g., deny StartSession unless the tag matches an expected value), but they cannot set or override the tag value -- they provide guardrails, not the actual mapping.
- A Lambda session broker can achieve per-role mapping by intercepting session requests, parsing the caller's AWSReservedSSO_<PermissionSetName>_<suffix> role ARN via STS GetCallerIdentity, and calling SSM StartSession with the appropriate per-role session document.
- The broker only handles session creation (control plane). The SSM WebSocket data channel flows directly between the user's session-manager-plugin and the SSM Agent on the target instance. There is no data-plane latency or throughput impact from the broker.
- StartSession returns SessionId, StreamUrl (WebSocket endpoint), and TokenValue (encrypted auth token). The session-manager-plugin accepts these as its first argument, enabling the broker to return the response and the client to hand it directly to the plugin for session establishment.
- When Lambda calls StartSession on behalf of a user, CloudTrail attributes the event to the Lambda execution role, not the original caller. This creates an audit attribution gap that must be addressed with compensating controls -- the Lambda must log the original caller ARN alongside the SessionId.
- Per-role SSM session documents must be deployed to every member account, adding to the StackSet footprint. IAM policy conditions on session document access (ssm:SessionDocumentAccessCheck) provide defense-in-depth even if the broker is bypassed.
- The session-manager-plugin uses a custom binary framing protocol over WebSocket after the initial JSON authentication handshake. Proxying this through API Gateway WebSocket would require reimplementing the full SSM agent message protocol, making the broker a control-plane-only intermediary by design.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SSMSessionRunAs Tag | An IAM tag with key SSMSessionRunAs whose value specifies the OS user account for SSM sessions. SSM checks for this tag on the calling IAM principal (user, role, or STS session). When present, it overrides the runAsDefaultUser in the session preferences document. |
| IdC ABAC Attributes | User attributes configured in IAM Identity Center's 'Attributes for access control' settings. These are sourced from the IdC identity store and passed as STS session tags (aws:PrincipalTag) when a user assumes any permission set. Attributes are per-user, not per-permission-set. |
| RunAs Resolution Precedence | The order in which SSM determines the OS user for a session: (1) SSMSessionRunAs tag on the calling principal, (2) runAsDefaultUser in the document specified by DocumentName, (3) runAsDefaultUser in the account default SSM-SessionManagerRunShell document. The tag always wins when present. |
| AWSReservedSSO_ Protected Roles | IAM roles created by IAM Identity Center in member accounts with names following AWSReservedSSO_<PermissionSetName>_<uniqueSuffix>. These roles are protected by AWS and cannot be tagged or modified by customers, but the permission set name is extractable from the role ARN. |
| Session Document (Standard_Stream) | An SSM document of type Session that defines session preferences including runAsEnabled, runAsDefaultUser, idleSessionTimeout, and maxSessionDuration. Per-role documents can specify different RunAs users and be restricted to specific permission sets via IAM policy. |
| ssm:SessionDocumentAccessCheck | A boolean condition key for ssm:StartSession that controls whether SSM validates the caller's permission to use the specified session document. Gates document access enforcement but does not influence RunAs user resolution or document selection. |
| StartSession API | SSM API operation that initiates a Session Manager session. Accepts Target, optional DocumentName, Parameters, and Reason. Returns SessionId, StreamUrl (WebSocket endpoint), and TokenValue (encrypted auth token) needed by session-manager-plugin. |
| session-manager-plugin | AWS-provided binary that establishes the WebSocket connection to the SSM data channel. Accepts six positional arguments: StartSession response JSON, region, 'StartSession', profile name, request parameters JSON, and SSM endpoint URL. |
| CloudTrail Attribution Gap | When a Lambda function calls StartSession, CloudTrail records the Lambda execution role as the caller, not the original user. The broker must implement compensating logging to maintain audit traceability. |
| SSM Binary WebSocket Protocol | After the initial JSON authentication handshake, SSM sessions use a custom binary framing protocol over WebSocket. This protocol is implemented by session-manager-plugin and the SSM Agent, making data-plane proxying impractical. |

---

## Tensions & Tradeoffs

- Per-user vs. per-role identity: IdC ABAC attributes are fundamentally per-user. SSM's RunAs tag resolution treats the tag as a property of the calling principal. There is no native seam where permission set identity can influence the RunAs value, creating an architectural mismatch between IdC's identity model and the per-role mapping requirement.
- Tag override vs. document settings: When the SSMSessionRunAs tag is present, it overrides runAsDefaultUser in any session document. The per-document workaround only works if the ABAC tag is removed entirely, forcing a choice between per-user override capability and per-role document-based mapping.
- Audit fidelity vs. architectural simplicity: The Lambda broker decouples the session initiator (Lambda role) from the actual user, breaking CloudTrail attribution. Compensating logging adds complexity but is essential for security compliance.
- Client-side simplicity vs. per-role mapping: Users must invoke a wrapper script that calls the broker API and feeds the response to session-manager-plugin, replacing the standard 'aws ssm start-session' workflow. This is a permanent UX cost for per-role mapping.
- Protected roles vs. direct tagging: AWSReservedSSO_ roles cannot be tagged, closing off the most obvious native approach. This protection exists for good reason (preventing privilege escalation) but blocks a legitimate use case.
- Defense-in-depth vs. operational overhead: IAM policies restricting document access per role provide security guarantees even if the broker is bypassed, but require coordinated management across permission sets, session documents, and member accounts.
- Broker availability vs. session access: The Lambda broker becomes a single point of failure for per-role session initiation. If unavailable, per-role mapping is lost, though fallback to native SSM (without per-role mapping) remains possible.
- Single shared document vs. per-role documents: Modifying a shared SSM document at runtime risks race conditions under concurrent access. Per-role documents are safer but require document lifecycle management across all member accounts via StackSets.

---

## Open Questions

- Could a future AWS feature allow IdC ABAC attributes to be scoped per-permission-set rather than per-user? This would natively solve per-role RunAs mapping. No public roadmap item was found.
- Does the SSM StartSession API actually reject runAsDefaultUser if passed in the Parameters map, or does it silently ignore it? Testing would determine whether a single parameterized document could replace per-role documents.
- What is the exact IAM permission set required on the Lambda execution role to call ssm:StartSession on target instances in member accounts? Cross-account session initiation may require additional trust relationships.
- How does the TokenValue expiry window interact with broker response latency? If Lambda cold-starts add several seconds, does the token remain valid for the client to connect?
- Can the broker architecture work with the AWS Console's built-in Session Manager connect button, or is it strictly limited to CLI/SDK-initiated sessions?
- If the SSMSessionRunAs ABAC attribute is removed for the per-document workaround, does the session still log the correct originating user identity in CloudTrail and Session Manager audit logs?
- Can the AWS CLI session-manager-plugin be configured with a default --document-name per profile, reducing UX friction of the per-document workaround without requiring the full broker?

---

## Sources & References

- [Turn on Run As support for Linux and macOS managed nodes - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Session document schema - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-schema.html)
- [StartSession API Reference - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_StartSession.html)
- [Actions, resources, and condition keys for AWS Systems Manager - Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html)
- [Start a session with a document by specifying session documents in IAM policies - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-specify-session-document.html)
- [Create a Session Manager preferences document (command line) - AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-create-preferences-cli.html)
- [Pass session tags in AWS STS - AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html)
- [Attribute-based access control - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html)
- [Resolve the IAM error Cannot perform the operation on the protected role AWSReservedSSO - AWS re:Post](https://repost.aws/knowledge-center/identity-center-aws-reserved-sso)
- [ABAC checklist - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/abac-checklist.html)
- [start-session CLI Reference - AWS Systems Manager](https://docs.aws.amazon.com/cli/latest/reference/ssm/start-session.html)
- [Referencing permission sets in resource policies - AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html)
- [GetCallerIdentity API Reference - AWS STS](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html)
- [Logging AWS Systems Manager API calls with AWS CloudTrail](https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-cloudtrail-logs.html)
- [AWS SSO and SSMSessionRunAs session tag - Hatem Mahmoud](https://mahmoudhatem.wordpress.com/2020/12/17/aws-sso-and-ssmsessionrunas-session-tag/)
- [Configuring AWS Systems Manager Session Manager run as support for federated users using session tags - AWS Cloud Operations Blog](https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/)
- [Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager - AWS Security Blog](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
- [aws-ssm-session - JavaScript library for SSM sessions (Browser and NodeJS)](https://github.com/bertrandmartel/aws-ssm-session)
- [How to use AWS SSM Session Manager Plugin - DEV Community](https://dev.to/leimd/how-to-use-aws-ssm-session-manager-plugin-33hh)
