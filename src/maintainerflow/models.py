from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class IssueType(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    QUESTION = "question"
    DOCUMENTATION = "documentation"
    MAINTENANCE = "maintenance"


class OutputFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IssueInput(BaseModel):
    title: str
    body: str


class TriageResult(BaseModel):
    issue_type: IssueType
    confidence: float = Field(ge=0, le=1)
    missing_information: list[str]
    suggested_labels: list[str]
    suggested_response: str
    redirect_suggestion: str | None = None


class PRReviewInput(BaseModel):
    diff_text: str


class PRReviewResult(BaseModel):
    summary: str
    risk_level: RiskLevel
    risk_analysis: list[str]
    manual_review_areas: list[str]
    missing_items: list[str]
    suggested_comments: list[str]


class ReleaseItem(BaseModel):
    title: str
    labels: list[str] = Field(default_factory=list)
    commit_message: str = ""


class ReleaseInput(BaseModel):
    version: str = "Unreleased"
    items: list[ReleaseItem]


class ReleaseNotesResult(BaseModel):
    highlights: list[str]
    sections: dict[str, list[str]]
    markdown: str


class ReplyTemplate(str, Enum):
    MISSING_REPRO = "missing-reproduction"
    MISSING_TESTS = "missing-tests"
    STALE_PR = "stale-pr-follow-up"
    DUPLICATE_ISSUE = "duplicate-issue"
    SCOPE_CLARIFICATION = "scope-clarification"
    DOCS_REQUEST = "docs-request"
