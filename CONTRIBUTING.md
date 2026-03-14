# Contributing to MaintainerFlow

Thanks for helping improve MaintainerFlow.

## Local development workflow

1. Create a virtual environment.
2. Install dependencies.
3. Run tests.
4. Run CLI smoke checks.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
pytest
maintainerflow --help
maintainerflow triage-issue examples/issue_bug_report_realistic.md --output json
```

## Coding expectations

- Keep behavior deterministic and explainable.
- Prefer small, single-purpose functions with type hints.
- Keep parsing/input in CLI + `io_utils.py`, and business rules in domain modules.
- Avoid introducing external API dependencies for core features.
- Use plain-language CLI help and actionable error messages.

## Testing and review workflow

Before opening a PR:

1. Run `pytest` locally.
2. Update tests when heuristics or output format change.
3. Update docs/examples if command behavior changes.
4. Keep claims realistic: MaintainerFlow assists maintainers; it does not replace review.

PRs are reviewed for deterministic behavior, clarity, and safe GitHub Action examples.

## Pull request checklist

- [ ] Scope is small and focused.
- [ ] Tests added/updated for changed behavior.
- [ ] README/docs/examples updated when needed.
- [ ] No overclaiming or autonomous-review wording.
