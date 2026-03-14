from maintainerflow.models import PRReviewInput, RiskLevel
from maintainerflow.review import review_pr


def test_review_detects_missing_tests_for_src_changes() -> None:
    diff = """diff --git a/src/mod.py b/src/mod.py
--- a/src/mod.py
+++ b/src/mod.py
+print('x')
"""
    result = review_pr(PRReviewInput(diff_text=diff))
    assert any("Tests may be missing" in item for item in result.missing_items)


def test_review_high_risk_for_large_change() -> None:
    lines = "\n".join([f"+line{i}" for i in range(450)])
    diff = f"""diff --git a/src/a.py b/src/a.py
--- a/src/a.py
+++ b/src/a.py
{lines}
"""
    result = review_pr(PRReviewInput(diff_text=diff))
    assert result.risk_level in {RiskLevel.MEDIUM, RiskLevel.HIGH}
    assert any("Large change" in point for point in result.risk_analysis)


def test_review_workflow_change_flags_ci_risk() -> None:
    diff = """diff --git a/.github/workflows/x.yml b/.github/workflows/x.yml
--- a/.github/workflows/x.yml
+++ b/.github/workflows/x.yml
+name: x
"""
    result = review_pr(PRReviewInput(diff_text=diff))
    assert any("CI workflow changes" in item for item in result.risk_analysis)


def test_review_security_path_adds_security_review() -> None:
    diff = """diff --git a/src/auth/policy.py b/src/auth/policy.py
--- a/src/auth/policy.py
+++ b/src/auth/policy.py
+allow = False
"""
    result = review_pr(PRReviewInput(diff_text=diff))
    assert any("Security-sensitive" in item for item in result.risk_analysis)
    assert any("security review" in item.lower() for item in result.manual_review_areas)


def test_review_defaults_when_no_patterns() -> None:
    diff = """diff --git a/notes.txt b/notes.txt
--- a/notes.txt
+++ b/notes.txt
+note
"""
    result = review_pr(PRReviewInput(diff_text=diff))
    assert result.risk_analysis
    assert result.manual_review_areas
    assert result.risk_level == RiskLevel.LOW
