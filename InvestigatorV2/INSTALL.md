# InvestigatorV2 — Installation Guide

Step-by-step instructions to activate InvestigatorV2 agent teams in an existing Investigator repo.
After completing these steps the `/gator` skill will orchestrate a two-teammate investigation team (investigator + validator) instead of running sequentially in the main session.

Prerequisites: Claude Code installed, Python 3.10+, an existing Investigator repo with `scripts/` and `templates/` in place.

---

## Step 1 — Enable agent teams

Agent teams are disabled by default and require an environment variable to activate.

Open `.claude/settings.local.json` and add the `env` block. If the file already has an `env` key, add the entry inside it rather than creating a second `env` block.

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

The full diff to merge is in `InvestigatorV2/settings-patch.json`. The simplest way to apply it without losing existing settings is to open the file in an editor and copy the two top-level keys (`env`, `hooks`) into your existing JSON.

Do not replace the entire `settings.local.json` — the file already contains `permissions.allow` entries that must be preserved.

---

## Step 2 — Set the teammate display mode

Teammate display mode is set via the `--teammate-mode` CLI flag rather than `settings.local.json`. Pass it when starting Claude Code:

```bash
# In-process mode (all teammates in the same terminal window)
claude --teammate-mode=in-process

# tmux mode (each teammate in its own split pane — requires tmux)
claude --teammate-mode=tmux
```

`in-process` works in any terminal without additional software. Use Shift+Down to cycle between the lead and active teammates.

`tmux` requires `tmux` installed (`brew install tmux` on macOS) and does not work in VS Code's integrated terminal, Windows Terminal, or Ghostty.

If you always want in-process mode without specifying the flag, create a shell alias:

```bash
alias claude='claude --teammate-mode=in-process'
```

---

## Step 3 — Register the hooks

The three hooks enforce pipeline quality gates automatically:

| Hook | File | When it fires | What it does |
|------|------|---------------|--------------|
| `PostToolUse` | `InvestigatorV2/hooks/post_tool_use.py` | After any Write or Edit tool call | Checks that `investigation.json` and `investigation.md` are in sync; exits 2 and blocks if they have drifted |
| `TeammateIdle` | `InvestigatorV2/hooks/teammate_idle.py` | When a teammate is about to go idle | Checks whether the teammate's assigned task is complete and all required output files exist; exits 2 with feedback if the teammate stopped early |
| `TaskCompleted` | `InvestigatorV2/hooks/task_completed.py` | When a task is being marked complete | Enforces quality gates (sync check, required files, validation report present) before allowing the task to close |

Add the `hooks` block to `.claude/settings.local.json`. The exact JSON is in `InvestigatorV2/settings-patch.json` under the `"hooks"` key:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 InvestigatorV2/hooks/post_tool_use.py"
          }
        ]
      }
    ],
    "TeammateIdle": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 InvestigatorV2/hooks/teammate_idle.py"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 InvestigatorV2/hooks/task_completed.py"
          }
        ]
      }
    ]
  }
}
```

Important: all commands are relative to the repo root. Claude Code resolves hook commands from the project's working directory, so `InvestigatorV2/hooks/post_tool_use.py` is correct as written — do not use absolute paths or `./` prefixes.

`TeammateIdle` and `TaskCompleted` do not support matchers. Any `matcher` field added to those events is silently ignored by Claude Code.

After editing the settings file, Claude Code does not pick up hook changes mid-session. Start a fresh Claude Code session for the hooks to take effect.

---

## Step 4 — Install the `/gator` skill

Skills live in `.claude/skills/`. Create the directory if it does not exist, then copy the skill file:

```bash
mkdir -p /Users/samfakhreddine/repos/research/.claude/skills
cp InvestigatorV2/SKILL.md .claude/skills/gator.md
```

The skill file tells Claude Code how to respond to `/gator <question>`. It instructs the lead to:
1. Run the scope gate
2. Create the investigation folder
3. Create the task list with `investigate` and `validate` (validate depends on investigate)
4. Spawn two teammates — one investigator, one validator — and assign tasks
5. Monitor progress and apply remediation if the validator returns `CONTRADICTED` or material `UNVERIFIED` verdicts
6. Synthesize findings for the user once both tasks are complete and `validation_report.md` is present

The skill source is `InvestigatorV2/SKILL.md`. It is installed as `gator.md` under `.claude/skills/` — the filename (without `.md`) becomes the slash command name.

---

## Step 5 — Verify the setup

Run each check in sequence. All three must pass before running a real investigation.

### 5a — Confirm agent teams are enabled

Start a fresh Claude Code session in the repo root and run:

```
/status
```

The status output should show `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in the environment. If it is absent, confirm the `env` block was added to `.claude/settings.local.json` and that you started a new session after saving.

