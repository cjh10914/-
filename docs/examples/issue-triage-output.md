# Example Output: Issue Triage

**Scenario:** A contributor reports a crash but forgets environment details and logs.

**Command used**

```bash
maintainerflow triage-issue examples/issue_bug_missing.md
```

**Output (markdown)**

```markdown
# Issue Triage
- **Type:** bug
- **Confidence:** 0.65
- **Suggested labels:** bug, needs-reproduction, needs-triage
- **Missing information:**
  - environment details
  - logs or stack trace

## Suggested Next Steps
- Ask reporter to update the issue with missing details.
- Move to maintainer review once required details are provided.

## Suggested Maintainer Reply
Thanks for opening this. To help maintainers act quickly, please update this issue with:
- environment details
- logs or stack trace

Once added, we can continue triage.
```

## Plain-language takeaway

MaintainerFlow does not close the issue automatically. It highlights gaps and
prepares a clear maintainer response so the next maintainer action is obvious.
