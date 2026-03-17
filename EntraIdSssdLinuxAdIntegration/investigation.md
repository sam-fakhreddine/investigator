# Investigation: Entra ID and SSSD Linux Identity Integration: End-to-End Architecture

**Date:** 2026-03-17
**Status:** Complete

---

## Question

> How does Linux identity integration work end-to-end when authenticating Linux hosts against Active Directory or Entra ID via SSSD — covering the UID/GID mapping strategies, centralized sudo policy management via FreeIPA/Red Hat IDM, SSSD caching behavior and performance for large deployments, and the architectural boundaries imposed by AWS Managed AD forest isolation?

---

## Context

Organizations running Linux fleets against Microsoft identity services — on-premises Active Directory, cloud-native Entra ID, or AWS Managed AD — must chain together four interdependent subsystems: POSIX UID/GID mapping, centralized sudo policy, SSSD caching, and AD forest topology. Each subsystem has distinct failure modes, and a decision made in one (for example, choosing ID-mapping mode for UIDs) constrains or invalidates decisions in others (POSIX attributes invisible across a forest trust become irrelevant if ID mapping is used, but ID mapping itself fails silently in multi-domain forests without additional configuration). AWS deployments add a structural complication: the subdomain naming convention for AWS Managed AD creates a false impression of child-domain inheritance that masks a hard forest isolation boundary, requiring explicit decisions about where POSIX attributes are provisioned and whether SSSD's single-forest constraint is a blocker. FreeIPA/Red Hat IDM sits in the middle of this stack, centralizing both sudo policy and identity caching policy, with its own latency and propagation characteristics that affect security posture independently of the upstream AD or Entra ID identity source.

---

## Linux Identity Integration: Component Decision Matrix

| Component / Decision | Sub-topic | Key Constraint or Default | Risk if Wrong |
| --- | --- | --- | --- |
| UID/GID mapping mode (ldap_id_mapping) | UID/GID Mapping | Default true (algorithmic, SID-derived); POSIX attrs silently ignored when enabled | Silent UID drift across nodes in multi-domain forests; file ownership mismatches on shared filesystems |
| Multi-domain forest UID pinning (ldap_idmap_default_domain_sid) | UID/GID Mapping | Not set by default; slice assignment is order-dependent without it | Same user receives different UIDs on different nodes — manifests as ownership errors, not auth failures |
| Pure cloud Entra ID provider | UID/GID Mapping | SSSD ad provider incompatible; requires idp provider (SSSD 2.11+) or Himmelblau | Fleet cannot authenticate against Entra ID at all; UID hash-collision risk in idp provider |
| SSSD sudo provider type (sudo_provider=ipa vs ldap) | FreeIPA Sudo | ipa provider resolves DN-based group memberships; ldap provider silently drops group-scoped rules | Group-scoped sudo rules never apply; no error is surfaced — misconfiguration is invisible |
| Local /etc/sudoers nsswitch ordering | FreeIPA Sudo | Default files sss — local sudoers evaluated first, shadowing LDAP rules | Stale local sudoers silently override centrally managed policy, defeating centralization |
| Sudo rule revocation propagation delay | FreeIPA Sudo / SSSD Caching | Smart refresh 15 min; full refresh 6 h by default | Revoked sudo privileges remain active on cached hosts for up to 6 hours without manual cache flush |
| Offline credential caching (cache_credentials) | SSSD Caching | Disabled by default — users cannot authenticate if IDM server is unreachable | Complete login failure during IDM outages; business continuity risk for all Linux hosts |
| First-login cold cache latency | SSSD Caching | enumerate=false by default; first login is always a live directory query | Users in large groups (thousands of members) experience 2-10 minute login delays or timeouts |
| AWS Managed AD forest topology | AWS Forest Isolation | Always a separate AD forest regardless of subdomain naming — no automatic parent-child trust | Engineers assume corp AD objects (users, POSIX attrs, GPOs) are visible in AWS forest; they are not |
| POSIX attribute visibility across forest trust | AWS Forest Isolation | uidNumber/gidNumber in corp AD are invisible to SSSD on aws-joined hosts via trust alone | Linux hosts joined to AWS Managed AD cannot resolve corp user UIDs — identity pipeline breaks |

