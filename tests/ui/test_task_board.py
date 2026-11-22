import allure
import pytest
from playwright.sync_api import expect


@allure.feature("Task board")
@pytest.mark.smoke
def test_add_task(task_page):
    task_page.open()
    expect(task_page.page).to_have_title("Quality Engineering Task Board")
    expect(task_page.tasks).to_have_count(0)
    task_page.add_task("Review synthetic release checklist")
    expect(task_page.tasks).to_have_text(["Review synthetic release checklist"])
    expect(task_page.task_input).to_be_empty()
    expect(task_page.page.get_by_role("status")).to_have_text("1 task(s) added")


@allure.feature("Task board")
def test_whitespace_task_is_rejected(task_page):
    task_page.open()
    task_page.add_task("   ")
    expect(task_page.tasks).to_have_count(0)
    expect(task_page.page.get_by_role("status")).to_have_text("Enter a task name")


@allure.feature("Task board")
def test_task_text_is_rendered_literally(task_page):
    task_page.open()
    task_page.add_task("<strong>Synthetic task</strong>")
    expect(task_page.tasks).to_have_text(["<strong>Synthetic task</strong>"])
    expect(task_page.tasks.locator("strong")).to_have_count(0)
