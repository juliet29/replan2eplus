from replan2eplus.errors import InvalidEpBunchException
from replan2eplus.ezobjects.zone import Zone
from eppy.bunch_subclass import EpBunch
from rich import print as rprint
import pytest


def test_init_zone(get_pytest_example_idf):
    idf = get_pytest_example_idf
    zones = idf.get_zones()
    zone = Zone(zones[0])
    assert zone  # TODO not the best test


def test_init_zone_with_surface(get_pytest_example_idf):
    with pytest.raises(InvalidEpBunchException) as excinfo:
        idf = get_pytest_example_idf
        surfaces = idf.get_surfaces()
        Zone(surfaces[0])
        assert "ZONE" in str(excinfo.value)


if __name__ == "__main__":
    pass
