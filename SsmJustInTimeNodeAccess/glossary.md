# Glossary — AWS SSM Just-in-Time Node Access (JITNA) — IAM Identity Center / Entra ID Federation and SSMSessionRunAs Compatibility

Quick definitions of key terms and concepts referenced in this investigation.

---

## Just-in-Time Node Access (JITNA)

An AWS Systems Manager feature that adds an approval gate before a user can establish an SSM Session Manager session. Users submit an access request specifying the target node and a reason; an approval policy (auto, manual, or deny) governs whether access is granted. On approval, Systems Manager generates a temporary token used to start the session.

## SSMSessionRunAs

A session tag evaluated at ssm:StartSession time that instructs Session Manager to open the shell as a named Linux OS user account rather than the default ssm-user. The tag can be set as an IAM entity tag or passed as a principal tag from a federated SAML assertion.

## IAM Identity Center (IdC)

AWS's centralized SSO and workforce identity service. Entra ID is federated into IdC via SAML 2.0 or OIDC, and IdC issues short-lived STS AssumeRole credentials to the user's local session. JITNA explicitly supports IdC-federated users as an identity source.

## Temporary STS Credential Token (JITNA)

After JITNA approval, the user runs get-access-token to retrieve temporary AWS STS credentials scoped to the approved access window. These credentials are exported to the environment and used with aws ssm start-session. Only STS AssumeRole credentials are supported — long-lived IAM user credentials are not.

## Approval Policy

A JITNA configuration object that targets nodes (by tag or all-nodes) and specifies one of three behaviors: auto-approval (access granted immediately), manual approval (specific approvers notified), or deny-access (requests blocked). Precedence: deny > auto > manual. A node with no policy means no requests can be made.

## Amazon Q Developer in chat applications

Formerly AWS Chatbot. JITNA's manual approval notification path routes through this service to deliver approval requests to Slack or Microsoft Teams channels, and allows approvers to act directly in the chat interface.

## Unified Systems Manager Console Setup

A prerequisite JITNA configuration step that establishes a State Manager Association across target accounts/regions. The association deploys an IAM role that Systems Manager uses to generate temporary credential tokens for approved sessions.

## Principal Tag (SAML)

A session attribute passed from an IdP during SAML federation that becomes a tag on the resulting STS session. SSMSessionRunAs can be passed this way — configured in Entra ID as a claim mapped to the Linux username, forwarded as a principal tag to AWS STS via SAML assertion.

---

*Back to: [investigation.md](investigation.md)*
