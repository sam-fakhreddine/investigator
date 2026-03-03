# Validation Report: RDS EventBridge Native Events vs CloudTrail Workaround
Date: 2026-03-03
Validator: Fact Validation Agent

## Summary
- Total sources checked: 11
- Verified: 11 | Redirected: 0 | Dead: 0 | Unverifiable: 0
- Findings checked: 10
- Confirmed: 7 | Partially confirmed: 2 | Unverified: 1 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/RdsEventBridgeNativeEvents
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        10           10           0610a61ea845   0610a61ea845
tensions             IN_SYNC        4            4            45a7555ae2e1   45a7555ae2e1
open_questions       IN_SYNC        4            4            31e517fc6538   31e517fc6538
sources              IN_SYNC        11           11           4240a89bb23b   4240a89bb23b
concepts             IN_SYNC        9            9            46460522b0a6   46040522b0a6

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Amazon Relational Database Service events - Amazon EventBridge (Events Reference) | https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-rds.html | VERIFIED | Page loads, lists all RDS detail-types, documents best-effort delivery. Source field aws.rds confirmed for both native and CloudTrail-delivered events. |
| 2 | Creating a rule that triggers on an Amazon RDS event - Amazon RDS User Guide | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-cloud-watch-events.html | VERIFIED | Page loads, confirms source: aws.rds and detail-type: RDS DB Instance Event with sample JSON. |
| 3 | Amazon RDS event categories and event messages - Amazon RDS User Guide | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.Messages.html | VERIFIED | Page loads, all referenced event IDs confirmed: RDS-EVENT-0005, 0003, 0087, 0088, 0019, 0043. |
| 4 | AWS service events delivered via AWS CloudTrail - Amazon EventBridge User Guide | https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html | VERIFIED | Page loads. Explicitly states source is the originating service (e.g., aws.ec2, not aws.cloudtrail). Explicitly states CloudTrail trail with logging must be enabled. |
| 5 | Receiving read-only management events from AWS services - Amazon EventBridge User Guide | https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail-management.html | VERIFIED | Page loads. ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS documented. Standard ENABLED rules exclude read-only events; write events covered by standard ENABLED. |
| 6 | Content filtering in Amazon EventBridge event patterns | https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns-content-based-filtering.html | VERIFIED | Page loads. anything-but with wildcard explicitly documented. Pipe support column shows "No" for this operator combination. |
| 7 | Comparison operators for use in event patterns in Amazon EventBridge | https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html | VERIFIED | Page loads. Wildcard nested inside anything-but shown as valid with sample JSON. Not supported in EventBridge Pipes confirmed. |
| 8 | Monitoring Amazon RDS API calls in AWS CloudTrail - Amazon RDS User Guide | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/logging-using-cloudtrail.html | VERIFIED | Page loads. CreateDBInstance shown as logged CloudTrail operation with sample log entry. Page states "All Amazon RDS actions are logged by CloudTrail." RestoreDBInstanceFromDBSnapshot not explicitly named in content fetched, but statement "all actions" covers it. |
| 9 | Tutorial: Create an EventBridge rule that reacts to AWS API calls via CloudTrail | https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-log-api-call.html | VERIFIED | Page loads. Step 1 explicitly creates a CloudTrail trail as a prerequisite, confirming trail required. Uses service source (EC2) not aws.cloudtrail. |
| 10 | Overview of Amazon RDS event notification - Amazon RDS User Guide | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.overview.html | VERIFIED | Page loads. RDS Event Subscription SNS routing confirmed. Page does not clearly distinguish between SNS-based and native EventBridge delivery paths — minor documentation gap, does not affect investigation accuracy. |
| 11 | Amazon RDS events - AWS Prescriptive Guidance (Monitoring and Alerting) | https://docs.aws.amazon.com/prescriptive-guidance/latest/amazon-rds-monitoring-alerting/rds-events.html | VERIFIED | Page loads. Confirms RDS delivers events to EventBridge. Does not discuss best-effort or CloudTrail workaround — supplementary source, not used for primary claims. |

## Finding Verification

### Finding 1: Native RDS EventBridge delivery without Event Subscription
- **Claim:** AWS documentation states that Amazon RDS sends service events directly to EventBridge natively, without requiring an RDS Event Subscription — the EventBridge Events Reference confirms this for the RDS DB Instance Event detail-type.
- **Verdict:** CONFIRMED
- **Evidence:** The EventBridge Events Reference (source 1) lists "RDS DB Instance Event" as a detail-type under aws.rds with delivery type "Best effort." The RDS User Guide (source 2) provides a console tutorial for creating EventBridge rules on RDS events with no mention of an Event Subscription requirement. The RDS Event Notification overview (source 10) documents Event Subscription as an SNS-based path distinct from EventBridge.
- **Source used:** https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-rds.html

