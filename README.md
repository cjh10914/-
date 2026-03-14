# MaintainerFlow

MaintainerFlow is a GitHub-native, open-source assistant that helps OSS maintainers cut repetitive workflow overhead without automating away judgment.

> **Positioning:** MaintainerFlow is assistive triage/review tooling. It is not an autonomous reviewer and does not replace maintainer decisions.

## Why this exists

Maintainers repeatedly do high-context but repetitive work:

- asking for missing issue details,
- writing first-pass PR summaries,
- collecting release notes,
- and posting similar reply templates.

MaintainerFlow gives deterministic, transparent outputs for those jobs so maintainers can spend more time on final decisions.

## MVP features

1. **Issue triage**
   - Classifies issue type: bug, feature, question, docs, maintenance.
   - Detects missing context by issue type.
   - Suggests labels and a maintainer-ready follow-up reply.

2. **PR review summary**
   - Summarizes file/line impact from unified diff.
   - Produces risk analysis and manual review hotspots.
   - Flags likely missing tests/docs and suggests review comments.

3. **Release notes generator**
   - Converts merged PR metadata into markdown release notes.
   - Groups by breaking changes, features, fixes, docs, chores.
   - Adds concise highlights.

4. **Maintainer reply templates**
   - Reusable templates for common maintainer conversations.

## Installation

### End users

```bash
python -m pip install maintainerflow
```

### Local development

```bash
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

## CLI

All commands support:

- `--output markdown|json` (default: markdown)
- `--out-file <path>` to write results to a file

### `maintainerflow triage-issue <file>`

Accepts:
- `.json` payload (`title`, `body`)
- `.md` issue body where first heading becomes title

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
  "version": "v0.1.0",
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
2. Ensure your project can install MaintainerFlow (`pip install .` for local checkout, or `pip install maintainerflow` for PyPI).
3. Trigger events:
   - `issues` (opened/edited) for issue triage output,
   - `pull_request` (opened/synchronize/reopened) for PR summary output,
   - `workflow_dispatch` for manual demo runs.
4. Check the uploaded artifact named `maintainerflow-output-<run_id>`.
5. Optionally keep/remove the demo PR comment step based on your repo policy.

Security note: keep workflow permissions minimal and review any automated commenting before enabling in production repositories.

## Publishability checklist highlights

- `src/` layout with typed modules.
- deterministic rule-based engine (no external LLM/API dependency in core flow).
- CLI + GitHub Actions example.
- test suite with unit + CLI coverage.
- contributor docs (`CONTRIBUTING.md`, `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`).

## Limitations (important)

MaintainerFlow intentionally has strict limits in v0.1.0:

- Heuristic keyword/diff analysis only (no semantic code understanding).
- Can produce false positives/negatives on labels, risk, and missing information.
- Not a merge gate, policy engine, or security scanner.
- GitHub Action is a demo integration, not a full GitHub App.
- Outputs must be reviewed by humans before maintainer action.

## Documentation map

- [CHANGELOG.md](CHANGELOG.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [ROADMAP.md](ROADMAP.md)
- [AGENTS.md](AGENTS.md)

## License

MIT. See [LICENSE](LICENSE).
