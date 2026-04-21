# Validation Report: Red Hat kpatch and Linux Kernel livepatch Internal Mechanics
Date: 2026-04-21
Validator: Fact Validation Agent

## Summary
- Total sources checked: 4
- Verified: 3 | Redirected: 0 | Dead: 1 | Unverifiable: 0
- Findings checked: 5
- Confirmed: 5 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/KernelLivePatchingDeepDive/KpatchInternals
Field                Status         JSON items   MD items     JSON hash      MD hash       
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        5            5            49e2d41b18dd   49e2d41b18dd  
tensions             IN_SYNC        3            3            1c5093de1fb8   1c5093de1fb8  
open_questions       IN_SYNC        3            3            d0de093e58da   d0de093e58da  
sources              IN_SYNC        4            4            460e043846bc   460e043846bc  
concepts             IN_SYNC        6            6            a34983f7454f   a34983f7454f  
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Kernel Livepatching (KLP) | https://www.kernel.org/doc/html/latest/livepatch/livepatch.html | VERIFIED | Official documentation for the KLP subsystem. |
| 2 | Ftrace: The hidden INT3 | https://lwn.net/Articles/576443/ | DEAD | URL points to an unrelated LWN article about a Firefox bug ("image.animation_mode broken?"). The correct URL for "Ftrace: The hidden INT3" is https://lwn.net/Articles/499190/. |
| 3 | Shadow Variables Documentation | https://www.kernel.org/doc/Documentation/livepatch/shadow-vars.txt | VERIFIED | Official documentation for shadow variables. |
| 4 | kpatch: dynamic kernel patching | https://github.com/dynup/kpatch | VERIFIED | Project repository. Notice confirmed that kpatch is deprecated in favor of klp-build as of Linux 6.19. |

## Finding Verification

### Finding: ftrace Redirection
- **Claim:** The Linux livepatch subsystem leverages the ftrace profiling infrastructure to intercept and redirect function execution... modifies the instruction pointer (IP) on the stack...
- **Verdict:** CONFIRMED
- **Evidence:** The `klp_ftrace_handler` is the standard callback used by KLP to perform redirection via ftrace. It modifies the stack frame to point to the new function body.
- **Source used:** https://www.kernel.org/doc/html/latest/livepatch/livepatch.html

### Finding: INT3 Breakpoint Mechanism
- **Claim:** Instruction modification on a live system is performed using the INT3 (breakpoint) mechanism... Ftrace replaces the first byte of a call site with the 0xCC opcode...
- **Verdict:** CONFIRMED
- **Evidence:** Ftrace uses the "breakpoint trick" (INT3) to safely update instructions on multi-core systems, avoiding race conditions during multi-byte writes.
- **Source used:** https://lwn.net/Articles/499190/ (Note: Corrected URL)

### Finding: klp-build Pipeline
- **Claim:** As of Linux 6.19 (Feb 2026), the legacy kpatch-build pipeline has been superseded by klp-build for upstream kernel livepatching.
- **Verdict:** CONFIRMED
- **Evidence:** `klp-build` was indeed merged in Linux 6.19 to provide a more integrated, upstream-first toolchain for generating livepatch modules.
- **Source used:** https://github.com/dynup/kpatch, search results confirm 6.19 merge.

### Finding: objtool Fixups
- **Claim:** Architectural fixups... previously handled by GCC plugins... have migrated to objtool... On architectures like ppc64le, objtool now manages Table of Contents (TOC) pointer reloading (r2 register).
- **Verdict:** CONFIRMED
- **Evidence:** `objtool` now includes subcommands like `klp diff` and `klp post-link` which handle binary diffing and architectural fixups, including the critical `r2` TOC reload for ppc64le.
- **Source used:** LWN coverage of `klp-build` and `objtool` integration.

### Finding: Shadow Variables
- **Claim:** Shadow variables provide a mechanism for extending kernel data structures... stored in a global, RCU-protected hash table (klp_shadow_hash)...
- **Verdict:** CONFIRMED
- **Evidence:** `klp_shadow_hash` is a global hashtable defined in `kernel/livepatch/shadow.c`, managed using RCU for lockless lookups.
- **Source used:** https://www.kernel.org/doc/Documentation/livepatch/shadow-vars.txt

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Source #2 | `DEAD` | Update URL to `https://lwn.net/Articles/499190/` in `investigation.json`. |

## Overall Assessment
The investigation is highly accurate and reflects the current state of the Linux kernel as of April 2026. The transition from legacy `kpatch-build` to the upstream `klp-build`/`objtool` pipeline is correctly identified and detailed. The technical mechanisms (ftrace, INT3, Shadow Variables) are confirmed against primary documentation. One source URL is incorrect but the content it was intended to support is verified. The investigation can be trusted as a whole once the source URL is corrected.
