import os
import re

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        self.page.goto(base_url + "login")

    def login(self, email: str, password: str) -> None:
        self.page.locator('[data-qa="login-email"]').fill(email)
        self.page.locator('[data-qa="login-password"]').fill(password)
        self.page.locator('[data-qa="login-button"]').click()

    def login_with_test_user(self) -> None:
        email = os.getenv("TEST_USER_EMAIL")
        password = os.getenv("TEST_USER_PASSWORD")
        if not email or not password:
            raise RuntimeError(
                "TEST_USER_EMAIL e TEST_USER_PASSWORD precisam estar definidos (veja .env.example)"
            )
        self.login(email, password)
        self.assert_logged_in()

    def assert_logged_in(self) -> None:
        expect(self.page.locator('a:has-text("Logged in as")')).to_be_visible()

    def assert_error_message(self, expected_error: str) -> None:
        expect(self.page.locator(".login-form p")).to_have_text(expected_error)

    def logout(self) -> None:
        self.page.locator('a[href="/logout"]').click()

    def assert_logged_out(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/login$"))
        expect(self.page.locator('a:has-text("Logged in as")')).to_have_count(0)
