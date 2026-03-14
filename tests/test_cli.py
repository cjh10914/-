import json

from typer.testing import CliRunner

from maintainerflow.cli import app

runner = CliRunner()


def test_cli_triage_issue_json_output(tmp_path) -> None:
    issue_file = tmp_path / "issue.json"
    issue_file.write_text('{"title":"bug: crash", "body":"it fails"}', encoding="utf-8")
    result = runner.invoke(app, ["triage-issue", str(issue_file), "--output", "json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["issue_type"] == "bug"


def test_cli_triage_issue_markdown(tmp_path) -> None:
    issue_md = tmp_path / "issue.md"
    issue_md.write_text("# docs typo\nplease fix", encoding="utf-8")
    result = runner.invoke(app, ["triage-issue", str(issue_md)])
    assert result.exit_code == 0
    assert "# Issue Triage" in result.stdout


def test_cli_triage_issue_marks_no_missing_info(tmp_path) -> None:
    issue_md = tmp_path / "issue.md"
    issue_md.write_text(
        "# bug: crash\nsteps to reproduce\nexpected behavior\nactual behavior\npython 3.11\nstack trace",
        encoding="utf-8",
    )
    result = runner.invoke(app, ["triage-issue", str(issue_md)])
    assert result.exit_code == 0
    assert "None detected by heuristic checks." in result.stdout


def test_cli_triage_issue_invalid_json(tmp_path) -> None:
    issue_file = tmp_path / "issue.json"
    issue_file.write_text('{"title":"bad"', encoding="utf-8")
    result = runner.invoke(app, ["triage-issue", str(issue_file)])
    assert result.exit_code != 0
    assert "Invalid issue input" in result.stdout


def test_cli_review_pr_json(tmp_path) -> None:
    diff = tmp_path / "change.diff"
    diff.write_text("diff --git a/src/x.py b/src/x.py\n--- a/src/x.py\n+++ b/src/x.py\n+print(1)\n", encoding="utf-8")
    result = runner.invoke(app, ["review-pr", str(diff), "--output", "json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert "risk_level" in payload


def test_cli_review_pr_includes_next_steps(tmp_path) -> None:
    diff = tmp_path / "change.diff"
    diff.write_text("diff --git a/src/x.py b/src/x.py\n--- a/src/x.py\n+++ b/src/x.py\n+print(1)\n", encoding="utf-8")
    result = runner.invoke(app, ["review-pr", str(diff)])
    assert result.exit_code == 0
    assert "## Suggested Next Steps" in result.stdout


def test_cli_generate_release_notes_markdown(tmp_path) -> None:
    data = {
        "version": "v1",
        "items": [{"title": "feat: add", "labels": ["feature"], "commit_message": "feat: add"}],
    }
    infile = tmp_path / "release.json"
    infile.write_text(json.dumps(data), encoding="utf-8")
    result = runner.invoke(app, ["generate-release-notes", str(infile)])
    assert result.exit_code == 0
    assert "# Release v1" in result.stdout


def test_cli_out_file_writes_content(tmp_path) -> None:
    data = {
        "version": "v1",
        "items": [{"title": "fix: add", "labels": ["fix"], "commit_message": "fix: add"}],
    }
    infile = tmp_path / "release.json"
    outfile = tmp_path / "release.md"
    infile.write_text(json.dumps(data), encoding="utf-8")
    result = runner.invoke(app, ["generate-release-notes", str(infile), "--out-file", str(outfile)])
    assert result.exit_code == 0
    assert outfile.exists()
    assert "# Release v1" in outfile.read_text(encoding="utf-8")


def test_cli_reply_template_json() -> None:
    result = runner.invoke(app, ["reply-template", "docs-request", "--output", "json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["template"] == "docs-request"


def test_cli_help_contains_assistive_language() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "human maintainer" in result.stdout.lower()
