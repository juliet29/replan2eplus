import pytest

def test_ezcase(get_sample_idf):
    idf = get_sample_idf
    assert idf

def test_get_zones(get_sample_idf):
    idf = get_sample_idf
    zones = idf.get_zones()
    assert len(zones) == 3


def test_get_surfaces(get_sample_idf):
    idf = get_sample_idf
    surfaces = idf.get_surfaces()
    assert len(surfaces) > 3

