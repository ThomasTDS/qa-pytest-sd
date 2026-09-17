import pytest

from pages.checkout_page import CheckoutPage, PaymentDetails
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def test_fill_payment_fills_each_field_into_the_matching_locator() -> None:
    page, locators = make_page_mock()
    details = PaymentDetails(
        name_on_card="QA Pytest SD",
        card_number="4111111111111111",
        cvc="123",
        expiry_month="12",
        expiry_year="2030",
    )

    CheckoutPage(page).fill_payment(details)

    locators['[data-qa="name-on-card"]'].fill.assert_called_once_with("QA Pytest SD")
    locators['[data-qa="card-number"]'].fill.assert_called_once_with("4111111111111111")
    locators['[data-qa="cvc"]'].fill.assert_called_once_with("123")
    locators['[data-qa="expiry-month"]'].fill.assert_called_once_with("12")
    locators['[data-qa="expiry-year"]'].fill.assert_called_once_with("2030")
    locators['[data-qa="pay-button"]'].click.assert_called_once()


def test_proceed_to_checkout_clicks_the_right_text() -> None:
    page, _ = make_page_mock()

    CheckoutPage(page).proceed_to_checkout()

    page.get_by_text.assert_called_once_with("Proceed To Checkout")
    page.get_by_text.return_value.click.assert_called_once()


def test_place_order_clicks_place_order_link() -> None:
    page, locators = make_page_mock()

    CheckoutPage(page).place_order()

    locators['a:has-text("Place Order")'].click.assert_called_once()
