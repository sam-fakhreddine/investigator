#!/usr/bin/env python3
"""
json_to_md.py — generates markdown files from investigation.json.

Agents write investigation.json only. This script produces all markdown.
Eliminates JSON/MD drift entirely — markdown is always derived, never authored.

Files produced (when data is present):
  investigation.md      — full engineering view
  brief_leadership.md   — engineering leadership brief (requires audience_briefs.engineering_leadership)
  brief_po.md           — product owner / PM / EM brief (requires audience_briefs.product_owner)
  glossary.md           — term definitions derived from concepts list

Usage:  python3 json_to_md.py <investigation_dir>
        python3 json_to_md.py <investigation_dir> --dry-run   (print to stdout, no write)
Exit:   0 = success, 2 = error
"""

import sys
import json
import os
import re
import tempfile
from pathlib import Path
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent))
from models import Investigation


REQUIRED_FIELDS = ('topic', 'date', 'status', 'question', 'context')

RISK_LABELS = {
    'Low':      'LOW',
    'Medium':   'MEDIUM',
    'High':     'HIGH',
    'Critical': 'CRITICAL',
}

_SAFE_URL_SCHEMES = {'https', 'http'}



def safe_url(url: str) -> str:
    """Return url if scheme is http/https; return empty string otherwise."""
    if not url:
        return ''
    scheme = url.split(':', 1)[0].lower()
    return url if scheme in _SAFE_URL_SCHEMES else ''


def safe_blockquote(text: str) -> str:
    """Render text as a Markdown blockquote, safe for multi-line values."""
    if not text:
        return '>'
    return '\n'.join(f'> {line}' for line in str(text).splitlines())


def safe_table_cell(value: str) -> str:
    """Escape pipes and collapse newlines for use inside a Markdown table cell."""
    return str(value).replace('\n', ' ').replace('|', '\\|')


def safe_list_item(value: str) -> str:
    """Collapse newlines in a Markdown list item value."""
    return str(value).replace('\n', ' ')


def safe_heading(value: str) -> str:
    """Strip newlines and leading # chars to prevent heading injection."""
    return str(value).replace('\n', ' ').lstrip('#').strip()


def _dedup_separators(text: str) -> str:
    """Collapse consecutive --- separators that result from optional block boundaries."""
    return re.sub(r'(\n---\n)+', '\n---\n', text)



def render(data: dict) -> str:
    """Generate the full engineering investigation markdown from structured data."""
    lines = [
        f"# Investigation: {data['topic']}",
        f"",
        f"**Date:** {data['date']}",
        f"**Status:** {data['status'].replace('_', ' ').title()}",
        f"",
        f"---",
        f"",
    ]

    quick_ref = data.get('quick_reference')
    if quick_ref and quick_ref.get('columns') and quick_ref.get('rows'):
        cols = quick_ref['columns']
        sep  = ['---'] * len(cols)
        lines += [
            f"## {quick_ref.get('title', 'Quick Reference')}",
            f"",
            f"| {' | '.join(safe_table_cell(str(c)) for c in cols)} |",
            f"| {' | '.join(sep)} |",
        ]
        for row in quick_ref['rows']:
            cells = [safe_table_cell(str(c)) for c in row]
            lines.append(f"| {' | '.join(cells)} |")
        if quick_ref.get('notes'):
            lines += ["", safe_blockquote(str(quick_ref['notes']))]
        lines += ["", "---", ""]

    lines += [
        f"## Question",
        f"",
        safe_blockquote(data['question']),
        f"",
        f"---",
        f"",
    ]

    lines += [
        f"## Context",
        f"",
        data['context'],
        f"",
        f"---",
        f"",
    ]

    lines += [f"## Key Findings", f""]
    for finding in data.get('key_findings', []):
        lines.append(f"- {safe_list_item(finding)}")
    lines += ["", "---", ""]

    lines += [
        f"## Concepts & Entities",
        f"",
        f"| Concept | Description |",
        f"|---------|-------------|",
    ]
    for concept in data.get('concepts', []):
        name = safe_table_cell(concept.get('name') or '')
        desc = safe_table_cell(concept.get('description') or '')
        lines.append(f"| {name} | {desc} |")
    lines += ["", "---", ""]

    lines += [f"## Tensions & Tradeoffs", f""]
    for tension in data.get('tensions', []):
        lines.append(f"- {safe_list_item(tension)}")
    lines += ["", "---", ""]

    lines += [f"## Open Questions", f""]
    for question in data.get('open_questions', []):
        lines.append(f"- {safe_list_item(question)}")
    lines += ["", "---", ""]

    lines += [f"## Sources & References", f""]
    for source in data.get('sources', []):
        title = safe_table_cell(source.get('title') or '')
        url   = safe_url(source.get('url') or '')
        if url:
            lines.append(f"- [{title}]({url})")
        else:
            lines.append(f"- {title}")
    lines.append("")

    return _dedup_separators("\n".join(lines))


