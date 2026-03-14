# Example Output: PR Review Summary

_Input file:_ `examples/pr_webhook_hardening.diff`

```markdown
# PR Review Summary
- **Summary:** PR changes 2 file(s) with +8/-1 lines.
- **Risk level:** medium

## Risk Analysis
- CI workflow changes can impact release safety.

## Manual Review Areas
- Validate workflow permissions and trigger scope.
- Confirm business logic and edge-case handling in src/ modules.

## Potentially Missing Items
- Tests may be missing for source changes.

## Suggested Review Comments
- Can we add or reference tests that cover the new behavior?
```

### What this means (plain language)

- The PR is not labeled high risk, but it touches workflow automation and should be reviewed carefully.
- Maintainers are reminded to check test coverage for logic changes.
- Suggested review comments are intentionally short and reusable.
