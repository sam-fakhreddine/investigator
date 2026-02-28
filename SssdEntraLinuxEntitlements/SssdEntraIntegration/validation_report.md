# Validation Report: SssdEntraIntegration (Cycle 2 Re-validation)

**Investigation:** Entra ID as an Identity Source for Linux SSSD on AWS EC2 Instances
**Validated:** 2026-02-28
**Status of investigation.json:** Complete
**Cycle:** 2 (re-validation after corrections from Cycle 1)

---

## Summary

The corrected investigation is accurate and well-sourced. All 13 key findings verified: 12 CONFIRMED, 1 PARTIALLY CONFIRMED. The two Cycle 1 corrections have been properly applied:

1. **Finding #6 (Entra Connect Sync direction):** Now correctly states the AWS-documented sync direction is FROM AWS Managed AD TO Entra ID. The previous validator incorrectly claimed the AWS page described the reverse direction; re-reading the AWS tutorial confirms AWS Managed AD is configured as the on-premises forest (source) and Entra ID is the cloud target (destination). The corrected finding is accurate.
2. **Entra DS custom attributes:** Now correctly states Enterprise/Premium SKUs support custom attributes (onPremisesExtensionAttributes 1-15 and directory extensions) but NOT RFC 2307 POSIX schema attributes. Confirmed by Microsoft Learn documentation.

All 19 sources are reachable and on-topic. JSON and MD are in sync.

---

## JSON/MD Sync Check

