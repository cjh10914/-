import json

from maintainerflow.io_utils import parse_issue_input


def test_parse_issue_input_from_json(tmp_path) -> None:
    issue_file = tmp_path / "issue.json"
    issue_file.write_text(json.dumps({"title": "bug: crash", "body": "details"}), encoding="utf-8")
    issue = parse_issue_input(issue_file)
    assert issue.title == "bug: crash"
    assert issue.body == "details"


def test_parse_issue_input_from_markdown_heading(tmp_path) -> None:
    issue_file = tmp_path / "issue.md"
    issue_file.write_text("# Feature request\nWe need export support", encoding="utf-8")
    issue = parse_issue_input(issue_file)
    assert issue.title == "Feature request"
    assert "export support" in issue.body


def test_parse_issue_input_from_plaintext_uses_stem(tmp_path) -> None:
    issue_file = tmp_path / "bug_report.txt"
    issue_file.write_text("raw body", encoding="utf-8")
    issue = parse_issue_input(issue_file)
    assert issue.title == "bug report"
    assert issue.body == "raw body"
