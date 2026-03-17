# Validation Report: FreeIPA / Red Hat IDM Centralized Sudoers Management
Date: 2026-03-17
Validator: Fact Validation Agent

## Summary
- Total sources checked: 9
- Verified: 7 | Redirected: 1 | Dead: 0 | Unverifiable: 1
- Findings checked: 12
- Confirmed: 10 | Partially confirmed: 0 | Unverified: 1 | Contradicted: 1
- JSON/MD sync issues: 0
- Items requiring remediation: 3

## JSON/MD Sync Check

```
check_sync.py: IN_SYNC — all generated files match investigation.json
```

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Red Hat Enterprise Linux 8: Configuring sudo rules in IdM | https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/... | REDIRECT | Content migrated to docs.redhat.com; update URL |
| 2 | Red Hat Enterprise Linux 9: Configuring sudo rules in IdM | https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/... | VERIFIED | Resolves and matches title |
| 3 | SSSD Documentation: sudo integration | https://sssd.io/docs/users/sudo_integration.html | UNVERIFIABLE | Path not confirmed via search |
| 4 | FreeIPA Design: Sudo integration (V3) | https://www.freeipa.org/page/V3/Sudo_Integration | VERIFIED | Resolves, content confirmed |
| 5 | RFC 4876: A Configuration Profile Schema for LDAP-Based Administration | https://www.rfc-editor.org/rfc/rfc4876 | VERIFIED | Title incorrect: RFC 4876 actual title is "LDAP-Based Agents" not "LDAP-Based Administration" |
| 6 | Red Hat IDM: Planning a cross-forest trust between IdM and AD | https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/... | VERIFIED | Resolves and matches title |
| 7 | FreeIPA: Active Directory trust setup | https://www.freeipa.org/page/Active_Directory_trust_setup | VERIFIED | Resolves and matches title |
| 8 | sssd-sudo(5) Linux man page | https://linux.die.net/man/5/sssd-sudo | VERIFIED | Resolves and matches title |
| 9 | FreeIPA: Howto - sudo with LDAP | https://www.freeipa.org/page/Howto/Sudo | VERIFIED | Resolves and matches title |

## Finding Verification

### Finding 1: FreeIPA dual-objectclass sudo storage
- **Claim:** FreeIPA stores sudo policy in 389-DS under cn=sudo,dc=realm using dual-objectclass model (ipaSudoRule + sudoRole)
- **Verdict:** CONFIRMED
- **Evidence:** Documented in FreeIPA V3/Sudo_Integration design page and RHEL 9 IdM sudo docs
- **Source used:** https://www.freeipa.org/page/V3/Sudo_Integration

### Finding 2: SSSD IPA sudo provider caches flattened rules in sysdb
- **Claim:** SSSD sudo_provider=ipa caches flattened sudoRole objects in /var/lib/sss/db/
- **Verdict:** CONFIRMED
- **Evidence:** Confirmed in sssd-sudo(5) man page
- **Source used:** https://linux.die.net/man/5/sssd-sudo

### Finding 3: SSSD sudo cache refresh timing
- **Claim:** Smart refresh default ~90 seconds, full refresh default ~3 hours
- **Verdict:** CONTRADICTED
- **Evidence:** Default smart refresh is 15 minutes (not 90 seconds); default full refresh is 6 hours (not 3 hours) per sssd-sudo(5). The 90-second figure appears in no official source. Error propagates into tension 5 and both audience briefs.
- **Source used:** https://linux.die.net/man/5/sssd-sudo

### Finding 4: IPA vs LDAP sudo provider distinction
- **Claim:** LDAP provider cannot resolve IPA DN-based group memberships, causing group-scoped rules to silently not apply
- **Verdict:** CONFIRMED
- **Evidence:** Confirmed in RHEL IdM and FreeIPA design documentation
- **Source used:** https://www.freeipa.org/page/V3/Sudo_Integration

### Finding 5: Three-dimensional rule scoping
- **Claim:** Rules scoped to users/groups, hostnames/host-groups, commands/command-groups
- **Verdict:** CONFIRMED
- **Evidence:** Documented in RHEL 9 sudo rules in IdM and sssd-sudo(5)
- **Source used:** https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/...

### Finding 6: ipaSudoCmdGrp command-group abstraction
- **Claim:** FreeIPA-specific command groups (ipaSudoCmdGrp) absent from RFC 4876
- **Verdict:** CONFIRMED
- **Evidence:** RFC 4876 confirmed; ipaSudoCmdGrp is a FreeIPA extension
- **Source used:** https://www.rfc-editor.org/rfc/rfc4876

### Finding 7: AD users via IPA external group indirection
- **Claim:** AD users reach FreeIPA sudo rules via AD SID to IPA external group to IPA POSIX group to sudo rule
- **Verdict:** CONFIRMED
- **Evidence:** Confirmed in Red Hat IDM AD trust planning documentation
- **Source used:** https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/...planning-a-cross-forest-trust

### Finding 8: SSSD IPA sudo provider host-filtered queries
- **Claim:** SSSD IPA sudo provider sends LDAP searches filtered by host FQDN and host group memberships
- **Verdict:** CONFIRMED
- **Evidence:** Documented in sssd-sudo(5)
- **Source used:** https://linux.die.net/man/5/sssd-sudo

### Finding 9: sudoOrder precedence and DENY semantics
- **Claim:** sudoOrder provides integer rule ordering; DENY takes precedence within a rule, not globally
- **Verdict:** CONFIRMED
- **Evidence:** Confirmed in sudoers LDAP schema docs and FreeIPA Howto/Sudo
- **Source used:** https://www.freeipa.org/page/Howto/Sudo

### Finding 10: nsswitch sudoers ordering shadows LDAP
- **Claim:** Default files-first nsswitch ordering allows local /etc/sudoers to shadow centrally managed policy
- **Verdict:** CONFIRMED
- **Evidence:** Standard nsswitch.conf sudo behavior; confirmed by SSSD documentation
- **Source used:** https://linux.die.net/man/5/sssd-sudo

### Finding 11: ipa-client-install auto-configures sudo stanza
- **Claim:** Red Hat IDM ipa-client-install automatically writes correct sssd.conf sudo stanza
- **Verdict:** CONFIRMED
- **Evidence:** Confirmed in RHEL IdM documentation
- **Source used:** https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/...

### Finding 12: sssctl sudo-check command
- **Claim:** sssctl exposes sudo rule tracing via "sssctl sudo-check user command on host"
- **Verdict:** UNVERIFIED
- **Evidence:** sssctl is documented but the specific "sudo-check" subcommand with "on host" syntax was not confirmed in official documentation.
- **Source used:** WebSearch — no primary source found for this specific subcommand

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 3: cache refresh timing | CONTRADICTED | Correct smart refresh to 15 minutes and full refresh to 6 hours; propagate into tension 5 and both audience briefs |
| Source 1: RHEL 8 URL | REDIRECT | Update to resolved docs.redhat.com URL |
| Source 5: RFC 4876 title | REDIRECT | Correct title to "RFC 4876: A Configuration Profile Schema for LDAP-Based Agents" |
| Finding 12: sssctl sudo-check | UNVERIFIED | Move to open_questions or replace with verified documentation |

## Overall Assessment
10 of 12 findings are confirmed by primary sources. One significant factual error: sudo cache refresh timing values are wrong by large margins (90 seconds vs 15 minutes smart refresh; 3 hours vs 6 hours full refresh), propagating into tensions and audience briefs. After correction of the cache timing error and Finding 12 disposition, the investigation will be trustworthy for engineering and leadership decisions.
