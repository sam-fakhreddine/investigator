# Investigation: Native AWS Mechanisms for Per-Role Linux Identity Mapping in SSM Session Manager

**Date:** 2026-02-28
**Status:** Complete

---

## Native Mechanism Evaluation Summary

| Mechanism | Can It Vary RunAs by Permission Set? | Why / Why Not |
| --- | --- | --- |
| SSMSessionRunAs tag (IdC ABAC) | No | ABAC attributes are per-user on the IdC identity store object; same tag value is sent regardless of which permission set is assumed |
| SSMSessionRunAs tag on AWSReservedSSO role | No (blocked) | AWSReservedSSO_ roles are protected by AWS; IAM TagRole is denied with 'Cannot perform the operation on the protected role' |
| Per-permission-set session documents via IAM policy | Partial (defense-in-depth only) | IAM policy on each permission set can restrict which SSM document ARN is allowed in ssm:StartSession Resource, but SSM still resolves RunAs from the SSMSessionRunAs tag, not the document, when the tag is present |
| Custom SSM document with runAsDefaultUser parameter | No (race condition or requires Lambda) | runAsDefaultUser supports {{parameter}} syntax in document schema, but StartSession Parameters map does not accept runAsDefaultUser as a key; modifying the shared document at runtime creates race conditions |
| ssm:SessionDocumentAccessCheck condition key | No | Boolean condition that controls whether document access is checked at all; does not select which document or RunAs user to use |
| STS session tags from SAML assertion | No (per-user) | IAM Identity Center sends the same ABAC attribute values for a user regardless of which permission set they select; session tags come from the user's IdC attributes, not the permission set |
| Permission set inline policy with aws:PrincipalTag condition | No (read-only) | Inline policies can reference aws:PrincipalTag/SSMSessionRunAs in Condition blocks for access control, but cannot set or override the tag value; they can only allow or deny based on existing tag values |

> No native AWS mechanism allows the SSMSessionRunAs value to vary by permission set for the same user. The tag is always resolved from the user's identity (IdC user attributes or IAM entity tags), never from the permission set or assumed role.

---

## Question

> Can per-role Linux identity mapping in SSM Session Manager be achieved using native AWS mechanisms -- such as SSM session document preferences, STS session tags from permission sets, SSM StartSession condition keys, or permission set inline policies -- without custom infrastructure like Lambda?

---

## Context

The current PoC uses Entra ID extensionAttribute1 mapped through SCIM to IdC ABAC SSMSessionRunAs tags. This achieves per-user Linux identity mapping via SSM-SessionManagerRunShell with runAsEnabled=true. The SSMSessionRunAs tag is set on the IdC user object, so if alice has SSMSessionRunAs=admin, she gets 'admin' regardless of which permission set she selects. The question is whether there is a native way to make the Linux session user depend on the permission set chosen, not just the user's identity.

---

## Key Findings

- SSM Session Manager resolves the RunAs user through a fixed precedence chain: first it checks whether the calling IAM principal has an SSMSessionRunAs tag (as an IAM user tag, role tag, or STS session tag via aws:PrincipalTag); if not found, it falls back to the runAsDefaultUser value in the account's Session Manager preferences document (SSM-SessionManagerRunShell). There is no mechanism to inject a per-permission-set value into this chain.
- IAM Identity Center ABAC attributes are per-user, not per-permission-set. When a user assumes any permission set, IdC sends the same set of ABAC attribute values (configured in 'Attributes for access control') as STS session tags. The permission set selection does not influence which attribute values are sent. This means SSMSessionRunAs will always resolve to the same value for a given user regardless of which permission set they choose.
- AWSReservedSSO_ roles created by IAM Identity Center are protected resources. AWS denies IAM TagRole operations on these roles with the error 'Cannot perform the operation on the protected role'. This prevents directly tagging each permission set's role with a different SSMSessionRunAs value in member accounts.
- The SSM session document schema supports parameterization of runAsDefaultUser using {{parameterName}} template syntax. However, the StartSession API's Parameters map is designed for document-defined parameters in the properties section (e.g., portNumber for port forwarding), and there is no documented support for passing runAsDefaultUser as a runtime parameter override through the StartSession API.
- Different permission sets can be restricted to different SSM session documents via IAM policy Resource elements (e.g., permission set A only allows arn:aws:ssm:region:account:document/SSMRunAs-Admin-Session). However, when the SSMSessionRunAs tag is present on the calling principal, SSM uses the tag value to determine the RunAs user, overriding the runAsDefaultUser in the document. This means document-level RunAs settings are subordinate to the tag.
- The ssm:SessionDocumentAccessCheck condition key is a boolean that controls whether SSM validates the caller's permission to use the specified session document. It does not select which document to use or influence RunAs user resolution. It serves as a gate for document access enforcement, not a mechanism for per-role identity mapping.
- For non-IdC federation (direct SAML to IAM), the IdP can theoretically include different SSMSessionRunAs values in the SAML assertion based on which role ARN the user selects. However, IAM Identity Center abstracts this -- the IdC-to-AWS SAML flow is not directly configurable by the customer, and the same ABAC attributes are always sent regardless of permission set selection.
- Permission set inline policies can reference aws:PrincipalTag/SSMSessionRunAs in IAM Condition blocks to allow or deny ssm:StartSession based on the tag value. This enables defense-in-depth (e.g., the 'Developer' permission set can deny StartSession unless SSMSessionRunAs matches 'developer'). But the inline policy cannot set or modify the tag value -- it can only gate access based on an already-existing tag.
- An alternative native approach considered was maintaining separate SSM preference documents per role (e.g., SSMRunAs-Admin-Session with runAsDefaultUser=admin) and restricting each permission set's IAM policy to only allow that specific document. This would work only if the SSMSessionRunAs tag is absent from the principal, because the tag overrides the document's runAsDefaultUser. Removing the ABAC SSMSessionRunAs attribute entirely and relying solely on per-document RunAs settings combined with per-permission-set IAM restrictions is a theoretically viable but fragile approach.
- The per-document-per-permission-set approach (finding above) has a critical limitation: if a user starts a session without specifying --document-name, SSM falls back to SSM-SessionManagerRunShell. The ssm:SessionDocumentAccessCheck condition key can enforce that a document must be specified, but the user experience degrades because every session start requires an explicit --document-name flag or a wrapper script.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| SSMSessionRunAs Tag | An IAM tag with key SSMSessionRunAs whose value specifies the OS user account for SSM Session Manager sessions. SSM checks for this tag on the calling IAM principal (user, role, or STS session). When present, it overrides the runAsDefaultUser in the session preferences document. The tag can be set as an IAM user tag, IAM role tag, or STS session tag (via aws:PrincipalTag). |
| IdC ABAC Attributes | User attributes configured in IAM Identity Center's 'Attributes for access control' settings. These attributes are sourced from the IdC identity store (or external IdP via SAML) and are passed as STS session tags (aws:PrincipalTag) when a user assumes any permission set. Attributes are per-user, not per-permission-set. |
| AWSReservedSSO_ Protected Roles | IAM roles created by IAM Identity Center in member accounts with names following the pattern AWSReservedSSO_<PermissionSetName>_<uniqueSuffix>. These roles are protected by AWS service-linked role policies and cannot be modified (including tagging) by customers or account administrators. |
| ssm:SessionDocumentAccessCheck | A boolean condition key for the ssm:StartSession action. When set to true in an IAM policy, SSM verifies that the caller has permission to use the session document specified in the StartSession request. It gates document access but does not influence RunAs user resolution or document selection. |
| Session Preferences Document (SSM-SessionManagerRunShell) | The default SSM document (type Session, sessionType Standard_Stream) that defines account-wide session preferences including runAsEnabled, runAsDefaultUser, logging, and encryption settings. Automatically created during Session Manager setup. Custom documents with different names can be created for per-session preferences. |
| RunAs Resolution Precedence | The order in which SSM determines the OS user for a session: (1) SSMSessionRunAs tag on the calling IAM principal, (2) runAsDefaultUser in the session document specified by DocumentName, (3) runAsDefaultUser in the account default SSM-SessionManagerRunShell document. The tag always wins when present. |

