from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from pydantic import ValidationError

from maintainerflow.io_utils import dump_json, load_json, load_text
from maintainerflow.models import IssueInput, OutputFormat, PRReviewInput, ReleaseInput, ReplyTemplate
from maintainerflow.release_notes import generate_release_notes
from maintainerflow.review import review_pr
from maintainerflow.templates import get_reply_template
from maintainerflow.triage import triage_issue

app = typer.Typer(
    help=(
        "MaintainerFlow: deterministic maintainer assistant for OSS repositories. "
        "The tool is assistive and does not replace human review."
    ),
    no_args_is_help=True,
)


def _emit(data: Any, output: OutputFormat) -> str:
    if output == OutputFormat.JSON:
        return dump_json(data)
    return data if isinstance(data, str) else json.dumps(data, indent=2)


def _write_result(text: str, out_file: Path | None) -> None:
    if out_file is None:
        typer.echo(text)
        return
    out_file.write_text(text + "\n", encoding="utf-8")
    typer.echo(f"Wrote output to {out_file}")


def _parse_issue_file(path: Path) -> IssueInput:
    if path.suffix.lower() == ".json":
        payload = load_json(path)
        return IssueInput.model_validate(payload)

    text = load_text(path)
    if text.startswith("#"):
        lines = text.splitlines()
        title = lines[0].lstrip("# ").strip()
        body = "\n".join(lines[1:]).strip()
        return IssueInput(title=title or "Untitled issue", body=body)

    return IssueInput(title=path.stem.replace("_", " "), body=text)


def _common_output_option() -> OutputFormat:
    return typer.Option(OutputFormat.MARKDOWN, "--output", "-o", help="Output format: markdown or json.")


def _common_out_file_option() -> Path | None:
    return typer.Option(None, "--out-file", "-f", help="Optional output file path.")


@app.command("triage-issue")
def triage_issue_cmd(
    file: Path = typer.Argument(..., exists=True, readable=True, help="Path to issue input (.json or .md)."),
    output: OutputFormat = _common_output_option(),
    out_file: Path | None = _common_out_file_option(),
) -> None:
    """Classify an issue, detect missing details, and draft a maintainer reply."""
    try:
        issue = _parse_issue_file(file)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise typer.BadParameter(f"Invalid issue input: {exc}") from exc

    result = triage_issue(issue)
    if output == OutputFormat.JSON:
        _write_result(_emit(result.model_dump(), output), out_file)
        return

    lines = [
        "# Issue Triage",
        f"- **Type:** {result.issue_type.value}",
        f"- **Confidence:** {result.confidence:.2f}",
        f"- **Labels:** {', '.join(result.suggested_labels)}",
    ]
    if result.missing_information:
        lines.append("- **Missing information:**")
        lines.extend([f"  - {item}" for item in result.missing_information])
    if result.redirect_suggestion:
        lines.append(f"- **Redirect suggestion:** {result.redirect_suggestion}")
    lines.extend(["", "## Suggested Maintainer Reply", result.suggested_response])
    _write_result("\n".join(lines), out_file)


@app.command("review-pr")
def review_pr_cmd(
    diff_file: Path = typer.Argument(..., exists=True, readable=True, help="Path to unified diff file."),
    output: OutputFormat = _common_output_option(),
    out_file: Path | None = _common_out_file_option(),
) -> None:
    """Summarize pull request risk and review hotspots from a unified diff."""
    diff = load_text(diff_file)
    result = review_pr(PRReviewInput(diff_text=diff))

    if output == OutputFormat.JSON:
        _write_result(_emit(result.model_dump(), output), out_file)
        return

    lines = [
        "# PR Review Summary",
        f"- **Summary:** {result.summary}",
        f"- **Risk level:** {result.risk_level.value}",
        "",
        "## Risk Analysis",
        *[f"- {item}" for item in result.risk_analysis],
        "",
        "## Manual Review Areas",
        *[f"- {item}" for item in result.manual_review_areas],
    ]
    if result.missing_items:
        lines.extend(["", "## Potentially Missing Items", *[f"- {item}" for item in result.missing_items]])
    lines.extend(["", "## Suggested Review Comments", *[f"- {item}" for item in result.suggested_comments]])
    _write_result("\n".join(lines), out_file)


@app.command("generate-release-notes")
def generate_release_notes_cmd(
    input_file: Path = typer.Argument(..., exists=True, readable=True, help="Release metadata JSON file."),
    output: OutputFormat = _common_output_option(),
    out_file: Path | None = _common_out_file_option(),
) -> None:
    """Generate markdown release notes from merged PR metadata."""
    try:
        payload = load_json(input_file)
        release_input = ReleaseInput.model_validate(payload)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise typer.BadParameter(f"Invalid release notes input: {exc}") from exc

    result = generate_release_notes(release_input)
    rendered = _emit(result.model_dump(), output) if output == OutputFormat.JSON else result.markdown
    _write_result(rendered, out_file)


@app.command("reply-template")
def reply_template_cmd(
    template_name: ReplyTemplate = typer.Argument(..., help="Template key, e.g. missing-tests."),
    output: OutputFormat = _common_output_option(),
    out_file: Path | None = _common_out_file_option(),
) -> None:
    """Emit a reusable maintainer reply template."""
    text = get_reply_template(template_name)
    if output == OutputFormat.JSON:
        rendered = _emit({"template": template_name.value, "message": text}, output)
    else:
        rendered = f"# Reply Template: {template_name.value}\n\n{text}"
    _write_result(rendered, out_file)


if __name__ == "__main__":
    app()
