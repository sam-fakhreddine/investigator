#!/usr/bin/env python3
"""
post_tool_use.py — PostToolUse hook: JSON write validator.

Fires after every tool call. When a Write or Edit tool writes investigation.json,
runs check_sync.py against the investigation directory. If the markdown is out of
sync with the JSON, exits 2 with a message telling the agent to re-run json_to_md.py.

Exit codes:
  0 — pass (either not a relevant tool call, or sync check passed)
  2 — block with feedback (sync check failed; message explains what drifted)

Stdin: JSON object with at least:
  {
    "tool_name": "Write" | "Edit" | ...,
    "tool_input": { "file_path": "..." }
  }
"""

import json
import subprocess
import sys
from pathlib import Path

_HOOKS_DIR = Path(__file__).resolve().parent
_REPO_ROOT  = _HOOKS_DIR.parent.parent
_CHECK_SYNC = _REPO_ROOT / "scripts" / "check_sync.py"
_JSON_TO_MD = _REPO_ROOT / "scripts" / "json_to_md.py"


def main() -> None:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)
        event = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if not isinstance(event, dict):
        sys.exit(0)

    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})

    if not isinstance(tool_input, dict):
        sys.exit(0)

    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if not file_path:
        sys.exit(0)

    file_path = Path(str(file_path))
    if file_path.name != "investigation.json":
        sys.exit(0)

    investigation_dir = file_path.parent

    md_path = investigation_dir / "investigation.md"
    if not md_path.exists():
        sys.exit(0)

    try:
        result = subprocess.run(
            [sys.executable, str(_CHECK_SYNC), str(investigation_dir)],
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        print(f"[post_tool_use] WARNING: could not run check_sync.py — {exc}", file=sys.stderr)
        sys.exit(0)

    if result.returncode == 0:
        sys.exit(0)

    check_output = (result.stdout or "").strip()
    error_output = (result.stderr or "").strip()

    lines = [
        "investigation.json was written but the markdown is OUT OF SYNC with the JSON.",
        "",
        "You must re-run the markdown generator before continuing:",
        f"  python3 scripts/json_to_md.py {investigation_dir}",
        "",
        "Then confirm sync passes:",
        f"  python3 scripts/check_sync.py {investigation_dir}",
        "",
    ]

    if check_output:
        lines += ["Sync check output:", check_output, ""]

    if error_output:
        lines += ["Stderr:", error_output, ""]

    print("\n".join(lines))
    sys.exit(2)


if __name__ == "__main__":
    main()
