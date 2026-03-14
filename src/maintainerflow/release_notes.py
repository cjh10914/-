from __future__ import annotations

from collections import defaultdict

from maintainerflow.models import ReleaseInput, ReleaseItem, ReleaseNotesResult

SECTIONS = ["breaking changes", "features", "fixes", "docs", "chores"]


def _category(item: ReleaseItem) -> str:
    labels = {label.lower() for label in item.labels}
    text = f"{item.title} {item.commit_message}".lower()

    if "breaking" in labels or "!" in item.title or "breaking" in text:
        return "breaking changes"
    if labels & {"feature", "enhancement", "feat"} or text.startswith("feat"):
        return "features"
    if labels & {"bug", "fix", "bugfix"} or text.startswith("fix"):
        return "fixes"
    if labels & {"docs", "documentation"} or text.startswith("docs"):
        return "docs"
    return "chores"


def _build_highlights(grouped: dict[str, list[str]]) -> list[str]:
    highlights: list[str] = []
    if grouped["breaking changes"]:
        highlights.append(f"{len(grouped['breaking changes'])} breaking change(s) require attention.")
    if grouped["features"]:
        highlights.append(f"Introduces {len(grouped['features'])} new feature(s).")
    if grouped["fixes"]:
        highlights.append(f"Includes {len(grouped['fixes'])} bug fix(es).")
    if not highlights:
        highlights.append("Primarily maintenance/documentation updates in this release.")
    return highlights


def generate_release_notes(release_input: ReleaseInput) -> ReleaseNotesResult:
    grouped: dict[str, list[str]] = defaultdict(list)
    for item in release_input.items:
        grouped[_category(item)].append(item.title)

    highlights = _build_highlights(grouped)

    lines: list[str] = [f"# Release {release_input.version}", "", "## Highlights"]
    lines.extend([f"- {highlight}" for highlight in highlights])

    for section in SECTIONS:
        if grouped[section]:
            lines.extend(["", f"## {section.title()}"])
            lines.extend([f"- {title}" for title in grouped[section]])

    sections = {section: grouped[section] for section in SECTIONS}
    markdown = "\n".join(lines)
    return ReleaseNotesResult(highlights=highlights, sections=sections, markdown=markdown)
