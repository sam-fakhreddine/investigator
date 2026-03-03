# Validation Report: AWS SSM Just-in-Time Node Access (JITNA) — IAM Identity Center / Entra ID Federation and SSMSessionRunAs Compatibility
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 10
- Verified: 9 | Redirected: 0 | Dead: 0 | Unverifiable: 1
- Findings checked: 11
- Confirmed: 8 | Partially confirmed: 2 | Unverified: 1 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 2

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/SsmJustInTimeNodeAccess
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        11           11           21c4151e7d2b   21c4151e7d2b
tensions             IN_SYNC        5            5            288bf5028c4c   288bf5028c4c
open_questions       IN_SYNC        6            6            c96f3cf1f49e   c96f3cf1f49e
sources              IN_SYNC        10           10           12d3661d5b2a   12d3661d5b2a
concepts             IN_SYNC        8            8            0e768f6e7eee   0e768f6e7eee
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Just-in-time node access using Systems Manager — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access.html | VERIFIED | Page exists; confirms IdC federated users, EventBridge events, 1-year retention |
| 2 | Just-in-time node access FAQ — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/just-in-time-node-access-faq.html | VERIFIED | Page exists; confirms same-account same-region restriction; addresses policy precedence and tag conflict rules |
| 3 | Setting up just-in-time access with Systems Manager — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-setting-up.html | VERIFIED | Page exists; confirms Unified Systems Manager Console prerequisite; confirms SSO auth unsupported for Windows RDP; confirms only STS AssumeRole credentials supported; references AWS Organizations OUs as targets |
| 4 | Moving to just-in-time node access from Session Manager — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-moving-from-session-manager.html | VERIFIED | Page exists; four-phase migration described; explicit removal of ssm:StartSession documented with example IAM policies |
| 5 | Start a just-in-time node access session — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-start-session.html | VERIFIED | Page exists; get-access-token command confirmed; temporary STS credentials exported to environment confirmed |
| 6 | Turn on Run As support for Linux and macOS managed nodes — AWS Systems Manager | https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html | VERIFIED | Page exists; SSMSessionRunAs tag evaluation at StartSession confirmed; no explicit mention of federated user flow in the page itself |
| 7 | Configuring Session Manager run as support for federated users using session tags — AWS Cloud Operations Blog | https://aws.amazon.com/blogs/mt/configuring-aws-systems-manager-session-manager-support-federated-users-using-session-tags/ | UNVERIFIABLE | Page URL resolves but page body rendered only CSS/JS — no readable article content retrieved. Web search confirms the blog post exists and that it demonstrates SSMSessionRunAs with SAML PrincipalTag:SSMSessionRunAs from an IdP (ADFS); content verified indirectly via search result snippets |
| 8 | AWS Systems Manager launches just-in-time node access — AWS What's New | https://aws.amazon.com/about-aws/whats-new/2025/04/aws-systems-manager-just-in-time-node-access/ | VERIFIED | Page exists; announces JITNA launch on April 29, 2025; lists 16 availability regions |
| 9 | AWS Systems Manager Pricing | https://aws.amazon.com/systems-manager/pricing/ | VERIFIED | Page exists; confirms $0.0137/node-hour for first 72,000 hours; tiered pricing confirmed; 30-day free trial confirmed |
| 10 | Credentials — AWS Systems Manager API Reference | https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_Credentials.html | VERIFIED | Page exists; describes the Credentials data type (AccessKeyId, SecretAccessKey, SessionToken, ExpirationTime) returned by JITNA get-access-token |

## Finding Verification

### Finding 1: JITNA explicitly supports IAM Identity Center federated users
- **Claim:** "JITNA explicitly supports IAM Identity Center federated users (Entra ID via SAML/OIDC to IdC) as a first-class identity type — AWS documentation states 'Systems Manager supports just-in-time node access for users federated with IAM Identity Center or IAM.'"
- **Verdict:** CONFIRMED
- **Evidence:** The main JITNA overview page contains the exact quoted sentence verbatim: "Systems Manager supports just-in-time node access for users federated with IAM Identity Center or IAM." Entra ID-to-IdC via SAML/OIDC is a standard federation path that IdC supports; the claim is accurate.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access.html

### Finding 2: JITNA does not replace Session Manager — it adds an approval gate on top
- **Claim:** "JITNA does not replace Session Manager — it adds an approval gate on top of Session Manager's session establishment. After JITNA approval, the user still calls aws ssm start-session using temporary STS AssumeRole credentials returned by the get-access-token command; the underlying transport is unchanged."
- **Verdict:** CONFIRMED
- **Evidence:** The start-session page explicitly shows the multi-step CLI flow: start-access-request → get-access-token → export AWS_SESSION_TOKEN → start-session. The setup page confirms only STS AssumeRole credentials are used. The migration guide shows Session Manager permissions (ssm:StartSession) remain the underlying mechanism.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-start-session.html

