from dataclasses import dataclass

from eppy.bunch_subclass import EpBunch
from eppy.geometry.surface import get_an_unit_normal, unit_normal
from geomeppy.geom.polygons import Polygon, Polygon3D
from rich import print as rprint

from replan2eplus.ezobjects.interfaces import EZObject
from replan2eplus.geometry.coords import Coordinate3D
from replan2eplus.geometry.domain import AXIS
from replan2eplus.geometry.plane import create_domain_from_coords


def compute_unit_normal(surface: EpBunch) -> AXIS:
    vector_map: dict[tuple[int, int, int], AXIS] = {
        (1, 0, 0): "X",
        (0, 1, 0): "Y",
        (0, 0, 1): "Z",
    }
    normal_vector = Polygon3D(surface.coords).normal_vector
    nv = tuple([abs(int(i)) for i in normal_vector])
    assert len(nv) == 3
    return vector_map[nv]


def get_surface_coords(surface: EpBunch):
    surf_coords = surface.coords
    assert surf_coords
    return [Coordinate3D(*i) for i in surf_coords]


def get_surface_domain(surface: EpBunch):
    unit_normal_drn = compute_unit_normal(surface)
    coords = get_surface_coords(surface)
    return create_domain_from_coords(unit_normal_drn, coords)


@dataclass
class EZObject2D(EZObject):
    @property
    def get_domain(self):
        return get_surface_domain(self.epbunch)
