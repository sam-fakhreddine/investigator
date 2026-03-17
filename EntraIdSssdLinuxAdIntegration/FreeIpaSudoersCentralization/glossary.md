# Glossary — FreeIPA / Red Hat IDM Centralized Sudoers Management

Quick definitions of key terms and concepts referenced in this investigation.

---

## cn=sudo subtree

The LDAP container in FreeIPA 389-DS where all sudo rules are stored. Each rule is a child entry with DN cn=<rulename>,cn=sudo,dc=<realm>. This subtree is replicated to all IPA replicas as part of standard DIT replication.

## ipaSudoRule objectClass

FreeIPA LDAP objectClass that extends sudoRole with DN-based membership attributes (memberUser, memberHost, memberAllowCmd, memberDenyCmd). It allows referencing IPA group and host-group objects by DN rather than flat string, enabling dynamic group membership resolution.

## sudoRole objectClass

The standard LDAP objectClass from the sudoers LDAP schema (RFC 4876). Defines flat string attributes like sudoUser, sudoHost, sudoCommand. FreeIPA entries carry both ipaSudoRule and sudoRole so they are readable by generic LDAP sudo clients, though those clients miss DN-based group expansions.

## SSSD sudo provider ipa

The SSSD backend activated by sudo_provider=ipa in sssd.conf. It retrieves sudo rules from the IPA LDAP server, resolves DN-based group memberships through IPA indexes, and stores flattened rules in the local sysdb SQLite cache. Required for correct IPA host-group and user-group scoping.

## SSSD sudo provider ldap

The generic SSSD backend for sudo that reads cn=sudo with plain LDAP searches. It cannot traverse IPA DN-based group membership, so rules scoped to IPA host groups or user groups are silently skipped when this provider is used against an IPA server.

## SSSD sysdb sudo cache

A local SQLite database at /var/lib/sss/db/cache_<domain>.ldb that stores sudo rules retrieved from the IPA server. SSSD performs smart refreshes for expiring rules and full refreshes on a longer cycle. All sudo enforcement uses this cache, providing policy continuity during IPA outages.

## ipaSudoCmdGrp

A FreeIPA-specific LDAP objectClass for command groups. Administrators collect related commands into a named group, then reference the group DN in a rule memberAllowCmd or memberDenyCmd attribute. Enables command policy reuse across multiple rules; absent from RFC 4876 sudoers LDAP schema.

## IPA external group

An IPA group with objectClass ipaExternalGroup that holds foreign SIDs (Active Directory users or groups) as members. AD identities are mapped into IPA external groups, which are nested inside IPA POSIX groups used in sudo rules -- the only supported path for granting AD-sourced users FreeIPA sudo access.

## nsswitch sudoers entry

The sudoers: line in /etc/nsswitch.conf that controls the order sudo searches rule sources. Common values: files sss (local first, then SSSD) or sss files (SSSD first). The default files-first ordering allows local /etc/sudoers to shadow centrally managed LDAP rules.

## sudoOrder

An integer attribute on sudoRole entries influencing evaluation ordering when multiple rules match. Lower integers are evaluated first. FreeIPA exposes this attribute in the IPA CLI (ipa sudorule-add --sudoorder) and Web UI.

---

*Back to: [investigation.md](investigation.md)*
