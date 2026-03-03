# Investigation: RDS EventBridge Native Events vs CloudTrail Workaround

**Date:** 2026-03-03
**Status:** Complete

---

## Question

> Which RDS DB instance events are published natively to EventBridge without an Event Subscription, and do create/restore events require a CloudTrail-based EventBridge rule as a workaround?

---

## Context

Engineers building automation around RDS instance lifecycle (creation, restoration, deletion, stop) need to know which events they can intercept via a native EventBridge rule (source: aws.rds, detail-type: RDS DB Instance Event) and which require a different pattern. A known complaint is that EventBridge rules with source aws.rds appear to fire for deletion and stop events but never for creation or restore events, prompting the hypothesis that creation events are either not published natively or arrive with unstable Message field values that cause content filters to never match.

---

## RDS Event Coverage by Rule Pattern

| Event | RDS Event ID | Native to EventBridge (no subscription) | Correct rule pattern | Instance state when rule fires |
| --- | --- | --- | --- | --- |
| DB instance deleted | RDS-EVENT-0003 | Yes — confirmed in docs | source: aws.rds / detail-type: RDS DB Instance Event | N/A (already deleted) |
| DB instance stopped | RDS-EVENT-0087 | Yes — AWS sample event shown in docs | source: aws.rds / detail-type: RDS DB Instance Event | stopped |
| DB instance started | RDS-EVENT-0088 | Yes — same native path as stop | source: aws.rds / detail-type: RDS DB Instance Event | available |
| DB instance created | RDS-EVENT-0005 | Ambiguous — docs assert native delivery but best-effort caveat applies; no sample event shown | source: aws.rds / detail-type: AWS API Call via CloudTrail + eventSource: rds.amazonaws.com + eventName: CreateDBInstance (requires CloudTrail trail) | creating (API call fires before instance is available) |
| Restored from snapshot | RDS-EVENT-0043 (snapshot) / RDS-EVENT-0019 (instance) | Ambiguous — same best-effort caveat; no sample event shown | source: aws.rds / detail-type: AWS API Call via CloudTrail + eventSource: rds.amazonaws.com + eventName: RestoreDBInstanceFromDBSnapshot (requires CloudTrail trail) | creating |

> All native RDS events use source: aws.rds. CloudTrail-based RDS events also use source: aws.rds — not aws.cloudtrail. A CloudTrail trail with logging enabled is required for AWS API Call via CloudTrail events to reach EventBridge.

---

## Key Findings

- AWS documentation states that Amazon RDS sends service events directly to EventBridge natively, without requiring an RDS Event Subscription — the EventBridge Events Reference confirms this for the RDS DB Instance Event detail-type.
- Native RDS events are delivered on a best-effort basis; AWS documentation explicitly warns that events may be missing, making creation and restore events unreliable triggers for automation that depends on guaranteed delivery.
- No AWS documentation explicitly confirms that RDS-EVENT-0005 (DB instance created) or RDS-EVENT-0019/0043 (restore events) are reliably published natively to EventBridge; the only sample native event shown in official docs is RDS-EVENT-0087 (DB instance stopped), creating an evidence gap for creation and restore coverage.
- CloudTrail captures all RDS API calls including CreateDBInstance and RestoreDBInstanceFromDBSnapshot; when a CloudTrail-based EventBridge rule fires on CreateDBInstance, the DB instance is in the 'creating' state — not yet available.
- For CloudTrail-based RDS API call events, the top-level EventBridge source field is aws.rds (not aws.cloudtrail); the pattern uses detail-type: 'AWS API Call via CloudTrail' and detail.eventSource: 'rds.amazonaws.com' — the background hypothesis of source: aws.cloudtrail is incorrect.
- A CloudTrail trail with logging enabled is a hard prerequisite for 'AWS API Call via CloudTrail' events to flow to EventBridge; without a trail, API call events are recorded internally in CloudTrail Event History but are not delivered to EventBridge.
- The ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS rule state allows EventBridge rules to match read-only CloudTrail management events; CreateDBInstance is a write management event and is covered by a standard ENABLED rule when a trail exists.
- The EventBridge content filter pattern {"anything-but": {"wildcard": "*awsbackup-restore-test*"}} is valid syntax; nesting wildcard inside anything-but is explicitly documented and supported for event bus rules (not Pipes).
- CloudTrail eventName values (CreateDBInstance, StartDBInstanceReadReplica, RestoreDBInstanceFromDBSnapshot) are AWS API operation names defined in the RDS API reference and are stable identifiers unlikely to change across service updates.
- RDS Event Subscription is a separate mechanism from native EventBridge delivery; it routes events through Amazon SNS and is unrelated to whether events appear in EventBridge under source: aws.rds.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Native RDS EventBridge Events | RDS service events published directly to the EventBridge default event bus by the RDS service itself, without requiring an RDS Event Subscription or CloudTrail. Identified by source: aws.rds and detail-type values like 'RDS DB Instance Event'. Delivered on a best-effort basis. |
| RDS Event Subscription | An Amazon RDS mechanism that routes selected event categories to Amazon SNS topics. Separate from native EventBridge delivery. Does not control whether events appear in EventBridge under source: aws.rds. |
| AWS API Call via CloudTrail | An EventBridge detail-type value for events that CloudTrail captures from AWS API calls and routes to EventBridge. For RDS API calls, the source is aws.rds and detail.eventSource is rds.amazonaws.com. Requires a CloudTrail trail with logging enabled. |
| CloudTrail Trail | An AWS CloudTrail configuration resource that captures API activity and delivers logs to an S3 bucket. A prerequisite for 'AWS API Call via CloudTrail' events to appear in EventBridge. Without a trail, API calls appear in CloudTrail Event History (90 days) but not in EventBridge. |
| Best-Effort Event Delivery | AWS documentation characterization of native RDS EventBridge event delivery. Events may be missing. AWS explicitly recommends against building automation that depends on guaranteed delivery of RDS events. |
| EventBridge Content Filtering — anything-but with wildcard | A valid EventBridge event pattern operator combination. The pattern {"anything-but": {"wildcard": "*string*"}} matches any field value that does not match the wildcard pattern. Supported for event bus rules; not supported for EventBridge Pipes. |
| ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS | An EventBridge rule state that allows the rule to match all CloudTrail management events, including read-only events that the default ENABLED state excludes. Write management events like CreateDBInstance are matched by standard ENABLED rules when a trail exists. |
| CreateDBInstance | The RDS API operation that initiates DB instance creation. When CloudTrail logs this call and EventBridge fires, the DB instance status is 'creating' — the instance is not yet available. Classified as a write management event in CloudTrail. |
| RestoreDBInstanceFromDBSnapshot | The RDS API operation that initiates DB instance restoration from a snapshot. Like CreateDBInstance, the CloudTrail event fires at API call time, not at completion — instance is in 'creating' state. |

