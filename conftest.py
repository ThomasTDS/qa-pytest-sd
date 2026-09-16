import base64
import os
from collections.abc import Generator
from typing import Any

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright
from pytest_html import extras

from pages.login_page import LoginPage
from pages.register_page import RegisterPage

load_dotenv()

PAGE_STASH_KEY = pytest.StashKey[Page]()


@pytest.fixture
def page(request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
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