### Finding 3: SSMSessionRunAs compatibility is unconfirmed by official documentation
- **Claim:** "SSMSessionRunAs compatibility is unconfirmed by official documentation. JITNA sessions end in a standard start-session call with STS temporary credentials, and SSMSessionRunAs is evaluated at StartSession time based on the caller's IAM principal tags. Whether the JITNA temporary token carries those principal tags from the original IdC-federated session is not stated in any official AWS doc reviewed."
- **Verdict:** CONFIRMED
- **Evidence:** Verified across the main JITNA overview, FAQ, setup, and start-session pages — none mention SSMSessionRunAs or principal tag propagation through the JITNA token. The Run As page (source 6) confirms SSMSessionRunAs is evaluated at StartSession but does not address JITNA. The blog post (source 7) addresses SSMSessionRunAs with federated users via SAML PrincipalTag but predates JITNA and does not address JITNA token propagation. No AWS documentation explicitly confirms or denies whether the JITNA-issued STS token preserves the SSMSessionRunAs principal tag.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html; https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access.html

### Finding 4: Three approval policy types — auto, manual, deny — with documented precedence
- **Claim:** "JITNA supports three approval policy types: auto-approval (no human in the loop), manual approval (one or more approvers notified via Amazon Q Developer in Slack or Microsoft Teams), and deny-access (explicit block). Precedence: deny-access wins over auto-approval, which wins over manual."
- **Verdict:** CONFIRMED
- **Evidence:** The FAQ page confirms policy precedence (deny-access → auto-approval → manual). The main JITNA overview confirms all three policy types and notification via Amazon Q Developer in chat applications (Slack/Teams).
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/just-in-time-node-access-faq.html

### Finding 5: Manual approval conflicts — overlapping tag targets block all access requests
- **Claim:** "Manual approval conflicts arise when multiple approval policies with overlapping node tags target the same node — in that case, users cannot request access until the conflict is resolved. One tag can only be targeted by one approval policy."
- **Verdict:** CONFIRMED
- **Evidence:** The FAQ page addresses tag targeting limitations and conflict resolution for overlapping tags, confirming that one policy per tag and that conflicts block access requests.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/just-in-time-node-access-faq.html

### Finding 6: JITNA is constrained to the same AWS account and same Region
- **Claim:** "JITNA is constrained to the same AWS account and same Region as the target node. Cross-account just-in-time access through JITNA is not supported."
- **Verdict:** CONFIRMED
- **Evidence:** The FAQ page states exactly: "Just-in-time node access supports requesting access to and starting sessions on nodes in the same account and Region as the requester." Cross-account access is explicitly not covered.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/just-in-time-node-access-faq.html

### Finding 7: JITNA does not support SSO authentication type for Windows Server RDP
- **Claim:** "JITNA does not support the Single Sign-On (SSO) authentication type for Windows Server RDP connections — only AWS STS AssumeRole temporary credentials are supported for Windows RDP sessions via JITNA."
- **Verdict:** CONFIRMED
- **Evidence:** The setup page contains an "Authentication support" section with the exact text: "Just-in-time node access doesn't support the Single Sign-On authentication type when connecting to Windows Server instances with Remote Desktop." This is verbatim confirmation. Only STS AssumeRole credentials are supported.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-setting-up.html

### Finding 8: Cost model — $0.0137/node-hour, first tier, ~$9.86/month, 30-day free trial
- **Claim:** "The cost model charges per enrolled node-hour, not per access request or session. At first-tier pricing ($0.0137/node-hour), a node enrolled 24/7 costs approximately $9.86/month. A 30-day free trial (two billing cycles) is available."
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** Pricing page confirms $0.0137/node-hour for the first tier (first 72,000 node-hours) and confirms the 30-day free trial. The monthly cost calculation of $9.86 (0.0137 × 24 × 30 = $9.864) is arithmetically correct. However, the investigation states the free trial covers "two billing cycles" — the pricing page states "for the remainder of the billing cycle as well as one additional billing cycle," which means it covers the current partial billing cycle plus one full billing cycle. Depending on when in the month JITNA is enabled, the effective free period could be less than 30 days. The "30-day free trial" characterization in the investigation is an approximation, not the exact policy language.
- **Source used:** https://aws.amazon.com/systems-manager/pricing/

