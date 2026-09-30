import base64
import os
import re
import time
from collections.abc import Generator
from pathlib import Path
from typing import Any

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext, Page, sync_playwright
from pytest_html import extras

from pages.accessibility_page import AccessibilityPage
from pages.api_page import ApiPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.contact_page import ContactPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.register_page import RegisterPage
from pages.security_page import SecurityPage

load_dotenv()

PAGE_STASH_KEY = pytest.StashKey[Page]()
CONTEXT_STASH_KEY = pytest.StashKey[BrowserContext]()
ACCESSIBILITY_NOTES_STASH_KEY = pytest.StashKey[list[str]]()
SUPPORTED_BROWSERS = ("chromium", "firefox", "webkit")
TRACES_DIR = Path("traces")


@pytest.fixture
def page(request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    browser_name = os.getenv("BROWSER", "chromium")
    if browser_name not in SUPPORTED_BROWSERS:
        raise ValueError(f"BROWSER inválido: {browser_name!r}. Use um de {SUPPORTED_BROWSERS}.")
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)
        browser = browser_type.launch(headless=headless)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        pg = context.new_page()
        request.node.stash[PAGE_STASH_KEY] = pg
        request.node.stash[CONTEXT_STASH_KEY] = context
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


@pytest.fixture
def api_page(page: Page) -> ApiPage:
    return ApiPage(page)


@pytest.fixture
def accessibility_page(page: Page) -> AccessibilityPage:
    return AccessibilityPage(page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]) -> Generator[None]:
    outcome = yield
    report = outcome.get_result()  # type: ignore[attr-defined]
    report_extras = getattr(report, "extras", [])

    if report.when == "call":
        context = item.stash.get(CONTEXT_STASH_KEY, None)
        if context is not None:
            if report.failed:
                TRACES_DIR.mkdir(parents=True, exist_ok=True)
                browser_name = os.getenv("BROWSER", "chromium")
                safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", item.name)
                trace_path = (
                    TRACES_DIR / f"{safe_name}-{browser_name}-{int(time.time() * 1000)}.zip"
                )
                context.tracing.stop(path=str(trace_path))
                trace_note = (
                    f'Trace salvo em {trace_path} (abrir com "playwright show-trace <arquivo>")'
                )
                report_extras.append(extras.text(trace_note))
                allure.attach(trace_note, name="trace", attachment_type=allure.attachment_type.TEXT)
            else:
                context.tracing.stop()

    if report.failed:
        page_fixture = item.stash.get(PAGE_STASH_KEY, None)
        if page_fixture is not None:
            screenshot_bytes = page_fixture.screenshot()
            encoded = base64.b64encode(screenshot_bytes).decode("utf-8")
            report_extras.append(extras.image(encoded, mime_type="image/png"))
            allure.attach(
                screenshot_bytes, name="screenshot", attachment_type=allure.attachment_type.PNG
            )

    if report.when == "call":
        for note in item.stash.get(ACCESSIBILITY_NOTES_STASH_KEY, []):
            report_extras.append(extras.text(note))
            allure.attach(note, name="acessibilidade", attachment_type=allure.attachment_type.TEXT)

    report.extras = report_extras
