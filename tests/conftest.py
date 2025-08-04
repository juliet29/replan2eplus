from replan2eplus.ezcase.defaults import PATH_TO_IDD
from replan2eplus.ezcase.examples import get_example_idf, get_minimal_idf
from replan2eplus.ezcase.main import EZCase
from replan2eplus.paths import static_paths
import pytest


@pytest.fixture()
def get_pytest_example_idf():
    return get_example_idf()


@pytest.fixture()
def get_pytest_minimal_idf():
    return get_minimal_idf()
