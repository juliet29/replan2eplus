from replan2eplus.ezcase.defaults import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.ezcase.main import EZCase
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range
from replan2eplus.zones.interfaces import Room


def get_minimal_idf():
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF)
    return case.initialize_idf()


def get_minimal_case():
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF)
    case.initialize_idf()
    return case




RangeX1 = Range(0, 1)
RangeX2 = Range(1, 2)
RangeY1 = Range(0, 1)

Domain1 = Domain(RangeX1, RangeY1)
Domain2 = Domain(RangeX2, RangeY1)

Height = 3.05  # m


ROOM1 = "room1"
ROOM2 = "room2"

TEST_ROOMS = [Room(ROOM1, Domain1, Height), Room(ROOM2, Domain2, Height)]




def get_minimal_case_with_rooms():
    case =  get_minimal_case()
    case.add_zones(TEST_ROOMS)
    return case