from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from pydantic import ValidationError

from maintainerflow.io_utils import dump_json, load_json, load_text, parse_issue_input
from maintainerflow.models import IssueInput, OutputFormat, PRReviewInput, ReleaseInput, ReplyTemplate
from maintainerflow.release_notes import generate_release_notes
from maintainerflow.review import review_pr
from maintainerflow.templates import get_reply_template
from maintainerflow.triage import triage_issue

app = typer.Typer(
    help=(
        "MaintainerFlow: deterministic maintainer assistant for OSS repositories. "
        "Use it for first-pass triage/review drafts, then keep a human maintainer in the loop."
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


def _common_output_option() -> OutputFormat:
    return typer.Option(
        OutputFormat.MARKDOWN,
        "--output",
        "-o",
        help="Output format (markdown for humans, json for automation).",
    )


def _common_out_file_option() -> Path | None:
    return typer.Option(None, "--out-file", "-f", help="Write output to a file instead of stdout.")


def _render_next_steps(items: list[str]) -> list[str]:
    if not items:
        return []
    return ["", "## Suggested Next Steps", *[f"- {item}" for item in items]]


@app.command("triage-issue")
def triage_issue_cmd(
    file: Path = typer.Argument(..., exists=True, readable=True, help="Issue input file (.json or .md)."),
    output: OutputFormat = _common_output_option(),
    out_file: Path | None = _common_out_file_option(),
) -> None:
    """Classify an issue, identify missing context, and draft a maintainer reply."""
    try:
        issue: IssueInput = parse_issue_input(file)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise typer.BadParameter(f"Invalid issue input: {exc}") from exc

    result = triage_issue(issue)
    if output == OutputFormat.JSON:
        _write_result(_emit(result.model_dump(), output), out_file)
        return

    missing = result.missing_information or ["None detected by heuristic checks."]
    next_steps: list[str] = []
    if result.missing_information:
        next_steps.append("Ask reporter to update the issue with missing details.")
    else:
        next_steps.append("Move to maintainer review or prioritization.")
    if result.redirect_suggestion:
        next_steps.append("Decide whether to redirect this thread to Discussions/docs.")

    lines = [
        "# Issue Triage",
        f"- **Type:** {result.issue_type.value}",
        f"- **Confidence:** {result.confidence:.2f}",
        f"- **Suggested labels:** {', '.join(result.suggested_labels)}",
        "- **Missing information:**",
        *[f"  - {item}" for item in missing],
    ]
    if result.redirect_suggestion:
        lines.append(f"- **Redirect suggestion:** {result.redirect_suggestion}")
    lines.extend(_render_next_steps(next_steps))
    lines.extend(["", "## Suggested Maintainer Reply", result.suggested_response])
    _write_result("\n".join(lines), out_file)


@app.command("review-pr")
def review_pr_cmd(
    diff_file: Path = typer.Argument(..., exists=True, readable=True, help="Path to unified diff file."),
    output: OutputFormat = _common_output_option(),
    out_file: Path | None = _common_out_file_option(),
) -> None:
    """Summarize PR impact, risk signals, and human review priorities."""
    diff = load_text(diff_file)
    result = review_pr(PRReviewInput(diff_text=diff))

    if output == OutputFormat.JSON:
        _write_result(_emit(result.model_dump(), output), out_file)
        return

    next_steps: list[str] = ["Review highlighted risk and manual-review areas before approval."]
    if result.missing_items:
        next_steps.append("Request missing tests/docs or explicit rationale from the author.")

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
    lines.extend(_render_next_steps(next_steps))
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
