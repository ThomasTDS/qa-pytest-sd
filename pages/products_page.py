import os

from playwright.sync_api import Page, expect

from pages.retry import is_visible, retry_while_failing


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> int:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        _, retries = retry_while_failing(
            first=lambda: self.page.goto(base_url + "products", wait_until="domcontentloaded"),
            again=lambda: self.page.reload(wait_until="domcontentloaded"),
            failed=lambda response: response is not None and response.status >= 500,
        )
        return retries

    def search(self, term: str) -> int:
        self.page.locator("#search_product").fill(term)
        _, retries = retry_while_failing(
            first=lambda: self.page.locator("#submit_search").click(),
            again=lambda: self.page.reload(wait_until="domcontentloaded"),
            failed=lambda _: not is_visible(self.page, "Searched Products"),
        )
        return retries

    def assert_search_results_visible(self) -> None:
        expect(self.page.get_by_text("Searched Products")).to_be_visible()
        expect(self.page.locator(".product-image-wrapper").first).to_be_visible()

    def add_product_to_cart(self, product_name: str) -> int:
        product_card = self.page.locator(".product-image-wrapper").filter(has_text=product_name)
        add_button = product_card.locator(".productinfo .add-to-cart")

        def click_and_get_status() -> int:
            with self.page.expect_response(lambda r: "/add_to_cart/" in r.url) as response_info:
                add_button.click()
            return response_info.value.status

        _, retries = retry_while_failing(
            first=click_and_get_status,
            again=click_and_get_status,
            failed=lambda status: status >= 500,
        )
        close_button = self.page.locator('button.close-modal[data-dismiss="modal"]')
        expect(close_button).to_be_visible()
        close_button.click()
        return retries
