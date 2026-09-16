import os

from playwright.sync_api import Page, expect


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        self.page.goto(base_url + "products")

    def search(self, term: str) -> None:
        self.page.locator("#search_product").fill(term)
        self.page.locator("#submit_search").click()

    def assert_search_results_visible(self) -> None:
        expect(self.page.get_by_text("Searched Products")).to_be_visible()
        expect(self.page.locator(".product-image-wrapper").first).to_be_visible()

    def add_product_to_cart(self, product_name: str) -> None:
        product_card = self.page.locator(".product-image-wrapper").filter(has_text=product_name)
        product_card.locator(".productinfo .add-to-cart").click()
        self.page.locator('button.close-modal[data-dismiss="modal"]').click()
