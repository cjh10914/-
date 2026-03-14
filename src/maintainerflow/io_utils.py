from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(load_text(path))


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)
