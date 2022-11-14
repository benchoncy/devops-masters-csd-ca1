import pytest
from bpcalc import app


@pytest.fixture(scope="session")
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def splinter_webdriver():
    """Override splinter webdriver to flask."""
    return 'flask'


@pytest.fixture(scope='session')
def splinter_driver_kwargs():
    return {"app": app}
