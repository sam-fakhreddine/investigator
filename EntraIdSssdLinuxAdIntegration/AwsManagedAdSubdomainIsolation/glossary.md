# Glossary — AWS Managed AD Subdomain Namespace: Forest Isolation and Identity Boundaries

Quick definitions of key terms and concepts referenced in this investigation.

---

## Active Directory Forest

The top-level security and replication boundary in Active Directory. Each forest has its own schema, global catalog, and trust relationships. Forests do not share directory data unless explicitly federated via trusts.

## Child Domain vs Separate Forest

A child domain (e.g., child.parent.example.com) is created inside an existing forest and automatically inherits a transitive two-way parent-child trust, shares the forest schema, and replicates to the same global catalog. A separate forest with a subdomain-style name (aws.corp.example.com) shares none of these properties — it is entirely isolated until a trust is manually established.

## Forest Trust

A manually configured trust between two forest root domains that allows Kerberos authentication to traverse the boundary. Recommended by Microsoft and AWS over external trusts because it fully supports Kerberos without caveats. Forest trusts are non-transitive across three or more forests — Forest A trusting Forest B and Forest B trusting Forest C does not grant Forest A access to Forest C.

## Kerberos Referral Flow

When a client in Forest A requests a service ticket for a resource in Forest A but presents a principal from Forest B, the Forest A DC issues a referral TGT pointing the client to a Forest B DC. The client then contacts the Forest B DC to obtain the actual service ticket. This is the only authentication mechanism that crosses a forest trust; no LDAP data crosses with it.

## SSSD ad_provider Single-Forest Constraint

SSSD's ad_provider binds LDAP and Kerberos connections to the single AD forest the Linux host is joined to. It cannot natively perform LDAP queries against a trusted foreign forest's DCs. SSSD's ad_provider does not natively support cross-forest trust authentication; organizations requiring Linux hosts to authenticate users from a trusted forest must use winbind or an IPA+trust configuration instead of SSSD alone.

## POSIX Attribute Locality

POSIX attributes (uidNumber, gidNumber, loginShell, homeDirectory) used by Linux systems must exist as populated attributes in the AD domain the Linux host is joined to, or be replicated to that forest's Global Catalog. Attributes stored exclusively in a remote (trusted) forest are not accessible to SSSD's LDAP queries on the joined host.

## AD Connector

An AWS Directory Service product that acts as a proxy, forwarding authentication requests to an existing on-premises AD over a VPN or Direct Connect link. It does not create or host any AD domain and cannot serve as a domain join target for Linux instances. Instances that attempt domain join via AD Connector end up communicating directly with on-premises DCs.

## AWS Managed AD Hybrid Edition

An AWS Directory Service offering (GA August 2025) that extends an existing on-premises AD domain into AWS by deploying AWS-managed domain controllers as members of the on-premises forest. Unlike Standard/Enterprise Managed AD, Hybrid Edition hosts DCs in the same forest — meaning full replication, same schema, and no cross-forest trust complexity.

## Selective Authentication

An optional trust configuration that restricts which users from the trusted forest are permitted to authenticate to specific computer objects in the trusting forest. More granular than a blanket forest trust; relevant for least-privilege access across the aws.corp.example.com / corp.example.com boundary.

## Global Catalog (GC)

A read-only partial replica of all objects in an AD forest, hosted on designated DCs. SSSD uses the GC to resolve cross-domain group memberships and to detect POSIX attributes across multiple domains within the same forest. GC does not span separate forests.

---

*Back to: [investigation.md](investigation.md)*
