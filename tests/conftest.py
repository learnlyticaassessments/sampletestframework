import pytest
from tests.pages.todo_page import TodoPage
from playwright.sync_api import Page, Browser, BrowserContext,sync_playwright
# launches browser and closes it after test is done

#Session scope for the browser, it will be launched once and closed after all tests are done
@pytest.fixture(scope="session")
def browwser_type_launch_args():
    return {
        "headless": True,
        "args": [
            "--disable-dev-shm-usage"
],
    }

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="session")
def browser():
        browser =sync_playwright().start().chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demo.playwright.dev/todomvc")
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }
#  base url for the tests
@pytest.fixture(scope="function")
def base_url():
    return "https://demo.playwright.dev/todomvc"

# Authentication
# @pytest.fixture(scope="function")
# def authentication_context(context):
#      context.add_cookies([{
#         "name": "auth_token",
#         "value": "your_auth_token",
#         "domain": "demo.playwright.dev",
#         "path": "/",
#      }])
#      return context

# cleanup storage after test is done
# @pytest.fixture(scope="function", autouse=True)
# def cleanup_storage(context):
#     yield
#     try:
#         Page.evaluate("localStorage.clear()")
#         Page.evaluate("sessionStorage.clear()")
#     except Exception as e:
#         print(f"Error during storage cleanup: {e}") 

@pytest.fixture(scope="function", autouse=True)
def log_test_name(request):
    """Print test name before each test runs."""
    print(f"\n{'='*60}")
    print(f"Running: {request.node.name}")
    print(f"{'='*60}")
    yield

# ── PYTEST HOOKS ─────────────────────────────────────────────────────────────
def pytest_configure(config):
    """Configure pytest - runs once at startup."""
    # Ensure reports directory exists
    import os
    os.makedirs("reports", exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Modify collected test items."""
    # Add 'smoke' marker to tests with 'smoke' in their name
    for item in items:
        if "smoke" in item.nodeid.lower():
            item.add_marker(pytest.mark.smoke)



