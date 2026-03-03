# Investigation: AWS SSM Just-in-Time Node Access (JITNA) — IAM Identity Center / Entra ID Federation and SSMSessionRunAs Compatibility

**Date:** 2026-03-02
**Status:** Complete

---

## JITNA Capability and Compatibility Summary

| Dimension | Finding | Detail |
| --- | --- | --- |
| IdC / Entra ID federation | Supported | AWS docs explicitly state JITNA supports users federated with IAM Identity Center or IAM |
| SSMSessionRunAs compatibility | Architecturally incompatible by default — empirical validation required | JITNA credentials come from fresh AssumeRole into JITNA-managed role; STS session tags are non-transitive by default; SSMSessionRunAs from the original IdC session does not propagate unless explicitly marked TransitiveTagKey; no AWS doc confirms tag propagation |
| Approval: auto-approval | Supported | Approval policy type: auto-approval — no human required |
| Approval: manual (Slack/Teams) | Supported via Amazon Q Developer | Notifications route through Amazon Q Developer in chat applications; approver acts in Slack or Teams |
| Approval: deny-access | Supported | Explicit deny policy overrides auto-approval; policy precedence: deny > auto > manual |
| Multi-account / cross-account | Not supported | Same account and same region only; cross-account JITNA not available |
| Windows RDP + SSO auth | Not supported | JITNA does not support the SSO authentication type for Windows RDP sessions |
| Cost | ~$9.86/node/month (first tier) | $0.0137/node-hour billed on enrolled nodes; free trial: remainder of current billing cycle plus one additional billing cycle |
| Migration model | Additive — phased migration supported | JITNA does not alter existing Session Manager config; remove ssm:StartSession to enforce JITNA-only access |
| Session retention | 1 year | Access request records retained for 1 year; EventBridge events on status changes |

> SSMSessionRunAs compatibility is architecturally incompatible with JITNA by default. JITNA credentials come from a fresh AssumeRole into a JITNA-managed role, and STS session tags are non-transitive across role chains by default. The SSMSessionRunAs principal tag from the original Entra ID / IdC session does not propagate automatically. Empirical validation is required before any production rollout that relies on per-user OS identity.

---

## Question

> Does AWS Systems Manager Just-in-Time Node Access (JITNA) integrate with IAM Identity Center / Entra ID federation, and does it work alongside or replace the SSMSessionRunAs model for temporary elevated production access without CyberArk or a custom approval workflow?

---

## Context

The team uses Entra ID federated to AWS IAM Identity Center (IdC). They use SSM Session Manager with the SSMSessionRunAs session tag to map federated users to named Linux OS accounts. A stakeholder asked whether AWS JITNA could provide a just-in-time temporary elevated prod access workflow — developer requests access, gets approved (auto or via Slack/Teams), connects — without building a custom approval system or adopting CyberArk. Key unknowns: whether JITNA explicitly supports IdC-federated users, whether SSMSessionRunAs still functions inside JITNA sessions, what approval models exist, multi-account constraints, cost, and the migration path from Session Manager.

---

## Key Findings

