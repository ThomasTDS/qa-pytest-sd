from unittest.mock import patch

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.login_page import LoginPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def test_goto_uses_default_base_url_when_env_not_set() -> None:
    page, _ = make_page_mock()

    LoginPage(page).goto()

    page.goto.assert_called_once_with(
        "https://automationexercise.com/login", wait_until="domcontentloaded"
    )


def test_goto_uses_base_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BASE_URL", "https://staging.example.com/")
    page, _ = make_page_mock()

    LoginPage(page).goto()

    page.goto.assert_called_once_with(
        "https://staging.example.com/login", wait_until="domcontentloaded"
    )


def test_login_fills_email_and_password_and_clicks() -> None:
    page, locators = make_page_mock()

    LoginPage(page).login("user@test.com", "secret")

    locators['[data-qa="login-email"]'].fill.assert_called_once_with("user@test.com")
    locators['[data-qa="login-password"]'].fill.assert_called_once_with("secret")
    locators['[data-qa="login-button"]'].click.assert_called_once()


def test_login_with_test_user_raises_when_credentials_missing() -> None:
    page, _ = make_page_mock()

    with pytest.raises(RuntimeError, match="TEST_USER_EMAIL"):
        LoginPage(page).login_with_test_user()


@pytest.mark.parametrize(
    ("env", "value"),
    [("TEST_USER_EMAIL", "user@test.com"), ("TEST_USER_PASSWORD", "secret")],
)
def test_login_with_test_user_raises_when_only_one_credential_is_set(
    monkeypatch: pytest.MonkeyPatch, env: str, value: str
) -> None:
    monkeypatch.setenv(env, value)
    page, _ = make_page_mock()

    with pytest.raises(RuntimeError, match="TEST_USER_EMAIL"):
        LoginPage(page).login_with_test_user()


def test_login_with_test_user_logs_in_with_env_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    # assert_logged_in() usa expect() do Playwright, que nao funciona sobre um Page
    # mockado (nao e um Locator/Page real) - stub para isolar so a logica de delegacao.
    monkeypatch.setenv("TEST_USER_EMAIL", "user@test.com")
    monkeypatch.setenv("TEST_USER_PASSWORD", "secret")
    page, locators = make_page_mock()

    with patch("pages.login_page.expect"):
        LoginPage(page).login_with_test_user()

    locators['[data-qa="login-email"]'].fill.assert_called_once_with("user@test.com")
    locators['[data-qa="login-password"]'].fill.assert_called_once_with("secret")


def test_is_on_login_page_returns_true_when_url_reaches_login() -> None:
    page, _ = make_page_mock()

    assert LoginPage(page).is_on_login_page() is True
    page.wait_for_url.assert_called_once()


def test_is_on_login_page_returns_false_when_url_never_reaches_login() -> None:
    page, _ = make_page_mock()
    page.wait_for_url.side_effect = PlaywrightTimeoutError("timeout")

    assert LoginPage(page).is_on_login_page() is False
