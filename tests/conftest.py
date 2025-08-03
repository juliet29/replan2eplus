from replan2eplus.ezcase.defaults import PATH_TO_IDD
from replan2eplus.ezcase.main import EZCase
from replan2eplus.paths import static_paths
import pytest


SAMPLE_IDF = "three_plan/out.idf"


@pytest.fixture()
def get_sample_idf():
    case = EZCase(PATH_TO_IDD, static_paths.models / SAMPLE_IDF)
    return case.initialize_idf()
