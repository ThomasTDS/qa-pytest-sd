from dataclasses import replace

import pytest

from pages.register_page import AccountInfo, RegisterPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def _account_info() -> AccountInfo:
    return AccountInfo(
        password="Secret123",
        first_name="QA",
        last_name="Tester",
        company="qa-pytest-sd",
        address="Rua de Teste, 123",
        state="SP",
        city="Sao Paulo",
        zipcode="01000-000",
        mobile_number="11999999999",
    )


def test_fill_account_information_fills_required_fields() -> None:
    page, locators = make_page_mock()

    RegisterPage(page).fill_account_information(_account_info())

    locators['[data-qa="password"]'].fill.assert_called_once_with("Secret123")
    locators['[data-qa="first_name"]'].fill.assert_called_once_with("QA")
    locators['[data-qa="last_name"]'].fill.assert_called_once_with("Tester")
    locators['[data-qa="company"]'].fill.assert_called_once_with("qa-pytest-sd")
    locators['[data-qa="address"]'].fill.assert_called_once_with("Rua de Teste, 123")
    locators['[data-qa="state"]'].fill.assert_called_once_with("SP")
    locators['[data-qa="city"]'].fill.assert_called_once_with("Sao Paulo")
    locators['[data-qa="zipcode"]'].fill.assert_called_once_with("01000-000")
    locators['[data-qa="mobile_number"]'].fill.assert_called_once_with("11999999999")
    locators["#days"].select_option.assert_called_once_with("10")
    locators["#months"].select_option.assert_called_once_with("5")
    locators["#years"].select_option.assert_called_once_with("1995")
    locators['[data-qa="create-account"]'].click.assert_called_once()


def test_fill_account_information_uses_custom_birth_date() -> None:
    page, locators = make_page_mock()
    info = replace(_account_info(), birth_day="1", birth_month="12", birth_year="2000")

    RegisterPage(page).fill_account_information(info)

    locators["#days"].select_option.assert_called_once_with("1")
    locators["#months"].select_option.assert_called_once_with("12")
    locators["#years"].select_option.assert_called_once_with("2000")


def test_fill_account_information_skips_country_when_not_set() -> None:
    page, locators = make_page_mock()

    RegisterPage(page).fill_account_information(_account_info())

    assert '[data-qa="country"]' not in locators


def test_fill_account_information_selects_country_when_set() -> None:
    page, locators = make_page_mock()
    info = replace(_account_info(), country="Canada")

    RegisterPage(page).fill_account_information(info)

    locators['[data-qa="country"]'].select_option.assert_called_once_with("Canada")


def test_submit_signup_fills_name_and_email_and_clicks() -> None:
    page, locators = make_page_mock()

    RegisterPage(page).submit_signup("QA Pytest SD", "user@test.com")

    locators['[data-qa="signup-name"]'].fill.assert_called_once_with("QA Pytest SD")
    locators['[data-qa="signup-email"]'].fill.assert_called_once_with("user@test.com")
    locators['[data-qa="signup-button"]'].click.assert_called_once()
