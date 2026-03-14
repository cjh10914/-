# Example Output: Reply Template

**Scenario:** A PR changes behavior but has no test coverage.

**Command used**

```bash
maintainerflow reply-template missing-tests
```

**Output (markdown)**

```markdown
# Reply Template: missing-tests

Thanks for the PR. Please add tests (or explain why tests are not feasible) so maintainers can safely verify behavior changes.
```

## Plain-language takeaway

Templates save maintainer time and keep requests consistent. Maintainers can
edit tone/context before posting.
