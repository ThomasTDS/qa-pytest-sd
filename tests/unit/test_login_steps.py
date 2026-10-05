from unittest.mock import MagicMock

import pytest

from conftest import REPORT_NOTES_STASH_KEY
from steps.login_steps import MAX_LOGOUT_RELOADS, logout

pytestmark = pytest.mark.unit


def make_request() -> MagicMock:
    request = MagicMock(name="request")
    request.node.stash = {}
    return request


def test_logout_does_not_reload_when_redirect_happens() -> None:
    login_page = MagicMock(name="login_page")
    login_page.is_on_login_page.return_value = True
    request = make_request()

    logout(login_page, request)

    login_page.logout.assert_called_once()
    login_page.reload.assert_not_called()
    assert REPORT_NOTES_STASH_KEY not in request.node.stash


def test_logout_reloads_until_redirect_and_records_note() -> None:
    login_page = MagicMock(name="login_page")
    login_page.is_on_login_page.side_effect = [False, True]
    request = make_request()

    logout(login_page, request)

    login_page.reload.assert_called_once()
    notes = request.node.stash[REPORT_NOTES_STASH_KEY]
    assert len(notes) == 1
    assert "1 vez(es)" in notes[0]


def test_logout_gives_up_after_max_reloads() -> None:
    login_page = MagicMock(name="login_page")
    login_page.is_on_login_page.return_value = False
    request = make_request()

    logout(login_page, request)

    assert login_page.reload.call_count == MAX_LOGOUT_RELOADS
    assert f"{MAX_LOGOUT_RELOADS} vez(es)" in request.node.stash[REPORT_NOTES_STASH_KEY][0]
