# Investigation: TypeScript-Native Entra Group Management — Graph SDK, Pulumi Automation API, and the State-Tracking Gap

**Date:** 2026-03-02
**Status:** Complete

---

## Question

> In a hybrid Entra ID + AWS IAM Identity Center environment, what TypeScript-native options exist for managing Entra group membership declaratively with state and drift tracking — without installing or invoking a separate IaC CLI tool (no `pulumi up`, no `terraform apply`)?

---

## Context

The team already uses TypeScript and wants to manage Entra cloud-native group membership as code with state tracking and drift detection, where groups are assigned to IAM Identity Center permission sets. Prior research confirmed Pulumi @pulumi/azuread and Terraform hashicorp/azuread are viable for this use case, but both require a separate CLI binary and a state backend. The team wants to know whether a credible TypeScript-native path exists — npm packages only, no out-of-band toolchain install — that provides equivalent guarantees.

---

## TypeScript-Native Entra Group Management — Option Comparison

| Option | State file | Drift detection | CLI required | Notes |
| --- | --- | --- | --- | --- |
| Pulumi Automation API (@pulumi/pulumi/automation) | Yes — Pulumi backends | Yes — built-in | Yes — pulumi binary in PATH required | Hides CLI from caller but does not eliminate the binary requirement |
| CDKTF (@cdktf/provider-azuread) | Yes — Terraform state | Yes — built-in | Yes — terraform binary required | Prebuilt provider archived Dec 2025; must generate bindings locally for cdktf >0.21.0 |
| Microsoft Graph SDK (@microsoft/microsoft-graph-client) | No | No | No — pure npm | Full CRUD for groups/membership; no state file, no reconciliation loop, no drift detection |
| Microsoft Graph SDK + DIY state layer | Yes — if engineered | Yes — if engineered | No — pure npm | Feasible but a substantial build: state file, locking, plan/apply loop, rollback |
| SST / Nitric / other TS frameworks | AWS only (SST) / limited Azure (Nitric) | N/A | No for SST; depends for Nitric | Neither supports Entra ID group membership management as of early 2026 |

> No production-ready TypeScript npm package provides Pulumi/Terraform-equivalent state + drift detection for Entra groups without a CLI binary. The Pulumi Automation API is the closest answer, but the pulumi binary must still be installed. Graph SDK alone is an imperative API; turning it into a declarative reconciler requires engineering a custom state layer.

---

## Key Findings