### Finding 9: Enabling JITNA does not modify existing Session Manager config; enforcing requires removing ssm:StartSession
- **Claim:** "Enabling JITNA does not modify existing Session Manager IAM policies, session documents, or preferences. Enforcing JITNA-only access requires explicitly removing ssm:StartSession from user IAM policies. A phased migration — piloting on non-critical nodes before full cutover — is the documented approach."
- **Verdict:** CONFIRMED
- **Evidence:** The migration guide explicitly documents removing ssm:StartSession from IAM policies to enforce JITNA-only access, with example JSON policies showing the before/after. The four-phase migration approach (setup, policy development, pilot, full migration) matches the "phased migration" claim exactly.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-moving-from-session-manager.html

### Finding 10: JITNA requires Unified Systems Manager Console Setup; State Manager Association deploys IAM role
- **Claim:** "JITNA requires a unified Systems Manager console setup as a prerequisite. A State Manager Association is deployed that creates an IAM role used by Systems Manager to generate the temporary credential tokens for approved sessions."
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The setup page and FAQ both confirm the Unified Systems Manager Console Setup as a mandatory prerequisite. The setup page confirms the IAM role creation and STS token generation. However, the setup page indicates JITNA targets are defined as "AWS Organizations organizational units (OUs) and AWS Regions," implying AWS Organizations is required — which the investigation does not mention as a prerequisite. The investigation's open question about whether JITNA requires AWS Organizations is legitimate and well-founded; the documentation strongly implies Organizations is required (references "delegated administrator account for your organization," OUs as targets), but the documentation does not explicitly state standalone accounts cannot use JITNA. The State Manager Association claim is consistent with how the unified console deploys configuration at scale, but the specific phrase "State Manager Association" was not explicitly confirmed in the pages reviewed — only the IAM role creation and token generation were confirmed.
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access-setting-up.html

### Finding 11: Access request records retained 1 year; EventBridge events emitted on failures and status updates
- **Claim:** "Access request records are retained for one year. Amazon EventBridge events are emitted on failed requests and status updates, enabling audit trail integration with SIEM or CloudWatch."
- **Verdict:** CONFIRMED
- **Evidence:** The main JITNA overview page contains exact text: "Systems Manager retains all access requests for 1 year." The same page states: "Systems Manager also emits EventBridge events for just-in-time node access for failed access requests and status updates to access requests for manual approvals."
- **Source used:** https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 8: Free trial described as "30-day free trial (two billing cycles)" | PARTIALLY CONFIRMED | The AWS pricing page states the trial covers "the remainder of the billing cycle as well as one additional billing cycle" — not a flat 30-day period. Update the quick_reference row and key finding to reflect the exact policy: "free for the remainder of the current billing cycle plus one additional billing cycle." |
| Finding 10: State Manager Association claim not confirmed in reviewed pages | PARTIALLY CONFIRMED | The specific claim that JITNA uses a "State Manager Association" was not explicitly confirmed in the documentation reviewed. Additionally, the investigation does not flag AWS Organizations as a likely prerequisite, which the setup page strongly implies. Consider adding an open question about whether JITNA requires AWS Organizations enrollment or can be deployed in a standalone account. |

## Overall Assessment

The investigation is well-sourced, accurate, and appropriately hedged on the critical open question (SSMSessionRunAs compatibility). All 10 sources resolve. Nine of 10 are fully verified; one blog source (source 7) could not have its body rendered directly but was confirmed via web search snippets to exist and contain the claimed content about SAML PrincipalTag:SSMSessionRunAs.

Eight of 11 key findings are fully confirmed by primary AWS documentation. Two findings are partially confirmed with minor precision issues: the free trial framing uses "30-day" as a simplification of the actual "remainder of current billing cycle plus one additional cycle" policy, and the State Manager Association mechanism was not explicitly named in the reviewed pages. Neither issue is materially misleading given the investigation's intended audience, but both warrant a targeted correction in `investigation.json`.

No findings are contradicted. The investigation correctly identifies SSMSessionRunAs compatibility as the critical open question and appropriately hedges all claims around it — this is the most important architectural unknown and the investigation communicates it accurately and with appropriate urgency. The Windows RDP SSO limitation and cross-account restriction are both confirmed by primary documentation. The cost arithmetic is correct.

The investigation's open question about whether JITNA requires AWS Organizations deserves elevation: the setup documentation references "delegated administrator account for your organization," OUs as targets, and "unified console for an organization" throughout — standalone account support is not addressed anywhere in the reviewed documentation and is a realistic prerequisite gap that could block teams not using AWS Organizations.