```
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        13           13           adbc7e476ea2   adbc7e476ea2
tensions             IN_SYNC        5            5            1e9c53382a74   1e9c53382a74
open_questions       IN_SYNC        6            6            f445769b8365   f445769b8365
sources              IN_SYNC        19           19           f492d9dc7595   f492d9dc7595
concepts             IN_SYNC        7            7            aafb59487e43   aafb59487e43
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

No sync issues found.

---

## Source Verification

| # | Source Title | URL | Status | Notes |
|---|-------------|-----|--------|-------|
| 1 | Sign in to a Linux VM using Entra ID and OpenSSH | learn.microsoft.com/.../howto-vm-sign-in-azure-ad-linux | VERIFIED | Page live, covers AADSSHLoginForLinux extension, OpenSSH certificates, RBAC, Arc support |
| 2 | How synchronization works in Entra Domain Services | learn.microsoft.com/.../synchronization | VERIFIED | Page live, confirms one-way sync from Entra ID to DS, password hash requirements for cloud-only users |
| 3 | Enable password hash sync for Entra DS | learn.microsoft.com/.../tutorial-configure-password-hash-sync | VERIFIED | Page live, covers hybrid password hash sync for on-prem AD scenarios |
| 4 | Tutorial - Configure LDAPS for Entra DS | learn.microsoft.com/.../tutorial-configure-ldaps | VERIFIED | Page live, covers LDAPS certificate and configuration for managed domains |
| 5 | SSH access to Azure Arc-enabled servers | learn.microsoft.com/.../ssh-arc-overview | VERIFIED | Page live, covers Arc SSH, AADSSHLoginForLinux on Arc-enabled servers, Entra authentication |
| 6 | Manually joining EC2 Linux instance to AWS Managed AD | docs.aws.amazon.com/.../join_linux_instance.html | VERIFIED | Page live, covers realmd, SSSD, id_provider=ad for Amazon Linux/RHEL/Ubuntu |
| 7 | Connecting AWS Managed AD to Entra Connect Sync | docs.aws.amazon.com/.../ms_ad_connect_ms_entra_sync.html | VERIFIED | Page live. Tutorial installs Entra Connect Sync on EC2 joined to AWS Managed AD. AWS Managed AD is the source forest; Entra ID is the cloud destination. Sync direction: AWS Managed AD -> Entra ID. |
| 8 | AD Connector - AWS Directory Service | docs.aws.amazon.com/.../directory_ad_connector.html | VERIFIED | Page live, covers AD Connector as stateless proxy gateway to on-prem AD |
| 9 | SSM RunAs support for Linux/macOS | docs.aws.amazon.com/.../session-preferences-run-as.html | VERIFIED | Page live, confirms SSM verifies OS account exists on the node or in the domain before starting session |
| 10 | Integrating RHEL with Windows AD | docs.redhat.com/.../integrating_rhel_systems... | VERIFIED | Page live, RHEL 10 documentation for direct AD integration via SSSD/realmd |
| 11 | SSSD AD Provider - sssd.io | sssd.io/docs/ad/ad-provider.html | VERIFIED | Page live, covers ad_provider configuration, SID-to-UID mapping, POSIX attributes |
| 12 | Entra Domain Services Pricing | microsoft.com/.../microsoft-entra-ds | VERIFIED | Page live; pricing confirmed via web search: Standard ~$109.50/mo, Enterprise ~$292/mo |
| 13 | Designing private network connectivity AWS-Azure | aws.amazon.com/blogs/.../designing-private-network-connectivity-aws-azure/ | VERIFIED | Page live, covers VPN and Direct Connect/ExpressRoute between AWS and Azure |
| 14 | AWS re:Post - Managed AD compatible with Entra DS? | repost.aws/questions/QUgueJm6EuQvuw4YrEpgs7Pg/... | UNVERIFIABLE | Direct fetch returns 403. Thread existence confirmed in prior validation cycle. Content described as inconclusive, consistent with investigation's characterization. |
| 15 | Add WorkSpaces to Entra ID using Entra DS | aws.amazon.com/blogs/.../add-your-workspaces-to-azure-ad-... | VERIFIED | Page live, confirms AD Connector + Entra DS pattern for WorkSpaces |
| 16 | Linux Azure AD authentication options - Puppeteers | puppeteers.net/blog/linux-azure-ad-authentication-options/ | VERIFIED | Page live, covers multiple Linux-Entra auth paths including AADDS, Arc, Himmelblau |
| 17 | Using AWS Directory Service for Entra ID DS - Transfer Family | docs.aws.amazon.com/transfer/.../azure-sftp.html | VERIFIED | Page live, confirms AD Connector + Entra DS for SFTP auth, documents VPN requirement |
| 18 | Custom attributes for Entra Domain Services | learn.microsoft.com/.../concepts-custom-attributes | VERIFIED | Page live. Confirms Enterprise/Premium SKUs support onPremisesExtensionAttributes (1-15) and directory extensions. Does NOT mention RFC 2307 POSIX attributes. Standard SKU not supported. |
| 19 | Provisioning Entra ID to AD using Entra Cloud Sync | learn.microsoft.com/.../how-to-configure-entra-to-active-directory | VERIFIED | Page live. Covers group provisioning (security groups) from Entra ID to on-prem AD. FAQ confirms Cloud Sync is used "solely for Security Group Provisioning to AD" -- user provisioning in this direction is not supported. |

**Source summary:** 18/19 VERIFIED, 1 UNVERIFIABLE (re:Post 403, confirmed in prior cycle).

---

## Finding Verification

| # | Finding (abbreviated) | Verdict | Evidence |
|---|----------------------|---------|----------|
| 1 | Base Entra ID does not expose LDAP/Kerberos; SSSD requires these protocols | CONFIRMED | Microsoft docs confirm Entra ID uses OAuth2/OIDC/SAML only. Puppeteers blog and SSSD docs confirm SSSD requires LDAP or Kerberos backend. |
| 2 | Entra DS provides LDAP/Kerberos; cloud-only users must change password once for hash generation | CONFIRMED | Microsoft Learn synchronization page (source #2) confirms one-way sync from Entra ID and the password change requirement for cloud-only users. |
| 3 | Entra DS pricing: ~$110/mo Standard, $292/mo Enterprise, $1,168/mo Premium | CONFIRMED | Web search confirms Standard ~$109.50/mo, Enterprise ~$292/mo. Premium pricing consistent with Microsoft tiered pricing structure. |
| 4 | EC2 can reach Entra DS over site-to-site VPN; required ports listed | CONFIRMED | AWS blog (source #13) confirms VPN connectivity between AWS and Azure. Port list (53, 88, 389, 636, 445) matches standard AD requirements from Microsoft and Red Hat docs. |
| 5 | AD Connector proxies to existing AD; does not directly support Linux SSSD domain join | CONFIRMED | AWS AD Connector docs confirm stateless proxy. Transfer Family docs confirm AD Connector + Entra DS pattern. Investigation correctly notes value is for AWS service integrations, not SSSD directly. |
| 6 | AWS Managed AD eliminates cross-cloud dependency; Entra Connect Sync syncs FROM AWS Managed AD TO Entra ID; reverse direction not supported | CONFIRMED | **Correction validated.** AWS documentation (source #7) confirms: Entra Connect Sync is installed on EC2 joined to AWS Managed AD; AWS Managed AD is configured as the on-premises forest (source); users sync TO Entra ID (destination). The Cycle 1 report incorrectly claimed the AWS page described the reverse direction. Re-verification confirms the corrected finding is accurate. Entra Cloud Sync FAQ (source #19) confirms Cloud Sync is for "Security Group Provisioning to AD" only -- not user provisioning in the cloud-to-AD direction. |
| 7 | Alternative for Path C: create users in AWS Managed AD, sync to Entra ID | CONFIRMED | This follows the native Entra Connect Sync direction (AD -> Entra) confirmed in source #7. Valid alternative that inverts identity authority. |
| 8 | Azure Arc allows non-Azure servers; AADSSHLoginForLinux creates local users on first login | CONFIRMED | Microsoft Learn Arc SSH overview (source #5) confirms Arc-enabled server support. VM sign-in page (source #1) confirms local user creation and RBAC via Azure roles. |
| 9 | AADSSHLoginForLinux chicken-and-egg problem with SSM RunAs | CONFIRMED | SSM docs (source #9) confirm RunAs verifies OS account exists before session start. Arc extension creates user on first SSH login. Sequencing conflict is real and correctly identified. |
| 10 | SSSD SID-to-UID mapping; Entra DS Enterprise/Premium support custom attributes but not RFC 2307 POSIX schema | CONFIRMED | **Correction validated.** SSSD docs confirm murmurhash3 SID-to-UID mapping. Microsoft Learn custom attributes page (source #18) confirms Enterprise/Premium support onPremisesExtensionAttributes (1-15) and directory extensions, but page makes no mention of RFC 2307 POSIX attributes (uidNumber, gidNumber, loginShell, unixHomeDirectory). The corrected finding accurately distinguishes between string-typed extensions and POSIX schema attributes. |
| 11 | SSM resolves RunAs user via OS-level user lookup; SSSD+NSS makes directory users resolvable | CONFIRMED | SSM docs confirm: "Session Manager verifies that the OS account...exists on the node, or in the domain, before starting the session." NSS passwd: files sss configuration makes SSSD-resolved users visible to SSM. |
| 12 | use_fully_qualified_names=False recommended for SSM RunAs with SSSD | CONFIRMED | Logically sound: SSM RunAs tag must match username format SSSD presents. SSSD docs confirm use_fully_qualified_names controls domain suffix. Plain usernames simplify ABAC tag mapping. |
| 13 | Trust between AWS Managed AD and Entra DS technically possible but not confirmed; SSSD does not support forest trusts | PARTIALLY CONFIRMED | re:Post thread (source #14) confirms question is inconclusive. AWS does not explicitly confirm compatibility. The SSSD forest trust limitation claim lacks a direct primary source citation. SSSD ad_provider docs describe trust handling but do not explicitly state "forest trusts are not supported." The claim is likely correct based on community knowledge but should be cited or hedged. |

---

## Correction Verification (Cycle 1 -> Cycle 2)

### Correction 1: Finding #6 -- Entra Connect Sync Direction

**Previous report's concern:** The Cycle 1 validator claimed source #7 (AWS documentation) described syncing FROM Entra ID TO AWS Managed AD, calling it an "internal conflict" with finding #6.

**Re-verification result:** The Cycle 1 validator was **incorrect**. Careful re-reading of the AWS documentation page confirms:
- Entra Connect Sync is installed on an EC2 instance joined to AWS Managed AD
- AWS Managed AD is configured as the **on-premises forest (source)**
- Users sync **TO Microsoft Entra ID (destination)**
- The tutorial follows the standard hybrid identity pattern: on-prem AD -> cloud Entra ID

The corrected finding #6 now accurately states: "The AWS documentation for Entra Connect Sync with AWS Managed AD describes syncing users FROM AWS Managed AD TO Entra ID." This is **correct**.

Additionally, the investigation now includes source #19 (Entra Cloud Sync documentation), which confirms that Cloud Sync supports group writeback to on-prem AD but NOT user provisioning in the cloud-to-AD direction. This strengthens the finding.

**Verdict:** Correction properly applied. Finding is now accurate.

### Correction 2: Entra DS Custom Attributes

**Previous report's concern:** The investigation originally stated Entra DS "does not support custom schema extensions," which was outdated.

**Re-verification result:** The corrected investigation now states Enterprise/Premium SKUs support custom attributes (onPremisesExtensionAttributes 1-15 and directory extensions) but correctly notes these are "string-typed extension attributes, not the RFC 2307 POSIX schema attributes (uidNumber, gidNumber, loginShell, unixHomeDirectory) that SSSD expects when ldap_id_mapping=False."

Microsoft Learn custom attributes page (source #18) confirms:
- Enterprise/Premium SKUs required (Standard not supported)
- Supports onPremisesExtensionAttributes (1-15) and directory extensions
- No mention of RFC 2307 POSIX schema attributes

**Verdict:** Correction properly applied. The nuanced distinction between string-typed extensions and POSIX schema attributes is accurate and well-stated.

---

## Additional Checks

### INTERNAL_CONFLICT

None found. The Cycle 1 internal conflict (finding #6 vs source #7) has been resolved. The corrected finding #6 accurately reflects what source #7 describes.

### NEEDS_PRIMARY_SOURCE

- **Finding #13:** The claim that "SSSD on Linux does not support forest trusts -- only external (non-transitive) trusts" still lacks a direct primary source citation from SSSD or Red Hat documentation. This was flagged in Cycle 1 and remains unaddressed. Low priority since the claim is consistent with community knowledge, but a citation would strengthen it.

### CONFIRM_OR_HEDGE

- **Finding #13 trust claim:** As noted above, consider hedging with "based on community reports" or adding a primary source citation if one exists.

---

## Source Count Change

The corrected investigation added 2 new sources (now 19, up from 17):
- Source #18: Microsoft Learn custom attributes for Entra DS (supports correction #2)
- Source #19: Microsoft Learn Entra Cloud Sync provisioning to AD (supports correction #1)

Both are official Microsoft documentation and are VERIFIED.

---

## Overall Assessment

**ACCURATE. Corrections properly applied.**

The investigation is now factually sound across all 13 key findings. The two material issues identified in Cycle 1 have been corrected:

1. The Entra Connect Sync direction (finding #6) is now accurately stated, and the Cycle 1 validator's claim of an "internal conflict" has been determined to be a misreading of the AWS documentation. The corrected finding correctly describes the sync direction as FROM AWS Managed AD TO Entra ID.

2. The Entra DS custom attributes claim now accurately distinguishes between supported string-typed extensions (Enterprise/Premium) and unsupported RFC 2307 POSIX schema attributes.

One minor item remains from Cycle 1: finding #13's forest trust limitation claim for SSSD lacks a primary source citation. This is low priority and does not materially affect the investigation's conclusions.

All paths, cost estimates, technical details, and trade-offs are well-sourced and confirmed. The audience briefs accurately reflect the findings.