- The Pulumi Automation API (@pulumi/pulumi/automation) allows a TypeScript program to invoke pulumi preview and pulumi up programmatically via LocalWorkspace.createOrSelectStack() and stack.up(), removing the need for a human to run CLI commands — but the pulumi CLI binary must still be installed and present in PATH; without it, Automation API calls throw at runtime.
- CDKTF (@cdktf/provider-azuread) synthesizes Terraform HCL from TypeScript and then requires the Terraform CLI binary to execute cdktf deploy; the prebuilt npm package @cdktf/provider-azuread was archived by HashiCorp on 10 December 2025 and will not receive updates for cdktf versions beyond 0.21.0, requiring local binding generation for newer versions.
- The Microsoft Graph SDK for TypeScript (@microsoft/microsoft-graph-client with @azure/identity) supports full CRUD for Entra security group membership via the v1.0 Graph API — POST /groups/{id}/members/$ref to add, DELETE /groups/{id}/members/{memberId}/$ref to remove, GET /groups/{id}/members to list — but provides no state file, no desired-state reconciliation, and no drift detection; it is an imperative HTTP client, not a declarative engine.
- The Microsoft Graph SDK does provide a delta query endpoint (GET /groups/delta?$select=members) that returns incremental changes since a saved deltaToken; this is a change-notification primitive, not drift detection against declared desired state — it tells the caller what Graph changed, not whether Graph diverged from a desired configuration the caller owns.
- A credible DIY state layer on top of Graph SDK would require: (1) a desired-state file format (e.g., JSON mapping group names to member lists), (2) a state store with concurrency locking (e.g., Azure Blob + lease API or S3 + conditional writes), (3) a plan step that calls Graph to read current state and diffs against desired, (4) an apply step that calls Graph to add/remove members, and (5) rollback logic on partial failure — this is equivalent to re-implementing the core of a declarative IaC engine and represents weeks of engineering work.
- SST v3 targets AWS exclusively and has no Azure or Entra resource management capability; it is not a candidate for this use case.
- Nitric is cloud-agnostic but focuses on application infrastructure (APIs, queues, buckets, key-value stores); it does not expose Entra ID group or membership management resources and is not a candidate for this use case.
- No open-source TypeScript npm package specifically implementing declarative Entra group membership management with state tracking and drift detection was found as of early 2026; the gap between the imperative Graph SDK and a full IaC engine is entirely unbridged at the library level.
- The Pulumi Automation API pattern (inline TypeScript program + LocalWorkspace) is the most credible path to 'just npm run' for a team that can accept a one-time CLI binary install in their CI environment — the developer experience is TypeScript only, and no human runs pulumi up directly.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| Pulumi Automation API | A TypeScript (and multi-language) SDK module (@pulumi/pulumi/automation) that wraps the Pulumi engine programmatically. Exposes LocalWorkspace.createOrSelectStack(), stack.preview(), and stack.up() as async functions callable from any Node.js program. Requires the pulumi CLI binary present in PATH at runtime; the binary is invoked by the SDK internally. Does not eliminate the binary requirement. |
| LocalWorkspace (Pulumi) | The primary Automation API class. Manages a local Pulumi project directory, installs provider plugins, and executes stack operations. For inline programs, the Pulumi project exists only in memory — no Pulumi.yaml file is required on disk. State is still stored in whichever backend is configured (Pulumi Cloud, S3, Azure Blob, etc.). |
| CDKTF (@cdktf/provider-azuread) | Cloud Development Kit for Terraform — a framework that generates Terraform HCL from TypeScript class definitions, then calls terraform CLI commands (init, plan, apply) to execute. The @cdktf/provider-azuread prebuilt npm package was archived by HashiCorp on 10 December 2025 and is not compatible with cdktf versions beyond 0.21.0. Teams using newer cdktf must generate provider bindings locally using cdktf provider add --force-local. |
| @microsoft/microsoft-graph-client | The official Microsoft Graph JavaScript/TypeScript SDK (older generation). Provides a fluent HTTP client for Graph API endpoints. Supports group CRUD and membership add/remove operations. Pure npm, no CLI binary required. No state file, no desired-state reconciliation, no plan/apply semantics. |
| @microsoft/msgraph-sdk (Kiota-generated) | The next-generation Microsoft Graph TypeScript SDK, generated by Kiota. As of early 2026 this SDK is in pre-release. Provides strongly-typed fluent access to Graph v1.0 endpoints including group membership. Installed via npm with no CLI binary dependency. Has the same absence of state/drift primitives as the older client library. |
| Graph API delta query | A Microsoft Graph feature (GET /groups/delta) that returns incremental changes to groups since a saved deltaToken. Surfaces additions and removals of group members via members@delta in responses. Useful for sync clients that maintain a local copy of group state; not a substitute for drift detection against a declared desired configuration, because the declared state is external to Graph and not known to the delta endpoint. |
| Desired-state reconciliation | The IaC pattern in which a tool compares a declared desired configuration (the code) against the current state of the system, generates a plan (diff), and then applies only the changes needed to close the gap. Pulumi and Terraform implement this via their state file plus provider refresh. The Graph SDK provides no equivalent — a developer using the SDK must implement the read/diff/write loop explicitly. |
| Concurrency locking (DIY state) | A mechanism that prevents two concurrent pipeline runs from simultaneously modifying group membership and corrupting state. Pulumi Cloud provides transactional locking natively. A DIY state layer over Graph SDK must implement this separately, e.g., using Azure Blob Storage lease tokens or S3 conditional writes (if-match on ETag). |
| SST v3 | A TypeScript-first framework for deploying full-stack serverless applications on AWS. AWS-only; no Azure or Entra ID resource support. As of 2025, SST's core team shifted focus to OpenCode and the framework entered maintenance mode. Not applicable to Entra group management. |
| Nitric | A cloud-agnostic TypeScript (and multi-language) application framework that deploys to AWS, GCP, and Azure. Targets application infrastructure primitives (APIs, queues, buckets). Does not expose identity plane resources such as Entra groups or Microsoft Graph operations. Not applicable to this use case. |

