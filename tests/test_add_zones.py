from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range
from replan2eplus.zones.interfaces import Room
from replan2eplus.zones.presentation import create_zones

from replan2eplus.ezcase.examples import get_minimal_idf


RangeX1 = Range(0, 1)
RangeX2 = Range(0, 1)
RangeY1 = Range(0, 1)

Domain1 = Domain(RangeX1, RangeY1)
Domain2 = Domain(RangeX2, RangeY1)

Height = 3.05  # m

TEST_ROOMS = [Room("room1", Domain1, Height), Room("room2", Domain2, Height)]


def test_add_zones(get_pytest_minimal_idf):
    idf = get_pytest_minimal_idf
    zones, _ = create_zones(idf, TEST_ROOMS)
    assert len(zones) == 2

    # print("jhi")


if __name__ == "__main__":
    pass
