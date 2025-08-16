from replan2eplus.examples.minimal import get_minimal_case, get_minimal_idf, get_minimal_case_with_rooms
from replan2eplus.examples.existing import get_example_idf
import pytest
from replan2eplus.examples.minimal import TEST_ROOMS


@pytest.fixture()
def get_pytest_example_idf():
    return get_example_idf()


@pytest.fixture()
def get_pytest_minimal_idf(): # TODO these could be combined.. 
    return get_minimal_idf()


@pytest.fixture()
def get_pytest_minimal_case():
    return get_minimal_case()


@pytest.fixture()
def get_pytest_minimal_case_with_rooms():
    return get_minimal_case_with_rooms()