- JITNA explicitly supports IAM Identity Center federated users (Entra ID via SAML/OIDC to IdC) as a first-class identity type — AWS documentation states 'Systems Manager supports just-in-time node access for users federated with IAM Identity Center or IAM.'
- JITNA does not replace Session Manager — it adds an approval gate on top of Session Manager's session establishment. After JITNA approval, the user still calls aws ssm start-session using temporary STS AssumeRole credentials returned by the get-access-token command; the underlying transport is unchanged.
- SSMSessionRunAs compatibility is architecturally incompatible with JITNA under default configuration. JITNA approval generates temporary STS credentials via a fresh AssumeRole into a JITNA-managed IAM role — not a delegation of the original IdC-federated session credentials. AWS STS session tags are not transitive across role chains by default; they must be explicitly declared as TransitiveTagKeys on the AssumeRole call. The JITNA-managed role's trust policy and credential generation process do not document SSMSessionRunAs as a TransitiveTagKey. Until AWS explicitly documents tag transitivity through the JITNA token generation step or provides an alternative configuration path, empirical validation in a non-production account is required before any production rollout that depends on per-user OS identity.
- JITNA supports three approval policy types: auto-approval (no human in the loop), manual approval (one or more approvers notified via Amazon Q Developer in Slack or Microsoft Teams), and deny-access (explicit block). Precedence: deny-access wins over auto-approval, which wins over manual.
- Manual approval conflicts arise when multiple approval policies with overlapping node tags target the same node — in that case, users cannot request access until the conflict is resolved. One tag can only be targeted by one approval policy.
- JITNA is constrained to the same AWS account and same Region as the target node. Cross-account just-in-time access through JITNA is not supported.
- JITNA does not support the Single Sign-On (SSO) authentication type for Windows Server RDP connections — only AWS STS AssumeRole temporary credentials are supported for Windows RDP sessions via JITNA.
- The cost model charges per enrolled node-hour, not per access request or session. At first-tier pricing ($0.0137/node-hour), a node enrolled 24/7 costs approximately $9.86/month. A free trial covering the remainder of the current billing cycle plus one additional billing cycle is available.
- Enabling JITNA does not modify existing Session Manager IAM policies, session documents, or preferences. Enforcing JITNA-only access requires explicitly removing ssm:StartSession from user IAM policies. A phased migration — piloting on non-critical nodes before full cutover — is the documented approach.
- JITNA requires a unified Systems Manager console setup as a prerequisite. The setup documentation targets AWS Organizations organizational units (OUs) and references a Systems Manager delegated administrator account — standalone account support is not documented in any reviewed source. The setup deploys infrastructure including an IAM role used by Systems Manager to generate temporary credential tokens; the specific internal mechanism (e.g., State Manager Association) is not named in the public-facing documentation.
- Access request records are retained for one year. Amazon EventBridge events are emitted on failed requests and status updates, enabling audit trail integration with SIEM or CloudWatch.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Just-in-Time Node Access (JITNA) | An AWS Systems Manager feature that adds an approval gate before a user can establish an SSM Session Manager session. Users submit an access request specifying the target node and a reason; an approval policy (auto, manual, or deny) governs whether access is granted. On approval, Systems Manager generates a temporary token used to start the session. |
| SSMSessionRunAs | A session tag evaluated at ssm:StartSession time that instructs Session Manager to open the shell as a named Linux OS user account rather than the default ssm-user. The tag can be set as an IAM entity tag or passed as a principal tag from a federated SAML assertion. |
| IAM Identity Center (IdC) | AWS's centralized SSO and workforce identity service. Entra ID is federated into IdC via SAML 2.0 or OIDC, and IdC issues short-lived STS AssumeRole credentials to the user's local session. JITNA explicitly supports IdC-federated users as an identity source. |
| Temporary STS Credential Token (JITNA) | After JITNA approval, the user runs get-access-token to retrieve temporary AWS STS credentials scoped to the approved access window. These credentials are exported to the environment and used with aws ssm start-session. Only STS AssumeRole credentials are supported — long-lived IAM user credentials are not. |
| Approval Policy | A JITNA configuration object that targets nodes (by tag or all-nodes) and specifies one of three behaviors: auto-approval (access granted immediately), manual approval (specific approvers notified), or deny-access (requests blocked). Precedence: deny > auto > manual. A node with no policy means no requests can be made. |
| Amazon Q Developer in chat applications | Formerly AWS Chatbot. JITNA's manual approval notification path routes through this service to deliver approval requests to Slack or Microsoft Teams channels, and allows approvers to act directly in the chat interface. |
| Unified Systems Manager Console Setup | A prerequisite JITNA configuration step that establishes a State Manager Association across target accounts/regions. The association deploys an IAM role that Systems Manager uses to generate temporary credential tokens for approved sessions. |
| Principal Tag (SAML) | A session attribute passed from an IdP during SAML federation that becomes a tag on the resulting STS session. SSMSessionRunAs can be passed this way — configured in Entra ID as a claim mapped to the Linux username, forwarded as a principal tag to AWS STS via SAML assertion. |