---

## Tensions & Tradeoffs

- The Pulumi Automation API offers developer-facing TypeScript-only ergonomics (no pulumi CLI invocations in developer flow) but does not eliminate the binary dependency — the pulumi binary must be installed in CI and on developer machines, which is exactly the kind of toolchain dependency the team wants to avoid.
- The Graph SDK eliminates all CLI binary dependencies and is pure npm, but it provides no state or drift abstractions — the team would be writing imperative group management scripts, not declarative IaC, and must build all reconciliation logic themselves.
- Building a DIY state layer on top of Graph SDK would give the team full TypeScript ownership with no external binary, but the engineering cost (state format, locking, plan step, apply step, rollback) approximates what Pulumi and Terraform already provide, raising the question of whether the team is better served by accepting the CLI binary as a CI dependency rather than re-implementing its core functionality.
- CDKTF synthesizes TypeScript into Terraform HCL and then calls the Terraform binary — it is farther from 'pure npm' than Pulumi Automation API, and the @cdktf/provider-azuread prebuilt package being archived adds additional friction.
- The Graph API delta query is a near-miss for drift detection: it efficiently surfaces changes that have occurred in Entra, but it cannot detect divergence from a desired state that is owned by the team's codebase rather than by Graph — the desired state must live somewhere, and Graph does not know about it.

---

## Open Questions

- Whether the Pulumi team has any roadmap item to bundle the Pulumi engine as a native Node.js module (eliminating the binary dependency), similar to how some tools embed their engines as npm packages.
- Whether an Azure Blob Storage lease-based locking primitive would satisfy the team's concurrency safety requirements if they choose to build a DIY state layer, and what the failure modes are if a CI runner crashes mid-apply while holding the lease.
- Whether the team's CI environment (GitHub Actions, Jenkins, etc.) would accept a pre-installed Pulumi binary as a documented tool dependency, which would make the Automation API path operationally indistinguishable from a pure-npm workflow from the developer's perspective.
- Whether the pre-release @microsoft/msgraph-sdk (Kiota-generated) is approaching GA stability for group membership operations, and whether a future Microsoft-published library will wrap the Graph SDK with any state-management primitives.

---

## Sources & References

- [Embedding Pulumi with the Automation API — Pulumi Docs](https://www.pulumi.com/docs/iac/automation-api/)
- [Getting Started with Automation API — Pulumi Docs](https://www.pulumi.com/docs/iac/automation-api/getting-started-automation-api/)
- [Pulumi Automation API — automation module Node.js SDK reference](https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/pulumi/automation/)
- [pulumi/automation-api-examples — GitHub](https://github.com/pulumi/automation-api-examples)
- [cdktf/cdktf-provider-azuread — GitHub (archived Dec 2025)](https://github.com/cdktf/cdktf-provider-azuread)
- [CLI Commands — CDK for Terraform (cdktf deploy requires terraform binary)](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands)
- [@microsoft/microsoft-graph-client — npm](https://www.npmjs.com/package/@microsoft/microsoft-graph-client)
- [microsoftgraph/msgraph-sdk-typescript — GitHub (pre-release)](https://github.com/microsoftgraph/msgraph-sdk-typescript)
- [Manage Groups in Microsoft Graph v1.0 — Microsoft Learn](https://learn.microsoft.com/en-us/graph/api/resources/groups-overview?view=graph-rest-1.0)
- [Add member (group) — Microsoft Graph v1.0 — Microsoft Learn](https://learn.microsoft.com/en-us/graph/api/group-post-members?view=graph-rest-1.0)
- [Get incremental changes for groups (delta query) — Microsoft Learn](https://learn.microsoft.com/en-us/graph/delta-query-groups)
- [How to use Pulumi Automation API, with examples — TechTarget](https://www.techtarget.com/searchitoperations/tutorial/How-to-use-Pulumi-Automation-API-with-examples)
- [IaC Best Practices: Using Automation API — Pulumi Blog](https://www.pulumi.com/blog/iac-best-practices-using-automation-api/)
- [SST alternatives in 2026 — Northflank Blog](https://northflank.com/blog/sst-alternatives-serverless-stack)
- [Nitric — cloud-agnostic TypeScript framework](https://nitric.io/)
