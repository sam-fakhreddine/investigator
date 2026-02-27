# IAM Identity Center InstanceAccessControlAttributeConfiguration — Drift, Idempotency, and Update Behavior — Product Brief

**Date:** 2026-02-27
**Risk Level:** HIGH

---

## What Is This?

> The AWS configuration that lets users' attributes (like department or team) control which AWS accounts they can access is a single, shared setting per Identity Center instance. If the infrastructure deployment stack that manages this setting is deleted, access stops working immediately for everyone relying on it — with no automatic recovery.

---

## What Does This Mean for Us?

This is not a setting that can be safely managed in an IaC stack without explicit protection turned on. By default, deleting the stack deletes the setting. Also, AWS has no built-in alarm or detection if someone changes this setting outside of the deployment pipeline — changes made via the AWS console are invisible to the pipeline.

---

## Next Steps

**Engineering Work Items:**
- I
- n
- f
- r
- a
- /
- a
- r
- c
- h
- i
- t
- e
- c
- t
- u
- r
- e
-  
- t
- e
- a
- m
-  
- t
- o
-  
- a
- d
- d
-  
- D
- e
- l
- e
- t
- i
- o
- n
- P
- o
- l
- i
- c
- y
- :
-  
- R
- e
- t
- a
- i
- n
-  
- t
- o
-  
- t
- h
- e
-  
- r
- e
- s
- o
- u
- r
- c
- e
-  
- a
- n
- d
-  
- e
- n
- a
- b
- l
- e
-  
- s
- t
- a
- c
- k
-  
- t
- e
- r
- m
- i
- n
- a
- t
- i
- o
- n
-  
- p
- r
- o
- t
- e
- c
- t
- i
- o
- n
-  
- o
- n
-  
- t
- h
- e
-  
- o
- w
- n
- i
- n
- g
-  
- s
- t
- a
- c
- k
- .

---

*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*
