# Glossary — Native AWS Mechanisms for Per-Role Linux Identity Mapping in SSM Session Manager

Quick definitions of key terms and concepts referenced in this investigation.

---

## SSMSessionRunAs Tag

An IAM tag with key SSMSessionRunAs whose value specifies the OS user account for SSM Session Manager sessions. SSM checks for this tag on the calling IAM principal (user, role, or STS session). When present, it overrides the runAsDefaultUser in the session preferences document. The tag can be set as an IAM user tag, IAM role tag, or STS session tag (via aws:PrincipalTag).

## IdC ABAC Attributes

User attributes configured in IAM Identity Center's 'Attributes for access control' settings. These attributes are sourced from the IdC identity store (or external IdP via SAML) and are passed as STS session tags (aws:PrincipalTag) when a user assumes any permission set. Attributes are per-user, not per-permission-set.

## AWSReservedSSO_ Protected Roles

IAM roles created by IAM Identity Center in member accounts with names following the pattern AWSReservedSSO_<PermissionSetName>_<uniqueSuffix>. These roles are protected by AWS service-linked role policies and cannot be modified (including tagging) by customers or account administrators.

## ssm:SessionDocumentAccessCheck

A boolean condition key for the ssm:StartSession action. When set to true in an IAM policy, SSM verifies that the caller has permission to use the session document specified in the StartSession request. It gates document access but does not influence RunAs user resolution or document selection.

## Session Preferences Document (SSM-SessionManagerRunShell)

The default SSM document (type Session, sessionType Standard_Stream) that defines account-wide session preferences including runAsEnabled, runAsDefaultUser, logging, and encryption settings. Automatically created during Session Manager setup. Custom documents with different names can be created for per-session preferences.

## RunAs Resolution Precedence

The order in which SSM determines the OS user for a session: (1) SSMSessionRunAs tag on the calling IAM principal, (2) runAsDefaultUser in the session document specified by DocumentName, (3) runAsDefaultUser in the account default SSM-SessionManagerRunShell document. The tag always wins when present.

---

*Back to: [investigation.md](investigation.md)*
