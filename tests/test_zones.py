from replan2eplus.examples.minimal import test_rooms
from replan2eplus.zones.presentation import create_zones
from replan2eplus.examples.minimal import get_minimal_idf
from replan2eplus.errors import InvalidEpBunchError
from replan2eplus.ezobjects.zone import Zone
import pytest
import replan2eplus.epnames.keys as keys


N_SURFACES_PER_CUBE = 6


## NOTE: this stuff applies to most ep objects and might be moved
def test_init_zone(get_pytest_example_idf):
    idf = get_pytest_example_idf
    zones = idf.get_zones()
    zone = Zone(zones[0])
    assert zone.expected_key == keys.ZONE  # TODO mayve test name?


def test_init_zone_with_surface(get_pytest_example_idf):
    with pytest.raises(InvalidEpBunchError) as excinfo:
        idf = get_pytest_example_idf
        surfaces = idf.get_surfaces()
        Zone(surfaces[0])
        assert "ZONE" in str(excinfo.value)


def test_zone_names(get_pytest_example_idf):  # TODO more thorough test of names..
    idf = get_pytest_example_idf
    zones = idf.get_zones()
    zone = Zone(zones[0])
    assert zone._dname.plan_name == "a"


## NOTE: This is more zone specific


def test_add_zones(get_pytest_minimal_idf):
    idf = get_pytest_minimal_idf
    zones, *_ = create_zones(idf, test_rooms)
    assert len(zones) == len(test_rooms)


def test_add_surfaces_with_zones(get_pytest_minimal_idf):
    idf = get_pytest_minimal_idf
    _, surfaces, _ = create_zones(idf, test_rooms)
    assert len(surfaces) == len(test_rooms) * N_SURFACES_PER_CUBE


if __name__ == "__main__":
    idf = get_minimal_idf()
    zones, surfaces, _ = create_zones(idf, test_rooms)
    print(surfaces)
    # EZObject2D(epbunch=)
