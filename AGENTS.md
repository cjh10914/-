# MaintainerFlow Agent Notes

These instructions apply to the whole repository.

## Project intent

- Keep MaintainerFlow deterministic and transparent in MVP.
- Favor maintainable heuristics over clever-but-opaque behavior.
- Do not introduce external API dependencies for core features.

## Coding guidelines

- Use small, single-purpose functions and explicit type hints.
- Keep domain models in `src/maintainerflow/models.py` and avoid ad-hoc dict schemas.
- Preserve clean separation:
  - parsing/input handling in CLI + `io_utils.py`,
  - business rules in `triage.py`, `review.py`, `release_notes.py`,
  - static templates in `templates.py`.
- If you add a rule, add or update tests in the same change.

## Testing expectations

- Run `pytest` before finalizing whenever dependencies are available.
- Add targeted tests for edge cases, not only happy paths.
- Keep tests deterministic: no network calls, no timestamps, no flaky randomness.

## CLI UX expectations

- All user-facing command help should be actionable and plain-language.
- New CLI behavior must support both markdown and JSON output.
- Error messages should guide maintainers to fix input shape/format quickly.

## Review checklist

Before submitting changes, verify:

1. deterministic behavior remains intact,
2. docs/examples reflect actual command behavior,
3. limitations are clearly documented (no overclaiming),
4. new heuristics are covered by tests,
5. GitHub Action examples remain safe and minimal-permission.
