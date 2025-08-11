from replan2eplus.zones.examples import TEST_ROOMS
from replan2eplus.zones.presentation import create_zones
from replan2eplus.ezobjects.object2D import EZObject2D
from replan2eplus.ezobjects.interfaces import EZObject

from replan2eplus.ezcase.examples import get_minimal_idf


def test_add_zones(get_pytest_minimal_idf):
    idf = get_pytest_minimal_idf
    zones, _ = create_zones(idf, TEST_ROOMS)
    assert len(zones) == len(TEST_ROOMS)

    # print("jhi")


if __name__ == "__main__":
    idf = get_minimal_idf()
    zones, surfaces = create_zones(idf, TEST_ROOMS)
    # EZObject2D(epbunch=)
