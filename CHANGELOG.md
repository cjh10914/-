# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
