from __future__ import annotations

from dataclasses import dataclass

from maintainerflow.models import IssueInput, IssueType, TriageResult


@dataclass(frozen=True)
class InfoCheck:
    name: str
    hints: tuple[str, ...]


TYPE_KEYWORDS: dict[IssueType, tuple[str, ...]] = {
    IssueType.BUG: ("bug", "error", "crash", "fails", "failing", "broken", "exception", "unexpected"),
    IssueType.FEATURE: ("feature", "enhancement", "proposal", "request", "would like", "add support", "idea"),
    IssueType.QUESTION: ("question", "how do", "how can", "is it possible", "help", "clarify"),
    IssueType.DOCUMENTATION: ("docs", "documentation", "readme", "typo", "guide"),
    IssueType.MAINTENANCE: ("refactor", "chore", "dependency", "ci", "build", "cleanup", "maintenance"),
}

BUG_INFO_CHECKS: tuple[InfoCheck, ...] = (
    InfoCheck("reproduction steps", ("steps to reproduce", "reproduce", "repro")),
    InfoCheck("expected behavior", ("expected", "should")),
    InfoCheck("actual behavior", ("actual", "instead", "happens")),
    InfoCheck("environment details", ("python", "os", "version", "environment")),
    InfoCheck("logs or stack trace", ("log", "trace", "stack")),
)

FEATURE_INFO_CHECKS: tuple[InfoCheck, ...] = (
    InfoCheck("clear use case", ("use case", "problem", "pain")),
    InfoCheck("expected outcome", ("expected", "outcome", "success")),
    InfoCheck("alternatives considered", ("alternative", "workaround", "considered")),
)


def _detect_issue_type(text: str) -> tuple[IssueType, float]:
    lower = text.lower()
    scores = {issue_type: sum(1 for kw in keywords if kw in lower) for issue_type, keywords in TYPE_KEYWORDS.items()}
    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]
    confidence = min(1.0, 0.35 + 0.15 * best_score) if best_score > 0 else 0.4
    return best_type, confidence


def _find_missing_info(text: str, checks: tuple[InfoCheck, ...]) -> list[str]:
    lower = text.lower()
    return [check.name for check in checks if not any(hint in lower for hint in check.hints)]


def _build_response(missing: list[str]) -> str:
    if not missing:
        return (
            "Thanks for the detailed report. A maintainer will review this soon. "
            "Please note this tool is assistive and does not replace human review."
        )

    missing_md = "\n".join(f"- {item}" for item in missing)
    return (
        "Thanks for opening this. To help maintainers act quickly, "
        "please update this issue with:\n"
        f"{missing_md}\n\n"
        "Once added, we can continue triage."
    )


def triage_issue(issue: IssueInput) -> TriageResult:
    text = f"{issue.title}\n{issue.body}".strip()
    issue_type, confidence = _detect_issue_type(text)

    missing: list[str] = []
    labels = [issue_type.value, "needs-triage"]
    redirect: str | None = None

    if issue_type == IssueType.BUG:
        missing = _find_missing_info(text, BUG_INFO_CHECKS)
        if "reproduction steps" in missing:
            labels.append("needs-reproduction")
    elif issue_type == IssueType.FEATURE:
        missing = _find_missing_info(text, FEATURE_INFO_CHECKS)
        labels.append("enhancement")
    elif issue_type == IssueType.QUESTION:
        redirect = "Consider redirecting to GitHub Discussions or project documentation."
        labels.append("support")
    elif issue_type == IssueType.DOCUMENTATION:
        labels.extend(["docs", "good first issue"])
    else:
        labels.append("chore")

    return TriageResult(
        issue_type=issue_type,
        confidence=confidence,
        missing_information=missing,
        suggested_labels=sorted(set(labels)),
        suggested_response=_build_response(missing),
        redirect_suggestion=redirect,
    )