def render_leadership_brief(data: dict) -> str:
    """Generate the engineering leadership brief markdown."""
    brief = data.get('audience_briefs', {}).get('engineering_leadership', {})
    topic = data['topic']
    date  = data['date']

    lines = [
        f"# {topic} — Engineering Leadership Brief",
        f"",
        f"**Date:** {date}",
        f"",
        f"---",
        f"",
    ]

    if brief.get('headline'):
        lines += [
            f"## Headline",
            f"",
            safe_blockquote(brief['headline']),
            f"",
            f"---",
            f"",
        ]

    if brief.get('so_what'):
        lines += [
            f"## So What",
            f"",
            brief['so_what'],
            f"",
            f"---",
            f"",
        ]

    bullets = brief.get('bullets', [])
    if bullets:
        lines += [f"## Key Points", f""]
        for b in bullets:
            lines.append(f"- {safe_list_item(b)}")
        lines += ["", "---", ""]

    action = brief.get('action_required')
    if action:
        lines += [
            f"## Action Required",
            f"",
            safe_blockquote(action),
            f"",
            f"---",
            f"",
        ]

    lines += [
        f"*Full engineering investigation: [investigation.md](investigation.md)*",
        f"",
    ]

    return _dedup_separators("\n".join(lines))


def render_po_brief(data: dict) -> str:
    """Generate the product owner brief markdown."""
    brief = data.get('audience_briefs', {}).get('product_owner', {})
    topic = data['topic']
    date  = data['date']
    risk  = brief.get('risk_level', '')

    lines = [
        f"# {topic} — Product Brief",
        f"",
        f"**Date:** {date}",
    ]

    if risk:
        label = RISK_LABELS.get(risk, risk.upper())
        lines.append(f"**Risk Level:** {label}")

    lines += ["", "---", ""]

    if brief.get('headline'):
        lines += [
            f"## What Is This?",
            f"",
            safe_blockquote(brief['headline']),
            f"",
            f"---",
            f"",
        ]

    if brief.get('so_what'):
        lines += [
            f"## What Does This Mean for Us?",
            f"",
            brief['so_what'],
            f"",
            f"---",
            f"",
        ]

    bullets = brief.get('bullets', [])
    if bullets:
        lines += [f"## Key Points", f""]
        for b in bullets:
            lines.append(f"- {safe_list_item(b)}")
        lines += ["", "---", ""]

    next_steps       = brief.get('next_steps', {})
    po_action        = next_steps.get('po_action')
    work_to_assign   = next_steps.get('work_to_assign', [])
    leadership_input = next_steps.get('leadership_input')

    if po_action or work_to_assign or leadership_input:
        lines += [f"## Next Steps", f""]

        if po_action:
            lines += [f"**PO/EM Decision:**", f"", safe_blockquote(po_action), f""]

        if work_to_assign:
            lines += [f"**Engineering Work Items:**"]
            for s in work_to_assign:
                lines.append(f"- {safe_list_item(s)}")
            lines.append(f"")

        if leadership_input:
            lines += [f"**Leadership Input Required:**", f"", safe_blockquote(leadership_input), f""]

        lines += ["---", ""]

    questions = brief.get('questions_to_ask_engineering', [])
    if questions:
        lines += [f"## Open Questions", f""]
        for q in questions:
            lines.append(f"- {safe_list_item(q)}")
        lines += ["", "---", ""]

    lines += [
        f"*Full investigation: [investigation.md](investigation.md) — [Glossary](glossary.md)*",
        f"",
    ]

    return _dedup_separators("\n".join(lines))


def render_glossary(data: dict) -> str:
    """Generate a glossary from the concepts section."""
    concepts = data.get('concepts', [])
    topic    = data['topic']

    if not concepts:
        return ""

    lines = [
        f"# Glossary — {topic}",
        f"",
        f"Quick definitions of key terms and concepts referenced in this investigation.",
        f"",
        f"---",
        f"",
    ]

    for concept in concepts:
        name = safe_heading(concept.get('name') or '')
        desc = concept.get('description') or ''
        lines += [
            f"## {name}",
            f"",
            f"{desc}",
            f"",
        ]

    lines += [
        f"---",
        f"",
        f"*Back to: [investigation.md](investigation.md)*",
        f"",
    ]

    return "\n".join(lines)



def write_atomic(path: Path, content: str) -> None:
    """Write content to path atomically via temp file + os.replace()."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.tmp_', suffix='.md')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as fh:
            fh.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise



def main():
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("Usage: json_to_md.py <investigation_dir> [--dry-run]")
        sys.exit(2)

    investigation_dir = Path(args[0])
    json_path = investigation_dir / "investigation.json"

    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        sys.exit(2)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: {json_path} contains invalid JSON — {exc}")
        sys.exit(2)
    except OSError as exc:
        print(f"ERROR: cannot read {json_path} — {exc}")
        sys.exit(2)

    missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
    if missing:
        print(f"ERROR: investigation.json is missing required fields: {', '.join(missing)}")
        sys.exit(2)

    try:
        Investigation.model_validate(data)
    except ValidationError as exc:
        print("ERROR: investigation.json failed schema validation:")
        for err in exc.errors():
            loc = " -> ".join(str(p) for p in err["loc"])
            print(f"  [{loc}] {err['msg']}")
        sys.exit(2)

    outputs = [("investigation.md", render(data))]

    glossary = render_glossary(data)
    if glossary:
        outputs.append(("glossary.md", glossary))

    briefs = data.get('audience_briefs', {})
    if briefs.get('engineering_leadership'):
        outputs.append(("brief_leadership.md", render_leadership_brief(data)))
    if briefs.get('product_owner'):
        outputs.append(("brief_po.md", render_po_brief(data)))

    if dry_run:
        for filename, content in outputs:
            print(f"\n{'='*60}")
            print(f"FILE: {filename}")
            print('='*60)
            print(content)
    else:
        for filename, content in outputs:
            out_path = investigation_dir / filename
            write_atomic(out_path, content)
            print(f"Written: {out_path.resolve()}")


if __name__ == "__main__":
    main()
