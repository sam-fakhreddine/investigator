# Investigation: FreeIPA / Red Hat IDM Centralized Sudoers Management

**Date:** 2026-03-17
**Status:** Complete

---

## Question

> How does FreeIPA / Red Hat IDM centralize sudoers management for Linux hosts, and what is the architecture and data flow for distributing sudo policy to SSSD-joined hosts?

---

## Context

Organizations running Red Hat Enterprise Linux or CentOS/Alma/Rocky Linux fleets often use FreeIPA (upstream) or Red Hat IDM (downstream) to replace /etc/sudoers with centrally managed rules stored in LDAP. SSSD on each host retrieves and enforces these rules locally. A secondary concern is whether AD-sourced users (via FreeIPA cross-forest trust) can also receive FreeIPA-managed sudo rules.

---

## FreeIPA Sudo Rule Scoping Attributes

| Attribute (LDAP) | Object Class | Purpose | Multivalued |
| --- | --- | --- | --- |
| cn | sudoRole | Rule name / DN component | No |
| sudoUser | sudoRole | Target users or groups (%, +group syntax) | Yes |
| sudoHost | sudoRole | Target hostnames, IP ranges, or IPA host groups | Yes |
| sudoCommand | sudoRole | Commands allowed or denied (ALL, negation with !) | Yes |
| sudoRunAsUser | sudoRole | User to run as (default root) | Yes |
| sudoRunAsGroup | sudoRole | Group to run as | Yes |
| sudoOption | sudoRole | Options equivalent to Defaults tags (NOPASSWD, etc.) | Yes |
| sudoOrder | sudoRole | Integer ordering for rule precedence | No |
| sudoNotBefore / sudoNotAfter | sudoRole | Time-boxed rule validity window | No |
| memberHost (IPA) | ipaSudoRule | IPA host group DN references (IPA-native) | Yes |
| memberUser (IPA) | ipaSudoRule | IPA user/group DN references (IPA-native) | Yes |

> FreeIPA stores rules under cn=sudo,dc=<realm>. The ipaSudoRule objectClass extends sudoRole with DN-based membership. SSSD resolves these DN references at query time and caches flattened results locally.

---

## Key Findings

- FreeIPA stores sudo policy in its 389-DS LDAP directory under cn=sudo,dc=<realm> using a dual-objectclass model: each rule carries both ipaSudoRule (IPA-native DN-linked membership) and sudoRole (RFC 4876 sudoers LDAP schema compatibility).
- The SSSD sudo provider for IPA-joined hosts (id_provider=ipa, sudo_provider=ipa) queries the IPA server and resolves group memberships through IPA LDAP indexes, then caches flattened sudoRole objects in the SSSD sysdb SQLite database under /var/lib/sss/db/.
- SSSD maintains a local SQLite cache of sudo rules and refreshes it on a configurable schedule (smart refresh default 15 minutes for expiring entries, full refresh default 6 hours); sudo decisions are made against this cache, so enforcement continues when the IPA server is unreachable.
- The IPA sudo provider is distinct from the generic LDAP sudo provider: the LDAP provider reads the cn=sudo subtree with plain LDAP searches and cannot resolve IPA DN-based group memberships (ipaSudoRule memberUser/memberHost), causing group-scoped rules to silently not apply.
- Sudo rule scoping in FreeIPA is three-dimensional: rules are scoped to users or IPA user groups (sudoUser / memberUser), to hostnames, IP ranges, or IPA host groups (sudoHost / memberHost), and to commands or IPA command groups (sudoCommand / memberAllowCmd / memberDenyCmd).
- FreeIPA supports a command-group abstraction (ipaSudoCmdGrp) that lets administrators collect commands into named groups referenced by DN in a rule; this is a FreeIPA extension absent from the base sudoers LDAP RFC 4876 schema.
- When FreeIPA establishes a cross-forest trust with Active Directory, AD users can receive FreeIPA sudo rules only if their AD identity is mapped into an IPA external group (containing AD SIDs) that is nested into an IPA POSIX group referenced in the sudo rule.
- SSSD sudo_provider=ipa sends LDAP searches to the IPA server filtered by the host FQDN and its host group memberships, retrieving only rules applicable to that host and limiting local cache size on large deployments.
- The sudoOrder attribute provides integer-based rule ordering; FreeIPA conflict resolution follows the sudoers LDAP model where DENY rules (! prefix on sudoCommand) take precedence within a rule, not globally across rules -- differing from classic /etc/sudoers first-match-wins line semantics.
- Local /etc/sudoers and /etc/sudoers.d/ entries coexist with LDAP-sourced rules; the nsswitch.conf sudoers entry controls source ordering, and the default files-first ordering means local entries silently override centrally managed policy.
- Red Hat IDM ipa-client-install automatically writes the correct sssd.conf sudo stanza on enrolled hosts; manual sssd.conf configuration is only required for non-IPA-enrolled hosts using the generic LDAP sudo provider against an IPA LDAP backend.
- SSSD logs sudo provider activity to /var/log/sssd/sssd_sudo.log, which can be used to trace rule evaluation and diagnose policy mismatches without requiring an actual sudo attempt.

