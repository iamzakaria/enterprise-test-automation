import logging
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import Page

from enterprise_qa.config import Settings
from enterprise_qa.pages.task_page import TaskPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def settings() -> Settings:
    try:
        value = Settings.from_env(os.environ)
    except ValueError as exc:
        raise pytest.UsageError(str(exc)) from exc
    logger.info("Test environment: %s", value.environment)
    return value


@pytest.fixture(scope="session")
def app_url(settings):
    if settings.base_url:
        yield settings.base_url
        return

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    demo = Path(__file__).resolve().parents[1] / "demo"
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(demo)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info("Local demo server started")
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def task_page(page: Page, app_url: str, settings: Settings) -> TaskPage:
    page.set_default_timeout(settings.timeout_ms)
    page.set_default_navigation_timeout(settings.timeout_ms)
    return TaskPage(page, app_url)
