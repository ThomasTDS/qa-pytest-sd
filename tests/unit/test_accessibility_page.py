from unittest.mock import MagicMock, patch

import pytest

from pages.accessibility_page import AccessibilityPage
from tests.unit.mocks import make_page_mock

pytestmark = pytest.mark.unit


def make_axe_results(violations: list[dict[str, object]]) -> MagicMock:
    results = MagicMock(name="axe_results")
    results.response = {"violations": violations}
    return results


def make_violation(impact: str | None, violation_id: str = "color-contrast") -> dict[str, object]:
    return {
        "id": violation_id,
        "impact": impact,
        "description": f"descricao de {violation_id}",
        "nodes": [{}, {}],
    }


def test_find_critical_or_serious_violations_keeps_only_critical_and_serious() -> None:
    page, _ = make_page_mock()
    violations = [
        make_violation("critical", "button-name"),
        make_violation("serious", "color-contrast"),
        make_violation("moderate", "region"),
        make_violation("minor", "landmark-one-main"),
    ]

    with patch("pages.accessibility_page.Axe") as axe_cls:
        axe_cls.return_value.run.return_value = make_axe_results(violations)
        result = AccessibilityPage(page).find_critical_or_serious_violations()

    assert [v["id"] for v in result] == ["button-name", "color-contrast"]


def test_find_critical_or_serious_violations_maps_fields_for_report() -> None:
    page, _ = make_page_mock()

    with patch("pages.accessibility_page.Axe") as axe_cls:
        axe_cls.return_value.run.return_value = make_axe_results(
            [make_violation("critical", "button-name")]
        )
        result = AccessibilityPage(page).find_critical_or_serious_violations()

    assert result == [
        {
            "impact": "critical",
            "id": "button-name",
            "description": "descricao de button-name",
            "element_count": 2,
        }
    ]


def test_find_critical_or_serious_violations_ignores_violations_without_impact() -> None:
    page, _ = make_page_mock()

    with patch("pages.accessibility_page.Axe") as axe_cls:
        axe_cls.return_value.run.return_value = make_axe_results([make_violation(None)])
        result = AccessibilityPage(page).find_critical_or_serious_violations()

    assert result == []


def test_find_critical_or_serious_violations_returns_empty_when_page_is_clean() -> None:
    page, _ = make_page_mock()

    with patch("pages.accessibility_page.Axe") as axe_cls:
        axe_cls.return_value.run.return_value = make_axe_results([])
        result = AccessibilityPage(page).find_critical_or_serious_violations()

    assert result == []


def test_find_critical_or_serious_violations_runs_axe_against_the_page() -> None:
    page, _ = make_page_mock()

    with patch("pages.accessibility_page.Axe") as axe_cls:
        axe_cls.return_value.run.return_value = make_axe_results([])
        AccessibilityPage(page).find_critical_or_serious_violations()

    axe_cls.return_value.run.assert_called_once_with(page)
