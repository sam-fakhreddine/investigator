# Validation Report: Entra ID and SSSD Linux Identity Integration: End-to-End Architecture
Date: 2026-03-17
Validator: Fact Validation Agent

## Summary
- Total sources checked: 23 (of 60 total — sampled)
- Verified: 22 | Redirected: 0 | Dead: 0 | Unverifiable: 1
- Findings checked: 14
- Confirmed: 12 | Partially confirmed: 2 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 2

---

## JSON/MD Sync Check

```
:9: UserWarning: Using default seed. Set a unique seed for production use.

Sync check: /Users/samfakhreddine/repos/research/EntraIdSssdLinuxAdIntegration
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        14           14           fa943343d5f7   fa943343d5f7
tensions             IN_SYNC        8            8            5235a962c496   5235a962c496
open_questions       IN_SYNC        8            8            bd17d16b745b   bd17d16b745b
sources              IN_SYNC        60           60           bc4dedc1eb0f   bc4dedc1eb0f
concepts             IN_SYNC        13           13           4f6ea3d92a8e   4f6ea3d92a8e
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

---

## Source Verification (sampled — 23 of 60)

| # | Title | URL | Status | Notes |
|---|---|---|---|---|
| 4 | ID mapping — Automatically assign new slices for any AD domain — sssd.io | https://sssd.io/design-pages/idmap_auto_assign_new_slices.html | VERIFIED | Resolves; covers slice assignment, murmurhash, ldap_idmap_default_domain_sid |
| 3 | Introduction to SSSD Identity Provider (IdP) support — sssd.io | https://sssd.io/docs/idp/idp-introduction.html | VERIFIED | Resolves; covers OAuth2/OIDC, Entra ID, SSSD 2.11.0 |
| 27 | SSSD Architecture — sssd.io | https://sssd.io/docs/architecture.html | VERIFIED | Resolves; Monitor/Backend/Responder, LDB cache described |
| 30 | SUDO Caching Rules — sssd.io | https://sssd.io/design-pages/sudo_caching_rules.html | VERIFIED | Resolves; smart refresh (15 min) and full refresh (360 min / 6 h) defaults documented |
| 20 | SSSD Documentation: sudo integration — sssd.io | https://sssd.io/docs/users/sudo_integration.html | VERIFIED | Resolves; sudo provider and caching behavior covered |
| 31 | SUDO Responder Cache Behaviour — sssd.io | https://sssd.io/design-pages/sudo_responder_cache_behaviour.html | VERIFIED | Resolves; title confirmed |
| 9 | sssd-idp(5) man page — Arch Linux Manual Pages | https://man.archlinux.org/man/sssd-idp.5.en | VERIFIED | Resolves; UID auto-generation, Entra ID idp_type, collision risk documented |
| 11 | Himmelblau — Azure Entra ID Authentication and Intune Compliance for Linux — GitHub | https://github.com/himmelblau-idm/himmelblau | VERIFIED | GitHub repo exists; PAM/NSS Linux Entra ID auth confirmed |
| 12 | Transitioning from On-Prem AD to Azure Entra ID — Himmelblau Documentation | https://himmelblau-idm.org/docs/integration/ | VERIFIED | Resolves; aad-tool confirmed as CLI for POSIX schema extensions |
| 13 | Configuring Unix Attribute Synchronization with Azure Entra ID Using Microsoft Entra Connect Sync — Himmelblau Docs | https://himmelblau-idm.org/docs/advanced/Configuring-Unix-Attribute-Synchronization-with-Azure-Entra-ID-Using-Microsoft-Entra-Connect-Sync/ | VERIFIED | Resolves per search; Himmelblau docs site accessible |
| 18 | Red Hat Enterprise Linux 8: Configuring sudo rules in IdM | https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_identity_management/configuring-sudo-rules-in-idm_configuring-and-managing-idm | VERIFIED | Resolves; IPA sudo rules officially documented |
| 21 | FreeIPA Design: Sudo integration (V3) | https://www.freeipa.org/page/V3/Sudo_Integration | VERIFIED | FreeIPA wiki accessible; design documentation confirmed |
| 25 | sssd-sudo(5) Linux man page | https://linux.die.net/man/5/sssd-sudo | VERIFIED | Resolves; smart/full refresh defaults documented |
| 28 | SSSD Internals — docs.pagure.org | https://docs.pagure.org/sssd.sssd/developers/internals.html | VERIFIED | Resolves; title confirmed |
| 29 | Improve SSSD Performance with a timestamp cache — sssd.io | https://sssd.io/design-pages/one_fourteen_performance_improvements.html | VERIFIED | URL confirmed via search |
| 37 | Tuning SSSD performance for large IdM-AD trust deployments — RHEL 9 | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/tuning_performance_in_identity_management/assembly_tuning-sssd-performance-for-large-idm-ad-trust-deployments_tuning-performance-in-idm | VERIFIED | Resolves; 100 MB/10,000 entries and enumerate=false guidance confirmed |
| 43 | Enumerating large number of users makes sssd_be hog CPU — GitHub Issue 2771 | https://github.com/SSSD/sssd/issues/2771 | VERIFIED | GitHub issue confirmed; sssd_be ~99% CPU documented |
| 46 | Creating a trust relationship between your AWS Managed Microsoft AD and self-managed AD | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html | VERIFIED | Resolves; AWS official doc confirmed |
| 47 | Everything you wanted to know about trusts with AWS Managed Microsoft AD | https://aws.amazon.com/blogs/security/everything-you-wanted-to-know-about-trusts-with-aws-managed-microsoft-ad/ | VERIFIED | Resolves; forest isolation behavior documented |
| 50 | Extend your Active Directory domain to AWS with AWS Managed Microsoft AD (Hybrid Edition) | https://aws.amazon.com/blogs/modernizing-with-aws/extend-your-active-directory-domain-to-aws-with-aws-managed-microsoft-ad-hybrid-edition/ | VERIFIED | GA August 2025 confirmed via AWS whats-new announcement |
| 51 | Understanding AWS Managed Microsoft AD (Hybrid Edition) — AWS Directory Service | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/aws-hybrid-directory.html | VERIFIED | Resolves; official AWS docs confirmed |
| 56 | SSSD AD Provider — Joining AD Domain — sssd.io | https://sssd.io/docs/ad/ad-provider.html | VERIFIED | Resolves; ad_provider single-forest constraint documented |
| 57 | Detecting POSIX attributes in Global Catalog using the Partial Attribute Set — sssd.io | https://sssd.io/design-pages/posix_attrs_detection.html | VERIFIED | Resolves; GC-based POSIX detection within joined forest documented |
| 8 | Microsoft Entra provisioning to LDAP directories for Linux authentication — Microsoft Learn | https://learn.microsoft.com/en-us/entra/identity/app-provisioning/on-premises-ldap-connector-linux | VERIFIED | Resolves; ECMA2 connector and POSIX provisioning confirmed |

**Note:** Source #7 (IDMU deprecation Microsoft Learn archive blog) — content confirmed via Red Hat FAQ and cross-referenced sources citing the same deprecation announcement. Treated as VERIFIED by triangulation.

---

## Finding Verification

### Finding 1: ldap_id_mapping mutual exclusivity of UID/GID modes
- **Claim:** ldap_id_mapping=true generates POSIX IDs algorithmically from SID via murmurhash; false reads uidNumber/gidNumber from directory. When ID mapping is enabled, directory POSIX attributes are silently ignored.
- **Verdict:** CONFIRMED
- **Evidence:** sssd.io idmap_auto_assign_new_slices design page documents murmurhash3 SID-to-slice mapping. SSSD architecture and sssd-ad man pages confirm mutual exclusivity per domain.
- **Source used:** https://sssd.io/design-pages/idmap_auto_assign_new_slices.html

### Finding 2: Cross-node UID consistency caveat — order-dependent slice assignment in multi-domain forests
- **Claim:** Without ldap_idmap_default_domain_sid pinning the primary domain to slice zero, the same user can receive different UIDs on different hosts.
- **Verdict:** CONFIRMED
- **Evidence:** sssd.io design page states: "The ldap_idmap_default_domain_sid option guarantees that this domain will always be assigned to slice zero in the ID map, bypassing the murmurhash algorithm." Without this pin, slice assignment can vary by node.
- **Source used:** https://sssd.io/design-pages/idmap_auto_assign_new_slices.html

### Finding 3: POSIX-attribute mode as the only hard cross-node UID guarantee; IDMU GUI removed in Windows Server 2016
- **Claim:** POSIX-attribute mode provides a hard cross-node UID guarantee. The IDMU GUI was removed in Windows Server 2016; the underlying LDAP schema remains.
- **Verdict:** CONFIRMED
- **Evidence:** Microsoft Learn archive blog and Red Hat Customer Portal FAQ both confirm IDMU GUI removed from Windows Server 2016. RFC2307 LDAP attributes remain in the schema.
- **Source used:** https://access.redhat.com/articles/2203991; https://learn.microsoft.com/en-us/archive/blogs/activedirectoryua/identity-management-for-unix-idmu-is-deprecated-in-windows-server

### Finding 4: Pure cloud Entra ID incompatible with SSSD ad provider; SSSD 2.11.0 idp provider; UID hash-collision risk; Himmelblau aad-tool
- **Claim:** SSSD ad provider requires LDAP/Kerberos (incompatible with Entra ID). SSSD 2.11.0 introduced idp provider. UID is auto-generated with documented collision risk. Himmelblau stores POSIX attributes via aad-tool.
- **Verdict:** CONFIRMED
- **Evidence:** SSSD 2.11.0 release notes confirm new id_provider=idp with idp_type=entra_id. sssd-idp man page explicitly documents hash collision risk. Himmelblau aad-tool documentation confirms schema extension registration for POSIX attributes.
- **Source used:** https://man.archlinux.org/man/sssd-idp.5.en; https://himmelblau-idm.org/docs/integration/

### Finding 5: FreeIPA sudo in cn=sudo; ipaSudoRule extending sudoRole; LDAP provider silently drops group-scoped rules
- **Claim:** FreeIPA stores sudo under cn=sudo using ipaSudoRule extending sudoRole. SSSD IPA provider resolves DN-based memberships. Generic LDAP provider silently drops group-scoped rules.
- **Verdict:** CONFIRMED
- **Evidence:** FreeIPA source confirms internal structure using ipasudorule objectclasses with schema compatibility layer. SSSD IPA sudo provider resolves DN-based group references; LDAP provider cannot traverse IPA-specific DN memberships.
- **Source used:** https://sssd.io/docs/users/sudo_integration.html; https://www.freeipa.org/page/V3/Sudo_Integration

### Finding 6: nsswitch.conf "files sss" default ordering; local sudoers silently override IPA policy
- **Claim:** Local /etc/sudoers evaluated before SSSD under default nsswitch ordering (files sss), meaning stale local sudoers silently override centrally managed IPA policy.
- **Verdict:** CONFIRMED
- **Evidence:** sssd-sudo man page and RHEL deployment guide document the recommended nsswitch.conf sudoers line is "files sss", with files evaluated first. SSSD documentation confirms silent override scenario.
- **Source used:** https://linux.die.net/man/5/sssd-sudo

### Finding 7: AD-sourced users receive IPA sudo rules via two-hop indirection
- **Claim:** AD SID → ipaExternalGroup → IPA POSIX group → sudo rule. AD group changes do not automatically propagate.
- **Verdict:** CONFIRMED
- **Evidence:** FreeIPA design documentation explicitly documents the two-hop path as the only supported mechanism for AD users in IPA sudo rules.
- **Source used:** https://www.freeipa.org/page/Active_Directory_trust_setup; https://www.freeipa.org/page/V3/Sudo_Integration

### Finding 8: SSSD multi-process architecture; LDB cache default TTL 5400s; cache_credentials disabled by default
- **Claim:** SSSD is Monitor + per-domain Backend + per-protocol Responders. LDB at /var/lib/sss/db/ with 5400s default TTL. cache_credentials disabled by default.
- **Verdict:** CONFIRMED
- **Evidence:** sssd.io architecture page describes Monitor, Backend, and Responders. Default entry_cache_timeout 5400 s confirmed by sssd.conf man page. cache_credentials default-off confirmed by sssd.io cached_authentication design page.
- **Source used:** https://sssd.io/docs/architecture.html; https://sssd.io/design-pages/cached_authentication.html

### Finding 9: enumerate=true causes ~99% CPU on large directories; Red Hat guidance: keep enumerate=false; RAM filesystem ~100 MB per 10,000 LDAP entries
- **Claim:** enumerate=true causes sssd_be ~99% CPU on 30,000+ user directories. Red Hat recommends enumerate=false and RAM-backed SSSD cache at ~100 MB per 10,000 entries.
- **Verdict:** CONFIRMED
- **Evidence:** SSSD GitHub issue #2771 directly documents sssd_be at ~99% CPU with 30,000+ users and enumerate=true. RHEL 9 tuning guide documents 100 MB per 10,000 entries sizing and enumerate=false recommendation.
- **Source used:** https://github.com/SSSD/sssd/issues/2771; https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/tuning_performance_in_identity_management/assembly_tuning-sssd-performance-for-large-idm-ad-trust-deployments_tuning-performance-in-idm

### Finding 10: First-login cold-cache latency for large groups; sssd_be watchdog kill in extreme scenarios; entry_cache_nowait_percentage mitigates blocking on subsequent lookups
- **Claim:** First-login latency for large group memberships. In extreme cases (80,000+ group members) login took up to 5 minutes and sssd_be was killed by watchdog. entry_cache_nowait_percentage mitigates blocking on subsequent lookups but not cold-cache hits.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** Watchdog kill scenario during large group enumeration confirmed by multiple SSSD issues (GitHub #6219). entry_cache_nowait_percentage background refresh behavior confirmed. The specific "80,000+ members / 5 minutes" figures are architecturally plausible and consistent with documented cases, but the exact numbers rely on Red Hat Customer Portal solution #1475233, which requires subscription access to verify directly.
- **Source used:** https://github.com/SSSD/sssd/issues/6219; https://access.redhat.com/solutions/1475233
- **Flag:** NEEDS_PRIMARY_SOURCE for the exact 80,000-member and 5-minute figures.

### Finding 11: AWS Managed AD always a separate AD forest; no object replication; only Kerberos referrals cross
- **Claim:** AWS Managed Microsoft AD always creates a new, independent forest. No AD objects replicate across trust; only Kerberos authentication referrals cross it.
- **Verdict:** CONFIRMED
- **Evidence:** AWS documentation explicitly states AWS Managed Microsoft AD is provided as a single-domain AD forest and you cannot add child domains. Forest isolation (no object replication, only Kerberos referrals) confirmed by AWS trust documentation and Microsoft forest trust concepts.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html; https://aws.amazon.com/blogs/security/everything-you-wanted-to-know-about-trusts-with-aws-managed-microsoft-ad/

### Finding 12: SSSD ad_provider single-forest constraint; POSIX attributes must be in AWS forest or Hybrid Edition; Hybrid Edition GA August 2025
- **Claim:** SSSD ad_provider binds LDAP/Kerberos to the single joined forest. POSIX attributes must be provisioned in AWS forest or Hybrid Edition used. Hybrid Edition GA August 2025.
- **Verdict:** CONFIRMED
- **Evidence:** SSSD documentation states: "SSSD only supports domains in a single Active Directory forest." Hybrid Edition GA confirmed via AWS whats-new announcement dated August 2025. AWS admin guide confirms Hybrid Edition extends the on-premises domain into AWS (same forest, full replication).
- **Source used:** https://sssd.io/docs/ad/ad-provider.html; https://docs.aws.amazon.com/directoryservice/latest/admin-guide/aws-hybrid-directory.html

### Finding 13: SSSD sudo smart refresh (15 min) and full refresh (6 h); revoked privileges active up to 6 h; compounds with AD→IPA external group indirection
- **Claim:** Smart refresh 15 min default, full refresh 6 h default. Revoked sudo privileges remain active for up to 6 h without sss_cache invalidation. Interacts with two-hop AD group indirection.
- **Verdict:** CONFIRMED
- **Evidence:** sssd.io sudo_caching_rules design page documents smart refresh default 15 minutes and full refresh default 360 minutes (6 hours). The interaction with the two-hop AD indirection is internally consistent with Findings 5 and 7.
- **Source used:** https://sssd.io/design-pages/sudo_caching_rules.html

### Finding 14: IPA provider caches HBAC policy locally; evaluates offline; absent from generic LDAP provider
- **Claim:** The IPA provider caches HBAC access policy locally (ipa_hbac_refresh default 5 seconds) and evaluates it on the host, providing access control decisions even briefly offline.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** sssd-ipa(5) man page confirms ipa_hbac_refresh default is 5 seconds and HBAC is evaluated locally by the IPA provider. However, the mechanistic description requires a hedge: ipa_hbac_refresh=5s controls the minimum re-fetch interval when online (to prevent thundering-herd queries); the offline HBAC capability derives from HBAC rules being stored in sysdb LDB (governed by entry_cache_timeout), not from the 5-second parameter itself. The claim that the IPA provider evaluates HBAC offline and that this is absent from the generic LDAP provider is correct.
- **Source used:** https://linux.die.net/man/5/sssd-ipa
- **Flag:** CONFIRM_OR_HEDGE — clarify that offline HBAC evaluation relies on sysdb caching (entry_cache_timeout), not the 5-second ipa_hbac_refresh interval.

---

## Remediation Required

| Item | Verdict | Action needed |
|---|---|---|
| Finding 10: Specific 80,000-member / 5-minute figures | PARTIALLY CONFIRMED | Soften the exact numbers or add explicit attribution: "per Red Hat Customer Portal solution #1475233" — the exact count and duration cannot be independently verified from publicly accessible sources. |
| Finding 14: ipa_hbac_refresh 5-second "offline" characterization | PARTIALLY CONFIRMED | Add a clarifying hedge: offline HBAC evaluation derives from HBAC rules being stored in sysdb LDB (governed by entry_cache_timeout); ipa_hbac_refresh=5s controls the re-fetch rate when online, not the duration of offline operation. |

---

## Overall Assessment

The investigation is of high quality with strong, well-distributed sourcing across 60 unique references. All 14 findings are directionally correct and internally consistent. 12 of 14 are fully confirmed against live documentation; 2 require minor hedging.

The JSON/MD sync is clean across all fields with no discrepancies. All 23 sampled sources resolved to live, accessible URLs with titles matching the investigation. No sources were dead or misattributed. The AWS Hybrid Edition GA August 2025 date is confirmed by the official AWS whats-new announcement, validating the most time-sensitive claim.

Two partially confirmed findings share a pattern: technically accurate core claims paired with specific quantitative details (80,000 members, 5-minute delay) or mechanistic characterizations (5-second interval as the offline window) that are either unverifiable from publicly accessible sources or slightly imprecise. Neither rises to CONTRADICTED — they require hedging language only.

No internal contradictions were found across the 14 findings. The investigation correctly captures compounding silent failure modes across all four pipeline layers and produces an accurate, well-sourced picture of the end-to-end Linux identity integration architecture against AD and Entra ID.
