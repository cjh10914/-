# Example Output: Release Notes

**Scenario:** Prepare a release draft from merged PR metadata.

**Command used**

```bash
maintainerflow generate-release-notes examples/release_input_v010.json
```

**Output (markdown)**

```markdown
# Release v0.1.0

## Highlights
- Introduces 2 new feature(s).
- Includes 3 bug fix(es).

## Features
- feat: add issue triage command
- feat: add release notes generator

## Fixes
- fix: handle empty issue body
- fix: avoid duplicate labels in triage output
- fix: improve diff parsing for deleted files

## Docs
- docs: clarify workflow setup
```

## Plain-language takeaway

This provides a draft release note structure quickly. Maintainers should still
edit wording, add upgrade guidance, and confirm accuracy before publishing.
