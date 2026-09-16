import os

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        self.page.goto(base_url + "view_cart")

    def assert_product_in_cart(self, product_name: str) -> None:
        expect(self.page.locator("tr").filter(has_text=product_name)).to_be_visible()

    def assert_product_not_in_cart(self, product_name: str) -> None:
        expect(self.page.locator("tr").filter(has_text=product_name)).to_have_count(0)

    def remove_product(self, product_name: str) -> None:
        self.page.locator("tr").filter(has_text=product_name).locator(
            ".cart_quantity_delete"
        ).click()