---

## Concepts & Entities

| Concept | Description |
|---------|-------------|
| cn=sudo subtree | The LDAP container in FreeIPA 389-DS where all sudo rules are stored. Each rule is a child entry with DN cn=<rulename>,cn=sudo,dc=<realm>. This subtree is replicated to all IPA replicas as part of standard DIT replication. |
| ipaSudoRule objectClass | FreeIPA LDAP objectClass that extends sudoRole with DN-based membership attributes (memberUser, memberHost, memberAllowCmd, memberDenyCmd). It allows referencing IPA group and host-group objects by DN rather than flat string, enabling dynamic group membership resolution. |
| sudoRole objectClass | The standard LDAP objectClass from the sudoers LDAP schema (RFC 4876). Defines flat string attributes like sudoUser, sudoHost, sudoCommand. FreeIPA entries carry both ipaSudoRule and sudoRole so they are readable by generic LDAP sudo clients, though those clients miss DN-based group expansions. |
| SSSD sudo provider ipa | The SSSD backend activated by sudo_provider=ipa in sssd.conf. It retrieves sudo rules from the IPA LDAP server, resolves DN-based group memberships through IPA indexes, and stores flattened rules in the local sysdb SQLite cache. Required for correct IPA host-group and user-group scoping. |
| SSSD sudo provider ldap | The generic SSSD backend for sudo that reads cn=sudo with plain LDAP searches. It cannot traverse IPA DN-based group membership, so rules scoped to IPA host groups or user groups are silently skipped when this provider is used against an IPA server. |
| SSSD sysdb sudo cache | A local SQLite database at /var/lib/sss/db/cache_<domain>.ldb that stores sudo rules retrieved from the IPA server. SSSD performs smart refreshes for expiring rules and full refreshes on a longer cycle. All sudo enforcement uses this cache, providing policy continuity during IPA outages. |
| ipaSudoCmdGrp | A FreeIPA-specific LDAP objectClass for command groups. Administrators collect related commands into a named group, then reference the group DN in a rule memberAllowCmd or memberDenyCmd attribute. Enables command policy reuse across multiple rules; absent from RFC 4876 sudoers LDAP schema. |
| IPA external group | An IPA group with objectClass ipaExternalGroup that holds foreign SIDs (Active Directory users or groups) as members. AD identities are mapped into IPA external groups, which are nested inside IPA POSIX groups used in sudo rules -- the only supported path for granting AD-sourced users FreeIPA sudo access. |
| nsswitch sudoers entry | The sudoers: line in /etc/nsswitch.conf that controls the order sudo searches rule sources. Common values: files sss (local first, then SSSD) or sss files (SSSD first). The default files-first ordering allows local /etc/sudoers to shadow centrally managed LDAP rules. |
| sudoOrder | An integer attribute on sudoRole entries influencing evaluation ordering when multiple rules match. Lower integers are evaluated first. FreeIPA exposes this attribute in the IPA CLI (ipa sudorule-add --sudoorder) and Web UI. |

