import pytest


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("BASE_URL", "TEST_USER_EMAIL", "TEST_USER_PASSWORD"):
        monkeypatch.delenv(var, raising=False)
