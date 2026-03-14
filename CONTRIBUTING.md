# Contributing to MaintainerFlow

Thanks for your interest in improving MaintainerFlow.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Guidelines

- Keep MVP behavior deterministic and explainable.
- Add tests for new logic and CLI paths.
- Prefer straightforward heuristics over opaque scoring.
- Keep this tool assistive; avoid language that implies replacing maintainers.
