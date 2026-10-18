"""Name this project. Run once after "Use this template" or a clone:

    python init.py                       # asks for each answer
    python init.py --yes --title "My paper" --author "Me" --email me@lab.org --starter manuscript

A thin shim: it runs `document-sanity init --in-place` (see `--help`) with the
version pinned in pyproject.toml, fetched by `uvx` so nothing needs to be
installed first. That command renames the project (pyproject.toml,
README.md), sets the title and authors in each starter's manifest.yaml,
drops the starters you don't keep (`--starter manuscript`, `proposal`, or
`both`), installs the agent skill, and removes this file.

Starting somewhere other than a template copy? Skip this file:
`uvx --from "document-sanity @ git+https://github.com/yakaboskic/document-sanity.git@vX.Y.Z" document-sanity init DIR`.

DOCUMENT_SANITY_FROM overrides where the tool comes from (e.g. a local
checkout, while working on the tool itself).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pinned_tool() -> str:
    """The document-sanity requirement in pyproject.toml, minus extras."""
    text = (ROOT / "pyproject.toml").read_text()
    m = re.search(r'"(document-sanity(?:\[[^\]]*\])?\s*@\s*[^"]+)"', text)
    if m is None:
        sys.exit("init.py: no document-sanity dependency in pyproject.toml")
    return re.sub(r"\[[^\]]*\]", "", m.group(1), count=1)


def main() -> int:
    args = ["init", "--in-place", str(ROOT), *sys.argv[1:]]
    if shutil.which("uvx"):
        tool = os.environ.get("DOCUMENT_SANITY_FROM") or pinned_tool()
        command = ["uvx", "--from", tool, "document-sanity", *args]
    else:
        try:
            import document_sanity  # noqa: F401
        except ImportError:
            print(
                "init.py needs uv (https://docs.astral.sh/uv/) to fetch document-sanity:\n"
                "  curl -LsSf https://astral.sh/uv/install.sh | sh\n"
                "then run `python init.py` again.",
                file=sys.stderr,
            )
            return 1
        command = [sys.executable, "-m", "document_sanity", *args]
    return subprocess.call(command)


if __name__ == "__main__":
    sys.exit(main())