---

## Tensions & Tradeoffs

- SSMSessionRunAs compatibility with JITNA is architecturally plausible (both use StartSession + STS credentials) but not explicitly confirmed by AWS documentation — teams relying on per-user OS identity must empirically validate this before removing Session Manager permissions in production.
- JITNA's cost is per enrolled node-hour regardless of whether users are actively requesting access, creating a flat monthly charge for any node enrolled in JITNA. Teams with large node fleets where JITNA coverage is needed across all nodes will face meaningful infrastructure cost increases without corresponding per-session pricing.
- Enforcing JITNA-only access requires removing ssm:StartSession from IAM policies — this is a hard cutover per-role, not a per-node toggle. Teams running mixed workloads where some users need direct Session Manager access and others require JITNA gates must carefully partition IAM policies to avoid either over-permissioning or access gaps.
- Manual approval policy conflict rules are strict: overlapping tag targets on the same node across multiple policies prevent any access requests. In environments with fine-grained node tagging, policy proliferation risk is real and requires governance to prevent deadlocks.
- The Windows RDP + SSO auth limitation means that teams with Entra ID federated users who need RDP access to Windows servers via JITNA cannot use the SSO authentication path — they must ensure STS AssumeRole credentials are used, which may require tooling changes for Windows-only users accustomed to IdC portal flows.

---

## Open Questions

- Can the JITNA-managed IAM role be configured with TransitiveTagKeys to preserve SSMSessionRunAs from the original Entra ID / IdC SAML session? JITNA uses a fresh STS AssumeRole into a managed role, and STS session tags are non-transitive by default. Whether AWS exposes TransitiveTagKeys configuration on the JITNA-generated AssumeRole call, or whether an alternative mechanism exists, is not documented in any reviewed source.
- Does the Unified Systems Manager Console Setup prerequisite require AWS Organizations? The setup documentation targets organizational units (OUs) and references a delegated administrator account for the organization, strongly suggesting AWS Organizations is required. Whether standalone account support exists is not addressed in any reviewed documentation.
- What is the maximum access window duration configurable per approval policy? The FAQ states access is time-bound and sessions are not automatically terminated, relying instead on session duration/idle timeout settings — but the ceiling on the approval window itself is not stated in reviewed docs.
- Can JITNA approval policies target nodes across multiple AWS accounts if those accounts are in the same AWS Organization, or is the same-account restriction absolute with no planned cross-account support?
- How does JITNA interact with the deny-all-sessions IAM condition key (ssm:resourceTag/tag-key) used in some ABAC Session Manager setups? Can the two coexist without conflicting IAM evaluation logic?
- Is there a self-service auto-approval path that still generates an audit event, or does auto-approval silently bypass all logging? The pre-fetched docs note EventBridge events for failed requests and status updates — whether auto-approved requests generate the same event stream is not confirmed.

---

## Sources & References

- [Just-in-time node access using Systems Manager — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access.html)
- [Just-in-time node access FAQ — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/just-in-time-node-access-faq.html)
- [Setting up just-in-time access with Systems Manager — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-setting-up.html)
- [Moving to just-in-time node access from Session Manager — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-moving-from-session-manager.html)
- [Start a just-in-time node access session — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-start-session.html)
- [Turn on Run As support for Linux and macOS managed nodes — AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)
- [Configuring Session Manager run as support for federated users using session tags — AWS Cloud Operations Blog](https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/)
- [AWS Systems Manager launches just-in-time node access — AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/04/aws-systems-manager-just-in-time-node-access/)
- [AWS Systems Manager Pricing](https://aws.amazon.com/systems-manager/pricing/)
- [Credentials — AWS Systems Manager API Reference](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_Credentials.html)
