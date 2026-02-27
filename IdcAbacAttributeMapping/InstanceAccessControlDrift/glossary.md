# Glossary — IAM Identity Center InstanceAccessControlAttributeConfiguration — Drift, Idempotency, and Update Behavior

Quick definitions of key terms and concepts referenced in this investigation.

---

## InstanceAccessControlAttributeConfiguration

The IAM Identity Center API resource (and CloudFormation resource type AWS::SSO::InstanceAccessControlAttributeConfiguration) that enables ABAC and defines the set of user attributes to be passed as principal tags when a user federates into an AWS account. Exactly one such configuration can exist per IdC instance.

## CreateInstanceAccessControlAttributeConfiguration

The sso-admin API call that enables ABAC for an IdC instance for the first time and sets the initial attribute mappings. Returns ConflictException if ABAC is already enabled. CloudFormation's create handler for this resource type calls this API.

## UpdateInstanceAccessControlAttributeConfiguration

The sso-admin API call that modifies the attribute mappings on an already-ABAC-enabled IdC instance. Called by the CloudFormation update handler when AccessControlAttributes changes without a resource replacement. Does not disable or re-enable ABAC — it only updates the attribute list.

## DeleteInstanceAccessControlAttributeConfiguration

The sso-admin API call that fully disables ABAC and removes all attribute mappings for an IdC instance. Called by the CloudFormation delete handler when the resource is removed from a stack or the stack is deleted. Immediately stops attribute propagation — ABAC-dependent policies become non-matching.

## DescribeInstanceAccessControlAttributeConfiguration

The sso-admin read-side API that returns the current ABAC status (ENABLED, CREATION_IN_PROGRESS, or CREATION_FAILED) and the configured attribute list for an IdC instance. Used by the CloudFormation resource provider's read handler to assess current state. Believed to return ResourceNotFoundException for instances with no ABAC configuration.

## Singleton resource

A CloudFormation resource pattern where only one physical resource can exist per logical scope (in this case, per IdC instance). The API enforces this — a second Create call against the same InstanceArn will fail. CloudFormation does not prevent two stacks from declaring the same InstanceArn; the conflict surfaces only at deploy time.

## Resource replacement

A CloudFormation update path where the existing resource is deleted and a new one is created, rather than updating in place. Triggered when an immutable property (InstanceArn for this resource type) is changed. For InstanceAccessControlAttributeConfiguration, replacement destroys ABAC config on the original instance.

## NOT_CHECKED drift status

The CloudFormation drift status assigned to resource types that do not support drift detection. AWS::SSO::InstanceAccessControlAttributeConfiguration receives this status. Changes made outside of CloudFormation will not be detected.

## DeletionPolicy / UpdateReplacePolicy

CloudFormation resource attributes that control what happens when a resource is deleted from a stack or replaced during an update. Setting DeletionPolicy: Retain prevents the Delete API from being called when the stack is deleted or the resource is removed. In CDK, these are set via applyRemovalPolicy() on the L1 construct's cfnOptions.

## ConflictException

An sso-admin API error returned when a write operation conflicts with a previous write. For CreateInstanceAccessControlAttributeConfiguration, this is the expected error when ABAC is already enabled on the instance. The documented recovery is retry with backoff, but in the context of a double-create (resource already exists), retry will not resolve the conflict.

---

*Back to: [investigation.md](investigation.md)*
