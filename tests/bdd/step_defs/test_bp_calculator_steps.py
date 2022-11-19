from pytest_bdd import scenario, given, when, then, parsers


@scenario('../features/bp_calculator.feature',
          'Calculate blood preasure category')
def test_calc():
    pass


@given("a blood preasure calculator", target_fixture="calculator")
def goto_calc(browser):
    browser.visit('http://127.0.0.1:5000/')


@when(parsers.parse("systolic is {systolic:d} and diastolic is {diastolic:d}"))
def bp_fill_values(browser, systolic, diastolic):
    browser.fill('bpsystolic', str(systolic))
    browser.fill('bpdiastolic', str(diastolic))


@when("form is submitted")
def submit_form(browser):
    browser.find_by_css('input[type=submit]').first.click()


@then(parsers.parse("blood preasure category is {bp_category}"))
def bp_check(browser, bp_category):
    assert bp_category in browser.find_by_id('response').html
