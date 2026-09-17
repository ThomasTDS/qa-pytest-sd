import pytest

from pages.login_page import LoginPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def test_goto_uses_default_base_url_when_env_not_set() -> None:
    page, _ = make_page_mock()

    LoginPage(page).goto()

    page.goto.assert_called_once_with("https://automationexercise.com/login")


def test_goto_uses_base_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BASE_URL", "https://staging.example.com/")
    page, _ = make_page_mock()

    LoginPage(page).goto()

    page.goto.assert_called_once_with("https://staging.example.com/login")


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


def test_login_with_test_user_logs_in_with_env_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEST_USER_EMAIL", "user@test.com")
    monkeypatch.setenv("TEST_USER_PASSWORD", "secret")
    page, locators = make_page_mock()

    LoginPage(page).login_with_test_user()

    locators['[data-qa="login-email"]'].fill.assert_called_once_with("user@test.com")
    locators['[data-qa="login-password"]'].fill.assert_called_once_with("secret")