---

## Tensions & Tradeoffs

- Per-user vs. per-role identity: IdC ABAC attributes are fundamentally per-user (set on the identity store user object). SSM's RunAs tag resolution also treats the tag as a property of the calling principal. There is no native seam where the permission set identity can influence the RunAs value without custom infrastructure.
- Tag override vs. document settings: When the SSMSessionRunAs tag is present, it overrides the runAsDefaultUser in any session document. This means the per-document-per-permission-set approach only works if the ABAC SSMSessionRunAs attribute is removed entirely, sacrificing the per-user override capability.
- Protected roles vs. direct tagging: AWSReservedSSO_ roles cannot be tagged, closing off the most obvious native approach (tag each permission set's role with a different SSMSessionRunAs value). This protection exists for good reason (preventing privilege escalation via role modification), but it blocks a legitimate use case.
- User experience vs. document enforcement: Requiring users to always specify --document-name to select the correct RunAs document degrades usability compared to transparent ABAC tag resolution. Wrapper scripts or CLI aliases can compensate, but these are not native AWS mechanisms.
- Defense-in-depth vs. actual enforcement: Permission set inline policies can deny SSM sessions unless the SSMSessionRunAs tag matches an expected value, but they cannot set the tag. This provides guardrails but not the actual per-role mapping -- the mapping must still come from somewhere else.

---

## Open Questions

- Could a future AWS feature allow IdC ABAC attributes to be scoped per-permission-set rather than per-user? This would natively solve the per-role RunAs mapping problem. No public roadmap item or feature request response was found.
- Does the SSM StartSession API actually reject runAsDefaultUser if passed in the Parameters map, or does it silently ignore it? The documentation does not list supported parameter keys for Standard_Stream session type documents. Testing would be needed to confirm.
- If the SSMSessionRunAs ABAC attribute is removed and per-document RunAs is used instead, does the session still log the correct originating user identity in CloudTrail and Session Manager audit logs?
- Can the AWS CLI session-manager-plugin be configured with a default --document-name per profile, avoiding the need for users to specify it manually on every session start?
- For non-IdC SAML federation (direct to IAM), could an IdP be configured to include different SSMSessionRunAs values in SAML assertions based on the selected role ARN? This would be a native-adjacent approach but is outside the IdC model.

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
- [AWS SSO and SSMSessionRunAs session tag - Hatem Mahmoud](https://mahmoudhatem.wordpress.com/2020/12/17/aws-sso-and-ssmsessionrunas-session-tag/)
- [Configuring AWS Systems Manager Session Manager run as support for federated users using session tags - AWS Cloud Operations Blog](https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/)
- [Configure AWS IAM Identity Center ABAC for EC2 instances and Systems Manager Session Manager - AWS Security Blog](https://aws.amazon.com/blogs/security/configure-aws-sso-abac-for-ec2-instances-and-systems-manager-session-manager/)
