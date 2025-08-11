from typing import Callable
from replan2eplus.geometry.coords import Coordinate3D
from replan2eplus.geometry.domain import AXIS, Plane
from replan2eplus.geometry.range import Range
from replan2eplus.geometry.domain import Domain
from dataclasses import dataclass
import pytest
from replan2eplus.geometry.plane import create_domain_from_coords
from replan2eplus.geometry.plane import compute_unit_normal_coords


@dataclass
class Bounds:
    tr: Coordinate3D
    tl: Coordinate3D
    bl: Coordinate3D
    br: Coordinate3D

    def to_list(self):
        return [self.tr, self.tl, self.bl, self.br]


def create_bounds_from_ranges(normal_plane: AXIS, x: Range, y: Range, z: Range):
    match normal_plane:
        case "Y":
            assert y.min == y.max
            yloc = y.min
            bounds = Bounds(
                tr=Coordinate3D(x.max, yloc, z.max),
                tl=Coordinate3D(x.min, yloc, z.max),
                bl=Coordinate3D(x.min, yloc, z.min),
                br=Coordinate3D(x.max, yloc, z.min),
            )

        case "X":
            assert x.min == x.max
            xloc = x.min
            bounds = Bounds(
                tr=Coordinate3D(xloc, y.max, z.max),
                tl=Coordinate3D(xloc, y.min, z.max),
                bl=Coordinate3D(xloc, y.min, z.min),
                br=Coordinate3D(xloc, y.max, z.min),
            )
        case "Z":
            assert z.min == z.max
            zloc = z.min
            bounds = Bounds(
                tr=Coordinate3D(x.max, y.max, zloc),
                tl=Coordinate3D(x.min, y.max, zloc),
                bl=Coordinate3D(x.min, y.min, zloc),
                br=Coordinate3D(x.max, y.min, zloc),
            )

    return bounds.to_list()


simple_range = Range(0, 1)
fixed_range = Range(1, 1)
# surface in the YZ Plane


def create_coords_for_surface_normal_x():  # normal to x
    x = fixed_range
    y = simple_range
    z = simple_range
    return create_bounds_from_ranges("X", x, y, z)


def create_coords_for_surface_normal_y():  # normal to y
    x = simple_range
    y = fixed_range
    z = simple_range
    return create_bounds_from_ranges("Y", x, y, z)


def create_coords_for_surface_normal_z():
    x = simple_range
    y = simple_range
    z = fixed_range
    return create_bounds_from_ranges("Z", x, y, z)


test_planes = [
    ("X", create_coords_for_surface_normal_x),
    ("Y", create_coords_for_surface_normal_y),
    ("Z", create_coords_for_surface_normal_z),
]


@pytest.mark.parametrize("plane, create_coords_fx", test_planes)
def test_find_normal(plane: AXIS, create_coords_fx: Callable[[], list[Coordinate3D]]):
    coords = create_coords_fx()
    tuple_coords = [i.as_tuple for i in coords]
    normal_axis = compute_unit_normal_coords(tuple_coords)
    assert normal_axis == plane


test_domains = [
    (
        "X",
        create_coords_for_surface_normal_x,
        Domain(simple_range, simple_range, plane=Plane("X", 1.0)),
    ),
    (
        "Y",
        create_coords_for_surface_normal_y,
        Domain(simple_range, simple_range, plane=Plane("Y", 1.0)),
    ),
    (
        "Z",
        create_coords_for_surface_normal_z,
        Domain(simple_range, simple_range, plane=Plane("Z", 1.0)),
    ),
]


@pytest.mark.parametrize("plane, create_coords_fx, expected_domain", test_domains)
def test_create_domain_in_correct_plane(plane, create_coords_fx, expected_domain):
    coords = create_coords_fx()
    true_domain = create_domain_from_coords(plane, coords)
    assert true_domain == expected_domain


if __name__ == "__main__":
    pass
    # test_find_normal()
