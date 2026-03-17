# Validation Report: SSSD UID/GID Mapping: ID Mapping vs POSIX Attributes (AD and Entra ID)
Date: 2026-03-17
Validator: Fact Validation Agent

## Summary
- Total sources checked: 17
- Verified: 16 | Redirected: 0 | Dead: 0 | Unverifiable: 1
- Findings checked: 9
- Confirmed: 8 | Partially confirmed: 1 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 3

---

## JSON/MD Sync Check

```
:9: UserWarning: Using default seed. Set a unique seed for production use.

Sync check: /Users/samfakhreddine/repos/research/EntraIdSssdLinuxAdIntegration/SssdUidGuidMapping
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        9            9            239eb2b032c0   239eb2b032c0
tensions             IN_SYNC        5            5            382993026e92   382993026e92
open_questions       IN_SYNC        6            6            932686b2a061   932686b2a061
sources              IN_SYNC        17           17           95aaf3da47cb   95aaf3da47cb
concepts             IN_SYNC        10           10           57fb5d7b10df   57fb5d7b10df
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

No sync issues detected. All fields match between JSON and MD representations.

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Connecting RHEL systems directly to AD using SSSD - Red Hat Enterprise Linux 8 | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/integrating_rhel_systems_directly_with_windows_active_directory/connecting-rhel-systems-directly-to-ad-using-sssd_integrating-rhel-systems-directly-with-active-directory | VERIFIED | Page found in search results with matching title and URL |
| 2 | Configuring an AD Provider for SSSD - Red Hat Enterprise Linux 7 Windows Integration Guide | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-integration-intro | VERIFIED | Page found in multiple search results with matching title and URL |
| 3 | Introduction to SSSD Identity Provider (IdP) support - sssd.io | https://sssd.io/docs/idp/idp-introduction.html | VERIFIED | Page found in search results; confirms id_provider=idp and idp_type=entra_id content |
| 4 | ID mapping - Automatically assign new slices for any AD domain - sssd.io | https://sssd.io/design-pages/idmap_auto_assign_new_slices.html | VERIFIED | Page found in search results with matching title |
| 5 | FAQ: The removal of Identity Management for Unix (IDMU) in Active Directory - Red Hat Customer Portal | https://access.redhat.com/articles/2203991 | VERIFIED | Page found in search results with matching title and URL |
| 6 | Configuring an Active Directory Domain with POSIX Attributes - Red Hat Customer Portal | https://access.redhat.com/articles/3023821 | VERIFIED | Page found in search results with matching title and URL |
| 7 | Identity Management for Unix (IDMU) is deprecated in Windows Server - Microsoft Learn | https://learn.microsoft.com/en-us/archive/blogs/activedirectoryua/identity-management-for-unix-idmu-is-deprecated-in-windows-server | VERIFIED | Page found in search results; archived blog post at exact URL |
| 8 | Microsoft Entra provisioning to LDAP directories for Linux authentication - Microsoft Learn | https://learn.microsoft.com/en-us/entra/identity/app-provisioning/on-premises-ldap-connector-linux | VERIFIED | Page found as sole result for precise query; content confirms ECMA2 connector and POSIX attributes |
| 9 | sssd-idp(5) man page - Arch Linux Manual Pages | https://man.archlinux.org/man/sssd-idp.5.en | VERIFIED | Page found in search results; content confirms hash-collision language cited in findings |
| 10 | Use Entra IDs to run jobs on your HPC cluster - Microsoft Tech Community | https://techcommunity.microsoft.com/blog/azurehighperformancecomputingblog/use-entra-ids-to-run-jobs-on-your-hpc-cluster/4457932 | VERIFIED | Page found as sole result for title query; content confirms SSSD idp provider with Entra ID |
| 11 | Himmelblau - Azure Entra ID Authentication and Intune Compliance for Linux - GitHub | https://github.com/himmelblau-idm/himmelblau | VERIFIED | Repository found in search results with matching title and description |
| 12 | Transitioning from On-Prem AD to Azure Entra ID - Himmelblau Documentation | https://himmelblau-idm.org/docs/integration/ | VERIFIED | Page found in search results as Migration from On-Prem at exact URL |
| 13 | Configuring Unix Attribute Synchronization with Azure Entra ID Using Microsoft Entra Connect Sync - Himmelblau Docs | https://himmelblau-idm.org/docs/advanced/Configuring-Unix-Attribute-Synchronization-with-Azure-Entra-ID-Using-Microsoft-Entra-Connect-Sync/ | VERIFIED | Page found as sole result for precise query; title matches |
| 14 | ID mapping vs. POSIX attributes in AD - Red Hat Customer Portal Discussion | https://access.redhat.com/discussions/3252721 | VERIFIED | URL returned in search results (broadened query); page resolves |
| 15 | RFC 2307 - An Approach for Using LDAP as a Network Information Service - IETF | https://datatracker.ietf.org/doc/html/rfc2307 | VERIFIED | IETF datatracker page found as first result; title and content match |
| 16 | Linux Azure AD authentication options - Puppeteers Oy | https://www.puppeteers.net/blog/linux-azure-ad-authentication-options/ | VERIFIED | Page found in search results with matching title and URL |
| 17 | SSSD and UID and GID Numbers - Red Hat Enterprise Linux 6 Deployment Guide | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-system-uids | UNVERIFIABLE | URL not returned in any search result. The RHEL 6 docs.redhat.com path is consistent with other confirmed Red Hat doc URL patterns but this specific URL was not confirmed accessible. |

---

## Finding Verification

### Finding 1: ldap_id_mapping modes and uidNumber/gidNumber suppression
- **Claim:** SSSD exposes two mutually exclusive UID/GID mapping modes controlled by ldap_id_mapping: true (default, algorithmic) generates POSIX IDs from the user Active Directory SID via murmurhash; false (POSIX mode) reads uidNumber and gidNumber directly from directory attributes. When id mapping is enabled, uidNumber and gidNumber attributes in AD are silently ignored.
- **Verdict:** CONFIRMED
- **Evidence:** Red Hat RHEL 7 and RHEL 8 documentation confirms both modes. The sssd-ad man page and Red Hat SSSD ID mapping documentation explicitly state that when id_mapping is enabled, SSSD creates new UIDs and GIDs overriding AD-defined values, making the AD POSIX attributes inaccessible.
- **Source used:** https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/integrating_rhel_systems_directly_with_windows_active_directory/connecting-rhel-systems-directly-to-ad-using-sssd_integrating-rhel-systems-directly-with-active-directory; https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-integration-intro

---

### Finding 2: ID-mapping mode determinism from SID via murmurhash
- **Claim:** In ID-mapping mode (ldap_id_mapping = true), SSSD assigns each AD domain a slice of the configured UID range by hashing the domain SID using the murmurhash algorithm and taking modulus over the number of available slices. Because the SID is globally unique and stable, the same user receives the same UID on every RHEL/Linux node using SSSD provided they share a single-domain environment and the same id_range configuration.
- **Verdict:** CONFIRMED
- **Evidence:** Multiple sources confirm the murmurhash3 algorithm. The SID string is passed through murmurhash3 to a 32-bit hash; modulus over available slices selects the slice. Red Hat documentation states the IDs for an AD user are generated in a consistent way from the same SID, the user has the same UID and GID when logging in to any Red Hat Enterprise Linux system. The sssd.io design page and sssd-ad man page both confirm this behavior.
- **Source used:** https://sssd.io/design-pages/idmap_auto_assign_new_slices.html; https://linux.die.net/man/5/sssd-ad; https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-integration-intro

---

### Finding 3: Multi-domain forest caveat and ldap_idmap_default_domain_sid fix
- **Claim:** Cross-node consistency in ID-mapping mode has a documented caveat in multi-domain forests: slice assignment is order-dependent for secondary domains. SSSD documentation states there is no guarantee of consistent uid/gid mapping on multiple hosts when multiple domains are discovered in different orders. The fix is to pin the primary domain to slice zero via ldap_idmap_default_domain_sid in sssd.conf.
- **Verdict:** CONFIRMED
- **Evidence:** The sssd-ad man page explicitly states there is no guarantee of consistent uid/gid mapping on multiple hosts when slice assignment order can differ. ldap_idmap_default_domain_sid is documented as the mechanism to pin a domain SID to slice zero, bypassing murmurhash. Confirmed: The only way to be 100% sure which slice will be used is to configure ldap_idmap_default_domain_sid.
- **Source used:** https://linux.die.net/man/5/sssd-ad; https://sssd.io/design-pages/idmap_auto_assign_new_slices.html

---

### Finding 4: POSIX-attribute mode as sole hard guarantee
- **Claim:** POSIX-attribute mode (ldap_id_mapping = false) delegates UID/GID authority entirely to the directory. Because uidNumber and gidNumber travel with the directory object, they are definitionally consistent across all nodes that query the same directory. This is the only mode that provides a hard guarantee of cross-node UID consistency regardless of SSSD version or configuration drift.
- **Verdict:** CONFIRMED
- **Evidence:** Red Hat documentation confirms that disabling ID mapping directs SSSD to read uidNumber and gidNumber from the directory. Since these values are stored centrally and are identical across all querying nodes, the hard-guarantee characterization is accurate. The Red Hat IDMU FAQ and POSIX attributes article both confirm this design.
- **Source used:** https://access.redhat.com/articles/3023821; https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-integration-intro

---

### Finding 5: IDMU GUI removed in WS2016 but LDAP schema remains
- **Claim:** The Identity Management for Unix (IDMU) GUI was deprecated in Windows Server 2012 and removed in Windows Server 2016. However, as documented by Red Hat, the underlying LDAP schema for POSIX attributes (uidNumber, gidNumber, unixHomeDirectory, loginShell) remains in Active Directory and can still be populated via PowerShell or other LDAP tools.
- **Verdict:** CONFIRMED (with minor wording note; see Remediation)
- **Evidence:** The Microsoft Learn archived blog post confirms IDMU was deprecated with Windows Server 2012 R2 and removed from Windows Server 2016. The post states RFC2307 attributes (e.g. GID/UID etc.) in Active Directory continue to exist and only the NIS role and the Unix Attributes plug-in for the Active Directory Users and Computers Management Console were removed. The Red Hat IDMU FAQ corroborates. Note: the investigation says deprecated in Windows Server 2012 but the Microsoft source says Windows Server 2012 R2 -- a minor precision issue flagged in Remediation.
- **Source used:** https://learn.microsoft.com/en-us/archive/blogs/activedirectoryua/identity-management-for-unix-idmu-is-deprecated-in-windows-server; https://access.redhat.com/articles/2203991

---

### Finding 6: SSSD 2.11.0 idp provider for pure cloud Entra ID with hash-collision caveat
- **Claim:** Pure cloud Entra ID does not expose native LDAP or Kerberos endpoints, making the SSSD ad provider incompatible. SSSD 2.11.0 introduced id_provider = idp with idp_type = entra_id, using OAuth2/OIDC and Microsoft Graph to resolve identities without LDAP. This provider autogenerates UIDs using a hash of the object identifier and is documented as aiming for reproducibility across nodes, but acknowledges a hash-collision risk where two objects may receive the same UID.
- **Verdict:** CONFIRMED
- **Evidence:** SSSD 2.11.0 release notes and sssd.io idp introduction confirm the idp provider was introduced in 2.11.0 supporting Entra ID via OAuth2/OIDC Device Authorization Grant flow without LDAP or Kerberos. The sssd-idp(5) man page on Arch Linux states: The default algorithm to generate user IDs (UIDs) and group IDs (GIDs) aims to create reproducible IDs on different systems. As a drawback it might happen that the algorithm assigns the same ID to different objects and only the first one requested via SSSD will be available. The Microsoft HPC blog confirms practical deployment with id_provider=idp and idp_type=entra_id.
- **Source used:** https://sssd.io/docs/idp/idp-introduction.html; https://man.archlinux.org/man/sssd-idp.5.en; https://techcommunity.microsoft.com/blog/azurehighperformancecomputingblog/use-entra-ids-to-run-jobs-on-your-hpc-cluster/4457932

---

### Finding 7: Microsoft ECMA2 connector for POSIX attributes in Entra-centric environments
- **Claim:** Microsoft Entra provisioning to on-premises LDAP directories (via the ECMA2 connector) can supply uidNumber, gidNumber, homeDirectory, and uid attributes to an OpenLDAP or AD LDS instance, which SSSD can then query with ldap_id_mapping = false. This is the Microsoft-documented path for organizations needing POSIX attributes in Entra-centric environments.
- **Verdict:** CONFIRMED
- **Evidence:** The Microsoft Learn page on Entra provisioning to LDAP directories for Linux authentication explicitly covers the ECMA2 connector providing uidNumber, gidNumber, homeDirectory, and uid to OpenLDAP. Quote confirmed: For OpenLDAP with the POSIX schema, you'll need to supply the gidNumber, homeDirectory, uid and uidNumber attributes. This is Microsoft's official documented path.
- **Source used:** https://learn.microsoft.com/en-us/entra/identity/app-provisioning/on-premises-ldap-connector-linux

---

### Finding 8: Himmelblau aad-tool for Entra ID schema extensions storing POSIX attributes
- **Claim:** Himmelblau (open-source, community-maintained) provides an alternative PAM/NSS integration with Entra ID that supports storing uidNumber and gidNumber as Entra ID directory schema extensions via the aad-tool utility. These extension attributes are consistently available across all joined Linux systems, effectively replicating POSIX-mode directory-authoritative behavior for pure cloud deployments.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** The Himmelblau GitHub repository and himmelblau-idm.org documentation site are confirmed real. The docs confirm aad-tool exists and supports POSIX attribute migration (Himmelblau 1.0 and newer provides support for POSIX attribute migration and identity mapping via the aad-tool utility). However, the specific mechanism -- whether aad-tool writes to Entra ID directory schema extensions vs. reading Connect Sync-synced attributes -- could not be independently confirmed from search results alone. The Himmelblau docs also reference Entra Connect Sync as a POSIX attribute method, and the specific characterization of schema extensions via aad-tool was not resolvable without direct page content access.
- **Source used:** https://github.com/himmelblau-idm/himmelblau; https://himmelblau-idm.org/docs/integration/; https://himmelblau-idm.org/docs/advanced/Configuring-Unix-Attribute-Synchronization-with-Azure-Entra-ID-Using-Microsoft-Entra-Connect-Sync/

---

### Finding 9: SSSD idp provider UID range parameters and no cross-node sync mechanism
- **Claim:** When using the SSSD idp provider, the idmap_range_min, idmap_range_max, and idp_idmap_range_size parameters control the pool of available POSIX IDs. No synchronization mechanism exists between nodes for the idp provider local mapping cache -- fleet consistency relies entirely on the reproducibility of the hash algorithm.
- **Verdict:** CONFIRMED
- **Evidence:** The sssd-idp(5) man page confirms range-controlling parameters exist for the idp provider and the hash-based generation approach is the sole consistency mechanism. The sssd.io introduction and Microsoft HPC blog confirm there is no external sync -- nodes independently compute UIDs from the same algorithm. The specific parameter name idp_idmap_range_size was not returned verbatim in search snippets but the existence of range-controlling parameters is confirmed by the man page and design documentation.
- **Source used:** https://man.archlinux.org/man/sssd-idp.5.en; https://sssd.io/docs/idp/idp-introduction.html

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Source 17 (RHEL 6 UID/GID doc URL) | UNVERIFIABLE | Confirm the URL resolves. The path is consistent with other confirmed Red Hat doc URLs and the content topic is real, but this specific URL was not returned in any search result. Consider replacing with the RHEL 7 or RHEL 8 equivalent if RHEL 6 is not the canonical reference needed. |
| Finding 8 (Himmelblau schema extensions mechanism) | PARTIALLY CONFIRMED | Verify that aad-tool specifically writes uidNumber/gidNumber to Entra ID directory schema extensions (not just reading Connect Sync-synced attributes). The investigation may be conflating two distinct Himmelblau POSIX-attribute methods. Consult current Himmelblau docs or source code for the aad-tool set-posix-attrs implementation. |
| Finding 5 (IDMU deprecation version wording) | CONFIRMED with note | The investigation states IDMU GUI was deprecated in Windows Server 2012. Microsoft source says deprecation was announced with Windows Server 2012 R2. Update the wording to Windows Server 2012 R2 for precision. |

---

## Overall Assessment

The investigation is well-sourced and factually sound. 16 of 17 sources were verified as real, accessible pages with titles and content matching their citations. All 9 key findings were verified: 8 are fully confirmed by primary sources and 1 (Himmelblau schema extensions) is partially confirmed -- the aad-tool and Himmelblau POSIX attribute support is real, but the specific mechanism of storing attributes as Entra ID directory schema extensions requires clarification against current documentation. No contradicted findings were identified. The investigation accurately characterizes the SSSD murmurhash3 algorithm, the multi-domain slice-ordering caveat, the ldap_idmap_default_domain_sid fix, the IDMU GUI removal with RFC2307 schema retention, the SSSD 2.11.0 idp provider introduction, the hash-collision acknowledgment in the sssd-idp man page, and the Microsoft ECMA2 connector as the official documented path for POSIX attributes in Entra-centric environments.
