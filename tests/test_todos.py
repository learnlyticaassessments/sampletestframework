import pytest
from tests.conftest import base_url, page
from tests.pages.locators import TodoLocator
from tests.pages.todo_page import TodoPage

class TestTodoApp:
# smoke test

    def __init__(self, todo_page: TodoPage, base_url: str):
        self.todo_page = todo_page
        self.base_url = base_url

    @pytest.fixture
    def todo_page(page, base_url):
        return TodoPage(page, base_url).goto(base_url)

    @pytest.fixture(scope="function", autouse=True)
    def todo_page_with_items(todo_page: TodoPage):
        # Add some default todo items before each test
        default_todos = ["Buy groceries", "Walk the dog", "Read a book"]
        todo_page.multiple_todos(default_todos)
        yield todo_page
        # Cleanup after test is done
        for _ in range(todo_page.todo_items.count()):
            todo_page.delete_todo(0)


    @pytest.mark.smoke
    def test_add_todo_and_verify_count(todo_page: TodoPage):
        todo_page.goto(todo_page.base_url)
        assert todo_page.is_loaded(), "Todo page did not load successfully"
        
        # Add a new todo item
        todo_page.add_todo("Buy groceries")
        
        # Verify the todo count is updated
        count_text = todo_page.todo_count.text_content()
        assert "1 item left" in count_text, f"Expected '1 item left' but got '{count_text}'"