---

## Tensions & Tradeoffs

- The IPA sudo provider and the generic LDAP sudo provider both target cn=sudo but only the IPA provider resolves DN-based group memberships; misconfiguring sudo_provider=ldap on an IPA-joined host produces no error but silently drops all group-scoped rules.
- Local /etc/sudoers is evaluated before SSSD by default (nsswitch sudoers: files sss), so a stale or overly permissive local sudoers file silently overrides centrally managed policy; full centralization requires inverting the nsswitch order or purging local sudoers.
- FreeIPA sudo rules use the sudoRole LDAP schema for wire compatibility, but the ipaSudoRule DN-based extensions are not part of RFC 4876 -- non-SSSD sudo LDAP clients (sudo built with --with-ldap) see only flat sudoRole attributes and miss group-expanded memberships.
- AD-sourced users can receive FreeIPA sudo rules only via the IPA external group indirection (AD SID -> IPA external group -> IPA POSIX group -> sudo rule); AD group changes do not automatically propagate to sudo policy until IPA group membership is also updated.
- SSSD sudo cache provides offline resilience but creates a policy-enforcement lag window: a deleted or modified rule may remain active on cached hosts until the next full refresh cycle (up to 6 hours by default).
- FreeIPA sudoOrder-based precedence differs from classic /etc/sudoers first-match-wins line semantics; administrators migrating from local sudoers must re-examine rule ordering logic to avoid unintended effective permissions.

---

## Open Questions

- What is the exact LDAP search filter SSSD IPA sudo provider sends to 389-DS, and does it perform server-side group expansion or client-side DN traversal?
- How does SSSD handle deeply nested IPA group membership in sudo rule resolution -- is there a documented recursion depth cap?
- Can sudoNotBefore/sudoNotAfter time-boxed rules be relied upon given SSSD cache refresh schedule -- can a time-expired rule remain cached and active past its intended end time?
- Is there an officially supported integration path for non-RHEL/non-Fedora distributions (Debian, Ubuntu) to use the IPA sudo provider, or does it require packages from non-native sources?
- What is the exact sudo behavior when the IPA server is unreachable and the local sysdb cache has fully expired -- does sudo fail open or fail closed?
- Does FreeIPA sudo rule model support RunAs group references as IPA group DNs via ipaSudoRule, or only flat group names per the sudoRole schema?
- Does sssctl support a sudo-check subcommand for pre-flight sudo policy verification without an actual sudo invocation, and if so, what is the documented syntax and which SSSD version introduced it?

---

## Sources & References

- [Red Hat Enterprise Linux 8: Configuring sudo rules in IdM](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_identity_management/configuring-sudo-rules-in-idm_configuring-and-managing-idm)
- [Red Hat Enterprise Linux 9: Configuring sudo rules in IdM](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_idm_users_groups_hosts_and_access_control_rules/configuring-sudo-rules-in-idm_managing-idm-users-groups-hosts-and-access-control-rules)
- [SSSD Documentation: sudo integration](https://sssd.io/docs/users/sudo_integration.html)
- [FreeIPA Design: Sudo integration (V3)](https://www.freeipa.org/page/V3/Sudo_Integration)
- [RFC 4876: A Configuration Profile Schema for LDAP-Based Agents](https://www.rfc-editor.org/rfc/rfc4876)
- [Red Hat IDM: Planning a cross-forest trust between IdM and AD](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/planning_identity_management/planning-a-cross-forest-trust-between-idm-and-ad_planning-identity-management)
- [FreeIPA: Active Directory trust setup](https://www.freeipa.org/page/Active_Directory_trust_setup)
- [sssd-sudo(5) Linux man page](https://linux.die.net/man/5/sssd-sudo)
- [FreeIPA: Howto - sudo with LDAP](https://www.freeipa.org/page/Howto/Sudo)
