# Investigation: IAM Role Consolidation Patterns Using Session Policies and IAM Identity Center

**Date:** 2026-03-02
**Status:** Complete

---

## IAM Role Consolidation Pattern Viability Matrix

| Pattern | Mechanism | Identity Center Compatible | Key Constraint |
| --- | --- | --- | --- |
| Broad base role + inline session policy | STS AssumeRole with Policy parameter | No — GetRoleCredentials accepts no Policy parameter | Session policy is caller-supplied; Identity Center credential issuance (GetRoleCredentials API) has no Policy parameter |
| Broad base role + managed session policy ARNs | STS AssumeRole with PolicyArns parameter (up to 10 ARNs) | No — same GetRoleCredentials limitation applies | Combined plaintext of inline policy + ARNs + tags capped at 2,048 chars; PackedPolicySize binary limit is a separate hard ceiling |
| Broad base role + chained AssumeRole with session policy | Identity Center issues credentials, caller then does second AssumeRole with Policy parameter | Partial — viable but introduces role chaining hard limit | Role chaining caps session duration at 1 hour regardless of permission set session duration (1–12 hours) |
| ABAC via permission set condition keys | Permission set policy uses aws:PrincipalTag conditions matched to resource tags; Identity Center propagates user attributes as session tags | Yes — natively supported | Attribute scope is limited to pre-configured Identity Center attributes; requires consistent resource tagging discipline; cannot express arbitrary per-session allow lists |
| Multiple narrow permission sets | One permission set per use case; admin assigns users to appropriate sets | Yes — fully supported | Restores role proliferation at the permission set level; no runtime dynamism; assignment is administrative, not caller-driven |
| GetFederationToken broker (non-Identity Center) | IAM user or service calls GetFederationToken with inline session policy on behalf of end user | Not applicable — bypasses Identity Center entirely | Requires IAM user credentials as base principal; incompatible with Identity Center user identity model; not viable in enterprise Identity Center deployments |

> The STS AssumeRole API natively supports a Policy parameter enabling the broad-base-role pattern. IAM Identity Center's GetRoleCredentials API — the actual credential issuance endpoint used by the portal and AWS CLI sso login — accepts no Policy parameter. This is the structural gap that makes the pattern non-viable through Identity Center's standard credential path.

---

## Question

> What documented patterns exist for consolidating IAM roles using session policies — specifically a 'broad base role + dynamic session policy' model — and how does IAM Identity Center's permission set model interact with or constrain these consolidation patterns?

---

## Context

Enterprise AWS environments accumulate large numbers of fine-grained IAM roles — one per application, environment, or team — creating management overhead and audit complexity. Session policies offer a potential consolidation mechanism: a single broad base role assumed with a caller-supplied restricting session policy at assume-role time. IAM Identity Center is the primary identity layer in many enterprise AWS environments and controls how roles are provisioned and assumed. The central question is whether the broad-base-role consolidation pattern is viable and where Identity Center enables or blocks it.

---

## Key Findings

- The STS AssumeRole API accepts an optional Policy parameter (inline JSON, max 2,048 chars combined with PolicyArns) and up to 10 managed policy ARN references, enabling a broad base role to be scoped down dynamically at assumption time. The effective session permissions are the strict intersection of the role's identity-based policies and the passed session policy — session policies cannot expand beyond what the role itself allows.
- IAM Identity Center issues credentials via its proprietary GetRoleCredentials portal API, not directly via STS AssumeRole. GetRoleCredentials accepts only three parameters — accessToken, accountId, and roleName — with no request body and no Policy parameter. This means a user or application obtaining credentials through the standard Identity Center path cannot inject a session policy at issuance time. The permission set's attached policies are the sole permission definition.
- A post-issuance chained AssumeRole from Identity Center credentials is technically viable as a workaround: Identity Center issues credentials for a broad base role; the application then calls STS AssumeRole with a session policy using those credentials as the principal. However, IAM role chaining imposes a hard 1-hour session duration ceiling regardless of the permission set's configured session duration (up to 12 hours), creating a UX and operational constraint.
- ABAC via session tags is the native Identity Center mechanism for differentiating permissions within a single permission set. Identity Center propagates user attributes (from the configured identity source) as session tags into the IAM session; permission set policies can reference these via aws:PrincipalTag condition keys. This reduces permission set proliferation — multiple users with the same permission set receive differentiated access based on their attributes — but requires consistent resource tagging and cannot produce an arbitrary per-session allow list of actions the way an inline session policy can.
- The AWS-documented identity broker pattern (GetFederationToken) explicitly supports the broad-base-role + session-policy model for custom federation scenarios. However, GetFederationToken requires an IAM user principal as the calling entity, making it architecturally incompatible with Identity Center user identities. Enterprises using Identity Center cannot use GetFederationToken without a parallel IAM user layer, which reintroduces the credential management complexity Identity Center is intended to eliminate.
- The practical consolidation ceiling under Identity Center is the permission set itself: one permission set maps to one IAM role per account, and role proliferation shifts from the IAM layer to the permission set layer. ABAC reduces this by allowing one permission set to serve users with distinct attribute-based access; without ABAC, each distinct permission profile requires a distinct permission set.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Session Policy | An optional JSON policy document (or set of up to 10 managed policy ARNs) passed as a parameter to STS AssumeRole, AssumeRoleWithSAML, or AssumeRoleWithWebIdentity. The effective session permissions are the intersection of the role's identity-based policies and the session policy. Session policies cannot grant permissions beyond what the role itself allows. |
| Broad Base Role | An IAM role with a relatively permissive set of policies intended to cover multiple use cases. In a consolidation pattern, a single such role is assumed by multiple callers, each supplying a narrowing session policy to scope down to their specific use case. The AWS Security Blog documents EC2Admin as a concrete example of this pattern. |
| GetRoleCredentials API | The IAM Identity Center portal API used by the AWS access portal and AWS CLI sso login to issue temporary credentials for a user's assigned permission set. Accepts only accessToken, accountId, and roleName — no session policy parameter exists. This is the structural constraint that blocks the broad-base-role pattern from operating through Identity Center's standard credential path. |
| Permission Set | An IAM Identity Center construct that defines a collection of IAM policies. When assigned to a user or group for an account, Identity Center provisions a corresponding IAM role in that account and attaches the permission set's policies to it. Users assume this role through GetRoleCredentials, not through direct STS calls. |
| Role Chaining | The pattern of using credentials from one assumed role to assume a second role. When a chain involves two separate role assumptions, the session duration of the second role is hard-capped at 1 hour regardless of the role's or permission set's MaxSessionDuration. Relevant because the Identity Center credentials + second AssumeRole workaround produces a chained session subject to this limit. |
| ABAC (Attribute-Based Access Control) via Session Tags | An Identity Center-native mechanism where user attributes (from the configured identity source such as Entra ID or Okta) are passed as session tags during authentication. Permission set policies reference these tags via the aws:PrincipalTag condition key. Enables a single permission set to produce differentiated access based on user attributes, without requiring caller-supplied session policies. |
| PackedPolicySize | A response element returned by STS that indicates as a percentage how close a request's combined session policy, session tags, and managed policy ARNs are to the binary packed limit. The plaintext combined limit is 2,048 characters, but a separate binary packing limit can reject requests that meet the plaintext requirement. Requests failing the binary limit return a PackedPolicyTooLarge HTTP 400 error. |

