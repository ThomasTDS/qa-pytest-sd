from typing import TypedDict

from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

RELEVANT_IMPACTS = {"critical", "serious"}


class AccessibilityViolation(TypedDict):
    impact: str
    id: str
    description: str
    element_count: int


class AccessibilityPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._axe = Axe()

    def find_critical_or_serious_violations(self) -> list[AccessibilityViolation]:
        results = self._axe.run(self.page)
        return [
            AccessibilityViolation(
                impact=violation["impact"],
                id=violation["id"],
                description=violation["description"],
                element_count=len(violation["nodes"]),
            )
            for violation in results.response["violations"]
            if violation.get("impact") in RELEVANT_IMPACTS
        ]
