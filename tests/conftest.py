import pytest
from playwright.sync_api import Playwright, sync_playwright

from tests.utils.api_utils import BASE_URL


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture
def api_request(playwright_instance: Playwright):
    request_context = playwright_instance.request.new_context(base_url=BASE_URL)
    yield request_context
    request_context.dispose()
