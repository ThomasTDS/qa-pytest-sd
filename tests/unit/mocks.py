from unittest.mock import MagicMock

PageMock = tuple[MagicMock, dict[str, MagicMock]]


def make_page_mock() -> PageMock:
    # cada seletor único sempre resolve para o mesmo Mock, permitindo
    # asserções isoladas por seletor (locators['#foo'].fill.assert_called_once_with(...))
    page = MagicMock(name="page")
    locators: dict[str, MagicMock] = {}

    def locator_side_effect(selector: str, *_args: object, **_kwargs: object) -> MagicMock:
        return locators.setdefault(selector, MagicMock(name=f"locator({selector!r})"))

    page.locator.side_effect = locator_side_effect
    return page, locators
