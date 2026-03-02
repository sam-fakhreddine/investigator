# Glossary — IAM Session Policy Real-World Constraints — Policy Size Limits, Tooling Gaps, Audit and Visibility

Quick definitions of key terms and concepts referenced in this investigation.

---

## Session Policy

An IAM policy passed as a parameter to AssumeRole, AssumeRoleWithSAML, AssumeRoleWithWebIdentity, or GetFederationToken that narrows the effective permissions of the resulting temporary session. Session policies cannot grant more permissions than the role's identity-based policy permits. Either one inline JSON document (Policy parameter) or up to 10 managed policy ARNs (PolicyArns parameter), or both, may be passed.

## PackedPolicySize

A percentage value returned in the STS AssumeRole response indicating how close the combined inline session policy, managed policy ARNs, and session tags are to an internal packed binary size ceiling. The actual byte ceiling is not published by AWS. Exceeding 100% results in a PackedPolicyTooLarge error, which can occur even when the 2,048-character plaintext limit has not been reached.

## Intersection Model (Session Policy Evaluation)

The permission evaluation rule applied when a session policy is present: effective permissions equal the intersection of the IAM role's identity-based policies and the session policy. An explicit deny in either layer overrides any allow. Session policies do not union with role policies.

## GetFederationToken

An STS API that issues temporary credentials scoped to an IAM user's permissions. Unlike AssumeRole, passing a session policy to GetFederationToken is mandatory, not optional. The resulting credentials cannot call any IAM API operations or other STS operations except GetCallerIdentity.

## IAM Identity Center GetRoleCredentials

The IAM Identity Center portal API that issues temporary credentials for a role assignment. It accepts exactly three parameters (accessToken, accountId, roleName) and has no Policy parameter, making it structurally incompatible with session policy attachment. Credentials issued through this path carry only the permissions of the configured permission set.

## SimulatePrincipalPolicy / SimulateCustomPolicy

IAM API operations and the corresponding console tool that evaluate how policies apply to a set of actions and resources. Neither operation accepts a session policy as a named input type; session policy intersection cannot be modeled in the simulator without workarounds.

## PackedPolicyTooLarge

An STS error returned when the packed binary representation of session policies, managed policy ARNs, and session tags exceeds the internal ceiling. The error message reports the current percentage of the budget consumed. Resolution requires reducing inline policy size, shortening session tag values, or removing tags.

## Role Consolidation Strategy

An IAM architecture pattern where multiple fine-grained roles are replaced by fewer broad base roles, with dynamic scoping applied at assumption time via session policies. The pattern reduces role count but shifts complexity to policy generation, transmission, and auditing at the call site.

---

*Back to: [investigation.md](investigation.md)*