---

## Tensions & Tradeoffs

- AWS documentation simultaneously asserts that RDS sends all service events natively to EventBridge AND warns that events are best-effort and may be missing — this tension is unresolved and the practical consequence for creation events is undocumented.
- The CloudTrail workaround fires at API call time (instance is 'creating'), whereas the native RDS-EVENT-0005 event presumably fires after creation completes — downstream automation must accommodate one of these two timing models, not both simultaneously.
- A CloudTrail trail is required for the CloudTrail workaround path, adding an infrastructure dependency that may not exist in all accounts; accounts relying only on CloudTrail Event History (the free 90-day default) cannot use EventBridge CloudTrail rules.
- The 'anything-but wildcard' filter pattern is not supported in EventBridge Pipes — teams using Pipes for event routing cannot use this filter directly and need an alternative exclusion mechanism.

---

## Open Questions

- Does RDS actually emit RDS-EVENT-0005 natively to EventBridge when a DB instance is created, or does the best-effort model mean this event is consistently absent? No primary source provides a sample event or confirms the creation event fires in practice.
- Is the hypothesized cause (filter mismatch on the Message field) confirmed or refuted? If RDS-EVENT-0005 fires natively, what is the exact Message field value AWS sends for a creation event?
- Does RestoreDBInstanceFromDBSnapshot produce an RDS-EVENT-0019 or RDS-EVENT-0043 natively on EventBridge, and if so, with what Message field value?
- For accounts with AWS Backup restores, does the backup service invoke RestoreDBInstanceFromDBSnapshot directly, or does it use a different API operation — affecting which eventName to filter on?

---

## Sources & References

- [Amazon Relational Database Service events - Amazon EventBridge (Events Reference)](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-rds.html)
- [Creating a rule that triggers on an Amazon RDS event - Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-cloud-watch-events.html)
- [Amazon RDS event categories and event messages - Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.Messages.html)
- [AWS service events delivered via AWS CloudTrail - Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html)
- [Receiving read-only management events from AWS services - Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail-management.html)
- [Content filtering in Amazon EventBridge event patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns-content-based-filtering.html)
- [Comparison operators for use in event patterns in Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html)
- [Monitoring Amazon RDS API calls in AWS CloudTrail - Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/logging-using-cloudtrail.html)
- [Tutorial: Create an EventBridge rule that reacts to AWS API calls via CloudTrail](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-log-api-call.html)
- [Overview of Amazon RDS event notification - Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.overview.html)
- [Amazon RDS events - AWS Prescriptive Guidance (Monitoring and Alerting)](https://docs.aws.amazon.com/prescriptive-guidance/latest/amazon-rds-monitoring-alerting/rds-events.html)
