from replan2eplus.examples.minimal import get_minimal_case, get_minimal_idf
from replan2eplus.examples.existing import get_example_idf
import pytest


@pytest.fixture()
def get_pytest_example_idf():
    return get_example_idf()


@pytest.fixture()
def get_pytest_minimal_idf():
    return get_minimal_idf()


@pytest.fixture()
def get_pytest_minimal_case():
    return get_minimal_case()
