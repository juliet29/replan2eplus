from dataclasses import dataclass

from eppy.bunch_subclass import EpBunch

from replan2eplus.ezobjects.base import EZObject
from replan2eplus.geometry.coords import Coordinate3D
from replan2eplus.geometry.plane import create_domain_from_coords
from replan2eplus.geometry.plane import compute_unit_normal


def get_surface_coords(surface: EpBunch):
    surf_coords = surface.coords
    assert surf_coords
    return [Coordinate3D(*i) for i in surf_coords]


def get_surface_domain(surface: EpBunch):
    coords = get_surface_coords(surface)
    unit_normal_drn = compute_unit_normal([coord.as_three_tuple for coord in coords])
    return create_domain_from_coords(unit_normal_drn, coords)


@dataclass
class EZObject2D(EZObject):

    @property
    def get_domain(self):
        return get_surface_domain(self.epbunch)
