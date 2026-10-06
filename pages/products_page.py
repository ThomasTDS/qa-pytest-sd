import os

from playwright.sync_api import Page, expect

MAX_ADD_TO_CART_RETRIES = 2


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        self.page.goto(base_url + "products", wait_until="domcontentloaded")

    def search(self, term: str) -> None:
        self.page.locator("#search_product").fill(term)
        self.page.locator("#submit_search").click()

    def assert_search_results_visible(self) -> None:
        expect(self.page.get_by_text("Searched Products")).to_be_visible()
        expect(self.page.locator(".product-image-wrapper").first).to_be_visible()

    def add_product_to_cart(self, product_name: str) -> int:
        product_card = self.page.locator(".product-image-wrapper").filter(has_text=product_name)
        add_button = product_card.locator(".productinfo .add-to-cart")
        retries = 0
        while True:
            with self.page.expect_response(lambda r: "/add_to_cart/" in r.url) as response_info:
                add_button.click()
            if response_info.value.status < 500 or retries == MAX_ADD_TO_CART_RETRIES:
                break
            retries += 1
        close_button = self.page.locator('button.close-modal[data-dismiss="modal"]')
        expect(close_button).to_be_visible()
        close_button.click()
        return retries
