# Glossary — IAM Session Policy Mechanics

Quick definitions of key terms and concepts referenced in this investigation.

---

## Session policy

A JSON IAM policy document (or reference to a managed policy ARN) passed as a parameter at STS credential issuance time. It applies for the lifetime of the temporary credential and restricts — but never expands — the role's existing identity-based permissions.

## Policy intersection

The fundamental evaluation rule for session policies: only actions that are allowed by BOTH the role's identity-based policy AND the session policy are permitted. Any explicit deny in either policy overrides all allows.

## Packed policy size

AWS compresses the combination of inline session policy, managed policy ARNs, and session tags into a binary format subject to a separate upper limit. The PackedPolicySize field in STS responses shows consumption as a percentage. Requests fail when this limit is exceeded, independently of the 2,048-character plaintext limit.

## PolicyArns parameter

An STS API parameter accepting up to 10 managed IAM policy ARNs to include as session policies in a single AssumeRole call. The policies must exist in the same account as the role being assumed.

## Role chaining

Using temporary credentials obtained from one AssumeRole call to perform a subsequent AssumeRole call. AWS caps all role-chained sessions at a maximum of one hour regardless of configured session duration.

## Permission set (IAM Identity Center)

An IAM Identity Center construct that defines the permissions a user has in a specific AWS account. A permission set is provisioned as an IAM role in the target account and can include AWS managed policies, customer managed policies, and an inline policy. The permission set's policies are fixed at provisioning time; no caller-supplied session policy is injected at login.

## OIDC device-code credential flow

The mechanism IAM Identity Center uses to issue temporary AWS credentials. The AWS CLI uses this flow via 'aws configure sso'. The flow results in standard STS temporary credentials scoped to the permission set's role; there is no hook for the caller to supply a session policy during this exchange.

## Session tags (ABAC)

Key-value attributes passed to STS at assume-role time, used in IAM policy conditions for attribute-based access control. IAM Identity Center passes configured user directory attributes as session tags. Session tags share the packed policy size budget with session policies.

## Session ARN vs. role ARN in resource policies

A critical distinction in evaluation: if a resource-based policy names the role ARN as principal, the session policy filters those permissions (intersection applies). If the resource-based policy names the session ARN directly, those permissions are added after session creation and are not filtered by the session policy.

## GetFederationToken

An STS API that issues temporary credentials for an IAM user identity rather than for a role. Session policies are required when using this API; the resulting session cannot exceed the permissions of the calling IAM user and is further scoped by the session policy. Maximum duration is 36 hours.

---

*Back to: [investigation.md](investigation.md)*
