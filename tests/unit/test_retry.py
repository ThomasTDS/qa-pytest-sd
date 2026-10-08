from unittest.mock import MagicMock, patch

import pytest

from pages.retry import MAX_RETRIES, assert_visible, is_visible, retry_while_failing

pytestmark = pytest.mark.unit


def test_retry_while_failing_returns_first_result_without_retry() -> None:
    first = MagicMock(return_value="ok")
    again = MagicMock()

    result, retries = retry_while_failing(first, again, failed=lambda _: False)

    assert (result, retries) == ("ok", 0)
    again.assert_not_called()


def test_retry_while_failing_repeats_until_it_succeeds() -> None:
    results = iter(["falhou", "ok"])
    first = MagicMock(side_effect=lambda: next(results))
    again = MagicMock(side_effect=lambda: next(results))

    result, retries = retry_while_failing(first, again, failed=lambda r: r == "falhou")

    assert (result, retries) == ("ok", 1)
    again.assert_called_once()


def test_retry_while_failing_stops_at_max_retries() -> None:
    first = MagicMock(return_value="falhou")
    again = MagicMock(return_value="falhou")

    result, retries = retry_while_failing(first, again, failed=lambda r: r == "falhou")

    assert (result, retries) == ("falhou", MAX_RETRIES)
    assert again.call_count == MAX_RETRIES


def test_is_visible_checks_the_right_text_and_timeout() -> None:
    page = MagicMock(name="page")

    with patch("pages.retry.expect") as expect_mock:
        result = is_visible(page, "ACCOUNT CREATED!", timeout_ms=5_000)

    page.get_by_text.assert_called_once_with("ACCOUNT CREATED!")
    expect_mock.assert_called_once_with(page.get_by_text.return_value)
    expect_mock.return_value.to_be_visible.assert_called_once_with(timeout=5_000)
    assert result is True


def test_is_visible_returns_false_when_text_never_appears() -> None:
    page = MagicMock(name="page")

    with patch("pages.retry.expect") as expect_mock:
        expect_mock.return_value.to_be_visible.side_effect = AssertionError()
        result = is_visible(page, "ACCOUNT CREATED!")

    expect_mock.return_value.to_be_visible.assert_called_once_with(timeout=10_000)
    assert result is False


def test_assert_visible_checks_the_right_text() -> None:
    page = MagicMock(name="page")

    with patch("pages.retry.expect") as expect_mock:
        assert_visible(page, "ACCOUNT CREATED!")

    page.get_by_text.assert_called_once_with("ACCOUNT CREATED!")
    expect_mock.assert_called_once_with(page.get_by_text.return_value)
    expect_mock.return_value.to_be_visible.assert_called_once_with()
