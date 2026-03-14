from maintainerflow.models import ReleaseInput, ReleaseItem
from maintainerflow.release_notes import generate_release_notes


def test_release_notes_grouping() -> None:
    payload = ReleaseInput(
        version="v1.0.0",
        items=[
            ReleaseItem(title="feat: new CLI", labels=["feature"]),
            ReleaseItem(title="fix: bug", labels=["fix"]),
            ReleaseItem(title="docs: update", labels=["docs"]),
        ],
    )
    result = generate_release_notes(payload)
    assert result.sections["features"] == ["feat: new CLI"]
    assert result.sections["fixes"] == ["fix: bug"]
    assert "# Release v1.0.0" in result.markdown


def test_release_notes_breaking_change_highlight() -> None:
    payload = ReleaseInput(version="v2", items=[ReleaseItem(title="feat!: API change", labels=["feature"])])
    result = generate_release_notes(payload)
    assert result.sections["breaking changes"]
    assert any("breaking change" in h for h in result.highlights)


def test_release_notes_default_highlight_when_no_major_sections() -> None:
    payload = ReleaseInput(version="v0", items=[ReleaseItem(title="chore: bump deps", labels=["chore"])])
    result = generate_release_notes(payload)
    assert "maintenance" in result.highlights[0].lower()


def test_release_notes_empty_items_still_renders() -> None:
    payload = ReleaseInput(version="v0.2.0", items=[])
    result = generate_release_notes(payload)
    assert "# Release v0.2.0" in result.markdown
    assert result.sections["features"] == []
