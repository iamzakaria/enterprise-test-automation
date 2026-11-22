"""Page interactions live here; business assertions stay in tests."""

import allure
from playwright.sync_api import Page


class TaskPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.task_input = page.get_by_role("textbox", name="Task name")
        self.add_button = page.get_by_role("button", name="Add task", exact=True)
        self.tasks = page.get_by_role("list", name="Tasks").get_by_role("listitem")

    @allure.step("Open task board")
    def open(self) -> None:
        self.page.goto(self.base_url)

    @allure.step("Add a synthetic task")
    def add_task(self, name: str) -> None:
        self.task_input.fill(name)
        self.add_button.click()
