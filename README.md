# MaintainerFlow

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Status: Active early-stage](https://img.shields.io/badge/status-active%20early--stage-orange.svg)
![CI](https://img.shields.io/badge/ci-pytest-informational.svg)

Deterministic, GitHub-native maintainer assistance for open-source repositories.

> **Quick value:** MaintainerFlow turns repetitive maintainer chores (triage, first-pass PR review summaries, release notes, and common replies) into structured drafts you can review and post quickly.

## Project status

MaintainerFlow is **active early-stage (v0.2.x)**. It is intentionally lightweight and practical: stable enough for real OSS maintainer workflows, but still opinionated and heuristic.

## Problem this project solves

Maintainers spend a lot of time on repetitive tasks that still require judgment:

- checking issue reports for missing context,
- writing first-pass PR summaries,
- grouping merged changes into release notes,
- and replying with similar clarification messages.

MaintainerFlow reduces this repetitive overhead with deterministic rules and transparent output.

## Who this is for / not for

### This is for

- OSS maintainers who want faster triage and review preparation.
- Projects that prefer deterministic heuristics over black-box automation.
- Repositories that want a small CLI and simple GitHub Actions demos.

### This is not for

- Teams wanting autonomous approvals or merge decisions.
- Security/compliance auditing pipelines.
- Workflows that require a paid external API dependency for core behavior.

## What maintainers get

1. **Issue triage**
   - classify issue type: bug, feature, question, documentation, maintenance,
   - detect missing details by type,
   - suggest labels,
   - generate an initial maintainer response.

2. **PR review summary**
   - summarize change size and risk signals from diffs,
   - highlight likely manual review areas,
   - flag likely missing tests/docs,
   - suggest review comments.

3. **Release notes generator**
   - convert merged change metadata to markdown release notes,
   - group into breaking changes, features, fixes, docs, chores,
   - generate highlights.

4. **Maintainer reply templates**
   - reusable templates for common maintainer responses.

## What this helps with vs what still needs human judgment

| What this helps with | What still requires human maintainer judgment |
| --- | --- |
| First-pass issue classification | Final prioritization and roadmap decisions |
| Missing-information checklist prompts | Deciding when report quality is sufficient |
| Risk hints from diff patterns | Correctness, architecture quality, security sign-off |
| Initial release note grouping | Final release narrative and compatibility promises |
| Reusable response drafts | Tone, context, and community-specific policy decisions |

## Installation

### End users

```bash
python -m pip install maintainerflow
```

### Local development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
pytest
```

## Quickstart

```bash
maintainerflow triage-issue examples/issue_bug_report_realistic.md
maintainerflow review-pr examples/pr_webhook_hardening.diff
maintainerflow generate-release-notes examples/release_input_v010.json
maintainerflow reply-template missing-tests
```

## Realistic example outputs

Review the examples before installing:

- [Issue triage output](docs/examples/issue-triage-output.md)
- [PR review summary output](docs/examples/pr-review-summary-output.md)
- [Release notes output](docs/examples/release-notes-output.md)
- [Reply template output](docs/examples/reply-template-output.md)

These examples are written so non-technical reviewers can quickly evaluate workflow fit.

## CLI

All commands support:

- `--output markdown|json` (default: markdown)
- `--out-file <path>` to write output to a file

### `maintainerflow triage-issue <file>`

Accepts:

- `.json` payload (`title`, `body`)
- `.md` issue body where first heading is used as title

```bash
maintainerflow triage-issue examples/issue_feature_request_realistic.json --output json
```

### `maintainerflow review-pr <diff-file>`

```bash
maintainerflow review-pr examples/pr_webhook_hardening.diff --output markdown
```

### `maintainerflow generate-release-notes <input-file>`

Input schema:

```json
{
  "version": "v0.2.0",
  "items": [{"title": "feat: ...", "labels": ["feature"], "commit_message": "feat: ..."}]
}
```

```bash
maintainerflow generate-release-notes examples/release_input_v010.json --out-file release-notes.md
```

### `maintainerflow reply-template <template-name>`

Supported template names:

- `missing-reproduction`
- `missing-tests`
- `stale-pr-follow-up`
- `duplicate-issue`
- `scope-clarification`
- `docs-request`

## GitHub Actions demo (step by step)

The repository includes `.github/workflows/demo-maintainerflow.yml`.

1. Copy that workflow into your repository.
2. Ensure the workflow can install MaintainerFlow (`pip install .` or `pip install maintainerflow`).
3. Trigger events:
   - `issues` (opened/edited) for issue triage output,
   - `pull_request` (opened/synchronize/reopened) for PR summary output,
   - `workflow_dispatch` for manual demo runs.
4. Download artifact `maintainerflow-output-<run_id>`.
5. Optionally keep or remove the demo PR-comment step based on your project policy.

Security note: keep workflow permissions minimal and review auto-comment behavior before enabling widely.

## Limitations (important)

MaintainerFlow intentionally has strict limits in v0.2.0:

- Heuristic keyword/diff analysis only (no semantic code understanding).
- Can produce false positives/negatives for labels, risk, and missing details.
- Not a merge gate, policy engine, or security scanner.
- GitHub Action is a demo integration, not a full GitHub App.
- Outputs must be reviewed by humans before maintainer action.

## Documentation map

- [CHANGELOG.md](CHANGELOG.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SUPPORT.md](SUPPORT.md)
- [SECURITY.md](SECURITY.md)
- [ROADMAP.md](ROADMAP.md)
- [AGENTS.md](AGENTS.md)

## License

MIT. See [LICENSE](LICENSE).
