from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config.settings import settings
from framework.api.client import BettingApiClient

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "reports" / "screenshots"


@pytest.fixture(scope="session")
def config():
    if not settings.user_id:
        pytest.exit("USER_ID is not set. Copy .env.example to .env and fill it in.", returncode=2)
    return settings


@pytest.fixture(scope="session")
def api_client(config) -> BettingApiClient:
    return BettingApiClient(config.base_url, config.user_id, timeout=config.api_timeout_seconds)


@pytest.fixture
def fresh_balance(api_client) -> float:
    api_client.reset_balance().raise_for_status()
    return api_client.get_balance_amount()


@pytest.fixture
def upcoming_match(api_client) -> dict:
    matches = api_client.upcoming_matches()
    if not matches:
        pytest.skip("No upcoming matches available to bet on")
    return matches[0]


@pytest.fixture
def driver(config, request):
    options = Options()
    if config.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    for arg in config.chrome_args.split():
        options.add_argument(arg)
    if config.chrome_binary:
        options.binary_location = config.chrome_binary
    service = Service(executable_path=config.chromedriver_path) if config.chromedriver_path else Service()
    browser = webdriver.Chrome(options=options, service=service)
    yield browser

    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        browser.save_screenshot(str(SCREENSHOT_DIR / f"{request.node.name}.png"))
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
