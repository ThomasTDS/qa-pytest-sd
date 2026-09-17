from unittest.mock import MagicMock

import pytest

from pages.security_page import SecurityPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def test_assert_security_headers_present_passes_when_headers_correct() -> None:
    page, _ = make_page_mock()
    response = MagicMock()
    response.headers = {"x-frame-options": "DENY", "x-content-type-options": "nosniff"}
    page.request.get.return_value = response

    SecurityPage(page).assert_security_headers_present()

    page.request.get.assert_called_once_with("https://automationexercise.com/")


def test_assert_security_headers_present_fails_when_header_missing() -> None:
    page, _ = make_page_mock()
    response = MagicMock()
    response.headers = {"x-content-type-options": "nosniff"}
    page.request.get.return_value = response

    with pytest.raises(AssertionError):
        SecurityPage(page).assert_security_headers_present()


def test_assert_http_redirects_to_https_passes_when_final_url_is_https() -> None:
    page, _ = make_page_mock()
    response = MagicMock()
    response.url = "https://automationexercise.com/"
    page.request.get.return_value = response

    SecurityPage(page).assert_http_redirects_to_https()

    page.request.get.assert_called_once_with("http://automationexercise.com/")


def test_assert_http_redirects_to_https_fails_when_final_url_stays_http() -> None:
    page, _ = make_page_mock()
    response = MagicMock()
    response.url = "http://automationexercise.com/"
    page.request.get.return_value = response

    with pytest.raises(AssertionError):
        SecurityPage(page).assert_http_redirects_to_https()


def test_assert_session_cookie_is_http_only_passes_when_flag_set() -> None:
    page, _ = make_page_mock()
    page.context.cookies.return_value = [
        {"name": "other", "httpOnly": False},
        {"name": "sessionid", "httpOnly": True},
    ]

    SecurityPage(page).assert_session_cookie_is_http_only()


def test_assert_session_cookie_is_http_only_fails_when_flag_not_set() -> None:
    page, _ = make_page_mock()
    page.context.cookies.return_value = [{"name": "sessionid", "httpOnly": False}]

    with pytest.raises(AssertionError):
        SecurityPage(page).assert_session_cookie_is_http_only()


def test_assert_session_cookie_is_http_only_fails_when_cookie_missing() -> None:
    page, _ = make_page_mock()
    page.context.cookies.return_value = [{"name": "other", "httpOnly": True}]

    with pytest.raises(AssertionError):
        SecurityPage(page).assert_session_cookie_is_http_only()
