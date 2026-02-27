#!/usr/bin/env python3
"""
teammate_idle.py — TeammateIdle hook: investigator idle gate.

Fires when a teammate is about to go idle. For teammates whose current task
is 'investigate', verifies that investigation.json exists and that
check_sync.py passes before allowing the agent to go idle.

Exit codes:
  0 — pass (teammate may go idle)
  2 — block with feedback (investigation incomplete or out of sync)

Stdin: JSON object with at least:
  {
    "teammate": { "name": "...", "task": "investigate" | "validate" | ... },
    "investigation_dir": "/abs/path/to/InvestigationDir"
  }

The "investigation_dir" key is the primary source for the directory path.
If absent, the hook exits 0 — it cannot gate without knowing where to look.
"""

import json
import subprocess
import sys
from pathlib import Path

_HOOKS_DIR  = Path(__file__).resolve().parent
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

    teammate = event.get("teammate", {})
    if not isinstance(teammate, dict):
        sys.exit(0)

    task = (teammate.get("task") or event.get("task") or "").strip().lower()

    if task != "investigate":
        sys.exit(0)

    raw_dir = event.get("investigation_dir") or event.get("investigation_directory") or ""
    if not raw_dir:
        sys.exit(0)

    investigation_dir = Path(str(raw_dir))

    json_path = investigation_dir / "investigation.json"
    if not json_path.exists():
        print(
            "investigation.json not found. "
            f"Complete the investigation and write {json_path} before going idle.\n"
            "\n"
            "Required steps before going idle:\n"
            f"  1. Write {json_path}\n"
            f"  2. python3 scripts/json_to_md.py {investigation_dir}\n"
            f"  3. python3 scripts/check_sync.py {investigation_dir}  # must exit 0\n"
        )
        sys.exit(2)

    try:
        result = subprocess.run(
            [sys.executable, str(_CHECK_SYNC), str(investigation_dir)],
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        print(
            f"[teammate_idle] WARNING: could not run check_sync.py — {exc}",
            file=sys.stderr,
        )
        sys.exit(0)

    if result.returncode == 0:
        sys.exit(0)

    check_output = (result.stdout or "").strip()
    error_output  = (result.stderr or "").strip()

    lines = [
        "investigation.json was written but check_sync failed.",
        "Re-run scripts/json_to_md.py and fix before going idle.",
        "",
        "Required steps:",
        f"  python3 scripts/json_to_md.py {investigation_dir}",
        f"  python3 scripts/check_sync.py {investigation_dir}  # must exit 0",
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
