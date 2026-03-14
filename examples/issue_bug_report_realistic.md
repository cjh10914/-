# Bug: `maintainerflow review-pr` reports low risk for workflow-only PRs

### Current behavior
When a PR only modifies `.github/workflows/release.yml`, the summary still says `low` risk in some cases.

### Expected behavior
Workflow edits should at least trigger explicit CI safety review notes.

### Steps to reproduce
1. Create a branch with only `.github/workflows/release.yml` changes.
2. Run `maintainerflow review-pr pr.diff --output json`.
3. Inspect `risk_analysis` and `risk_level`.

### Environment
- MaintainerFlow: 0.1.0
- Python: 3.11.9
- OS: Ubuntu 22.04

### Logs
```
No crash, but output omitted the expected workflow warning once in a real repo diff.
```