### Finding 2: Best-effort delivery caveat
- **Claim:** Native RDS events are delivered on a best-effort basis; AWS documentation explicitly warns that events may be out of sequence or missing, making creation and restore events unreliable triggers for automation that depends on guaranteed delivery.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The EventBridge delivery level documentation confirms best-effort delivery and states "in some rare cases an event might not be delivered." However, the documentation does NOT explicitly state that events may be "out of sequence" nor does it explicitly recommend against building automation that depends on guaranteed delivery. The investigation's language ("may be out of sequence") is slightly stronger than what primary documentation states. The core claim that best-effort means events may be missing is accurate.
- **Source used:** https://docs.aws.amazon.com/eventbridge/latest/ref/event-delivery-level.html
- **Flag:** CONFIRM_OR_HEDGE — the "out of sequence" language should be hedged to "may be missing; out-of-sequence behavior is not explicitly documented but consistent with best-effort semantics."

### Finding 3: No confirmed sample event for RDS-EVENT-0005 and 0019/0043 native delivery
- **Claim:** No AWS documentation explicitly confirms that RDS-EVENT-0005 (DB instance created) or RDS-EVENT-0019/0043 (restore events) are reliably published natively to EventBridge; the only sample native event shown in official docs is RDS-EVENT-0087 (DB instance stopped).
- **Verdict:** CONFIRMED
- **Evidence:** The EventBridge Events Reference (source 1) does not show sample event payloads for any specific RDS event IDs. The RDS User Guide (source 2) shows source: aws.rds and detail-type: RDS DB Instance Event but does not provide per-event-ID samples. No documentation was found that shows RDS-EVENT-0005 or restore events with a sample payload confirming native EventBridge delivery. The claim of an evidence gap is accurate. Note: the investigation claims RDS-EVENT-0087 is "the only sample native event shown in docs" — this could not be independently confirmed as the sample event source was not identified in the docs fetched; however the absence of creation/restore samples is confirmed.
- **Source used:** https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-rds.html

### Finding 4: CloudTrail fires at API call time; instance in 'creating' state
- **Claim:** CloudTrail captures all RDS API calls including CreateDBInstance and RestoreDBInstanceFromDBSnapshot; when a CloudTrail-based EventBridge rule fires on CreateDBInstance, the DB instance is in the 'creating' state — not yet available.
- **Verdict:** CONFIRMED
- **Evidence:** The CloudTrail logging page (source 8) confirms CreateDBInstance is logged by CloudTrail with a full sample log entry. The EventBridge tutorial (source 9) confirms the CloudTrail event fires when the API call is made (not when the operation completes). The CreateDBInstance API semantics are well-established: the call initiates the operation and returns before the instance is available. The 'creating' state follows directly from CloudTrail capturing the API call at invocation time.
- **Source used:** https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/logging-using-cloudtrail.html

### Finding 5 (Critical): CloudTrail-based RDS events use source aws.rds, not aws.cloudtrail
- **Claim:** For CloudTrail-based RDS API call events, the top-level EventBridge source field is aws.rds (not aws.cloudtrail); the pattern uses detail-type: 'AWS API Call via CloudTrail' and detail.eventSource: 'rds.amazonaws.com' — the background hypothesis of source: aws.cloudtrail is incorrect.
- **Verdict:** CONFIRMED
- **Evidence:** The EventBridge User Guide (source 4) explicitly states that CloudTrail-delivered events use the originating service as the source — shown with EC2 example: source is aws.ec2, not aws.cloudtrail. The EventBridge Events Reference (source 1) explicitly documents the CloudTrail-delivered RDS event pattern as source: aws.rds with detail-type: "AWS API Call via CloudTrail" and detail.eventSource: rds.amazonaws.com. Web search results independently confirm the same pattern. This is unambiguous in primary documentation.
- **Source used:** https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-rds.html; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html

### Finding 6 (Critical): CloudTrail trail required for AWS API Call via CloudTrail events
- **Claim:** A CloudTrail trail with logging enabled is a hard prerequisite for 'AWS API Call via CloudTrail' events to flow to EventBridge; without a trail, API call events are recorded internally in CloudTrail Event History but are not delivered to EventBridge.
- **Verdict:** CONFIRMED
- **Evidence:** The EventBridge User Guide (source 4) states explicitly: "To record events with one of the CloudTrail detail-type values, you must enable a CloudTrail trail with logging." The EventBridge tutorial (source 9) begins with Step 1: Create an AWS CloudTrail trail as a hard prerequisite. The distinction between CloudTrail Event History (no EventBridge delivery) and a CloudTrail trail (EventBridge delivery) is accurate.
- **Source used:** https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-log-api-call.html

