#!/usr/bin/env python3
"""
check_sync.py — verifies that investigation.md and investigation.json are in sync.

Extracts structured fields from both files, normalizes and hashes them,
and reports any fields where content has drifted.

Usage:  python3 check_sync.py <investigation_dir>
Exit:   0 = IN_SYNC, 1 = OUT_OF_SYNC, 2 = error
"""

import sys
import json
import re
import hashlib
from pathlib import Path



_RE_BOLD     = re.compile(r'\*{1,3}([^*]+)\*{1,3}')
_RE_CODE     = re.compile(r'`([^`]+)`')
_RE_LINK     = re.compile(r'\[([^\]]+)\]\([^)]+\)')
_RE_SPACE    = re.compile(r'\s+')
_RE_ESCAPED_PIPE = re.compile(r'\\\\?\|')
_RE_BULLET   = re.compile(r'^[-*]\s+(.+)$')
_RE_NUMBERED = re.compile(r'^\d+\.\s+(.+)$')
_RE_BOLD_PREFIX = re.compile(r'^\*\*[^*]+\*\*:\s*')
_RE_LINK_IN_LINE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
_RE_HEADING  = re.compile(r'^##\s+(.+?)\s*$', re.MULTILINE)



def normalize(text: str) -> str:
    """Strip markdown formatting, unescape pipes, and collapse whitespace."""
    text = _RE_ESCAPED_PIPE.sub('|', text)
    text = _RE_BOLD.sub(r'\1', text)
    text = _RE_CODE.sub(r'\1', text)
    text = _RE_LINK.sub(r'\1', text)
    text = _RE_SPACE.sub(' ', text)
    return text.strip()


