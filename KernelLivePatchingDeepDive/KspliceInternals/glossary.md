# Glossary — Internal Mechanics of Oracle Ksplice

Quick definitions of key terms and concepts referenced in this investigation.

---

## Pre-Post Differencing

A method of identifying code changes by comparing ELF object files generated from original (Pre) and patched (Post) sources.

## Run-Pre Matching

A technique to resolve symbols and verify in-memory code by comparing it to the original object code structure.

## 5-byte JMP Trampoline

A relative jump instruction injected at a function's entry point to redirect execution to a patched version.

## Enhanced Client

The Ksplice component responsible for applying rebootless updates to userspace shared libraries.

## Stop-the-world

A brief execution pause used to safely modify process memory and instruction streams during a patch application.

---

*Back to: [investigation.md](investigation.md)*