---

## Tensions & Tradeoffs

- The STS API surface enables dynamic session policy injection at assume-role time, which would support broad-base-role consolidation. Identity Center's credential issuance API (GetRoleCredentials) does not expose this surface to callers, creating a gap between what IAM supports in principle and what Identity Center-mediated access allows in practice.
- Role chaining as a workaround restores dynamic session policy capability for Identity Center users but imposes a hard 1-hour session ceiling, conflicting with the permission set's configurable session duration (up to 12 hours) and creating a poor operational experience for long-running workloads or interactive users.
- ABAC via session tags reduces permission set proliferation but operates on a fundamentally different model than dynamic session policies: ABAC enforces access at resource-match time (user attribute must match resource tag), while session policies restrict the action namespace for the entire session. ABAC cannot replace session policies in use cases that require restricting which actions or resource ARNs are accessible regardless of tagging state.
- Consolidation via fewer, broader permission sets creates a base-permissions tension: the permission set must be broad enough to serve all intended use cases, but a broader permission set increases the blast radius if ABAC conditions are misconfigured or resources are mis-tagged.
- The identity broker (GetFederationToken) pattern is the closest native AWS mechanism to the broad-base-role + session-policy model but requires IAM user credentials as the calling principal, making it architecturally incompatible with Identity Center — the enterprise identity standard for human access in modern AWS organizations.

---

## Open Questions

- Whether AWS plans to extend the GetRoleCredentials or equivalent Identity Center credential API to accept a session policy parameter has not been publicly announced or documented as of this investigation's date.
- To what extent ABAC-based consolidation is operationally viable depends on how consistently resource tags are applied across an organization. No documentation quantifies tag coverage rates in typical enterprise AWS environments.
- Whether the role chaining 1-hour session limit is a fundamental STS security boundary or a removable constraint (e.g., via IAM Roles Anywhere or session context features) is not addressed in scope — these mechanisms are out of scope for this investigation.
- The interaction between Identity Center's Trusted Identity Propagation (CreateTokenWithIAM) and the role consolidation pattern is not addressed here; this mechanism targets service-to-service authorization and may merit a separate sub-investigation.

---

## Sources & References

- [AssumeRole API Reference — AWS Security Token Service](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [Permissions for AssumeRole, AssumeRoleWithSAML, and AssumeRoleWithWebIdentity — AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_assumerole.html)
- [GetRoleCredentials API Reference — AWS IAM Identity Center Portal API](https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_GetRoleCredentials.html)
- [Manage AWS accounts with permission sets — AWS IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html)
- [Attribute-based access control — AWS IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html)
- [Create permission policies for ABAC in IAM Identity Center — AWS IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac-policies.html)
- [IAM and AWS STS quotas — AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html)
- [Methods to assume a role — AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage-assume.html)
- [Create fine-grained session permissions using IAM managed policies — AWS Security Blog](https://aws.amazon.com/blogs/security/create-fine-grained-session-permissions-using-iam-managed-policies/)
- [Build an end-to-end attribute-based access control strategy with AWS IAM Identity Center and Okta — AWS Security Blog](https://aws.amazon.com/blogs/security/build-an-end-to-end-attribute-based-access-control-strategy-with-aws-sso-and-okta/)
- [AssumeRoleWithWebIdentity API Reference — AWS Security Token Service](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)
- [GetFederationToken API Reference — AWS Security Token Service](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html)
- [Set session duration for AWS accounts — AWS IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html)
