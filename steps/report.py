import pytest

from conftest import REPORT_NOTES_STASH_KEY


def add_report_note(request: pytest.FixtureRequest, note: str) -> None:
    request.node.stash.setdefault(REPORT_NOTES_STASH_KEY, []).append(note)