def hash_list(items: list) -> str:
    """Canonical hash of a list — sorted so order differences do not flag as drift."""
    canonical = json.dumps(sorted(str(i) for i in items), separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def diff_lists(label: str, json_items: list, md_items: list) -> list[str]:
    """Return human-readable diff lines for items that differ between JSON and MD."""
    json_set = set(json_items)
    md_set   = set(md_items)
    lines = []
    for item in sorted(json_set - md_set):
        lines.append(f"  [{label}] in JSON, missing from MD: {item!r}")
    for item in sorted(md_set - json_set):
        lines.append(f"  [{label}] in MD, missing from JSON: {item!r}")
    return lines



def parse_sections(md: str) -> dict[str, str]:
    """
    Parse a markdown document into a dict of {heading: body} in a single pass.
    Only ## headings are extracted; body is the text up to the next ## heading.
    """
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in md.splitlines():
        m = _RE_HEADING.match(line)
        if m:
            if current_heading is not None:
                sections[current_heading] = '\n'.join(current_lines).strip()
            current_heading = m.group(1)
            current_lines = []
        else:
            if current_heading is not None:
                current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = '\n'.join(current_lines).strip()

    return sections



def extract_list_items(text: str) -> list[str]:
    """Pull bullet / numbered list items, strip markdown."""
    items = []
    for line in text.splitlines():
        line = line.strip()
        m = _RE_BULLET.match(line) or _RE_NUMBERED.match(line)
        if m:
            content = _RE_BOLD_PREFIX.sub('', m.group(1))
            items.append(normalize(content))
    return items


def extract_sources(text: str) -> list[str]:
    """Pull [title](url) links → 'title|url' strings."""
    items = []
    for line in text.splitlines():
        m = _RE_LINK_IN_LINE.search(line)
        if m:
            items.append(f"{m.group(1).strip()}|{m.group(2).strip()}")
    return items


def extract_table_rows(text: str) -> list[str]:
    """
    Pull | col | col | table rows, skipping the header row and separator lines.
    The first non-separator row is always the column header and is skipped unconditionally.
    """
    rows = []
    header_skipped = False
    for line in text.splitlines():
        line = line.strip()
        if not (line.startswith('|') and line.endswith('|')):
            continue
        if '---' in line:
            continue
        if not header_skipped:
            header_skipped = True
            continue
        cols = [normalize(c) for c in line.strip('|').split('|') if normalize(c)]
        if cols:
            rows.append('|'.join(cols))
    return rows



def main():
    if len(sys.argv) != 2:
        print("Usage: check_sync.py <investigation_dir>")
        sys.exit(2)

    investigation_dir = Path(sys.argv[1])
    json_path = investigation_dir / 'investigation.json'
    md_path   = investigation_dir / 'investigation.md'

    for p in (json_path, md_path):
        if not p.exists():
            print(f"ERROR: {p} not found")
            print(f"  Recovery: run 'python3 _scripts/json_to_md.py {investigation_dir}' to generate missing markdown")
            sys.exit(2)

    try:
        data = json.loads(json_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        print(f"ERROR: {json_path} contains invalid JSON — {exc}")
        print(f"  Recovery: fix the JSON syntax error and re-run this check")
        sys.exit(2)
    except OSError as exc:
        print(f"ERROR: cannot read {json_path} — {exc}")
        sys.exit(2)

    try:
        md = md_path.read_text(encoding='utf-8')
    except OSError as exc:
        print(f"ERROR: cannot read {md_path} — {exc}")
        sys.exit(2)

    sections = parse_sections(md)

    checks = [
        {
            'field': 'key_findings',
            'json_items': [normalize(f) for f in data.get('key_findings', [])],
            'md_items':   extract_list_items(sections.get('Key Findings', '')),
        },
        {
            'field': 'tensions',
            'json_items': [normalize(t) for t in data.get('tensions', [])],
            'md_items':   extract_list_items(sections.get('Tensions & Tradeoffs', '')),
        },
        {
            'field': 'open_questions',
            'json_items': [normalize(q) for q in data.get('open_questions', [])],
            'md_items':   extract_list_items(sections.get('Open Questions', '')),
        },
        {
            'field': 'sources',
            'json_items': [
                f"{(s.get('title') or '').strip()}|{(s.get('url') or '').strip()}"
                for s in data.get('sources', [])
            ],
            'md_items': extract_sources(sections.get('Sources & References', '')),
        },
        {
            'field': 'concepts',
            'json_items': [
                f"{normalize(c.get('name') or '')}|{normalize(c.get('description') or '')}"
                for c in data.get('concepts', [])
            ],
            'md_items': extract_table_rows(sections.get('Concepts & Entities', '')),
        },
    ]

    results  = []
    all_sync = True
    diff_lines: list[str] = []

    for check in checks:
        j_hash = hash_list(check['json_items'])
        m_hash = hash_list(check['md_items'])
        status = 'IN_SYNC' if j_hash == m_hash else 'OUT_OF_SYNC'
        if status == 'OUT_OF_SYNC':
            all_sync = False
            diff_lines += diff_lists(check['field'], check['json_items'], check['md_items'])
        results.append({
            'field':      check['field'],
            'status':     status,
            'json_count': len(check['json_items']),
            'md_count':   len(check['md_items']),
            'json_hash':  j_hash[:12],
            'md_hash':    m_hash[:12],
        })

    col_widths = [20, 14, 12, 12, 14, 14]
    header = (
        f"{'Field':<{col_widths[0]}} {'Status':<{col_widths[1]}} "
        f"{'JSON items':<{col_widths[2]}} {'MD items':<{col_widths[3]}} "
        f"{'JSON hash':<{col_widths[4]}} {'MD hash':<{col_widths[5]}}"
    )
    print(f"\nSync check: {investigation_dir.resolve()}")
    print(header)
    print('-' * sum(col_widths))
    for r in results:
        print(
            f"{r['field']:<{col_widths[0]}} {r['status']:<{col_widths[1]}} "
            f"{r['json_count']:<{col_widths[2]}} {r['md_count']:<{col_widths[3]}} "
            f"{r['json_hash']:<{col_widths[4]}} {r['md_hash']:<{col_widths[5]}}"
        )

    briefs = data.get('audience_briefs', {})
    brief_checks = [
        ('engineering_leadership', investigation_dir / 'brief_leadership.md'),
        ('product_owner',          investigation_dir / 'brief_po.md'),
    ]
    for key, path in brief_checks:
        if briefs.get(key):
            exists = path.exists()
            status = 'IN_SYNC' if exists else 'OUT_OF_SYNC (missing file)'
            if not exists:
                all_sync = False
                diff_lines.append(
                    f"  [{path.name}] defined in audience_briefs but file not found"
                    f" — run 'python3 _scripts/json_to_md.py {investigation_dir}' to generate it"
                )
            print(f"{path.name:<20} {status}")

    print()
    if all_sync:
        print("Result: IN_SYNC")
    else:
        drifted = [r['field'] for r in results if r['status'] == 'OUT_OF_SYNC']
        print(f"Result: OUT_OF_SYNC — {', '.join(drifted) if drifted else 'missing brief files'}")
        print()
        print("Differences:")
        for line in diff_lines:
            print(line)
        print()
        print("Recovery: re-run 'python3 _scripts/json_to_md.py <investigation_dir>' to regenerate markdown from JSON")

    sys.exit(0 if all_sync else 1)


if __name__ == '__main__':
    main()
