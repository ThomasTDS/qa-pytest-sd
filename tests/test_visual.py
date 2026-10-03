import os
import sys
from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image, ImageChops
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.products_page import ProductsPage

pytestmark = [
    pytest.mark.visual,
    pytest.mark.skipif(
        sys.platform != "linux", reason="baselines são gerados em Linux (CI e Docker)"
    ),
]

BASELINES_DIR = Path("tests/visual_baselines")
FAILURES_DIR = Path("reports/visual")
CHANNEL_TOLERANCE = 16
MAX_DIFFERENT_PIXELS_RATIO = 0.001
# Anúncios do Google AdSense mudam a cada carregamento e alteram a altura da página.
THIRD_PARTY_CONTENT_CSS = "ins.adsbygoogle, iframe { display: none !important; }"
WAIT_FOR_IMAGES_JS = """() => Promise.all([...document.images].map(img => img.complete ? null :
    new Promise(resolve => { img.onload = img.onerror = resolve; })))"""


def assert_matches_baseline(page: Page, name: str, full_page: bool = True) -> None:
    browser_name = os.getenv("BROWSER", "chromium")
    baseline_path = BASELINES_DIR / f"{name}-{browser_name}.png"
    page.add_style_tag(content=THIRD_PARTY_CONTENT_CSS)
    page.evaluate(WAIT_FOR_IMAGES_JS)
    screenshot = page.screenshot(full_page=full_page, animations="disabled", caret="hide")
    actual = Image.open(BytesIO(screenshot)).convert("RGB")

    if os.getenv("UPDATE_VISUAL_BASELINES") == "1":
        BASELINES_DIR.mkdir(parents=True, exist_ok=True)
        actual.save(baseline_path)
        return

    if not baseline_path.exists():
        pytest.fail(f"Baseline ausente: {baseline_path}. Gere com UPDATE_VISUAL_BASELINES=1.")

    expected = Image.open(baseline_path).convert("RGB")
    if actual.size != expected.size:
        _save_failure(name, browser_name, actual, expected, None)
        pytest.fail(f"Dimensões diferentes: atual {actual.size}, baseline {expected.size}")

    diff = ImageChops.difference(actual, expected)
    red, green, blue = diff.split()
    max_channel_diff = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    changed = max_channel_diff.point(lambda v: 255 if v > CHANNEL_TOLERANCE else 0)
    different_pixels = changed.histogram()[255]
    ratio = different_pixels / (actual.width * actual.height)

    if ratio > MAX_DIFFERENT_PIXELS_RATIO:
        _save_failure(name, browser_name, actual, expected, changed)
        pytest.fail(f"{ratio:.4%} dos pixels mudaram (limite {MAX_DIFFERENT_PIXELS_RATIO:.2%})")


def _save_failure(
    name: str,
    browser_name: str,
    actual: Image.Image,
    expected: Image.Image,
    changed: Image.Image | None,
) -> None:
    FAILURES_DIR.mkdir(parents=True, exist_ok=True)
    prefix = FAILURES_DIR / f"{name}-{browser_name}"
    actual.save(f"{prefix}-atual.png")
    expected.save(f"{prefix}-baseline.png")
    if changed is not None:
        changed.save(f"{prefix}-diff.png")


def test_pagina_de_login_visualmente_estavel(page: Page, login_page: LoginPage) -> None:
    login_page.goto()

    assert_matches_baseline(page, "login")


def test_pagina_de_produtos_visualmente_estavel(page: Page, products_page: ProductsPage) -> None:
    products_page.goto()

    assert_matches_baseline(page, "produtos", full_page=False)
