from __future__ import annotations

from maintainerflow.models import ReplyTemplate

TEMPLATES: dict[ReplyTemplate, str] = {
    ReplyTemplate.MISSING_REPRO: (
        "Thanks for the report. Could you share clear steps to reproduce, expected behavior, "
        "actual behavior, and environment details? That will help maintainers validate quickly."
    ),
    ReplyTemplate.MISSING_TESTS: (
        "Thanks for the PR. Please add tests (or explain why tests are not feasible) so maintainers "
        "can safely verify behavior changes."
    ),
    ReplyTemplate.STALE_PR: (
        "Friendly follow-up: this PR has been inactive for a while. If you still want to proceed, "
        "please rebase/update and let us know what help you need."
    ),
    ReplyTemplate.DUPLICATE_ISSUE: (
        "Thanks for opening this. It appears similar to an existing issue. Please continue discussion "
        "there so context remains in one place."
    ),
    ReplyTemplate.SCOPE_CLARIFICATION: (
        "Thanks for the proposal. Could you clarify scope, non-goals, and acceptance criteria so we "
        "can evaluate implementation effort?"
    ),
    ReplyTemplate.DOCS_REQUEST: (
        "Could you include documentation updates (README/docs/changelog) for this change? "
        "This helps users adopt the feature confidently."
    ),
}


def get_reply_template(template: ReplyTemplate) -> str:
    return TEMPLATES[template]
