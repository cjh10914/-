# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-14

### Added
- Added `docs/application-summary.md` for OSS support-program/application use.
- Added `docs/release-v0.2.0.md` with a publish-ready release draft.
- Expanded documentation examples with clearer, non-technical explanations.

### Changed
- README rewritten for clearer maintainer value proposition, audience fit, limitations, and a human-judgment comparison table.
- CONTRIBUTING strengthened with fixture conventions, review expectations, and a deterministic rule/template proposal flow.
- CLI markdown output for triage and PR review now includes clearer "Suggested Next Steps" sections.
- Refactored issue input parsing into `io_utils.py` to keep parsing logic centralized.
- Updated release checklist and support/security docs for ongoing OSS maintenance.

### Limitations
- Core behavior remains deterministic and heuristic-driven; maintainers must review outputs before acting.

## [0.1.1] - 2026-03-14

### Added
- Community governance and support docs: `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `SUPPORT.md`.
- GitHub collaboration templates: issue templates for bug/feature/question and a pull request template.
- Human-readable output walkthroughs in `docs/examples/` for issue triage, PR review summary, release notes, and reply templates.
- Release-readiness documentation: `docs/release-checklist.md` and `docs/release-v0.1.1.md`.

### Changed
- README positioning and front matter updated with badges, project status, clearer value proposition, and audience fit/non-fit guidance.
- CONTRIBUTING workflow simplified with local setup, test/run checks, and review checklist language.
- Version bumped from `0.1.0` to `0.1.1` for a non-breaking credibility/documentation patch release.

### Limitations
- Core behavior remains deterministic and heuristic-driven; maintainers must review outputs before acting.

## [0.1.0] - 2026-03-14

### Added
- Initial MaintainerFlow MVP with deterministic issue triage, PR review summary, release note generation, and maintainer reply templates.
- Typer CLI commands: `triage-issue`, `review-pr`, `generate-release-notes`, and `reply-template`.
- GitHub Actions examples for CI and demo maintainer workflows.
- Example fixtures for realistic issue reports, feature requests, PR diffs, and release metadata.
- Contributor and governance docs: README, CONTRIBUTING, ROADMAP, AGENTS, and LICENSE.

### Changed
- Hardened CLI UX with stronger help text, output file support, and structured input validation errors.
- Refactored heuristic engines into smaller abstractions to improve readability and contributor onboarding.
- Expanded test suite with edge-case coverage across triage, PR review, release notes, and CLI paths.

### Limitations
- v0.1.0 remains intentionally heuristic and assistive; human maintainer review is always required.
