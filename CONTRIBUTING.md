# Contributing to MaintainerFlow

Thanks for helping improve MaintainerFlow.

## Core contribution principles

- Keep behavior deterministic and explainable.
- Prefer small, single-purpose functions with type hints.
- Keep parsing/input in CLI + `io_utils.py`; keep business rules in `triage.py`, `review.py`, and `release_notes.py`.
- Avoid introducing external paid API dependencies for core features.
- Use plain-language CLI help and actionable error messages.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
```

## Running checks

```bash
pytest
maintainerflow --help
maintainerflow triage-issue examples/issue_bug_report_realistic.md
maintainerflow review-pr examples/pr_webhook_hardening.diff --output json
```

## Fixture conventions

- Put runnable sample inputs in `examples/`.
- Put human-readable walkthrough outputs in `docs/examples/`.
- Keep fixtures deterministic (no network calls, no timestamps).
- If a rule changes expected behavior, update the relevant fixture and tests in the same PR.

## How to propose a new rule or reply template

When proposing a new heuristic rule or template:

1. Describe the maintainer pain point in one paragraph.
2. Explain the deterministic trigger/logic.
3. Add or update tests for both normal and edge cases.
4. Update docs/examples if user-facing output changes.
5. Confirm language stays assistive (no autonomous-review claims).

## Review expectations before opening a PR

- [ ] Scope is small and focused.
- [ ] `pytest` passes locally.
- [ ] Changed behavior includes tests.
- [ ] README/docs/examples updated where needed.
- [ ] Limitations remain accurate and no overclaiming is introduced.
- [ ] GitHub Action examples remain minimal-permission and safe.
