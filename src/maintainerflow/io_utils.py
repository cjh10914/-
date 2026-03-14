from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from maintainerflow.models import IssueInput


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(load_text(path))


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def parse_issue_input(path: Path) -> IssueInput:
    """Parse issue input from JSON or markdown/plaintext files."""
    if path.suffix.lower() == ".json":
        payload = load_json(path)
        return IssueInput.model_validate(payload)

    text = load_text(path)
    if text.startswith("#"):
        lines = text.splitlines()
        title = lines[0].lstrip("# ").strip()
        body = "\n".join(lines[1:]).strip()
        return IssueInput(title=title or "Untitled issue", body=body)

    return IssueInput(title=path.stem.replace("_", " "), body=text)
