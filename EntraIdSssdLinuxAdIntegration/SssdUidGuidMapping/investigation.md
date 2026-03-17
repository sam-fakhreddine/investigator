# Investigation: SSSD UID/GID Mapping: ID Mapping vs POSIX Attributes (AD and Entra ID)

**Date:** 2026-03-17
**Status:** Complete

---

## Question

> How does SSSD handle UID/GID mapping when authenticating Linux hosts against Entra ID or Active Directory — via locally generated IDs vs. POSIX attributes stored in the directory — and what mechanisms exist for centralizing that mapping across a fleet?

---

## Context

Linux fleets authenticating against Microsoft identity services (on-premises Active Directory or cloud-native Entra ID) require a stable, cross-node-consistent mapping between directory objects and POSIX UIDs/GIDs. SSSD supports two fundamentally different approaches, each with distinct operational and fleet-management consequences. The landscape changed significantly with the deprecation of IDMU in Windows Server 2016 and the introduction of SSSD 2.11.0 native IdP provider for Entra ID in 2024.

---

## SSSD UID/GID Mapping Mode Comparison

| Dimension | ID Mapping (ldap_id_mapping = true) | POSIX Attributes (ldap_id_mapping = false) | IdP Provider (id_provider = idp, Entra ID) |
| --- | --- | --- | --- |
| Works with pure cloud Entra ID | No — requires LDAP/Kerberos | No — requires LDAP/Kerberos | Yes — OAuth2/OIDC, no LDAP required |
| Works with on-prem AD | Yes (default) | Yes, if POSIX attrs populated | No — ad provider only |
| Works with Entra Domain Services (AAD DS) | Yes | Yes, with PowerShell-populated attrs | No |
| UID source | Algorithmic: murmurhash(domain SID) + RID offset | Directory attribute: uidNumber on user object | Algorithmic: hash of object UUID or name; no SID |
| Cross-node consistency | High — same SID yields same UID on any node running same SSSD version; caveats apply for multi-domain | Guaranteed — UID lives in directory, identical everywhere | Documented as reproducible; acknowledged hash-collision risk |
| Directory preparation required | None | Yes — populate uidNumber and gidNumber on every object; IDMU GUI removed in WS2016, use PowerShell or Himmelblau aad-tool | None for auto-map; schema extensions needed to pin UIDs |
| Risk of UID collision | Low (murmur hash + large range) | None (admin-controlled) | Non-zero — documented in sssd-idp man page |
| Ignores uidNumber/gidNumber in AD | Yes — explicit override not possible when enabled | No — reads them | N/A |
| Fleet centralization mechanism | Shared sssd.conf via config management; pin primary domain with ldap_idmap_default_domain_sid | Authoritative UIDs live in directory; sssd.conf uniformity less critical | Shared sssd.conf; or Himmelblau aad-tool to pin UIDs via Entra schema extensions |
| POSIX attribute admin GUI | N/A | Removed in Windows Server 2016; LDAP schema still present; use PowerShell | N/A |

> Entra ID (pure cloud) cannot be used with id_provider = ad because SSSD requires LDAP and Kerberos, which Entra ID does not expose natively. Use id_provider = idp (SSSD 2.11+) or Himmelblau for pure cloud scenarios.

---

## Key Findings

