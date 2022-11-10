import pytest
from bpcalc import validate_values, get_bp_category, BPCategory, app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_validate_values():
    assert validate_values(100, 80) is None
    assert validate_values(80, 100) is not None
    assert validate_values(60, 50) is not None
    assert validate_values(80, 110) is not None
    assert validate_values(50, 150) is not None


def test_get_bp_category():
    assert get_bp_category(80, 50) == BPCategory.LOW
    assert get_bp_category(110, 70) == BPCategory.IDEAL
    assert get_bp_category(130, 80) == BPCategory.PRE_HIGH
    assert get_bp_category(160, 90) == BPCategory.HIGH
    assert get_bp_category(90, 60) == BPCategory.IDEAL
    assert get_bp_category(90, 50) == BPCategory.IDEAL


def test_index_page(client):
    response = client.get('/')
    assert b'BPCalculator' in response.data


def test_index_form(client):
    response = client.post("/", data={
        "bpsystolic": "100",
        "bpdiastolic": "80",
    })
    assert b'pre-high' in response.data
    response = client.post("/", data={
        "bpsystolic": "500",
        "bpdiastolic": "80",
    })
    assert b'Error' in response.data
