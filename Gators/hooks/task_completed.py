#!/usr/bin/env python3
"""
task_completed.py — TaskCompleted hook: validation gate.

Fires when a task is being marked complete. For the 'validate' task, reads
validation_report.md from the investigation directory and checks for any
CONTRADICTED verdicts. If found, exits 2 with a list of the contradicted
items so the investigation agent can be re-opened with specific corrections.

Exit codes:
  0 — pass (either not the validate task, or no CONTRADICTED verdicts found)
  2 — block with feedback (CONTRADICTED findings must be corrected first)

Stdin: JSON object with at least:
  {
    "task_id": "validate",
    "investigation_dir": "/abs/path/to/InvestigationDir"
  }

The "investigation_dir" key is the primary source for the directory path.
If absent or the validation_report.md cannot be read, the hook exits 0 —
it fails open rather than permanently blocking on missing context.
"""

import json
import re
import sys
from pathlib import Path

_RE_CONTRADICTED = re.compile(r'\bCONTRADICTED\b')

_RE_UNVERIFIED = re.compile(r'\bUNVERIFIED\b')


def _extract_verdict_lines(text: str, pattern: re.Pattern) -> list[str]:
    """Return stripped lines from text that match pattern."""
    return [line.strip() for line in text.splitlines() if pattern.search(line)]


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

    task_id = (event.get("task_id") or event.get("task") or "").strip().lower()
    if task_id != "validate":
        sys.exit(0)

    raw_dir = event.get("investigation_dir") or event.get("investigation_directory") or ""
    if not raw_dir:
        sys.exit(0)

    investigation_dir = Path(str(raw_dir))
    report_path = investigation_dir / "validation_report.md"

    if not report_path.exists():
        sys.exit(0)

    try:
        report_text = report_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(
            f"[task_completed] WARNING: could not read {report_path} — {exc}",
            file=sys.stderr,
        )
        sys.exit(0)

    contradicted_lines = _extract_verdict_lines(report_text, _RE_CONTRADICTED)
    unverified_lines   = _extract_verdict_lines(report_text, _RE_UNVERIFIED)

    if not contradicted_lines:
        sys.exit(0)

    lines = [
        "Validation found CONTRADICTED findings.",
        "The investigate task must be reopened with these corrections:",
        "",
    ]

    for item in contradicted_lines:
        lines.append(f"  - {item}")

    lines += [
        "",
        "Remediation steps (per CLAUDE.md):",
        "  1. Re-spawn the investigation agent with the specific CONTRADICTED claim",
        "     and the contradicting evidence from the validation report.",
        "  2. Agent corrects only the affected sections in investigation.json.",
        f"  3. Re-run: python3 scripts/json_to_md.py {investigation_dir}",
        f"  4. Re-run: python3 scripts/check_sync.py {investigation_dir}  # must exit 0",
        "  5. Re-spawn the validation agent and confirm no CONTRADICTED verdicts remain.",
        "",
    ]

    if unverified_lines:
        lines += [
            "Additionally, the following UNVERIFIED verdicts were found.",
            "Material claims must be corrected or downgraded to open questions.",
            "Minor / peripheral claims may be noted in open_questions and left as-is.",
            "",
        ]
        for item in unverified_lines:
            lines.append(f"  - {item}")
        lines.append("")

    print("\n".join(lines))
    sys.exit(2)


if __name__ == "__main__":
    main()