- SSSD exposes two mutually exclusive UID/GID mapping modes controlled by ldap_id_mapping: true (default, algorithmic) generates POSIX IDs from the user Active Directory SID via murmurhash; false (POSIX mode) reads uidNumber and gidNumber directly from directory attributes. When id mapping is enabled, uidNumber and gidNumber attributes in AD are silently ignored.
- In ID-mapping mode (ldap_id_mapping = true), SSSD assigns each AD domain a slice of the configured UID range by hashing the domain SID using the murmurhash algorithm and taking modulus over the number of available slices. Because the SID is globally unique and stable, the same user receives the same UID on every RHEL/Linux node using SSSD — provided they share a single-domain environment and the same id_range configuration.
- Cross-node consistency in ID-mapping mode has a documented caveat in multi-domain forests: slice assignment is order-dependent for secondary domains. SSSD documentation states there is no guarantee of consistent uid/gid mapping on multiple hosts when multiple domains are discovered in different orders. The fix is to pin the primary domain to slice zero via ldap_idmap_default_domain_sid in sssd.conf.
- POSIX-attribute mode (ldap_id_mapping = false) delegates UID/GID authority entirely to the directory. Because uidNumber and gidNumber travel with the directory object, they are definitionally consistent across all nodes that query the same directory — this is the only mode that provides a hard guarantee of cross-node UID consistency regardless of SSSD version or configuration drift.
- The Identity Management for Unix (IDMU) GUI was deprecated in Windows Server 2012 R2 and removed in Windows Server 2016. However, as documented by Red Hat, the underlying LDAP schema for POSIX attributes (uidNumber, gidNumber, unixHomeDirectory, loginShell) remains in Active Directory and can still be populated via PowerShell or other LDAP tools.
- Pure cloud Entra ID does not expose native LDAP or Kerberos endpoints, making the SSSD ad provider incompatible. SSSD 2.11.0 introduced id_provider = idp with idp_type = entra_id, using OAuth2/OIDC and Microsoft Graph to resolve identities without LDAP. This provider autogenerates UIDs using a hash of the object identifier and is documented as aiming for reproducibility across nodes, but acknowledges a hash-collision risk where two objects may receive the same UID.
- Microsoft Entra provisioning to on-premises LDAP directories (via the ECMA2 connector) can supply uidNumber, gidNumber, homeDirectory, and uid attributes to an OpenLDAP or AD LDS instance, which SSSD can then query with ldap_id_mapping = false. This is the Microsoft-documented path for organizations needing POSIX attributes in Entra-centric environments.
- Himmelblau (open-source, community-maintained) provides an alternative PAM/NSS integration with Entra ID that, as documented on himmelblau-idm.org, supports POSIX attribute assignment via the aad-tool utility — with Entra Connect Sync and directory schema extension approaches both referenced. The specific write mechanism for pinning uidNumber/gidNumber in Entra ID is documented in Himmelblau's own guides; the net effect is fleet-wide UID consistency without a separate on-premises LDAP store.
- When using the SSSD idp provider, the idmap_range_min, idmap_range_max, and idp_idmap_range_size parameters control the pool of available POSIX IDs. No synchronization mechanism exists between nodes for the idp provider local mapping cache — fleet consistency relies entirely on the reproducibility of the hash algorithm.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| ldap_id_mapping | SSSD configuration parameter (boolean, default true for ad provider) that selects between algorithmic UID generation from SID and directory-resident POSIX attributes. Setting it to false makes SSSD read uidNumber/gidNumber from the directory; setting it to true ignores those attributes and computes IDs locally. |
| SID (Security Identifier) | A globally unique, immutable identifier assigned by Active Directory to every security principal. In ID-mapping mode, the SID is the stable seed from which SSSD derives a deterministic POSIX UID/GID. |
| murmurhash (SSSD ID mapping) | The non-cryptographic hash function used by SSSD sss_idmap library to map a domain SID to a slice index within the configured UID range. The same SID always produces the same hash, making the mapping reproducible; however, hash collisions across domains can produce non-deterministic slice assignment in multi-domain forests. |
| ldap_idmap_default_domain_sid | An sssd.conf option that pins a specific domain SID to slice zero of the ID range, bypassing the murmurhash algorithm for that domain. This is the mechanism for guaranteeing that the primary AD domain always receives the same UID sub-range on every node in the fleet. |
| RFC 2307 / RFC 2307bis POSIX attributes | RFC 2307 defines LDAP schema extensions (posixAccount, posixGroup object classes; uidNumber, gidNumber, uid attributes) for representing Unix identity information in an LDAP directory. Active Directory carries these attributes natively via its built-in schema; RFC 2307bis is a later draft that extended group membership handling. SSSD reads these attributes when ldap_id_mapping = false. |
| Identity Management for Unix (IDMU) | A Windows Server feature that provided a GUI (Unix Attributes tab in ADUC) and NIS role for managing POSIX attributes on AD objects. Deprecated in Windows Server 2012 R2 and removed as a UI component in Windows Server 2016. The underlying LDAP schema for uidNumber and gidNumber remains in AD and can be written via PowerShell. |
| SSSD idp provider | Introduced in SSSD 2.11.0, this provider integrates Linux hosts with OAuth2/OIDC identity providers including Entra ID (idp_type = entra_id) and Keycloak without requiring LDAP or Kerberos. POSIX IDs are autogenerated locally using a hash of the object cloud identifier. |
| Entra ID Directory Schema Extensions | Application-registered custom attributes on Entra ID objects, exposed via Microsoft Graph. Himmelblau uses schema extensions to store uidNumber, gidNumber, unixHomeDirectory, loginShell, and gecos on user and group objects, enabling directory-authoritative POSIX identity for pure cloud environments. |
| ID range and slice | SSSD divides the configured UID/GID range (idmap_range_min to idmap_range_max) into equal slices, each assigned to one AD domain. Each user UID is computed as: slice_base_uid + (RID mod slice_size), where RID is the relative identifier portion of the user SID. |
| Himmelblau | An open-source PAM/NSS daemon that authenticates Linux systems against Entra ID via OAuth2/OIDC and Microsoft Graph API. Supports storing POSIX attributes in Entra ID schema extensions via the aad-tool CLI, providing fleet-wide UID consistency without a separate LDAP store. |

---

## Tensions & Tradeoffs

