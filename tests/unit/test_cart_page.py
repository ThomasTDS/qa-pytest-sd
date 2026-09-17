import pytest

from pages.cart_page import CartPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def test_goto_uses_default_base_url_when_env_not_set() -> None:
    page, _ = make_page_mock()

    CartPage(page).goto()

    page.goto.assert_called_once_with("https://automationexercise.com/view_cart")


def test_goto_uses_base_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BASE_URL", "https://staging.example.com/")
    page, _ = make_page_mock()

    CartPage(page).goto()

    page.goto.assert_called_once_with("https://staging.example.com/view_cart")


def test_remove_product_filters_by_name_and_clicks_delete() -> None:
    page, locators = make_page_mock()

    CartPage(page).remove_product("Blue Top")

    row = locators["tr"]
    row.filter.assert_called_once_with(has_text="Blue Top")
    row.filter.return_value.locator.assert_called_once_with(".cart_quantity_delete")
    row.filter.return_value.locator.return_value.click.assert_called_once()