### Finding 7: ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS
- **Claim:** The ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS rule state allows EventBridge rules to match read-only CloudTrail management events without an explicit trail; CreateDBInstance is a write management event and is covered by a standard ENABLED rule when a trail exists.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The EventBridge management events page (source 5) confirms ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS covers read-only events and standard ENABLED rules exclude read-only events. CreateDBInstance as a write event covered by standard ENABLED rules is confirmed. However, the claim "without an explicit trail" is inaccurate or ambiguous: the management events page does not explicitly state that ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS operates without a trail — and source 4 states a trail is required for CloudTrail detail-type events. This sub-clause needs verification or correction.
- **Source used:** https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail-management.html
- **Flag:** UNVERIFIED sub-claim — "without an explicit trail" is not confirmed by source 5 and may contradict the general CloudTrail trail requirement documented in source 4. This should be investigated further or the phrase removed.

### Finding 8 (Critical): anything-but with wildcard filter syntax validity
- **Claim:** The EventBridge content filter pattern {"anything-but": {"wildcard": "..."}} is valid syntax; nesting wildcard inside anything-but is explicitly documented and supported for event bus rules (not Pipes).
- **Verdict:** CONFIRMED
- **Evidence:** Both source 6 (content filtering page) and source 7 (comparison operators page) explicitly document this syntax with sample JSON. Source 6 shows both single and array wildcard forms inside anything-but. Both sources include a support table showing this operator combination as unsupported in EventBridge Pipes. Documentation is unambiguous.
- **Source used:** https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns-content-based-filtering.html; https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html

### Finding 9: CloudTrail eventName values are stable identifiers
- **Claim:** CloudTrail eventName values (CreateDBInstance, StartDBInstanceReadReplica, RestoreDBInstanceFromDBSnapshot) are AWS API operation names defined in the RDS API reference and are stable identifiers unlikely to change across service updates.
- **Verdict:** CONFIRMED
- **Evidence:** CloudTrail logging page (source 8) uses CreateDBInstance as the canonical example with the exact eventName in the sample log. The characterization of API operation names as stable identifiers follows from standard AWS API versioning practice (RDS uses versioned APIs, operations are not renamed). No contradicting evidence found.
- **Source used:** https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/logging-using-cloudtrail.html

### Finding 10: RDS Event Subscription is separate from native EventBridge delivery
- **Claim:** RDS Event Subscription is a separate mechanism from native EventBridge delivery; it routes events through Amazon SNS and is unrelated to whether events appear in EventBridge under source: aws.rds.
- **Verdict:** CONFIRMED
- **Evidence:** The RDS event notification overview (source 10) confirms Event Subscription is SNS-based ("Amazon RDS uses the ARN of an Amazon SNS topic to identify each subscription"). The EventBridge Events Reference (source 1) documents native delivery as a separate path requiring no subscription. No documentation links these two mechanisms.
- **Source used:** https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.overview.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 2: "may be out of sequence" language | PARTIALLY CONFIRMED | Narrow claim to match documentation: best-effort means events may be missing; "out of sequence" is not explicitly documented. Remove or hedge the "out of sequence" assertion. |
| Finding 7: "without an explicit trail" sub-clause in ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS description | UNVERIFIED sub-claim | The claim that this rule state operates without an explicit trail is not confirmed by source 5 and potentially contradicts the trail requirement documented in source 4. Either remove "without an explicit trail" or replace with verified language from the management events page. |

## Overall Assessment

The investigation is well-sourced and accurate on all critical claims. All 11 sources are live and accessible official AWS documentation. The two most critical architectural claims — that CloudTrail-delivered RDS events use source: aws.rds (not aws.cloudtrail), and that a CloudTrail trail is required for these events to reach EventBridge — are unambiguously confirmed by primary documentation. The anything-but wildcard syntax and its Pipes restriction are also directly confirmed by two independent official sources.

Two findings require minor remediation. Finding 2 overstates the best-effort caveat: the documentation says events may be missing, but the "out of sequence" characterization is not in primary sources. Finding 7 contains an unverified sub-clause claiming ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS operates "without an explicit trail," which is not confirmed and may contradict the trail requirement documented elsewhere. Neither issue affects the investigation's core recommendations or the primary audience's decision-making, but both should be corrected for accuracy before this investigation is treated as authoritative.

No sources were dead, redirected, or unverifiable. No contradictions between findings were identified. The investigation's open questions are appropriately scoped — the absence of a confirmed sample event for RDS-EVENT-0005 native delivery is a real evidence gap, not a documentation error.