### 5b — Confirm hooks are registered

Type `/hooks` in Claude Code. You should see three entries:

- `PostToolUse` — matcher `Write|Edit` — `python3 InvestigatorV2/hooks/post_tool_use.py`
- `TeammateIdle` — no matcher — `python3 InvestigatorV2/hooks/teammate_idle.py`
- `TaskCompleted` — no matcher — `python3 InvestigatorV2/hooks/task_completed.py`

If a hook is missing, check that the `hooks` block in `settings.local.json` is valid JSON (no trailing commas, balanced braces) and restart the session.

### 5c — Smoke-test the PostToolUse hook

Trigger the hook manually by writing a test JSON file and then verifying the hook catches drift:

```bash
# Write a valid investigation.json with no matching investigation.md
echo '{"topic":"Test","date":"2026-02-27","status":"in_progress","question":"Test?","context":"Test.","key_findings":[],"concepts":[],"tensions":[],"open_questions":[],"sources":[]}' \
  > /tmp/test_hook_investigation.json
```

Then run the hook script directly:

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/test_hook_investigation.json"}}' \
  | python3 InvestigatorV2/hooks/post_tool_use.py
echo "Exit code: $?"
```

Expected: exit code 0 (no `investigation.md` present means the hook skips the check). This confirms the hook runs without errors. A real drift detection test requires a paired `investigation.md` and a modified `investigation.json`.

### 5d — Confirm the skill loads

Type `/gator` in Claude Code. Claude should recognize the command and start the scope gate questions. If it does not, confirm `.claude/skills/gator.md` exists and that the skill frontmatter is correct.

---

## Known limitations

These are documented limitations of Claude Code agent teams as of February 2026. They are inherent to the platform and not specific to InvestigatorV2.

**No session resumption with in-process teammates.** If you use `/resume` or `/rewind` to restore a session, in-process teammates are not restored. The lead may attempt to message teammates that no longer exist. If this happens, tell the lead to spawn replacement teammates.

**Task status can lag.** Teammates sometimes fail to mark tasks as completed, which blocks dependent tasks from becoming available. If `task-002` (validate) appears stuck as `pending` even though `task-001` (investigate) is clearly done, tell the lead to check task status and update it manually or nudge the investigator teammate to re-mark the task complete.

**One team per session.** A lead can only manage one active team at a time. If you need to run a second investigation in parallel, open a second Claude Code session in the same repo. Clean up the first team before starting a second one in the same session (`Clean up the team`).

**No nested teams.** Teammates cannot spawn their own teams or sub-teammates. Only the lead manages the team. InvestigatorV2's two-teammate structure (investigator + validator) stays flat by design.

**Hook changes require a session restart.** Claude Code captures a snapshot of hooks at startup. If you edit `settings.local.json` during a session, the new hooks will not fire until you start a fresh session. Claude Code will warn you and require review in `/hooks` before changes apply.

**Shutdown can be slow.** When you ask a teammate to shut down, it finishes its current tool call or request first. During an active investigation this can take several minutes. Wait for both teammates to go idle before issuing a cleanup.

**Permissions set at spawn.** All teammates start with the lead's permission mode. If the lead requires permission approvals for certain tools, teammates will too. Pre-approve common operations in `settings.local.json` before spawning to reduce interruptions during investigation.

---

## Troubleshooting quick reference

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Teammates not appearing after `/gator` | Agent teams not enabled or wrong session | Confirm `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `/status`, restart session |
| Hooks not firing | Settings edited mid-session | Restart Claude Code session |
| `task-002` stuck as pending | Teammate failed to mark `task-001` complete | Tell lead: "Check task-001 status and mark it complete if the investigation files are present" |
| PostToolUse hook exits 2 unexpectedly | `investigation.md` not regenerated after JSON edit | Run `python3 scripts/json_to_md.py <investigation_dir>` |
| `/gator` not recognized | Skill file missing or bad frontmatter | Confirm `.claude/skills/gator.md` exists and frontmatter is valid YAML |
| Split panes not working | tmux not installed or wrong terminal | Use `"in-process"` mode or install tmux via `brew install tmux` |
