#!/usr/bin/env python3
"""
gen_schema.py — generates templates/investigation_schema.json from the Pydantic model.

Run this whenever models.py changes:
    python3 scripts/gen_schema.py

The generated schema is embedded in templates/agent_persona.md so agents receive
the exact JSON Schema spec (not prose) for the investigation.json they must produce.

Exit: 0 = success, 2 = error
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models import Investigation


def main():
    repo_root = Path(__file__).parent.parent
    out_path = repo_root / "templates" / "investigation_schema.json"

    schema = Investigation.model_json_schema()
    out_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"Written: {out_path.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(2)
