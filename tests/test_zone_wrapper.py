from replan2eplus.errors import InvalidEpBunchException
from replan2eplus.ezobjects.zone import Zone
from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from rich import print as rprint
import pytest


def test_init_with_zone(get_sample_idf):
    idf = get_sample_idf
    zones = idf.get_zones()
    zone = Zone(zones[0])
    assert zone  # TODO not the best test


def test_init_with_nonzone(get_sample_idf):
    with pytest.raises(InvalidEpBunchException) as excinfo:
        idf = get_sample_idf
        surfaces = idf.get_surfaces()
        zone = Zone(surfaces[0])
        assert "ZONE" in str(excinfo.value)


if __name__ == "__main__":
    pass