> SSSD ad_provider binds LDAP to the single joined forest; cross-forest POSIX attribute resolution requires Hybrid Edition, local re-provisioning, or a winbind/IPA+trust alternative. AWS Managed AD Hybrid Edition (GA August 2025) is the only AWS-managed option that eliminates forest isolation.

---

## Key Findings

- SSSD exposes two mutually exclusive UID/GID mapping modes controlled by ldap_id_mapping: true (default) generates POSIX IDs algorithmically from the Active Directory SID via murmurhash; false reads uidNumber and gidNumber from directory attributes. When ID mapping is enabled, directory POSIX attributes are silently ignored — the two modes cannot be mixed.
- Cross-node UID consistency in ID-mapping mode has a documented multi-domain caveat: slice assignment for secondary domains is order-dependent across nodes. Without ldap_idmap_default_domain_sid pinning the primary domain to slice zero in every node's sssd.conf, the same user can receive different UIDs on different hosts in the fleet, producing file-ownership mismatches rather than authentication failures.
- POSIX-attribute mode (ldap_id_mapping = false) is the only mode that provides a hard cross-node UID guarantee — UID authority lives in the directory and is identical everywhere — but requires populating uidNumber and gidNumber on every AD object. The IDMU GUI was removed in Windows Server 2016; the underlying LDAP schema remains and can be written via PowerShell, but the operational friction is significant at scale.
- Pure cloud Entra ID is incompatible with the SSSD ad provider, which requires LDAP and Kerberos endpoints that Entra ID does not expose. SSSD 2.11.0 introduced id_provider = idp (idp_type = entra_id) using OAuth2/OIDC and Microsoft Graph. This provider auto-generates UIDs from a hash of the object identifier and is documented as reproducible but carries a non-zero hash-collision risk. Himmelblau provides an alternative path that stores POSIX attributes in Entra ID schema extensions via the aad-tool utility.
- FreeIPA stores sudo policy in 389-DS LDAP under cn=sudo,dc=<realm> using a dual-objectclass model (ipaSudoRule extending sudoRole). SSSD's IPA sudo provider resolves DN-based group memberships and caches flattened rules in the local sysdb LDB database. The generic LDAP sudo provider cannot traverse IPA DN-based memberships — group-scoped rules silently fail to apply with no error output when sudo_provider=ldap is used against an IPA server.
- Local /etc/sudoers is evaluated before SSSD under the default nsswitch.conf ordering (files sss), meaning stale or overly permissive local sudoers silently override centrally managed IPA policy. Full sudo centralization requires either inverting the nsswitch source order or purging local sudoers from all enrolled hosts.
- AD-sourced users can receive FreeIPA sudo rules only via a two-hop indirection: AD SID is mapped into an IPA external group (ipaExternalGroup), which is nested inside an IPA POSIX group that is referenced in the sudo rule. AD group changes do not automatically propagate to sudo policy until IPA group membership is also updated.
- SSSD is a multi-process daemon (Monitor, per-domain Backend, per-protocol Responders). The primary identity store is an LDB database at /var/lib/sss/db/cache_<domain>.ldb with a default TTL of 5400 seconds (90 minutes). Offline credential caching (cache_credentials) is disabled by default — users cannot authenticate at all if the identity server is unreachable without this setting explicitly enabled.
- Enabling enumerate = true causes sssd_be to download all directory objects at startup. On large directories (30,000+ users), documented cases show sssd_be consuming ~99% CPU during enumeration, blocking all login operations for minutes. Red Hat's guidance for large IPA-AD trust deployments recommends keeping enumerate = false and mounting the SSSD cache directory on a RAM-backed filesystem, sizing approximately 100 MB per 10,000 LDAP entries.
- First-login latency spikes occur when SSSD must resolve large or deeply nested group memberships during a cold-cache lookup — no cached entry exists until the first lookup completes. Documented cases show login delays of several minutes and sssd_be watchdog kills in extreme group-membership scenarios (per Red Hat Customer Portal solution #1475233). The entry_cache_nowait_percentage parameter mitigates blocking on subsequent lookups by serving stale cache while refreshing in the background, but does not help the initial cold-cache hit.
- AWS Managed Microsoft AD always creates a new, independent Active Directory forest — regardless of whether its DNS name resembles a subdomain (aws.corp.example.com). This is not a child domain of the corporate forest. No AD objects (users, groups, GPOs, POSIX attributes) replicate across the trust boundary; only Kerberos authentication referrals cross it.
- SSSD's ad_provider binds LDAP and Kerberos to the single forest the Linux host is joined to. On an AWS Managed AD-joined host, SSSD cannot directly LDAP-query the corporate forest for POSIX attributes stored there. POSIX attributes must be provisioned within the AWS forest, replicated to its Global Catalog, or the architecture must shift to Hybrid Edition (GA August 2025), which extends the on-premises domain into AWS and eliminates the cross-forest constraint entirely.
- The SSSD sudo cache uses two independent refresh cycles — smart refresh (incremental, 15 min default) and full refresh (6 h default) — meaning revoked sudo privileges can remain active on cached hosts for up to 6 hours without a manual sss_cache invalidation. This lag interacts with the AD-sourced user indirection through IPA external groups: an AD group change that should remove sudo access requires both the AD change and an IPA group membership update before the next SSSD full refresh cycle removes the cached rule.
- The IPA provider caches HBAC access policy in the local sysdb LDB and evaluates it on the host, providing access control decisions even briefly offline. The ipa_hbac_refresh parameter (default 5 seconds) controls the minimum re-fetch interval when online, not the offline cache window — offline HBAC availability is governed by entry_cache_timeout. This capability is absent from the generic LDAP provider configuration and represents a qualitative architectural advantage of the IPA provider stack for environments requiring offline access policy enforcement.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| ldap_id_mapping | SSSD configuration boolean (default true for ad provider) selecting between algorithmic UID generation from the AD SID and directory-resident POSIX attribute reading. When true, uidNumber and gidNumber in AD are silently ignored. The two modes are mutually exclusive per domain. |
| murmurhash (SSSD ID mapping) | The non-cryptographic hash function used by the SSSD sss_idmap library to map a domain SID to a slice index within the configured UID range. Same SID always produces the same hash; however, slice assignment for secondary domains is order-dependent in multi-domain forests, producing inconsistent UIDs across nodes without the ldap_idmap_default_domain_sid pin. |
| ldap_idmap_default_domain_sid | An sssd.conf option that pins a specific domain SID to slice zero of the ID range, bypassing the murmurhash algorithm for that domain. Required for guaranteed cross-node UID consistency on the primary domain in multi-domain AD forest environments. |
| SSSD idp provider | Introduced in SSSD 2.11.0, this provider integrates Linux hosts with OAuth2/OIDC identity providers including Entra ID (idp_type = entra_id) without requiring LDAP or Kerberos. POSIX IDs are auto-generated locally using a hash of the cloud object identifier, with a documented but unquantified hash-collision risk. |
| Himmelblau | An open-source PAM/NSS daemon authenticating Linux systems against Entra ID via OAuth2/OIDC and Microsoft Graph API. Supports storing POSIX attributes in Entra ID schema extensions via the aad-tool CLI, providing fleet-wide UID consistency without a separate on-premises LDAP store. |
| ipaSudoRule objectClass | FreeIPA LDAP objectClass extending sudoRole with DN-based membership attributes (memberUser, memberHost, memberAllowCmd, memberDenyCmd). Allows referencing IPA group and host-group objects by DN for dynamic membership resolution. Requires the SSSD IPA sudo provider — the generic LDAP sudo provider cannot traverse these DN references and silently omits group-scoped rules. |
| IPA external group | An IPA group with objectClass ipaExternalGroup that holds foreign SIDs (Active Directory users or groups) as members. AD identities are mapped into IPA external groups, which are nested inside IPA POSIX groups used in sudo rules — the only supported path for granting AD-sourced users FreeIPA sudo access. |
| LDB (sysdb) cache | The primary SSSD on-disk identity store — an LDAP-like embedded database at /var/lib/sss/db/cache_<domain>.ldb. Stores all fetched identity objects: users, groups, sudo rules, HBAC policy, SSH keys, and autofs maps. Only the Backend process writes to it; Responders (NSS, PAM, sudo) read from it. Default TTL 5400 seconds. |
| Offline credential cache | A salted password hash stored per-user in the sysdb LDB. Enables password authentication when the identity server is unreachable. Disabled by default (cache_credentials = false). Without it, users cannot authenticate at all during IDM outages. |
| entry_cache_nowait_percentage | When a lookup arrives after this percentage of entry_cache_timeout has elapsed, SSSD returns the stale cached entry immediately and refreshes in the background. Prevents blocking waits at the cost of brief staleness; critical for avoiding login latency spikes on large deployments when cache entries approach their TTL. |
| Active Directory Forest (isolation boundary) | The top-level security and replication boundary in Active Directory. AWS Managed AD always creates a new, separate forest regardless of subdomain naming. No directory objects (users, groups, POSIX attributes, GPOs) replicate across a forest trust; only Kerberos authentication referrals cross it. |
| SSSD ad_provider Single-Forest Constraint | SSSD's ad_provider binds LDAP and Kerberos to the single AD forest the Linux host is joined to. It cannot natively LDAP-query a trusted foreign forest's DCs. Organizations requiring Linux hosts to authenticate users from a trusted forest must use winbind or an IPA+trust configuration, or adopt AWS Managed AD Hybrid Edition which eliminates the separate-forest constraint. |
| AWS Managed AD Hybrid Edition | An AWS Directory Service offering (GA August 2025) that extends an existing on-premises AD domain into AWS by deploying AWS-managed DCs as members of the on-premises forest. Unlike Standard and Enterprise Managed AD, Hybrid Edition hosts DCs in the same forest — full replication, same schema, POSIX attributes visible — eliminating all cross-forest identity constraints. |

---

## Tensions & Tradeoffs

- ID-mapping mode (ldap_id_mapping = true) eliminates directory preparation burden but silently ignores uidNumber and gidNumber attributes — which are also invisible across the AWS Managed AD forest trust boundary. The combination means organizations using both features have no viable POSIX-attribute path and must commit to algorithmic IDs with the associated fleet-consistency risks.
- POSIX-attribute mode provides the only hard cross-node UID guarantee but requires populating uidNumber and gidNumber on every AD object. For AWS Managed AD deployments, these attributes must be provisioned within the AWS forest independently from the corporate forest — doubling the attribute management burden across two separate schemas.
- Offline credential caching (cache_credentials = false, the default) is the safer posture against credential replay on a compromised host, but produces complete login failures during IDM outages. Enabling it stores a password hash on each Linux host disk — a security posture choice with no correct default that must be made explicitly.
- The SSSD sudo provider misconfiguration (sudo_provider=ldap instead of sudo_provider=ipa on IPA-joined hosts) produces no error but silently drops all group-scoped sudo rules. Combined with the default nsswitch ordering (files first), a deployment can appear to be centrally managed while local /etc/sudoers entries dominate and IPA group-scoped rules never apply.
- The SSSD sudo rule revocation lag (up to 6 hours for full refresh) compounds with the IPA external group indirection for AD-sourced users: removing sudo access from an AD group requires both an AD change and an IPA external group membership update, then waiting for the next SSSD full refresh cycle — creating a multi-step, time-delayed revocation path for privileged access.
- AWS Managed AD Hybrid Edition resolves the cross-forest identity problem entirely but requires on-premises DC registration via SSM and a Windows Server 2012 R2+ domain functional level. Legacy environments that cannot meet these prerequisites have no AWS-managed alternative — they must either re-provision POSIX attributes locally in the AWS forest or abandon SSSD in favor of winbind or IPA+trust, both of which add architectural complexity.
- The SSSD idp provider for pure cloud Entra ID resolves the LDAP/Kerberos dependency but introduces UID consistency ambiguity: the algorithm is documented as aiming for reproducibility while acknowledging hash collisions. This is weaker than ID-mapping mode (which uses a collision-prevention mechanism) and far weaker than POSIX-attribute mode. Microsoft's supported path for POSIX attributes in Entra-centric environments routes through an on-premises LDAP proxy (ECMA2 connector), reintroducing on-premises infrastructure dependency for organizations attempting to go cloud-native.
- enumerate = false (the default) keeps startup load low but means first-ever logins for any user are always live directory queries with no cache warmup. For users in large or deeply nested AD groups, this cold-cache first-login is the primary documented cause of multi-minute login delays and sssd_be watchdog kills — a reliability risk that worsens as the directory grows.

---

## Open Questions

- If POSIX attributes are published to the corporate Global Catalog, can SSSD on an aws.corp.example.com-joined host reach that GC across the forest trust — and does SSSD's ad_provider GC detection (posix_attrs_detection) work cross-forest or only within the joined forest?
- Is there a supported, non-destructive migration path from ID-mapping mode to POSIX-attribute mode for an existing fleet — specifically, can the algorithmically-generated UIDs be written back into AD uidNumber attributes so that the transition does not cause UID churn and file-ownership breakage?
- What is the exact SSSD behavior when a sysdb LDB entry has expired (past entry_cache_timeout) and the backend is simultaneously offline: does SSSD serve the stale entry, return a lookup failure, or queue the request until the backend reconnects?
- For the SSSD idp provider (Entra ID), does the UID-generation hash use the Entra ID objectId (immutable GUID) as its input, and is that GUID guaranteed stable across tenant migrations, object restores, or cross-tenant moves?
- Can sudoNotBefore/sudoNotAfter time-boxed FreeIPA sudo rules be relied upon for access control given the SSSD cache refresh schedule — specifically, can a time-expired rule remain cached and active past its intended end time if the smart refresh cycle has not yet fired?
- Does AWS Managed AD enforce SID filtering on forest trusts by default, and what is the documented impact on group membership traversal for corporate users accessing AWS-joined Linux resources when SID filtering is active?
- For large IPA-AD trust deployments using ignore_group_members = true, does SSSD resolve group membership for sudo and HBAC rule evaluation from the local sysdb memberof attribute on user objects, or does it issue live LDAP memberof queries — and does the answer change between the IPA and LDAP providers?
- What is the failure mode when an IPA server is unreachable and the local sysdb sudo cache has fully expired: does sudo fail open (permit all), fail closed (deny all), or fall back to /etc/sudoers — and is this behavior consistent across SSSD versions?

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
- [Red Hat Enterprise Linux 8: Configuring sudo rules in IdM](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_identity_management/configuring-sudo-rules-in-idm_configuring-and-managing-idm)
- [Red Hat Enterprise Linux 9: Configuring sudo rules in IdM](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_idm_users_groups_hosts_and_access_control_rules/configuring-sudo-rules-in-idm_managing-idm-users-groups-hosts-and-access-control-rules)
- [SSSD Documentation: sudo integration](https://sssd.io/docs/users/sudo_integration.html)
- [FreeIPA Design: Sudo integration (V3)](https://www.freeipa.org/page/V3/Sudo_Integration)
- [RFC 4876: A Configuration Profile Schema for LDAP-Based Agents](https://www.rfc-editor.org/rfc/rfc4876)
- [Red Hat IDM: Planning a cross-forest trust between IdM and AD](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/planning_identity_management/planning-a-cross-forest-trust-between-idm-and-ad_planning-identity-management)
- [FreeIPA: Active Directory trust setup](https://www.freeipa.org/page/Active_Directory_trust_setup)
- [sssd-sudo(5) Linux man page](https://linux.die.net/man/5/sssd-sudo)
- [FreeIPA: Howto - sudo with LDAP](https://www.freeipa.org/page/Howto/Sudo)
- [SSSD Architecture - sssd.io](https://sssd.io/docs/architecture.html)
- [SSSD Internals - docs.pagure.org](https://docs.pagure.org/sssd.sssd/developers/internals.html)
- [Improve SSSD Performance with a timestamp cache - sssd.io](https://sssd.io/design-pages/one_fourteen_performance_improvements.html)
- [SUDO Caching Rules - sssd.io](https://sssd.io/design-pages/sudo_caching_rules.html)
- [SUDO Responder Cache Behaviour - sssd.io](https://sssd.io/design-pages/sudo_responder_cache_behaviour.html)
- [Authenticate against cache in SSSD - sssd.io](https://sssd.io/design-pages/cached_authentication.html)
- [KCM server for SSSD - sssd.io](https://sssd.io/design-pages/kcm.html)
- [Managing the SSSD Cache - Red Hat RHEL 6 Deployment Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache)
- [Domain Options Enabling Offline Authentication - Red Hat RHEL 6](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sssd-cache-cred)
- [Understanding SSSD and its benefits - Red Hat RHEL 8](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/configuring_authentication_and_authorization_in_rhel/understanding-sssd-and-its-benefits_configuring-authentication-and-authorization-in-rhel)
- [Tuning SSSD performance for large IdM-AD trust deployments - RHEL 9](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/tuning_performance_in_identity_management/assembly_tuning-sssd-performance-for-large-idm-ad-trust-deployments_tuning-performance-in-idm)
- [Tuning performance in Identity Management - Red Hat RHEL 8](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/tuning_performance_in_identity_management/index)
- [SSSD logins and user lookups from large domains are slow - Red Hat Customer Portal](https://access.redhat.com/solutions/705623)
- [Slow logins with SSSD due to large and nested groups in Active Directory - Red Hat Customer Portal](https://access.redhat.com/solutions/1475233)
- [Cache credentials with SSSD in offline mode - Red Hat Customer Portal](https://access.redhat.com/solutions/500963)
- [sssd-ipa(5) man page - configuration file for SSSD IPA provider](https://linux.die.net/man/5/sssd-ipa)
- [Enumerating large number of users makes sssd_be hog CPU - GitHub Issue 2771](https://github.com/SSSD/sssd/issues/2771)
- [SSSD Frequently Asked Questions - docs.pagure.org](https://docs.pagure.org/sssd.sssd/users/faq.html)
- [Performance tuning SSSD for large IPA-AD trust deployments - jhrozek blog](https://jhrozek.wordpress.com/2015/08/19/performance-tuning-sssd-for-large-ipa-ad-trust-deployments/)
- [Creating a trust relationship between your AWS Managed Microsoft AD and self-managed AD](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html)
- [Everything you wanted to know about trusts with AWS Managed Microsoft AD](https://aws.amazon.com/blogs/security/everything-you-wanted-to-know-about-trusts-with-aws-managed-microsoft-ad/)
- [AWS Managed Microsoft AD best practices - AWS Directory Service](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_best_practices.html)
- [Design consideration for AWS Managed Microsoft Active Directory](https://docs.aws.amazon.com/whitepapers/latest/active-directory-domain-services/design-consideration-for-aws-managed-microsoft-active-directory.html)
- [Extend your Active Directory domain to AWS with AWS Managed Microsoft AD (Hybrid Edition)](https://aws.amazon.com/blogs/modernizing-with-aws/extend-your-active-directory-domain-to-aws-with-aws-managed-microsoft-ad-hybrid-edition/)
- [Understanding AWS Managed Microsoft AD (Hybrid Edition) - AWS Directory Service](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/aws-hybrid-directory.html)
- [AD Connector - AWS Directory Service](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html)
- [Extend your AWS Managed Microsoft AD schema](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_schema_extensions.html)
- [How trust relationships work for forests in Active Directory - Microsoft](https://learn.microsoft.com/en-us/entra/identity/domain-services/concepts-forest-trust)
- [Active Directory Replication Concepts - Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/replication/active-directory-replication-concepts)
- [SSSD AD Provider - Joining AD Domain - sssd.io](https://sssd.io/docs/ad/ad-provider.html)
- [Detecting POSIX attributes in Global Catalog using the Partial Attribute Set - sssd.io](https://sssd.io/design-pages/posix_attrs_detection.html)
- [Chapter 7. Planning a cross-forest trust between IdM and AD - Red Hat RHEL 9](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/planning_identity_management/planning-a-cross-forest-trust-between-idm-and-ad_planning-identity-management)
- [Scenario 6: AWS Microsoft AD, shared services VPC, and one-way trust to on-premises](https://docs.aws.amazon.com/whitepapers/latest/best-practices-deploying-amazon-workspaces/scenario-6-aws-microsoft-ad-shared-services-vpc-and-a-one-way-trust-to-on-premises.html)
- [EC2 Linux Domain Join with SSM - winbind vs sssd - AWS re:Post](https://repost.aws/questions/QU2I3mMdDbQuW-_psNoHRjzQ/ec2-linux-domain-join-w-ssm-aws-joindirectoryservicedomain-winbind-vs-sssd)
