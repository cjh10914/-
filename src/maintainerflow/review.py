from __future__ import annotations

import re
from dataclasses import dataclass

from maintainerflow.models import PRReviewInput, PRReviewResult, RiskLevel


@dataclass(frozen=True)
class DiffStats:
    files: int
    paths: list[str]
    additions: int
    deletions: int


def _extract_diff_stats(diff_text: str) -> DiffStats:
    files = len(re.findall(r"^diff --git", diff_text, flags=re.MULTILINE))
    paths = [m for m in re.findall(r"^\+\+\+ b/(.+)$", diff_text, flags=re.MULTILINE) if m != "/dev/null"]
    additions = len(re.findall(r"^\+(?!\+\+\+)", diff_text, flags=re.MULTILINE))
    deletions = len(re.findall(r"^-(?!---)", diff_text, flags=re.MULTILINE))
    return DiffStats(files=files, paths=paths, additions=additions, deletions=deletions)


def _compute_risk_level(stats: DiffStats, risk_points: list[str]) -> RiskLevel:
    if len(risk_points) >= 2:
        return RiskLevel.HIGH
    if stats.additions > 120 or stats.files > 5:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def review_pr(payload: PRReviewInput) -> PRReviewResult:
    stats = _extract_diff_stats(payload.diff_text)
    summary = f"PR changes {stats.files} file(s) with +{stats.additions}/-{stats.deletions} lines."

    risk_points: list[str] = []
    manual_areas: list[str] = []
    missing_items: list[str] = []
    comments: list[str] = []

    if stats.files > 10 or stats.additions > 400:
        risk_points.append("Large change set may hide regressions.")
    if any(path.startswith(".github/workflows/") for path in stats.paths):
        risk_points.append("CI workflow changes can impact release safety.")
        manual_areas.append("Validate workflow permissions and trigger scope.")
    if any(path.startswith("src/") for path in stats.paths):
        manual_areas.append("Confirm business logic and edge-case handling in src/ modules.")
    if any("security" in path.lower() or "auth" in path.lower() for path in stats.paths):
        risk_points.append("Security-sensitive files changed.")
        manual_areas.append("Perform focused security review.")

    has_tests = any(path.startswith("tests/") or path.endswith("_test.py") for path in stats.paths)
    has_docs = any(path.lower().startswith("docs/") or path.lower().endswith(".md") for path in stats.paths)

    if not has_tests and any(path.startswith("src/") for path in stats.paths):
        missing_items.append("Tests may be missing for source changes.")
        comments.append("Can we add or reference tests that cover the new behavior?")
    if not has_docs and any(path.startswith("src/") for path in stats.paths):
        missing_items.append("Documentation updates may be needed.")
        comments.append("Please confirm whether README/docs should be updated.")

    if not risk_points:
        risk_points.append("No high-risk patterns detected by heuristic scan.")
    if not manual_areas:
        manual_areas.append("Review key logic paths and user-facing behavior.")
    if not comments:
        comments.append("Could you provide a short validation plan for maintainers?")

    return PRReviewResult(
        summary=summary,
        risk_level=_compute_risk_level(stats, risk_points),
        risk_analysis=risk_points,
        manual_review_areas=manual_areas,
        missing_items=missing_items,
        suggested_comments=comments,
    )
