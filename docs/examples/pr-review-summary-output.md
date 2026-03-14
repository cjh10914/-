# Example Output: PR Review Summary

**Scenario:** A PR changes source code but does not include tests or docs updates.

**Command used**

```bash
maintainerflow review-pr examples/pr_webhook_hardening.diff
```

**Output (markdown)**

```markdown
# PR Review Summary
- **Summary:** PR changes 2 file(s) with +18/-2 lines.
- **Risk level:** medium

## Risk Analysis
- CI workflow changes can impact release safety.

## Manual Review Areas
- Validate workflow permissions and trigger scope.
- Confirm business logic and edge-case handling in src/ modules.

## Potentially Missing Items
- Tests may be missing for source changes.
- Documentation updates may be needed.

## Suggested Review Comments
- Can we add or reference tests that cover the new behavior?
- Please confirm whether README/docs should be updated.

## Suggested Next Steps
- Review highlighted risk and manual-review areas before approval.
- Request missing tests/docs or explicit rationale from the author.
```

## Plain-language takeaway

MaintainerFlow gives maintainers a structured starting point for review. It does
not decide whether the PR should be merged.
