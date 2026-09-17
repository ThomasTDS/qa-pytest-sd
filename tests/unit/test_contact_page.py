import pytest

from pages.contact_page import ContactPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def test_goto_uses_contact_us_path() -> None:
    page, _ = make_page_mock()

    ContactPage(page).goto()

    page.goto.assert_called_once_with("https://automationexercise.com/contact_us")


def test_goto_home_uses_bare_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BASE_URL", "https://staging.example.com/")
    page, _ = make_page_mock()

    ContactPage(page).goto_home()

    page.goto.assert_called_once_with("https://staging.example.com/")


def test_submit_form_registers_dialog_handler_and_fills_fields() -> None:
    page, locators = make_page_mock()

    ContactPage(page).submit_form("QA", "user@test.com", "Assunto", "Mensagem")

    event, handler = page.once.call_args.args
    assert event == "dialog"
    assert callable(handler)

    locators['[data-qa="name"]'].fill.assert_called_once_with("QA")
    locators['[data-qa="email"]'].fill.assert_called_once_with("user@test.com")
    locators['[data-qa="subject"]'].fill.assert_called_once_with("Assunto")
    locators['[data-qa="message"]'].fill.assert_called_once_with("Mensagem")
    locators['[data-qa="submit-button"]'].click.assert_called_once()


def test_subscribe_to_newsletter_fills_email_and_clicks_subscribe() -> None:
    page, locators = make_page_mock()

    ContactPage(page).subscribe_to_newsletter("user@test.com")

    locators["#susbscribe_email"].fill.assert_called_once_with("user@test.com")
    locators["#subscribe"].click.assert_called_once()
