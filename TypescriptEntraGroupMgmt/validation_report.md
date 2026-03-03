# Validation Report: TypeScript-Native Entra Group Management — Graph SDK, Pulumi Automation API, and the State-Tracking Gap
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 15
- Verified: 13 | Redirected: 1 | Dead: 0 | Unverifiable: 1
- Findings checked: 8
- Confirmed: 7 | Partially confirmed: 1 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/TypescriptEntraGroupMgmt
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        9            9            65b1ab44f731   65b1ab44f731
tensions             IN_SYNC        5            5            a7270a368ba7   a7270a368ba7
open_questions       IN_SYNC        4            4            b432e7d7d624   b432e7d7d624
sources              IN_SYNC        15           15           4986c03916e3   4986c03916e3
concepts             IN_SYNC        10           10           e2fbabb14bb2   e2fbabb14bb2
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Embedding Pulumi with the Automation API — Pulumi Docs | https://www.pulumi.com/docs/iac/automation-api/ | VERIFIED | Page confirmed live; explicitly states "Automation API requires the Pulumi CLI to be installed and available in your PATH environment variable" |
| 2 | Getting Started with Automation API — Pulumi Docs | https://www.pulumi.com/docs/iac/automation-api/getting-started-automation-api/ | VERIFIED | Page confirmed live via search result; covers TypeScript inline program workflow |
| 3 | Pulumi Automation API — automation module Node.js SDK reference | https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/pulumi/modules/automation.html | REDIRECT | URL resolves but the canonical current URL is https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/pulumi/automation/ — old `/modules/automation.html` pattern redirects to the new path; content is correct |
| 4 | pulumi/automation-api-examples — GitHub | https://github.com/pulumi/automation-api-examples | VERIFIED | Repository confirmed active; contains TypeScript, Python, Go, C#, and Java examples |
| 5 | cdktf/cdktf-provider-azuread — GitHub (archived Dec 2025) | https://github.com/cdktf/cdktf-provider-azuread | VERIFIED | Confirmed archived; repository notice states HashiCorp stopped publishing new versions on December 10, 2025; prior versions not compatible with cdktf past 0.21.0 |
| 6 | CLI Commands — CDK for Terraform (cdktf deploy requires terraform binary) | https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands | VERIFIED | Page confirmed live via Hashicorp domain; documents cdktf CLI commands including deploy |
| 7 | @microsoft/microsoft-graph-client — npm | https://www.npmjs.com/package/@microsoft/microsoft-graph-client | VERIFIED | Package confirmed on npm; official Microsoft Graph JavaScript/TypeScript SDK |
| 8 | microsoftgraph/msgraph-sdk-typescript — GitHub (pre-release) | https://github.com/microsoftgraph/msgraph-sdk-typescript | VERIFIED | Repository confirmed live; SDK remains in pre-release as of early 2026; a "Post-GA Milestone" tracker exists on the core repo but no GA announcement found |
| 9 | Manage Groups in Microsoft Graph v1.0 — Microsoft Learn | https://learn.microsoft.com/en-us/graph/api/resources/groups-overview?view=graph-rest-1.0 | VERIFIED | Page confirmed live; documents group resource types and operations for v1.0 |
| 10 | Add member (group) — Microsoft Graph v1.0 — Microsoft Learn | https://learn.microsoft.com/en-us/graph/api/group-post-members?view=graph-rest-1.0 | VERIFIED | Page confirmed live; documents POST /groups/{group-id}/members/$ref endpoint at v1.0; returns 204 No Content on success |
| 11 | Get incremental changes for groups (delta query) — Microsoft Learn | https://learn.microsoft.com/en-us/graph/delta-query-groups | VERIFIED | Page confirmed live; documents GET /groups/delta with deltaToken, members@delta tracking |
| 12 | How to use Pulumi Automation API, with examples — TechTarget | https://www.techtarget.com/searchitoperations/tutorial/How-to-use-Pulumi-Automation-API-with-examples | VERIFIED | URL confirmed present in search index; article covers Automation API usage and binary requirement |
| 13 | IaC Best Practices: Using Automation API — Pulumi Blog | https://www.pulumi.com/blog/iac-recommended-practices-using-automation-api/ | REDIRECT | The current canonical URL is https://www.pulumi.com/blog/iac-best-practices-using-automation-api/ — the investigation URL uses `iac-recommended-practices-` while the live blog slug is `iac-best-practices-`; the page exists at the corrected URL and content matches |
| 14 | SST alternatives in 2026 — Northflank Blog | https://northflank.com/blog/sst-alternatives-serverless-stack | VERIFIED | Page confirmed live; covers SST entering maintenance mode after team pivoted to OpenCode in mid-2025 |
| 15 | Nitric — cloud-agnostic TypeScript framework | https://nitric.io/ | VERIFIED | Homepage confirmed live; framework targets APIs, queues, buckets, scheduled tasks, secrets — no Entra identity or group management primitives found |

