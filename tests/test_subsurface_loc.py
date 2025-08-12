import pytest
from replan2eplus.geometry.range import Range
from replan2eplus.geometry.contact_points import (
    Nonant,
    NonantEntries,
    CornerEntries,
    CardinalEntries,
)
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.coords import Coord
import numpy as np


@pytest.fixture()
def base_domain():
    return Domain(Range(0, 3), Range(0, 3))


cardinal_groups: list[tuple[CardinalEntries, Coord]] = [
    ("NORTH", Coord(1.5, 3)),
    ("EAST", Coord(3, 1.5)),
    ("SOUTH", Coord(1.5, 0)),
    ("WEST", Coord(0, 1.5)),
]


@pytest.mark.parametrize("corner, coord", cardinal_groups)
def test_cardinal_points(corner, coord, base_domain):
    assert base_domain.cardinal[corner] == coord


corner_groups: list[tuple[CornerEntries, Coord]] = [
    ("NORTH_EAST", Coord(3, 3)),
    ("SOUTH_EAST", Coord(3, 0)),
    ("SOUTH_WEST", Coord(0, 0)),
    ("NORTH_WEST", Coord(0, 3)),
]


@pytest.mark.parametrize("corner, coord", corner_groups)
def test_corner_points(corner, coord, base_domain):
    assert base_domain.corner[corner] == coord


trirange_groups = [(Range(0, 3), 0, 1, 2, 3), (Range(-3, 0), -3, -2, -1, 0)]


@pytest.mark.parametrize("range, min, mid1, mid2, max", trirange_groups)
def test_create_trirange(range, min, mid1, mid2, max):
    trirange = range.trirange
    assert trirange.min == min
    assert trirange.mid1 == mid1
    assert trirange.mid2 == mid2
    assert trirange.max == max
    assert trirange.dist_between == 1


# TODO seems like something that could test with hypothesis
points_groups: list[tuple[NonantEntries, Coord]] = [
    # left
    ("bl", Coord(0, 0)),
    ("ml", Coord(0, 1)),
    ("tl", Coord(0, 2)),
    # middle
    ("bm", Coord(1, 0)),
    ("mm", Coord(1, 1)),
    ("tm", Coord(1, 2)),
    # right
    ("br", Coord(2, 0)),
    ("mr", Coord(2, 1)),
    ("tr", Coord(2, 2)),
]


@pytest.mark.parametrize("corner, coord", points_groups)
def test_nonant_points(corner, coord, base_domain):
    assert base_domain.nonant[corner] == coord


domain_groups: list[tuple[NonantEntries, Domain]] = [
    ("bl", Domain(Range(0, 1), Range(0, 1))),
    ("mm", Domain(Range(1, 2), Range(1, 2))),
    ("tr", Domain(Range(2, 3), Range(3, 3))),
    ("mr", Domain(Range(2, 3), Range(1, 2))),
]


@pytest.mark.skip()
@pytest.mark.parametrize("corner, expected_domain", domain_groups)
def test_nonant_domain(corner, expected_domain, base_domain):
    new_domain = create_nonant_domain(
        base_domain, corner
    )  # TODO can be nonant entry string..
    assert expected_domain == new_domain


# this would be a combinatorial thing..but just a few -> will test all cardinal points differently.. better yet -> is the same as if had defined the domain independently..
@pytest.mark.skip()
def test_get_corner_point_of_nonant_domain(base_domain):
    new_domain = create_nonant_domain(base_domain, "bl")
    new_domain.cardinal.NORTH == Coord(0.5, 1)


# if __name__ == "__main__":
#     range = Range(0,3)
#     res = np.linspace(range.min, range.max, num=4)
#     res2 = [i.item() for i in res]
#     print(res2)
