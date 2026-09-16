import os

from playwright.sync_api import Page, expect


class ContactPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        self.page.goto(base_url + "contact_us")

    def goto_home(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        self.page.goto(base_url)

    def submit_form(self, name: str, email: str, subject: str, message: str) -> None:
        self.page.once("dialog", lambda dialog: dialog.accept())

        self.page.locator('[data-qa="name"]').fill(name)
        self.page.locator('[data-qa="email"]').fill(email)
        self.page.locator('[data-qa="subject"]').fill(subject)
        self.page.locator('[data-qa="message"]').fill(message)
        self.page.locator('[data-qa="submit-button"]').click()

    def assert_message_sent(self) -> None:
        expect(
            self.page.locator("#contact-page").get_by_text(
                "Success! Your details have been submitted successfully."
            )
        ).to_be_visible()

    def subscribe_to_newsletter(self, email: str) -> None:
        input_field = self.page.locator("#susbscribe_email")
        input_field.scroll_into_view_if_needed()
        input_field.fill(email)

        button = self.page.locator("#subscribe")
        button.scroll_into_view_if_needed()
        button.click()

    def assert_subscribed(self) -> None:
        expect(self.page.locator("#success-subscribe")).to_have_text(
            "You have been successfully subscribed!"
        )
