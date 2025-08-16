from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass, field
from replan2eplus.ezobjects.base import EZObject

import replan2eplus.epnames.keys as epkeys
from replan2eplus.ezobjects.surface import Surface
from typing import Callable, Iterable, TypeVar, Any
from itertools import groupby

from replan2eplus.geometry.directions import WallNormal

T = TypeVar("T")


# TOOD move to utils 4 plans..
def sort_and_group_objects_dict(
    lst: Iterable[T], fx: Callable[[T], Any]
) -> dict[Any, list[T]]:
    sorted_objs = sorted(lst, key=fx)
    d = {}
    for k, g in groupby(sorted_objs, fx):
        d[k] = [i for i in list(g)]
    return d


@dataclass
class DirectedSurfaces:
    NORTH: list[Surface]
    EAST: list[Surface]
    SOUTH: list[Surface]
    WEST: list[Surface]
    UP: list[Surface]
    DOWN: list[Surface]

    # @property
    # def only(self):
    #     assert


@dataclass
class Zone(EZObject):
    _epbunch: EpBunch
    expected_key: str = epkeys.ZONE
    surfaces: list[Surface] = field(default_factory=list)

    @property
    def room_name(self):
        return self._dname.plan_name

    @property
    def zone_name(self):  # idf name?
        return self._idf_name

    @property
    def surface_names(self):
        return [i.surface_name for i in self.surfaces]

    @property
    def directed_surfaces(self):
        d: dict[WallNormal, list[Surface]] = sort_and_group_objects_dict(
            self.surfaces, lambda x: x.direction
        )
        d_names = {k.name: v for k, v in d.items()}
        return d_names  # DirectedSurfaces(**d_names)


# TODO create a parent class, but figure out visuals first..
