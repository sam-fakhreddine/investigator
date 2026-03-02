# Investigation: IAM Session Policy Mechanics

**Date:** 2026-03-02
**Status:** Complete

---

## Session Policy Mechanics — Key Facts

| Dimension | Detail |
| --- | --- |
| Core principle | Intersection only — session policy can restrict but never expand the role's identity-based permissions |
| STS APIs with Policy param | AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity, GetFederationToken |
| Inline policy size limit | 2,048 plaintext characters (combined with PolicyArns and session tags) |
| Managed policies via PolicyArns | Up to 10 managed policy ARNs per AssumeRole call |
| Packed policy size | Separate binary limit; PackedPolicySize response field shows % consumed; session tags share this budget |
| Role-chaining session cap | 1 hour maximum regardless of role's configured max duration |
| Console role-switch | No session policy support — programmatic API or CLI only |
| Identity Center credential flow | Credentials issued via OIDC device-code flow; no caller-supplied session policy parameter is surfaced |
| Identity Center ABAC | Session tags (attributes) are passed at federation time; these are distinct from session policies |
| Resource-based policy exception | If a resource-based policy grants the session ARN directly, those permissions bypass the session policy filter |
| Explicit deny | An explicit deny in any applicable policy overrides all allows regardless of session policy content |

> Session policies are enforced at the STS credential issuance layer. They apply for the lifetime of the temporary credential only and have no persistence beyond the session.

---

## Question

> How do AWS IAM session policies work mechanically — what is the policy evaluation logic, how do they interact with the STS AssumeRole API, how do they integrate with IAM Identity Center (SSO), and what are the hard limits that constrain their use?

---

## Context

Engineering teams building AWS environments often create a large number of fine-grained IAM roles — one per use case, per team, or per environment. Session policies offer a potential mechanism to reduce this sprawl by applying scoped, dynamic permissions at assume-role time rather than building a separate role per context. Understanding the mechanics is the foundation for evaluating whether this pattern is viable, especially in organizations that use IAM Identity Center as their primary identity layer.

---

## Key Findings

- Session policies are passed as parameters to STS AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity, and GetFederationToken — they are not attached to the role itself and have no existence outside the credential issuance call.
- The effective permission set for a role session is the intersection of the role's identity-based policies and the supplied session policies; a session policy cannot grant permissions the role does not already possess.
- Two separate size constraints apply: a 2,048-character plaintext limit on the combined inline policy and PolicyArns payload, and a separate packed binary format limit that counts session tags in the same budget — a request can fail the packed limit even if it satisfies the plaintext limit.
- Up to 10 managed policy ARNs can be passed via the PolicyArns parameter in a single AssumeRole call, in addition to one inline JSON policy document via the Policy parameter.
- When a resource-based policy grants access to the session ARN (not the role ARN), those permissions are not filtered by the session policy — the bypass applies only when the session ARN itself is the named principal in the resource policy.
- When both a permissions boundary and a session policy are active on the same session, the effective permissions are the three-way intersection of identity-based policy, permissions boundary, and session policy.
- Role chaining — where one assumed role calls AssumeRole again — caps the resulting session at one hour maximum, regardless of the DurationSeconds parameter or the target role's configured maximum session duration.
- The AWS Management Console role-switch documentation does not describe a session policy parameter; all official session policy documentation frames the feature as programmatic or CLI-only, with no console UI path documented.
- IAM Identity Center issues temporary credentials through an OIDC device-code authorization flow and does not expose a session policy parameter to the caller — the permission set inline and managed policies constitute the full permission definition at issuance time.
- IAM Identity Center ABAC passes user directory attributes as session tags at federation time; session tags share the packed policy size budget with any session policies present in a given credential issuance.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Session policy | A JSON IAM policy document (or reference to a managed policy ARN) passed as a parameter at STS credential issuance time. It applies for the lifetime of the temporary credential and restricts — but never expands — the role's existing identity-based permissions. |
| Policy intersection | The fundamental evaluation rule for session policies: only actions that are allowed by BOTH the role's identity-based policy AND the session policy are permitted. Any explicit deny in either policy overrides all allows. |
| Packed policy size | AWS compresses the combination of inline session policy, managed policy ARNs, and session tags into a binary format subject to a separate upper limit. The PackedPolicySize field in STS responses shows consumption as a percentage. Requests fail when this limit is exceeded, independently of the 2,048-character plaintext limit. |
| PolicyArns parameter | An STS API parameter accepting up to 10 managed IAM policy ARNs to include as session policies in a single AssumeRole call. The policies must exist in the same account as the role being assumed. |
| Role chaining | Using temporary credentials obtained from one AssumeRole call to perform a subsequent AssumeRole call. AWS caps all role-chained sessions at a maximum of one hour regardless of configured session duration. |
| Permission set (IAM Identity Center) | An IAM Identity Center construct that defines the permissions a user has in a specific AWS account. A permission set is provisioned as an IAM role in the target account and can include AWS managed policies, customer managed policies, and an inline policy. The permission set's policies are fixed at provisioning time; no caller-supplied session policy is injected at login. |
| OIDC device-code credential flow | The mechanism IAM Identity Center uses to issue temporary AWS credentials. The AWS CLI uses this flow via 'aws configure sso'. The flow results in standard STS temporary credentials scoped to the permission set's role; there is no hook for the caller to supply a session policy during this exchange. |
| Session tags (ABAC) | Key-value attributes passed to STS at assume-role time, used in IAM policy conditions for attribute-based access control. IAM Identity Center passes configured user directory attributes as session tags. Session tags share the packed policy size budget with session policies. |
| Session ARN vs. role ARN in resource policies | A critical distinction in evaluation: if a resource-based policy names the role ARN as principal, the session policy filters those permissions (intersection applies). If the resource-based policy names the session ARN directly, those permissions are added after session creation and are not filtered by the session policy. |
| GetFederationToken | An STS API that issues temporary credentials for an IAM user identity rather than for a role. Session policies are required when using this API; the resulting session cannot exceed the permissions of the calling IAM user and is further scoped by the session policy. Maximum duration is 36 hours. |

