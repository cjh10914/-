from maintainerflow.models import IssueInput, IssueType
from maintainerflow.triage import triage_issue


def test_triage_bug_detects_missing_details() -> None:
    result = triage_issue(IssueInput(title="Crash on boot", body="It crashes with error"))
    assert result.issue_type == IssueType.BUG
    assert "reproduction steps" in result.missing_information
    assert "needs-reproduction" in result.suggested_labels


def test_triage_feature_detects_complete_info() -> None:
    body = "Use case: teams need exports. Expected outcome: csv reports. Alternatives considered: scripts."
    result = triage_issue(IssueInput(title="Feature request", body=body))
    assert result.issue_type == IssueType.FEATURE
    assert result.missing_information == []
    assert "enhancement" in result.suggested_labels


def test_triage_question_has_redirect_suggestion() -> None:
    result = triage_issue(IssueInput(title="Question: how do I configure this?", body="help please"))
    assert result.issue_type == IssueType.QUESTION
    assert result.redirect_suggestion is not None


def test_triage_docs_classification() -> None:
    result = triage_issue(IssueInput(title="Docs typo in README", body="small typo"))
    assert result.issue_type == IssueType.DOCUMENTATION
    assert "docs" in result.suggested_labels


def test_triage_maintenance_labels() -> None:
    result = triage_issue(IssueInput(title="Chore: refactor dependency pinning", body="CI cleanup"))
    assert result.issue_type == IssueType.MAINTENANCE
    assert "chore" in result.suggested_labels


def test_triage_fallback_confidence_and_response() -> None:
    result = triage_issue(IssueInput(title="Untitled", body="misc text with no clear hints"))
    assert 0.0 <= result.confidence <= 1.0
    assert "assistive" in result.suggested_response
