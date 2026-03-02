# Glossary — IAM Session Policies and Role Sprawl Reduction in AWS with IAM Identity Center

Quick definitions of key terms and concepts referenced in this investigation.

---

## Session policy

A JSON IAM policy document (or reference to up to 10 managed policy ARNs) passed as a parameter at STS credential issuance time via AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity, or GetFederationToken. Applies for the lifetime of the temporary credential; restricts but never expands the role's existing identity-based permissions. The intersection with the role's policies is the sole effective permission set for the session.

## GetRoleCredentials API

The IAM Identity Center portal API used by the AWS access portal and AWS CLI sso login to issue temporary credentials for a permission set assignment. Accepts only three parameters: accessToken, accountId, and roleName. Has no Policy or PolicyArns parameter. This API design is the structural constraint that makes session policy injection unavailable to Identity Center-mediated access.

## Broad base role

An IAM role with a relatively permissive set of policies intended to serve multiple use cases. In a consolidation pattern, a single such role is assumed by multiple callers, each supplying a narrowing session policy at assume-role time. This pattern is viable only for direct STS callers; it is not available through Identity Center's standard credential path.

## ABAC (Attribute-Based Access Control) via session tags

An Identity Center-native mechanism where user directory attributes are propagated as session tags during authentication. Permission set policies reference these tags via aws:PrincipalTag condition keys matched against resource tags. Enables a single permission set to differentiate access for multiple users without caller-supplied session policies, but cannot restrict the action namespace the way an inline session policy can. Session tags share the packed binary size budget with session policies.

## PackedPolicySize

A percentage value returned in the STS AssumeRole response indicating how close the combined inline session policy, managed policy ARNs, and session tags are to an internal packed binary size ceiling. The actual byte ceiling is not published by AWS. Exceeding 100% results in a PackedPolicyTooLarge HTTP 400 error, which can occur even when the 2,048-character plaintext limit has not been reached. Unpredictable when ABAC session tags are also in use.

## Role chaining

Using temporary credentials from one assumed role to call AssumeRole again. AWS caps the resulting session at 1 hour maximum regardless of the configured MaxSessionDuration on the target role or the permission set's session duration (up to 12 hours). Relevant because the Identity Center credentials + second AssumeRole workaround for session policy injection produces a chained session subject to this ceiling.

## Permission set (IAM Identity Center)

An IAM Identity Center construct that defines a collection of IAM policies provisioned as an IAM role in each assigned account. Permission set policies are fixed at provisioning time; no caller-supplied session policy is injected at login. Role proliferation shifts from IAM to the permission set layer — ABAC reduces this by allowing one permission set to serve users with differentiated access based on attributes.

## Policy intersection

The fundamental evaluation rule for session policies: only actions allowed by both the role's identity-based policy and the session policy are permitted. When a permissions boundary is also active, effective permissions are the three-way intersection. An explicit deny in any layer overrides all allows. Session policies do not union with role policies.

---

*Back to: [investigation.md](investigation.md)*
