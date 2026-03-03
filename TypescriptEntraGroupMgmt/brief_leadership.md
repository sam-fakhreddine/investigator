# TypeScript-Native Entra Group Management — Graph SDK, Pulumi Automation API, and the State-Tracking Gap — Engineering Leadership Brief

**Date:** 2026-03-02

---

## Headline

> No production-ready TypeScript npm package provides Pulumi-equivalent state and drift detection for Entra groups without a CLI binary; the Pulumi Automation API is the closest answer but still requires the pulumi binary in CI.

---

## So What

The team's preference for a pure-npm toolchain has no viable off-the-shelf answer for this use case. The Pulumi Automation API removes the need for developers to invoke CLI commands manually but does not remove the binary dependency from the CI environment. Building a custom state layer over the Graph SDK is technically feasible but represents weeks of undifferentiated engineering work. The practical decision is between accepting the Pulumi binary as a CI dependency (low-effort, high-capability) or investing in a DIY reconciler (high-effort, full TypeScript ownership).

---

## Key Points

- Pulumi Automation API: TypeScript developers never run pulumi CLI commands directly; the SDK calls pulumi internally — but the binary must be installed in CI and on dev machines
- Microsoft Graph SDK: pure npm, no binary, full CRUD for group membership — but no state file, no plan step, no drift detection; it is an HTTP client, not a declarative engine
- CDKTF: synthesizes TypeScript to Terraform HCL and then shells out to terraform binary; the prebuilt @cdktf/provider-azuread npm package was archived December 2025 and adds toolchain complexity without removing the binary requirement
- SST and Nitric: neither supports Entra ID group management; both are application-infrastructure frameworks not identity-plane tools
- DIY state layer on Graph SDK: the team would need to build a desired-state store, a locking mechanism, a plan/diff step, an apply step, and rollback logic — weeks of work and ongoing maintenance burden

---

## Action Required

> Architects must make a pragmatic choice: accept the Pulumi binary as a documented CI dependency and use Automation API (low-effort, full IaC guarantees), or scope and staff a DIY reconciler project (high-effort, no binary dependency). A hybrid option — Pulumi Automation API now, DIY later if needed — is viable.

---

*Full engineering investigation: [investigation.md](investigation.md)*
