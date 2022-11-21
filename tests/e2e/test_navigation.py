from playwright.sync_api import Page, expect
from pytest_bdd import scenario, when, then, parsers


@scenario('../features/navigation.feature',
          'Navigate to home page')
def test_nav():
    pass


@when(parsers.parse("Navigation button \"{button_name}\" exists"),
      target_fixture="button")
def verify_button(page: Page, button_name):
    nav = page.locator(".navbar-nav")
    button = nav.get_by_text(button_name)
    return button


@when(parsers.parse("Navigation button is clicked"))
def click_button(button):
    button.click()


@then(parsers.parse("url should be \"{route}\""))
def verify_route(page: Page, route):
    expect(page).to_have_url(route)
