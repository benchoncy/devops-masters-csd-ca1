from pytest_bdd import scenario, given, when, then, parsers


@scenario('../../features/bp_calculator.feature',
          'Calculate blood preasure category')
def test_calc():
    pass


@given("a blood preasure calculator")
def goto_calc(client):
    response = client.get('/')
    assert response.status_code == 200


@when(parsers.parse("systolic is {systolic:d} and diastolic is {diastolic:d}"),
      target_fixture="data")
def bp_fill_values(systolic, diastolic):
    data = {
        "bpsystolic": systolic,
        "bpdiastolic": diastolic
    }
    return data


@when("form is submitted",
      target_fixture="response")
def submit(client, data):
    response = client.post("/", data=data)
    return response


@then(parsers.parse("blood preasure category is {bp_category}"))
def bp_check(response, bp_category):
    assert str.encode(bp_category) in response.data
