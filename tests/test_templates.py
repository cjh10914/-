from maintainerflow.models import ReplyTemplate
from maintainerflow.templates import get_reply_template


def test_all_templates_have_text() -> None:
    for template in ReplyTemplate:
        assert get_reply_template(template)


def test_missing_tests_template_mentions_tests() -> None:
    msg = get_reply_template(ReplyTemplate.MISSING_TESTS)
    assert "tests" in msg.lower()
