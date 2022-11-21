import re
from playwright.sync_api import Page, expect


class TestIndexPage():
    def test_has_title_and_form(self, page: Page, base_url):
        page.goto(base_url)
        expect(page).to_have_title("BPCalculator")
        form = page.locator("#bpform")
        expect(form).to_have_attribute("method", "post")