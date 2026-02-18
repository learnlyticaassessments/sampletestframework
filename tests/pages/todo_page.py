# can use locator,defines business actions , state queries

from .locators import TodoLocator
from playwright.sync_api import Page

class TodoPage:
    def __init__(self, page: Page, base_url: str = "https://demo.playwright.dev/todomvc"):
        self.page = page
        self.new_todo_input = page.locator(TodoLocator.NEW_TODO_CSS)
        self.todo_list = page.locator(TodoLocator.TODO_LIST_CSS)
        self.todo_items = page.locator(TodoLocator.TODO_ITEM_CSS)
        self.toggle_buttons = page.locator(TodoLocator.TOGGLE_CSS)
        self.destroy_buttons = page.locator(TodoLocator.DESTROY_CSS)
        self.todo_count = page.locator(TodoLocator.TODO_COUNT_CSS)
        self.clear_completed_button = page.locator(TodoLocator.CLEAR_COMPLETED_CSS)
        self.filter_active = page.locator(TodoLocator.FILTER_ACTIVE_CSS)
        self.filter_completed = page.locator(TodoLocator.FILTER_COMPLETED_CSS)  

# Assume no data_testid is speciefied for the elements, 
# we will use css selectors from locators.py

    def goto(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        return self
    
    def is_loaded(self):
        return self.new_todo_input.is_visible()
    
    #Busines actions-1
    def add_todo(self, todo_text: str):
        self.new_todo_input.fill(todo_text)
        self.new_todo_input.press("Enter")
        self.page.wait_for_timeout(500)  # wait for the todo to be added
        return self
    
    def multiple_todos(self, todos: list):
        for todo in todos:
            self.add_todo(todo)
        return self
    
    def delete_todo(self, index: int):
        self.todo_items.nth(index).hover()
        self.destroy_buttons.nth(index).click()
        self.page.wait_for_timeout(500)  # wait for the todo to be deleted
        return self
    
    def filter_active_todos(self):
        self.filter_active.click()
        self.page.wait_for_timeout(500)  # wait for the filter to apply
        return self
    
    def filter_completed_todos(self):
        self.filter_completed.click()
        self.page.wait_for_timeout(500)  # wait for the filter to apply
        return self
    


        


    
