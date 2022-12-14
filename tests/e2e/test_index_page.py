import re
from playwright.sync_api import Page, expect
from pytest_bdd import scenario, when, then, parsers


@scenario('../features/bp_calculator.feature',
          'Calculate blood preasure category')
def test_calc_correct():
    pass


@scenario('../features/bp_calculator_feedback.feature',
          'Input incorrect values into the calculator')
def test_calc_incorrect_values():
    pass


@when(parsers.parse("systolic is {systolic} and diastolic is {diastolic}"))
def bp_fill_values(page: Page, systolic, diastolic):
    page.locator("input[name=bpsystolic]").fill(str(systolic))
    page.locator("input[name=bpdiastolic]").fill(str(diastolic))


@when("form is submitted")
def submit(page: Page):
    page.locator("input[type=submit]").click()


@then(parsers.parse("blood preasure category is {bp_category}"))
def bp_check_value(page: Page, bp_category):
    response = page.locator('#response')
    regex = re.compile(bp_category)
    expect(response).to_have_text(regex)


@then(parsers.parse("error should list \"{error}\""))
def bp_check_error(page: Page, error):
    alert = page.locator('#bpform .alert')
    regex = re.compile(error)
    expect(alert).to_have_text(regex)
