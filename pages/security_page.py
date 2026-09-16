import os

from playwright.sync_api import Page, expect


class SecurityPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def assert_security_headers_present(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        response = self.page.request.get(base_url)
        headers = response.headers
        assert headers.get("x-frame-options") == "DENY"
        assert headers.get("x-content-type-options") == "nosniff"

    def assert_http_redirects_to_https(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        http_url = base_url.replace("https://", "http://")
        response = self.page.request.get(http_url)
        assert response.url.startswith("https://")

    def assert_password_field_is_masked(self) -> None:
        base_url = os.getenv("BASE_URL", "https://automationexercise.com/")
        self.page.goto(base_url + "login")
        expect(self.page.locator('[data-qa="login-password"]')).to_have_attribute(
            "type", "password"
        )

    def assert_session_cookie_is_http_only(self) -> None:
        cookies = self.page.context.cookies()
        session_cookie = next((cookie for cookie in cookies if cookie["name"] == "sessionid"), None)
        assert session_cookie is not None
        assert session_cookie["httpOnly"] is True