---

## Tensions & Tradeoffs

- Session policies enable dynamic permission scoping at call time, which could theoretically replace many fine-grained roles — but the 2,048-character plaintext limit and packed policy size constraint create a hard ceiling on policy complexity that makes them unsuitable for anything beyond simple Allow statements over a narrow action/resource scope.
- Session tags (ABAC) and session policies share the same packed binary size budget; organizations attempting to use both mechanisms simultaneously face a tighter combined limit than either mechanism alone, forcing a trade-off between attribute richness and policy scope.
- The intersection-only constraint makes session policies useful for narrowing access but useless for granting access to a broad role that needs context-specific narrowing only if that context cannot be expressed within the role's own policy — the role must already be over-permissioned relative to the session's need for the session policy to be meaningful.
- IAM Identity Center's credential flow does not accept caller-supplied session policies, which means organizations using Identity Center as the primary access layer cannot inject dynamic session scoping at login time — the permission set definition must be revised at the infrastructure level, not at the session level.
- Role chaining hard-caps sessions at one hour, which conflicts with workflows where a caller uses one assumed role to assume a narrowly scoped role (a pattern that might otherwise use session policies); the one-hour cap applies regardless of how the downstream role is configured.

---

## Open Questions

- Whether AWS will expand the packed policy size budget or decouple session tag consumption from session policy consumption in future STS API versions.
- Whether IAM Identity Center will expose a session policy injection point in a future API version (e.g., a caller-supplied policy at GetRoleCredentials time).
- How the packed policy size limit behaves under heavy session tag usage (e.g., 20+ ABAC attributes passed via Identity Center) and whether this leaves meaningful budget for any session policy payload.
- Whether the resource-based policy session-ARN bypass (where session policies do not filter resource-policy grants to the session ARN) is exploitable in privilege-escalation scenarios — this appears out of scope for the current investigation but surfaces as a material security question.
- Practical upper bound on session policy complexity for real-world use cases: what action and resource scope can realistically fit within 2,048 plaintext characters for a non-trivial policy.

---

## Sources & References

- [AWS IAM User Guide: Session Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session)
- [AWS STS API Reference: AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [AWS STS API Reference: AssumeRoleWithSAML](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html)
- [AWS IAM User Guide: Requesting Temporary Credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html)
- [AWS IAM User Guide: IAM Quotas and Limits](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html)
- [AWS IAM User Guide: Policy Evaluation Logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [AWS IAM User Guide: Permissions Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
- [AWS IAM User Guide: Session Tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html)
- [AWS IAM Identity Center User Guide: Permission Sets](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsets.html)
- [AWS IAM Identity Center User Guide: Attributes for Access Control (ABAC)](https://docs.aws.amazon.com/singlesignon/latest/userguide/attributesforaccesscontrol.html)
- [AWS IAM Identity Center User Guide: Getting Credentials](https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html)
- [AWS IAM User Guide: Switching Roles via Console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)
