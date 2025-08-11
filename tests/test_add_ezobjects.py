from replan2eplus.zones.examples import TEST_ROOMS
from replan2eplus.zones.presentation import create_zones
from replan2eplus.ezcase.examples import get_minimal_idf

N_SURFACES_PER_CUBE = 6


def test_add_zones(get_pytest_minimal_idf):
    idf = get_pytest_minimal_idf
    zones, _ = create_zones(idf, TEST_ROOMS)
    assert len(zones) == len(TEST_ROOMS)

def test_add_surfaces_with_zones(get_pytest_minimal_idf):
    idf = get_pytest_minimal_idf
    _, surfaces = create_zones(idf, TEST_ROOMS)
    assert len(surfaces) == len(TEST_ROOMS)*N_SURFACES_PER_CUBE



if __name__ == "__main__":
    idf = get_minimal_idf()
    zones, surfaces = create_zones(idf, TEST_ROOMS)
    print(surfaces)
    # EZObject2D(epbunch=)
