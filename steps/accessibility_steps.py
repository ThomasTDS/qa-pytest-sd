import pytest
from pytest_bdd import then

from conftest import ACCESSIBILITY_NOTES_STASH_KEY
from pages.accessibility_page import AccessibilityPage


@then("a página não deve ter violações críticas de acessibilidade")
def assert_no_critical_accessibility_violations(
    accessibility_page: AccessibilityPage, request: pytest.FixtureRequest
) -> None:
    violations = accessibility_page.find_critical_or_serious_violations()
    if not violations:
        return

    details = "\n".join(
        f"- [{v['impact']}] {v['id']}: {v['description']} ({v['element_count']} elemento(s))"
        for v in violations
    )
    note = (
        "Violações de acessibilidade observadas na aplicação sob teste "
        f"(QA passivo, não bloqueia o teste):\n{details}"
    )
    request.node.stash.setdefault(ACCESSIBILITY_NOTES_STASH_KEY, []).append(note)
