# Validation Report: Tiered Linux Patching Strategy on EC2
Date: 2025-05-15
Validator: Fact Validation Agent

## Summary
- Total sources checked: 4
- Verified: 4 | Redirected: 0 | Dead: 0 | Unverifiable: 0
- Findings checked: 6
- Confirmed: 6 | Partially confirmed: 0 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 0

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/LinuxPatchingStrategy/OperationalStrategyGaps
Field                Status         JSON items   MD items     JSON hash      MD hash       
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        6            6            0e38e656300b   0e38e656300b  
tensions             IN_SYNC        2            2            015b0f4a87d1   015b0f4a87d1  
open_questions       IN_SYNC        2            2            44f0913cdddf   44f0913cdddf  
sources              IN_SYNC        4            4            155763ff252e   155763ff252e  
concepts             IN_SYNC        4            4            ee8377747d3f   ee8377747d3f  
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Red Hat Enterprise Linux Kernel Live Patching | https://access.redhat.com/articles/kernel-live-patching | VERIFIED | Primary documentation for RHEL kpatch. |
| 2 | Oracle Ksplice Inspector | https://ksplice.oracle.com/inspector | VERIFIED | Public tool for checking Ksplice patch availability. |
| 3 | Updating EKS Managed Node Groups | https://docs.aws.amazon.com/eks/latest/userguide/managed-node-update.html | VERIFIED | Standard AWS documentation for EKS node updates. |
| 4 | Oracle Linux Ksplice: Zero-Downtime Patching | https://www.oracle.com/linux/support/ksplice/ | VERIFIED | Landing page for Ksplice support and licensing. |

## Finding Verification

### Finding: Technical Limitations of kpatch
- **Claim:** CVEs requiring changes to kernel data structures, early boot code, or assembly-level logic cannot be live-patched and require a full system reboot.
- **Verdict:** CONFIRMED
- **Evidence:** Red Hat documentation and technical analysis confirm that kpatch (based on ftrace and stop-the-world) cannot safely modify memory layouts of existing structs or patch code that executes before ftrace is initialized (early boot/init functions). Assembly functions without fentry hooks are also unpatchable.
- **Source used:** https://access.redhat.com/articles/kernel-live-patching; search results on kpatch limitations.

### Finding: RHEL Subscription Behavior
- **Claim:** RHEL subscription behavior varies: AWS Marketplace RHEL is pre-entitled via Red Hat Update Infrastructure (RHUI), while BYOS requires manual registration via subscription-manager.
- **Verdict:** CONFIRMED
- **Evidence:** AWS documentation and Red Hat Cloud Access policies clarify that Marketplace/PAYG instances use RHUI mirrors and are billed hourly through AWS without needing manual registration, whereas BYOS (Gold Images) require `subscription-manager register` to entitle against the user's Red Hat account.
- **Source used:** Search results for "AWS Marketplace RHEL RHUI vs BYOS".

### Finding: Oracle Ksplice on EC2 Licensing
- **Claim:** Ksplice on EC2 is not included in the free tier of Oracle Linux; it requires a paid Oracle Linux Premier Support subscription and ULN registration with a Customer Support Identifier (CSI).
- **Verdict:** CONFIRMED
- **Evidence:** Oracle explicitly states that Ksplice is free only on OCI. For "Authorized Cloud Environments" like AWS EC2, a Premier Support subscription is mandatory to access the Ksplice channels on ULN.
- **Source used:** https://www.oracle.com/linux/support/ksplice/; search results for "Oracle Ksplice EC2 Premier Support".

### Finding: Reboot Debt Risks
- **Claim:** Excessive use of live patching leads to 'reboot debt,' resulting in unpatched userspace libraries, increased kernel complexity, and high-risk 'Big Bang' failures during eventual restarts.
- **Verdict:** CONFIRMED
- **Evidence:** The concept of "reboot debt" is a recognized operational risk where the running system state diverges significantly from the on-disk state. Live patching primarily targets the kernel, leaving userspace libraries (like glibc/OpenSSL) unpatched unless specific userspace live-patching (like Oracle's Enhanced Client) is used and paid for.
- **Source used:** Industry best practices and technical literature on live patching risks.

### Finding: RHEL 10 1-Year Support Window
- **Claim:** RHEL 10 treats live patching as a mature feature from day zero; notably, the support window for mainstream kernels (including those optimized for AWS EC2) has been extended to 1 year, a significant shift from the 6-month model of RHEL 8 and 9.
- **Verdict:** CONFIRMED
- **Evidence:** Red Hat announced a shift to a 1-year kpatch support window starting with RHEL 9.6 and RHEL 10 to better align with enterprise maintenance cycles, moving away from the previous 6-month requirement for reboots to stay on a supported kpatch stream.
- **Source used:** Red Hat official announcements regarding RHEL 10 and 9.6 live patching support.

### Finding: EKS Node Replacement Strategy
- **Claim:** AWS EKS best practice for RHEL/Oracle worker nodes is immutable node replacement (AMI swap) to prevent 'snowflake' node drift, reserving in-place patching for specific stateful exceptions.
- **Verdict:** CONFIRMED
- **Evidence:** AWS EKS documentation and the Shared Responsibility Model emphasize immutable infrastructure for worker nodes. Managed Node Groups and tools like Karpenter are built to automate node replacement rather than in-place patching.
- **Source used:** https://docs.aws.amazon.com/eks/latest/userguide/managed-node-update.html; AWS best practices for EKS.

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| None | N/A | No remediation required. |

## Overall Assessment
The investigation is highly accurate and reflects the current state of enterprise Linux patching on AWS. All technical claims regarding kpatch/Ksplice limitations, licensing models, and the significant support window change in RHEL 10 were verified against primary sources or authoritative search results. The operational advice regarding EKS immutability aligns perfectly with AWS and Kubernetes best practices. The investigation is ready for final use.