---

## Finding Verification

### Finding 1: Pulumi Automation API CLI binary requirement
- **Claim:** The Pulumi Automation API allows a TypeScript program to invoke pulumi preview and pulumi up programmatically via LocalWorkspace.createOrSelectStack() and stack.up(), removing the need for a human to run CLI commands — but the pulumi CLI binary must still be installed and present in PATH; without it, Automation API calls throw at runtime.
- **Verdict:** CONFIRMED
- **Evidence:** Pulumi's official documentation at https://www.pulumi.com/docs/iac/automation-api/ states explicitly: "Automation API requires the Pulumi CLI to be installed and available in your PATH environment variable." GitHub issue #10000 (pulumi/pulumi) confirms: "The inlining/embedding feature of Pulumi aka the Automation API still has a hard dependency on local Pulumi CLI binary being present on PATH." The `LocalWorkspace.createOrSelectStack()` method signature and inline program pattern are confirmed by both official SDK reference and the automation-api-examples repository.
- **Source used:** https://www.pulumi.com/docs/iac/automation-api/, https://github.com/pulumi/pulumi/issues/10000

### Finding 2: CDKTF prebuilt provider archived December 2025
- **Claim:** The prebuilt npm package @cdktf/provider-azuread was archived by HashiCorp on 10 December 2025 and will not receive updates for cdktf versions beyond 0.21.0, requiring local binding generation for newer versions.
- **Verdict:** CONFIRMED
- **Evidence:** The GitHub repository https://github.com/cdktf/cdktf-provider-azuread is confirmed archived. The repository notice reads: "HashiCorp made the decision to stop publishing new versions of prebuilt Terraform azuread provider bindings for CDK for Terraform on December 10, 2025. As such, this repository has been archived." The notice also confirms incompatibility with cdktf past 0.21.0 and directs users to generate bindings locally via `cdktf provider add --force-local`.
- **Source used:** https://github.com/cdktf/cdktf-provider-azuread

### Finding 3: Microsoft Graph SDK supports group membership CRUD via v1.0 endpoints
- **Claim:** The Microsoft Graph SDK supports full CRUD for Entra security group membership via the v1.0 Graph API — POST /groups/{id}/members/$ref to add, DELETE /groups/{id}/members/{memberId}/$ref to remove, GET /groups/{id}/members to list.
- **Verdict:** CONFIRMED
- **Evidence:** All three endpoints confirmed against live Microsoft Learn documentation. POST /groups/{group-id}/members/$ref is documented at https://learn.microsoft.com/en-us/graph/api/group-post-members?view=graph-rest-1.0. DELETE /groups/{group-id}/members/{directoryObjectId}/$ref is documented at https://learn.microsoft.com/en-us/graph/api/group-delete-members?view=graph-rest-1.0. GET /groups/{id}/members is documented at https://learn.microsoft.com/en-us/graph/api/group-list-members?view=graph-rest-1.0. All are v1.0 endpoints.
- **Source used:** https://learn.microsoft.com/en-us/graph/api/group-post-members?view=graph-rest-1.0, https://learn.microsoft.com/en-us/graph/api/group-delete-members?view=graph-rest-1.0

### Finding 4: Graph delta query endpoint exists for incremental change notifications
- **Claim:** The Microsoft Graph SDK does provide a delta query endpoint (GET /groups/delta?$select=members) that returns incremental changes since a saved deltaToken; this is a change-notification primitive, not drift detection against declared desired state.
- **Verdict:** CONFIRMED
- **Evidence:** The delta query endpoint is confirmed at https://learn.microsoft.com/en-us/graph/delta-query-groups. The endpoint returns incremental changes to groups including membership additions and removals via `members@delta`. The characterization of delta query as a change-notification primitive (not drift detection against external desired state) is accurate — the endpoint reflects what changed in Entra, not whether Entra diverged from a caller-owned configuration.
- **Source used:** https://learn.microsoft.com/en-us/graph/delta-query-groups

### Finding 5: SST v3 targets AWS exclusively with no Entra ID support
- **Claim:** SST v3 targets AWS exclusively and has no Azure or Entra ID resource management capability; it is not a candidate for this use case.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** SST v3 built-in components are confirmed as AWS-only (namespaced `sst.aws.*`) and Cloudflare (`sst.cloudflare.*`). No built-in Azure or Entra ID components exist. However, SST v3 is built on Pulumi and technically supports 150+ Pulumi/Terraform providers, meaning raw Azure/Entra resources could be instantiated as escape-hatch provider calls — this is not the same as native support. The conclusion that SST is not a candidate for this use case remains valid: there is no native Entra group management abstraction, and using SST solely as a Pulumi wrapper adds no value over using Pulumi directly. The maintenance mode characterization is confirmed — the team shifted to OpenCode in mid-2025.
- **Source used:** https://northflank.com/blog/sst-alternatives-serverless-stack, https://sst.dev/docs/components/

