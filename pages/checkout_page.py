from dataclasses import dataclass

from playwright.sync_api import Page, expect


@dataclass
class PaymentDetails:
    name_on_card: str
    card_number: str
    cvc: str
    expiry_month: str
    expiry_year: str


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def proceed_to_checkout(self) -> None:
        self.page.get_by_text("Proceed To Checkout").click()

    def assert_login_required_message(self) -> None:
        expect(
            self.page.get_by_text("Register / Login account to proceed on checkout.")
        ).to_be_visible()

    def place_order(self) -> None:
        self.page.locator('a:has-text("Place Order")').click()

    def fill_payment(self, details: PaymentDetails) -> None:
        self.page.locator('[data-qa="name-on-card"]').fill(details.name_on_card)
        self.page.locator('[data-qa="card-number"]').fill(details.card_number)
        self.page.locator('[data-qa="cvc"]').fill(details.cvc)
        self.page.locator('[data-qa="expiry-month"]').fill(details.expiry_month)
        self.page.locator('[data-qa="expiry-year"]').fill(details.expiry_year)
        self.page.locator('[data-qa="pay-button"]').click()

    def assert_order_placed(self) -> None:
        expect(self.page.get_by_text("Order Placed!")).to_be_visible()
