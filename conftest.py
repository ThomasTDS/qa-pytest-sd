import base64
import os
from collections.abc import Generator
from typing import Any

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright
from pytest_html import extras

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.contact_page import ContactPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.register_page import RegisterPage
from pages.security_page import SecurityPage

load_dotenv()

PAGE_STASH_KEY = pytest.StashKey[Page]()
SUPPORTED_BROWSERS = ("chromium", "firefox", "webkit")


@pytest.fixture
def page(request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    browser_name = os.getenv("BROWSER", "chromium")
    if browser_name not in SUPPORTED_BROWSERS:
        raise ValueError(f"BROWSER inválido: {browser_name!r}. Use um de {SUPPORTED_BROWSERS}.")
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)
        browser = browser_type.launch(headless=headless)
        pg = browser.new_page()
        request.node.stash[PAGE_STASH_KEY] = pg
        yield pg
        browser.close()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    return RegisterPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def contact_page(page: Page) -> ContactPage:
    return ContactPage(page)


@pytest.fixture
def security_page(page: Page) -> SecurityPage:
    return SecurityPage(page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]) -> Generator[None]:
    outcome = yield
    report = outcome.get_result()  # type: ignore[attr-defined]
    report_extras = getattr(report, "extras", [])

    if report.failed:
        page_fixture = item.stash.get(PAGE_STASH_KEY, None)
        if page_fixture is not None:
            screenshot_bytes = page_fixture.screenshot()
            encoded = base64.b64encode(screenshot_bytes).decode("utf-8")
            report_extras.append(extras.image(encoded, mime_type="image/png"))

    report.extras = report_extras
