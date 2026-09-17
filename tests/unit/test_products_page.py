import pytest

from pages.products_page import ProductsPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def test_goto_uses_default_base_url_when_env_not_set() -> None:
    page, _ = make_page_mock()

    ProductsPage(page).goto()

    page.goto.assert_called_once_with("https://automationexercise.com/products")


def test_goto_uses_base_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BASE_URL", "https://staging.example.com/")
    page, _ = make_page_mock()

    ProductsPage(page).goto()

    page.goto.assert_called_once_with("https://staging.example.com/products")


def test_search_fills_term_and_submits() -> None:
    page, locators = make_page_mock()

    ProductsPage(page).search("Top")

    locators["#search_product"].fill.assert_called_once_with("Top")
    locators["#submit_search"].click.assert_called_once()


def test_add_product_to_cart_filters_by_name_and_closes_modal() -> None:
    page, locators = make_page_mock()

    ProductsPage(page).add_product_to_cart("Blue Top")

    wrapper = locators[".product-image-wrapper"]
    wrapper.filter.assert_called_once_with(has_text="Blue Top")

    card = wrapper.filter.return_value
    card.locator.assert_called_once_with(".productinfo .add-to-cart")
    card.locator.return_value.click.assert_called_once()

    locators['button.close-modal[data-dismiss="modal"]'].click.assert_called_once()
