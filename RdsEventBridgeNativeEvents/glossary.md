# Glossary — RDS EventBridge Native Events vs CloudTrail Workaround

Quick definitions of key terms and concepts referenced in this investigation.

---

## Native RDS EventBridge Events

RDS service events published directly to the EventBridge default event bus by the RDS service itself, without requiring an RDS Event Subscription or CloudTrail. Identified by source: aws.rds and detail-type values like 'RDS DB Instance Event'. Delivered on a best-effort basis.

## RDS Event Subscription

An Amazon RDS mechanism that routes selected event categories to Amazon SNS topics. Separate from native EventBridge delivery. Does not control whether events appear in EventBridge under source: aws.rds.

## AWS API Call via CloudTrail

An EventBridge detail-type value for events that CloudTrail captures from AWS API calls and routes to EventBridge. For RDS API calls, the source is aws.rds and detail.eventSource is rds.amazonaws.com. Requires a CloudTrail trail with logging enabled.

## CloudTrail Trail

An AWS CloudTrail configuration resource that captures API activity and delivers logs to an S3 bucket. A prerequisite for 'AWS API Call via CloudTrail' events to appear in EventBridge. Without a trail, API calls appear in CloudTrail Event History (90 days) but not in EventBridge.

## Best-Effort Event Delivery

AWS documentation characterization of native RDS EventBridge event delivery. Events may be missing. AWS explicitly recommends against building automation that depends on guaranteed delivery of RDS events.

## EventBridge Content Filtering — anything-but with wildcard

A valid EventBridge event pattern operator combination. The pattern {"anything-but": {"wildcard": "*string*"}} matches any field value that does not match the wildcard pattern. Supported for event bus rules; not supported for EventBridge Pipes.

## ENABLED_WITH_ALL_CLOUDTRAIL_MANAGEMENT_EVENTS

An EventBridge rule state that allows the rule to match all CloudTrail management events, including read-only events that the default ENABLED state excludes. Write management events like CreateDBInstance are matched by standard ENABLED rules when a trail exists.

## CreateDBInstance

The RDS API operation that initiates DB instance creation. When CloudTrail logs this call and EventBridge fires, the DB instance status is 'creating' — the instance is not yet available. Classified as a write management event in CloudTrail.

## RestoreDBInstanceFromDBSnapshot

The RDS API operation that initiates DB instance restoration from a snapshot. Like CreateDBInstance, the CloudTrail event fires at API call time, not at completion — instance is in 'creating' state.

---

*Back to: [investigation.md](investigation.md)*
