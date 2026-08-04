#!/usr/bin/env python3
"""
DEPRECATED — replaced by scripts/ensure_descriptions.py at the repository root.

This file is retained inside the submodule as a thin wrapper so legacy
invocations continue to work, and so the side effect the old fixer performed
(rewriting `whenToUse` to "Activate this mode when you need a: {desc}") is gone
entirely — a description fixer must never rewrite `whenToUse`.

The consolidated, deterministic, idempotent tool lives at ../../scripts/
ensure_descriptions.py and covers agents/, custom_modes.d/ and
vs-code/converted_modes.d/ with a canonical curated store, a deterministic
derivation fallback (whenToUse -> roleDefinition first line), and surgical,
byte-preserving edits (only the `description:` scalar is touched).

Usage (unchanged from before):
    python3 custom-modes/scripts/fix_descriptions.py [--dir agents|custom_modes.d|vs-code/converted_modes.d|all]
"""

import runpy
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
# custom-modes/scripts/ -> repository root scripts/ensure_descriptions.py
_CONSOLIDATED = _HERE.parent.parent / "scripts" / "ensure_descriptions.py"

if __name__ == "__main__":
    if not _CONSOLIDATED.exists():
        sys.stderr.write(
            "fix_descriptions.py is deprecated: run scripts/ensure_descriptions.py "
            "from the repository root (custom-modes/ is a git submodule of roo-plus).\n"
        )
        sys.exit(1)
    runpy.run_path(str(_CONSOLIDATED), run_name="__main__")
