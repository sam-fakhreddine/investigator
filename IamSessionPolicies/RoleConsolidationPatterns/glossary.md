# Glossary — IAM Role Consolidation Patterns Using Session Policies and IAM Identity Center

Quick definitions of key terms and concepts referenced in this investigation.

---

## Session Policy

An optional JSON policy document (or set of up to 10 managed policy ARNs) passed as a parameter to STS AssumeRole, AssumeRoleWithSAML, or AssumeRoleWithWebIdentity. The effective session permissions are the intersection of the role's identity-based policies and the session policy. Session policies cannot grant permissions beyond what the role itself allows.

## Broad Base Role

An IAM role with a relatively permissive set of policies intended to cover multiple use cases. In a consolidation pattern, a single such role is assumed by multiple callers, each supplying a narrowing session policy to scope down to their specific use case. The AWS Security Blog documents EC2Admin as a concrete example of this pattern.

## GetRoleCredentials API

The IAM Identity Center portal API used by the AWS access portal and AWS CLI sso login to issue temporary credentials for a user's assigned permission set. Accepts only accessToken, accountId, and roleName — no session policy parameter exists. This is the structural constraint that blocks the broad-base-role pattern from operating through Identity Center's standard credential path.

## Permission Set

An IAM Identity Center construct that defines a collection of IAM policies. When assigned to a user or group for an account, Identity Center provisions a corresponding IAM role in that account and attaches the permission set's policies to it. Users assume this role through GetRoleCredentials, not through direct STS calls.

## Role Chaining

The pattern of using credentials from one assumed role to assume a second role. When a chain involves two separate role assumptions, the session duration of the second role is hard-capped at 1 hour regardless of the role's or permission set's MaxSessionDuration. Relevant because the Identity Center credentials + second AssumeRole workaround produces a chained session subject to this limit.

## ABAC (Attribute-Based Access Control) via Session Tags

An Identity Center-native mechanism where user attributes (from the configured identity source such as Entra ID or Okta) are passed as session tags during authentication. Permission set policies reference these tags via the aws:PrincipalTag condition key. Enables a single permission set to produce differentiated access based on user attributes, without requiring caller-supplied session policies.

## PackedPolicySize

A response element returned by STS that indicates as a percentage how close a request's combined session policy, session tags, and managed policy ARNs are to the binary packed limit. The plaintext combined limit is 2,048 characters, but a separate binary packing limit can reject requests that meet the plaintext requirement. Requests failing the binary limit return a PackedPolicyTooLarge HTTP 400 error.

---

*Back to: [investigation.md](investigation.md)*
