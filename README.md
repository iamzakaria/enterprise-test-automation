# Enterprise Test Automation Framework

Project 1 of a five-project Software Quality Engineering portfolio. This first increment provides a runnable Python + Playwright + Pytest foundation, with page objects, validated environment configuration, Allure result generation, and GitHub Actions.

## Architecture

```text
src/enterprise_qa/
  config.py              # immutable, validated environment settings
  pages/task_page.py     # accessible locators and reusable interactions
tests/
  conftest.py            # configuration, local server, page fixtures
  unit/test_config.py    # environment and URL validation
  ui/test_task_board.py  # browser journeys and business assertions
demo/index.html          # synthetic, deterministic test application
.github/workflows/tests.yml
requirements.lock        # exact installed dependency versions
```

Tests own assertions; page objects own interactions. The official pytest-playwright plugin owns browser/context/page lifecycle and gives every UI test a fresh browser context. A session-scoped server binds to an ephemeral loopback port and serves only the demo directory; fixture teardown stops it. There are no fixed sleeps, external demo-service dependencies, credentials, or production integrations.

This is a foundation, not a claim of production readiness. The demo is an in-memory task board with no backend or persistence. Authentication, API clients, parallel execution, additional browsers, and container execution are future increments. Projects 2–5 are maintained as separate sibling repositories in the portfolio.

## macOS Apple Silicon setup

Use a native arm64 terminal and Python 3.12. Current Playwright documentation requires macOS 14 or newer. Homebrew on Apple Silicon normally resides at `/opt/homebrew`.

```bash
brew install python@3.12
cd /path/to/enterprise-test-automation
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps -e .
python -m playwright install chromium
python -m pytest
```

The first browser installation needs network access. No separately started app is required. If browser binaries are missing after updating Playwright, run the install command again. Do not use sudo pip. Check `python -c 'import platform; print(platform.machine())'` if a terminal is running under Rosetta.

## Run and debug

```bash
python -m pytest tests/unit
python -m pytest -m smoke --browser chromium
python -m pytest tests/ui --headed
python -m pytest --junitxml=artifacts/junit.xml
ruff check .
ruff format --check .
```

Default runs are headless Chromium. Firefox/WebKit can be explored by installing their binaries and selecting `--browser firefox` or `--browser webkit`; they are not part of the initial verified baseline.

## Environments and secrets

| Variable | Default | Meaning |
| --- | --- | --- |
| `TEST_ENV` | `local` | `local`, `qa`, or `staging` |
| `BASE_URL` | unset | Optional local override; required for qa/staging |
| `UI_TIMEOUT_MS` | `5000` | Positive action/navigation timeout |

The `.env.example` file is documentation; it is not automatically loaded. Export variables explicitly. A remote target must serve this same demo application's interface; these tests cannot exercise an arbitrary website without new page objects and assertions.

```bash
TEST_ENV=qa BASE_URL=https://your-demo-host.example/ python -m pytest tests/ui
```

Invalid environment configuration fails before browser navigation. URLs with embedded credentials, query parameters, or fragments are rejected. Future credentials should come from environment variables or CI secrets, never committed files. Trace files, screenshots, and reports can contain application data: use synthetic data and review artifacts before sharing.

## Reports and failure evidence

Each run writes fresh Allure results to `artifacts/allure-results`. Pytest's Playwright plugin retains screenshots and traces for failures under `artifacts/playwright`. The directories are ignored by Git. Each run replaces previous results: copy evidence before another run if needed.

```bash
brew install allure
allure serve artifacts/allure-results
# Use the actual trace path printed by the test run:
python -m playwright show-trace artifacts/playwright/<test-folder>/trace.zip
```

Allure CLI is optional; the Python adapter generates results without it. Browser artifacts are separate files, not embedded Allure attachments in this increment. Pytest's captured logs are included by the Allure adapter. Tests do not retry automatically, so failures stay visible.

## CI and repository setup

GitHub Actions installs pinned Python dependencies and Chromium with Linux system dependencies, checks lint/formatting, executes tests, and uploads JUnit, Allure results, and failure artifacts even when tests fail. Artifacts expire after seven days. The workflow has read-only repository permissions and a 15-minute job timeout.

This folder is a standalone local Git repository. No GitHub remote, commit, or push is created automatically. Publish its contents at a repository root so GitHub recognizes `.github/workflows/tests.yml`. Review the initial files with `git status` before creating your first commit.

## Extension sequence

1. Add application-specific page objects and meaningful regression journeys.
2. Add API setup/cleanup and authentication fixtures when a real test target exists.
3. Establish Firefox/WebKit and parallel-worker coverage, then container support.
4. Expand CI quality gates using measured reliability and runtime.
5. Use `continuous-quality-platform` to run this baseline alongside Projects 2–4.

## References

- [Playwright installation and requirements](https://playwright.dev/python/docs/intro)
- [Playwright Pytest fixtures and CLI options](https://playwright.dev/python/docs/test-runners)
- [Playwright CI](https://playwright.dev/python/docs/ci)
- [Allure Pytest configuration](https://allurereport.org/docs/pytest-configuration/)

## Executed validation

See [VALIDATION.md](VALIDATION.md) for the observed 16-test pass, failure-artifact check, dependency warning, and verification boundaries.
