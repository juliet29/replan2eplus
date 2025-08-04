from replan2eplus.ezcase.defaults import (
    PATH_TO_IDD,
    PATH_TO_MINIMAL_IDF,
    PATH_TO_SAMPLE_IDF,
)
from replan2eplus.ezcase.main import EZCase


def get_example_idf():
    case = EZCase(PATH_TO_IDD, PATH_TO_SAMPLE_IDF)
    return case.initialize_idf()


def get_minimal_idf():
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF)
    return case.initialize_idf()
