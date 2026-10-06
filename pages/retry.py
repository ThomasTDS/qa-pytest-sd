from collections.abc import Callable

from playwright.sync_api import Page, expect

MAX_RETRIES = 2


def retry_while_failing[T](
    first: Callable[[], T],
    again: Callable[[], T],
    failed: Callable[[T], bool],
    max_retries: int = MAX_RETRIES,
) -> tuple[T, int]:
    result = first()
    retries = 0
    while failed(result) and retries < max_retries:
        retries += 1
        result = again()
    return result, retries


def is_visible(page: Page, text: str, timeout_ms: int = 10_000) -> bool:
    try:
        expect(page.get_by_text(text)).to_be_visible(timeout=timeout_ms)
    except AssertionError:
        return False
    return True


def assert_visible(page: Page, text: str) -> None:
    expect(page.get_by_text(text)).to_be_visible()