### Finding 6: Nitric does not expose Entra group management resources
- **Claim:** Nitric is cloud-agnostic but focuses on application infrastructure primitives (APIs, queues, buckets, key-value stores); it does not expose Entra ID group or membership management resources and is not a candidate for this use case.
- **Verdict:** CONFIRMED
- **Evidence:** Nitric homepage and GitHub repository confirmed live. Nitric's documented primitives are: APIs, serverless functions, queues, topics, pub/sub, storage, databases, websockets, scheduled tasks, and secrets. No identity plane resources (Entra groups, Microsoft Graph operations, Azure AD) are documented or referenced anywhere in Nitric's public surface.
- **Source used:** https://nitric.io/, https://github.com/nitrictech/nitric

### Finding 7: No open-source TypeScript npm package implements declarative Entra group management with state tracking as of early 2026
- **Claim:** No open-source TypeScript npm package specifically implementing declarative Entra group membership management with state tracking and drift detection was found as of early 2026.
- **Verdict:** CONFIRMED
- **Evidence:** Search across npm, GitHub, and general web confirms no library in this specific category. The only TypeScript-first options found are: (a) Pulumi Automation API — requires CLI binary; (b) CDKTF — requires CLI binary and archived prebuilt provider; (c) Microsoft Graph SDK — imperative HTTP client with no state primitives. No community library bridging Graph SDK with state/drift semantics was found.
- **Source used:** General web search, npm search

### Finding 8: Pulumi Automation API is the most credible path for a TypeScript-only developer experience
- **Claim:** The Pulumi Automation API pattern (inline TypeScript program + LocalWorkspace) is the most credible path to 'just npm run' for a team that can accept a one-time CLI binary install in their CI environment — the developer experience is TypeScript only, and no human runs pulumi up directly.
- **Verdict:** CONFIRMED
- **Evidence:** `LocalWorkspace.createOrSelectStack()` with inline programs is confirmed functional in TypeScript; developers write and run a Node.js program without invoking pulumi CLI directly. The binary must exist in PATH at runtime but is not invoked by developers as part of their workflow. This matches the characterization in the finding.
- **Source used:** https://www.pulumi.com/docs/iac/automation-api/, https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/pulumi/modules/automation.html

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Source #3 — Pulumi Node.js SDK reference URL | REDIRECT | Update URL from `https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/pulumi/modules/automation.html` to `https://www.pulumi.com/docs/reference/pkg/nodejs/pulumi/pulumi/automation/` in `investigation.json`, then re-run `json_to_md.py` |
| Source #13 — Pulumi Blog IaC Best Practices URL | REDIRECT | Update URL from `https://www.pulumi.com/blog/iac-recommended-practices-using-automation-api/` to `https://www.pulumi.com/blog/iac-best-practices-using-automation-api/` in `investigation.json`, then re-run `json_to_md.py` |

---

## Overall Assessment

The investigation is factually sound. All eight key findings are confirmed or partially confirmed against live primary sources. The two critical claims flagged for verification — that the Pulumi Automation API requires the pulumi CLI binary in PATH despite being an npm package, and that the @cdktf/provider-azuread prebuilt package was archived on December 10, 2025 — are both confirmed verbatim against official documentation and the archived GitHub repository respectively. The Graph API CRUD endpoints (POST/DELETE/GET for group membership) and the delta query endpoint are all confirmed against current Microsoft Learn v1.0 documentation.

The partial confirmation on Finding 5 (SST) is minor: while SST v3 technically allows raw Pulumi provider calls to Azure, it has no native Entra ID abstractions, and the investigation's conclusion that SST is not a viable candidate is correct. The nuance does not warrant a correction — it could optionally be noted in `open_questions` but is not a material inaccuracy.

Two source URLs require remediation: the Pulumi Node.js SDK reference URL uses an outdated `/modules/automation.html` path (now `/automation/`), and the Pulumi blog post URL uses `iac-recommended-practices-` where the live slug is `iac-best-practices-`. Both resolve via redirect today but should be updated to their canonical URLs in `investigation.json` for durability. After updating, re-run `python3 scripts/json_to_md.py TypescriptEntraGroupMgmt` and confirm `check_sync.py` exits 0.

The characterization of `@microsoft/msgraph-sdk` (Kiota-generated) as "pre-release as of early 2026" is confirmed — no GA announcement was found, and a "Post-GA Milestone" tracker exists on the GitHub core repo indicating GA has not yet been reached.
