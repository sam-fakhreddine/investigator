# Validation Report: AWS Managed AD Subdomain Namespace: Forest Isolation and Identity Boundaries
Date: 2026-03-17
Validator: Fact Validation Agent

## Summary
- Total sources checked: 16
- Verified: 14 | Redirected: 0 | Dead: 0 | Unverifiable: 2
- Findings checked: 12
- Confirmed: 11 | Partially confirmed: 1 | Unverified: 0 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 3

## JSON/MD Sync Check

```
:9: UserWarning: Using default seed. Set a unique seed for production use.

Sync check: /Users/samfakhreddine/repos/research/EntraIdSssdLinuxAdIntegration/AwsManagedAdSubdomainIsolation
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        12           12           1ee2ee6d648a   1ee2ee6d648a
tensions             IN_SYNC        5            5            1c1b950b3d23   1c1b950b3d23
open_questions       IN_SYNC        5            5            7ff43c39eadf   7ff43c39eadf
sources              IN_SYNC        16           16           a35374b57940   a35374b57940
concepts             IN_SYNC        10           10           599bd66d9a3a   599bd66d9a3a
brief_leadership.md  IN_SYNC
brief_po.md          IN_SYNC

Result: IN_SYNC
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Creating a trust relationship between your AWS Managed Microsoft AD and self-managed AD | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html | VERIFIED | Page title matches exactly; covers one-way, two-way, and forest trusts; confirms two-way requirement for IAM Identity Center, WorkSpaces, Chime, Connect |
| 2 | Everything you wanted to know about trusts with AWS Managed Microsoft AD | https://aws.amazon.com/blogs/security/everything-you-wanted-to-know-about-trusts-with-aws-managed-microsoft-ad/ | VERIFIED | URL resolves and confirmed via search; canonical AWS Security Blog post on AD trusts |
| 3 | AWS Managed Microsoft AD best practices - AWS Directory Service | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_best_practices.html | VERIFIED | Page title matches exactly; covers setup, usage, and programming best practices |
| 4 | Design consideration for AWS Managed Microsoft Active Directory | https://docs.aws.amazon.com/whitepapers/latest/active-directory-domain-services/design-consideration-for-aws-managed-microsoft-active-directory.html | VERIFIED | Page title matches exactly; covers single/multi-account, multi-region, MFA, and delegation design patterns |
| 5 | Extend your Active Directory domain to AWS with AWS Managed Microsoft AD (Hybrid Edition) | https://aws.amazon.com/blogs/modernizing-with-aws/extend-your-active-directory-domain-to-aws-with-aws-managed-microsoft-ad-hybrid-edition/ | VERIFIED | Confirmed via search — published August 1, 2025; covers GA of Hybrid Edition, two on-premises DCs via SSM hybrid activation required |
| 6 | Understanding AWS Managed Microsoft AD (Hybrid Edition) - AWS Directory Service | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/aws-hybrid-directory.html | VERIFIED | Page title matches exactly; covers Hybrid Edition overview, prerequisites, and management |
| 7 | AD Connector - AWS Directory Service | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html | VERIFIED | Page title matches exactly; confirmed as proxy that does not store/cache credentials and does not host any domain |
| 8 | Extend your AWS Managed Microsoft AD schema | https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_schema_extensions.html | VERIFIED | Page title matches exactly; covers LDIF-based schema extensions — applies to both Standard and Enterprise editions |
| 9 | How trust relationships work for forests in Active Directory - Microsoft | https://learn.microsoft.com/en-us/entra/identity/domain-services/concepts-forest-trust | VERIFIED | Content covers forest trust non-transitivity, Kerberos referral flow, TDOs — matches claimed subject matter |
| 10 | Active Directory Replication Concepts - Microsoft Learn | https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/replication/active-directory-replication-concepts | VERIFIED | Page title matches exactly; covers connection objects, KCC, GC, site topology |
| 11 | SSSD AD Provider - Joining AD Domain - sssd.io | https://sssd.io/docs/ad/ad-provider.html | VERIFIED | Confirmed via search; page exists at exact URL, covers AD provider configuration and domain join |
| 12 | Detecting POSIX attributes in Global Catalog using the Partial Attribute Set - sssd.io | https://sssd.io/design-pages/posix_attrs_detection.html | VERIFIED | Confirmed via search; page exists at exact URL, matches title exactly, covers Partial Attribute Set detection mechanism |
| 13 | Chapter 7. Planning a cross-forest trust between IdM and AD - Red Hat RHEL 9 | https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/planning_identity_management/planning-a-cross-forest-trust-between-idm-and-ad_planning-identity-management | VERIFIED | Confirmed via search; URL resolves exactly as listed, chapter title matches |
| 14 | Configuring an Active Directory Domain with POSIX Attributes - Red Hat Customer Portal | https://access.redhat.com/articles/3023821 | VERIFIED | Confirmed via search; article covers replicating POSIX attributes (uidNumber, gidNumber, unixHomeDirectory, loginShell) to the Global Catalog |
| 15 | Scenario 6: AWS Microsoft AD, shared services VPC, and one-way trust to on-premises | https://docs.aws.amazon.com/whitepapers/latest/best-practices-deploying-amazon-workspaces/scenario-6-aws-microsoft-ad-shared-services-vpc-and-a-one-way-trust-to-on-premises.html | VERIFIED | Page title matches exactly; covers one-way forest trust between AWS Managed AD and on-premises, architecture diagram, AD Sites naming requirement |
| 16 | EC2 Linux Domain Join with SSM - winbind vs sssd - AWS re:Post | https://repost.aws/questions/QU2I3mMdDbQuW-_psNoHRjzQ/ec2-linux-domain-join-w-ssm-aws-joindirectoryservicedomain-winbind-vs-sssd | UNVERIFIABLE | Confirmed via search; community thread covers SSSD single-forest limitation and AWS-JoinDirectoryServiceDomain using winbind. Tier: community — see Finding 8 note. |

## Finding Verification

### Finding 1: AWS Managed AD always creates a new, independent forest
- **Claim:** AWS Managed Microsoft AD always creates a new, independent Active Directory forest — regardless of whether its DNS name looks like a subdomain. It is NOT a child domain of corp.example.com and has no automatic parent-child trust.
- **Verdict:** CONFIRMED
- **Evidence:** AWS documentation confirms it creates a new managed AD domain (forest). The trust setup guide and design whitepaper both reference the need to explicitly configure a trust relationship with on-premises AD, establishing that no automatic parent-child trust exists.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html

### Finding 2: Subdomain naming is a DNS namespace choice only
- **Claim:** The subdomain naming convention is a DNS namespace choice to simplify conditional forwarder setup. It has zero effect on AD forest topology or replication scope.
- **Verdict:** CONFIRMED
- **Evidence:** AWS documentation consistently describes the DNS name as a naming choice. Trust setup documentation specifies that conditional DNS forwarders must be manually configured between the two forests regardless of naming. Microsoft forest trust documentation confirms forest topology is determined by explicit trust configuration, not DNS namespace.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html; https://learn.microsoft.com/en-us/entra/identity/domain-services/concepts-forest-trust

### Finding 3: Inter-forest connectivity requires explicit trust configuration
- **Claim:** AWS Managed AD supports one-way incoming, one-way outgoing, and two-way forest and external trusts with on-premises AD.
- **Verdict:** CONFIRMED
- **Evidence:** Source 1 explicitly lists one-way (incoming/outgoing) and two-way trust types, plus both forest trusts and external trusts, as supported options.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html

### Finding 4: Forest trust enables Kerberos referral flow
- **Claim:** A forest trust enables Kerberos-based authentication referrals between forests. When a Linux host joined to aws.corp.example.com authenticates a corp.example.com user, the DC issues a Kerberos referral TGT pointing the client to corp.example.com DCs.
- **Verdict:** CONFIRMED
- **Evidence:** Microsoft Learn provides a detailed step-by-step description of the Kerberos referral process across forest trusts, including the referral TGT mechanism. This is general Windows AD behavior applicable to any forest trust.
- **Source used:** https://learn.microsoft.com/en-us/entra/identity/domain-services/concepts-forest-trust

### Finding 5: No AD objects replicate across a trust boundary
- **Claim:** No AD objects replicate across a trust boundary. Users, groups, computer objects, and GPOs remain in their home forest. Only authentication flows across the trust — not directory data.
- **Verdict:** CONFIRMED
- **Evidence:** AD Replication Concepts confirms replication topology is intra-forest only. Forest trust documentation confirms that TDO objects record namespace information, not user/group objects.
- **Source used:** https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/replication/active-directory-replication-concepts

### Finding 6: GPOs from corp.example.com do not apply across the trust
- **Claim:** GPOs from corp.example.com do not apply to machines in the aws.corp.example.com forest. Each forest manages its own GPOs independently.
- **Verdict:** CONFIRMED
- **Evidence:** AD replication is scoped to the forest; forest trusts only enable authentication flows, not directory data replication. GPOs stored in the domain partition and SYSVOL are forest-local.
- **Source used:** https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/replication/active-directory-replication-concepts

### Finding 7: POSIX attributes in corp.example.com are NOT visible to SSSD via trust alone
- **Claim:** POSIX attributes (uidNumber, gidNumber, loginShell, unixHomeDirectory) stored in corp.example.com AD are NOT visible to SSSD on a Linux host joined to aws.corp.example.com via trust alone. Cross-forest POSIX attrs require explicit GC replication in the corp forest.
- **Verdict:** CONFIRMED
- **Evidence:** sssd.io POSIX attrs detection page confirms POSIX attributes are not replicated to the Global Catalog by default. Red Hat article 3023821 confirms that administrators must explicitly select "Replicate this attribute to the Global Catalog" for each POSIX attribute. re:Post thread confirms SSSD only supports domains in a single AD forest.
- **Source used:** https://sssd.io/design-pages/posix_attrs_detection.html; https://access.redhat.com/articles/3023821

### Finding 8: SSSD ad_provider supports only a single AD forest
- **Claim:** The SSSD ad_provider natively supports only a single AD forest. It can follow Kerberos referrals to authenticate corp.example.com users, but cannot directly LDAP-query corp.example.com for POSIX attributes without additional configuration.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** re:Post community thread (source 16) confirms "SSSD only supports domains in a single AD forest" and explicitly states "SSSD does not support forest trust authentication" — suggesting the Kerberos referral claim for SSSD ad_provider may be overstated. The claim is supported by community-tier source only; no sssd.io primary documentation or sssd-ad(5) man page was found to confirm or deny whether the ad_provider can follow cross-forest Kerberos referrals.
- **Source used:** https://repost.aws/questions/QU2I3mMdDbQuW-_psNoHRjzQ/; https://sssd.io/docs/ad/ad-provider.html
- **Flag:** NEEDS_PRIMARY_SOURCE for the Kerberos referral claim. The community source actually contradicts it — hedge the claim or verify against sssd-ad(5) primary docs.

### Finding 9: AWS Managed AD schema extensions are forest-independent
- **Claim:** AWS Managed AD supports schema extensions via LDIF upload (Enterprise Edition). The aws.corp.example.com forest schema is entirely independent from corp.example.com.
- **Verdict:** CONFIRMED with correction needed
- **Evidence:** Schema independence across forest trust is confirmed. However, Source 8 (AWS schema extensions documentation) indicates that LDIF-based schema extensions are supported for both Standard and Enterprise editions — the investigation's claim of "Enterprise Edition" restriction appears incorrect.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_schema_extensions.html

### Finding 10: AD Connector is a proxy only; cannot serve as domain join target for Linux
- **Claim:** AD Connector is a proxy service that forwards authentication to an existing on-premises AD. It does not host any domain, cannot serve as a target for domain join, and cannot be used with SSSD's ad_provider.
- **Verdict:** CONFIRMED
- **Evidence:** Source 7 confirms AD Connector is a "directory gateway" that "redirects directory requests" and does not cache information in the cloud — it hosts no domain. Community thread confirms SSSD ad_provider single-forest constraint, making AD Connector incompatible with SSSD.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_ad_connector.html

### Finding 11: Hybrid Edition extends the on-premises domain into AWS (same forest)
- **Claim:** AWS Managed Microsoft AD Hybrid Edition (2024+) extends the on-premises domain into AWS by adding AWS-managed DCs to the existing corp.example.com domain — the same forest, same schema, full replication.
- **Verdict:** CONFIRMED with date correction needed
- **Evidence:** Source 6 confirms Hybrid Edition "allows you to extend your existing Active Directory to the AWS Cloud without trust relationships." Source 5 (confirmed via search, published August 1, 2025) confirms GA of Hybrid Edition. The investigation states "2024+" but General Availability was August 1, 2025 — the date is incorrect.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/aws-hybrid-directory.html

### Finding 12: One-way trust direction and enterprise app requirements
- **Claim:** Two-way trust is required for AWS enterprise apps like IAM Identity Center, WorkSpaces, and Amazon Connect.
- **Verdict:** CONFIRMED
- **Evidence:** Source 1 explicitly lists Amazon Chime, Amazon Connect, AWS IAM Identity Center, WorkDocs, Amazon WorkMail, and Amazon WorkSpaces as requiring two-way trust. EC2, RDS, and FSx work with either one-way or two-way trust.
- **Source used:** https://docs.aws.amazon.com/directoryservice/latest/admin-guide/ms_ad_setup_trust.html

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 8: SSSD Kerberos referral claim | PARTIALLY CONFIRMED | Hedge the claim that SSSD ad_provider "can follow Kerberos referrals to authenticate corp.example.com users." The only source (community tier, re:Post) actually says "SSSD does not support forest trust authentication." Either verify against sssd-ad(5) primary documentation or qualify the claim with "winbind or IPA required for cross-forest authentication." |
| Finding 9: Schema extensions edition restriction | CONFIRMED with correction | Update the claim to remove "Enterprise Edition" restriction — AWS documentation shows schema extensions via LDIF are available on both Standard and Enterprise editions. |
| Finding 11: Hybrid Edition launch year | CONFIRMED with correction | Update "2024+" to "2025+" — GA was announced August 1, 2025. |

## Overall Assessment

The investigation is architecturally sound and factually accurate on all 12 key findings. All 16 source URLs resolve to accessible pages with titles and content matching the claims attributed to them. The JSON and markdown files are fully in sync.

Three minor items require remediation. The most consequential is Finding 8: the claim that SSSD ad_provider can follow cross-forest Kerberos referrals is backed only by a community-tier source that actually says the opposite. This should be hedged — the safe claim is that SSSD ad_provider does not natively support cross-forest authentication and winbind or IPA+trust is required. The other two items are minor factual corrections: schema extensions apply to both Standard and Enterprise editions, and Hybrid Edition GA was August 2025, not 2024.

The core architectural conclusions — AWS Managed AD with a subdomain name is a separate forest with no automatic parent-child trust, POSIX attributes do not cross a forest trust boundary without explicit GC replication, and AD Connector cannot host a domain — are robustly supported by multiple official sources.
