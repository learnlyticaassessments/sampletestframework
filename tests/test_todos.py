import pytest
from tests.pages.todo_page import TodoPage


class TestTodoApp:
    @pytest.fixture
    def todo_page(self, page, base_url):
        return TodoPage(page, base_url).goto(base_url)

    @pytest.fixture(scope="function", autouse=True)
    def todo_page_with_items(self, todo_page: TodoPage):
        self.todo_page = todo_page
        # Add some default todo items before each test
        default_todos = ["Buy groceries", "Walk the dog", "Read a book"]
        todo_page.multiple_todos(default_todos)
        yield todo_page
        # Cleanup after test is done
        for _ in range(todo_page.todo_items.count()):
            todo_page.delete_todo(0)

    @pytest.mark.smoke
    def test_add_todo_and_verify_count(self):
        self.todo_page.goto(self.todo_page.base_url)
        assert self.todo_page.is_loaded(), "Todo page did not load successfully"

        # Add a new todo item
        self.todo_page.add_todo("Buy groceries")

        # Verify the todo count is updated
        count_text = self.todo_page.todo_count.text_content()
        assert "4 items left" in count_text, f"Expected '4 items left' but got '{count_text}'"

    def test_delete_todo_updates_item_count(self):
        self.todo_page.delete_todo(1)

        assert self.todo_page.todo_items.count() == 2
        count_text = self.todo_page.todo_count.text_content()
        assert "2 items left" in count_text, f"Expected '2 items left' but got '{count_text}'"

    def test_complete_todo_shows_clear_completed_and_active_count(self):
        self.todo_page.complete_todo(0)

        assert self.todo_page.clear_completed_button.is_visible()
        count_text = self.todo_page.todo_count.text_content()
        assert "2 items left" in count_text, f"Expected '2 items left' but got '{count_text}'"

    def test_clear_completed_removes_completed_items(self):
        self.todo_page.complete_todo(0)
        self.todo_page.clear_completed()

        assert self.todo_page.todo_items.count() == 2
        visible_todos = self.todo_page.visible_todo_texts()
        assert "Buy groceries" not in visible_todos

    def test_filter_active_shows_only_active_todos(self):
        self.todo_page.complete_todo(0)
        self.todo_page.filter_active_todos()

        assert self.todo_page.visible_todo_count() == 2
        visible_todos = self.todo_page.visible_todo_texts()
        assert "Buy groceries" not in visible_todos

    def test_filter_completed_shows_only_completed_todos(self):
        self.todo_page.complete_todo(0)
        self.todo_page.filter_completed_todos()

        assert self.todo_page.visible_todo_count() == 1
        visible_todos = self.todo_page.visible_todo_texts()
        assert visible_todos == ["Buy groceries"]
