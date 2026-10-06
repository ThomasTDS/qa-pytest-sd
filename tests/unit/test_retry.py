from unittest.mock import MagicMock

import pytest

from pages.retry import MAX_RETRIES, retry_while_failing

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
