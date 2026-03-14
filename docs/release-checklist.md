# Release Checklist

Use this checklist before cutting a public release.

## Quality checks

- [ ] `pytest` passes.
- [ ] CLI help text matches current behavior.
- [ ] Example inputs and outputs are up to date.
- [ ] Limitations section is still accurate.

## Repository hygiene

- [ ] `CHANGELOG.md` updated.
- [ ] Version bumped in `pyproject.toml` and `src/maintainerflow/__init__.py`.
- [ ] Community files are present (`CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`).
- [ ] GitHub issue templates and PR template remain actionable.

## Release communication

- [ ] Draft GitHub release notes from `docs/release-v0.2.0.md`.
- [ ] Confirm release title/tag and compare link.
- [ ] Link to key docs and examples in release body.
- [ ] Include limitations to avoid overclaiming.
