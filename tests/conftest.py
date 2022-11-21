import pytest
from bpcalc import app
from pytest_bdd import given
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


@given("a blood preasure calculator")
def goto_calc(page: Page, base_url):
    page.goto(base_url)
    expect(page).to_have_title("BPCalculator")
    form = page.locator("#bpform")
    expect(form).to_have_attribute("method", "post")