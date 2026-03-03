# TypeScript-Native Entra Group Management — Graph SDK, Pulumi Automation API, and the State-Tracking Gap — Product Brief

**Date:** 2026-03-02
**Risk Level:** MEDIUM

---

## What Is This?

> Developers cannot manage Entra group membership declaratively from TypeScript alone with no extra tool to install — the team must either accept a one-time CLI install or build custom state management from scratch.

---

## What Does This Mean for Us?

The team's goal of 'just npm run, no separate tools to install' is not achievable with any production-ready library today for this specific use case. The closest option (Pulumi Automation API) hides the CLI from daily developer workflow but still requires the pulumi binary pre-installed in CI. The other option (Graph SDK) requires the team to build the state-management layer themselves, which is weeks of engineering work not directly related to business value.

---

## Key Points

- There is no npm package today that combines Entra group management with state tracking and drift detection without a separate CLI binary
- Pulumi Automation API: Developers write TypeScript and run 'npm run deploy' — the binary is installed once in CI and is transparent to daily work; this is the lowest-friction path
- Graph SDK alone: Developers can add/remove members via TypeScript, but manual bookkeeping is required to know what changed and to detect unintended drift — this is not declarative IaC
- Building a custom state manager on top of Graph SDK is technically possible but is a multi-week engineering project to replicate what Pulumi already provides

---

## Next Steps

**PO/EM Decision:**

> Confirm with Architects whether accepting the Pulumi binary as a CI install dependency is acceptable; if yes, the Automation API path unblocks the team immediately with no custom build required.

**Engineering Work Items:**
- Architects: evaluate Pulumi Automation API path — document the CI binary install requirement, select a state backend (Pulumi Cloud vs S3), and prototype an inline TypeScript stack managing one Entra group
- Architects: if pure-npm is a hard requirement, scope the DIY state layer — define the desired-state file format, locking strategy (Azure Blob lease vs S3 conditional writes), and plan/apply loop design before committing to the build
- Developers: do not build imperative Graph SDK scripts as a substitute for IaC — scripts with no state file create long-term drift risk and are hard to audit

**Leadership Input Required:**

> Decision needed on whether the Pulumi binary as a CI tool dependency is acceptable. This is a toolchain governance question, not a capability question — Pulumi Automation API delivers the desired developer experience once the binary is present.

---

## Open Questions

- Is the Pulumi binary an acceptable CI dependency, or is there a policy that prevents installing non-npm tools in the build environment?
- If a DIY state layer is built, who owns ongoing maintenance — what happens when the Graph API adds pagination behavior or the state format needs to evolve?
- Would the Pulumi Automation API running in CI satisfy the 'just npm run' experience from a developer's perspective, even if the binary is pre-installed in the CI image?

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