- ID-mapping mode offers the lowest directory-preparation burden (no UID provisioning required) but sacrifices the ability to pre-assign specific UIDs — which matters for NFS, shared filesystems, and compliance environments where UIDs must match across heterogeneous systems such as Linux nodes using SSSD alongside macOS nodes using dscl.
- POSIX-attribute mode provides the only hard cross-node UID guarantee but requires operational discipline to populate and maintain uidNumber/gidNumber on every AD object at scale. The removal of the IDMU GUI in Windows Server 2016 increases the operational friction of this approach, shifting burden to PowerShell scripting or third-party tooling.
- The SSSD idp provider for Entra ID resolves the LDAP/Kerberos dependency problem but introduces a new consistency ambiguity: the UID-generation algorithm is documented as aiming for reproducibility while simultaneously acknowledging hash collisions where two objects may receive the same ID. This is weaker than either ID-mapping mode (which has a collision-prevention mechanism) or POSIX mode (which has no algorithmic collisions).
- Microsoft supported path for Entra ID POSIX attributes (provisioning to an on-premises LDAP directory via ECMA2 connector) reintroduces on-premises infrastructure dependency for organizations attempting to go cloud-native, partially negating the operational simplicity benefit of moving to Entra ID.
- Fleet-wide UID consistency in ID-mapping mode is achievable via shared sssd.conf (deployed by Ansible/Puppet/Chef) combined with ldap_idmap_default_domain_sid, but this consistency is fragile: a misconfigured node with a different id_range or missing domain_sid pin will silently assign different UIDs to the same user, manifesting as file-ownership mismatches rather than authentication failures.

---

## Open Questions

- Does SSSD 2.11.0 idp provider UID-generation algorithm use the Entra ID object immutable ID (objectId/GUID) as its hash input, and if so, is this guaranteed to be stable across tenant migrations or object restores?
- What is the exact collision probability of the idp provider hash algorithm across a tenant with tens of thousands of users, and is there an operator-visible collision log or metric?
- Does Entra Domain Services (AAD DS) expose the same SID structure as on-premises AD, allowing ldap_idmap_default_domain_sid to pin slice zero reliably in AAD DS environments?
- Is there a supported mechanism for migrating an existing fleet from ID-mapping mode to POSIX-attribute mode without UID churn — i.e., using existing algorithmically-generated UIDs as the canonical values to write back into directory POSIX attributes?
- What is the interaction between SSSD idp provider local cache and node reimaging — does a fresh node compute the same UID for a given Entra ID user as an existing node, given the same idmap_range configuration?
- For organizations using Entra ID and Himmelblau, is the schema extension attribute write (aad-tool set-posix-attrs) replicated globally across all Entra ID nodes with the same eventual-consistency guarantees as standard user attributes, or are extension attributes subject to different replication behavior?

---

## Sources & References

- [Connecting RHEL systems directly to AD using SSSD — Red Hat Enterprise Linux 8](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/integrating_rhel_systems_directly_with_windows_active_directory/connecting-rhel-systems-directly-to-ad-using-sssd_integrating-rhel-systems-directly-with-active-directory)
- [Configuring an AD Provider for SSSD — Red Hat Enterprise Linux 7 Windows Integration Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-integration-intro)
- [Introduction to SSSD Identity Provider (IdP) support — sssd.io](https://sssd.io/docs/idp/idp-introduction.html)
- [ID mapping — Automatically assign new slices for any AD domain — sssd.io](https://sssd.io/design-pages/idmap_auto_assign_new_slices.html)
- [FAQ: The removal of Identity Management for Unix (IDMU) in Active Directory — Red Hat Customer Portal](https://access.redhat.com/articles/2203991)
- [Configuring an Active Directory Domain with POSIX Attributes — Red Hat Customer Portal](https://access.redhat.com/articles/3023821)
- [Identity Management for Unix (IDMU) is deprecated in Windows Server — Microsoft Learn](https://learn.microsoft.com/en-us/archive/blogs/activedirectoryua/identity-management-for-unix-idmu-is-deprecated-in-windows-server)
- [Microsoft Entra provisioning to LDAP directories for Linux authentication — Microsoft Learn](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/on-premises-ldap-connector-linux)
- [sssd-idp(5) man page — Arch Linux Manual Pages](https://man.archlinux.org/man/sssd-idp.5.en)
- [Use Entra IDs to run jobs on your HPC cluster — Microsoft Tech Community](https://techcommunity.microsoft.com/blog/azurehighperformancecomputingblog/use-entra-ids-to-run-jobs-on-your-hpc-cluster/4457932)
- [Himmelblau — Azure Entra ID Authentication and Intune Compliance for Linux — GitHub](https://github.com/himmelblau-idm/himmelblau)
- [Transitioning from On-Prem AD to Azure Entra ID — Himmelblau Documentation](https://himmelblau-idm.org/docs/integration/)
- [Configuring Unix Attribute Synchronization with Azure Entra ID Using Microsoft Entra Connect Sync — Himmelblau Docs](https://himmelblau-idm.org/docs/advanced/Configuring-Unix-Attribute-Synchronization-with-Azure-Entra-ID-Using-Microsoft-Entra-Connect-Sync/)
- [ID mapping vs. POSIX attributes in AD — Red Hat Customer Portal Discussion](https://access.redhat.com/discussions/3252721)
- [RFC 2307 — An Approach for Using LDAP as a Network Information Service — IETF](https://datatracker.ietf.org/doc/html/rfc2307)
- [Linux Azure AD authentication options — Puppeteers Oy](https://www.puppeteers.net/blog/linux-azure-ad-authentication-options/)
- [SSSD and UID and GID Numbers — Red Hat Enterprise Linux 6 Deployment Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-system-uids)
