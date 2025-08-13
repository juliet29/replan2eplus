from dataclasses import dataclass
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.nonant import Nonant, NonantEntries
from replan2eplus.geometry.range import Range
from replan2eplus.geometry.contact_points import (
    CardinalEntries,
    CornerEntries,
    CornerPoints,
)
from typing import Literal, NamedTuple, Union
from replan2eplus.geometry.domain_calcs import (
    BaseDomain,
    calculate_cardinal_points,
    calculate_corner_points,
)

AXIS = Literal["X", "Y", "Z"]


class Plane(NamedTuple):
    axis: AXIS
    location: float


@dataclass(frozen=True)
class Domain(BaseDomain):
    plane: Plane | None = None

    @property
    def area(self):
        return self.horz_range.size * self.vert_range.size

    @property
    def aspect_ratio(self):
        return self.horz_range.size / self.vert_range.size

    @property
    def centroid(self):
        return Coord(self.horz_range.midpoint, self.vert_range.midpoint)

    @property
    def cardinal(self):
        return calculate_cardinal_points(self)  # TODO

    @property
    def corner(self):  # TODO should these be anscestors?
        return calculate_corner_points(self)  # TODO
    
    @property
    def bounds(self):
        return self.corner.tuple_list

    @property
    def nonant(self):
        return Nonant(self.horz_range.trirange, self.vert_range.trirange)  # TODO


def create_domain_from_coords_list(coords: list[Coord]):
    xs = sorted(set([i.x for i in coords]))
    ys = sorted(set([i.y for i in coords]))
    horz_range = Range(xs[0], xs[-1])
    vert_range = Range(ys[0], ys[-1])
    return Domain(horz_range, vert_range)

# @dataclass
# class MultiDomain:
#     domains: list[Domain]

#     @property
#     def total_domain(self):
#         min_x = min([i.horz_range.min for i in self.domains])
#         max_x = max([i.horz_range.max for i in self.domains])
#         min_y = min([i.vert_range.min for i in self.domains])
#         max_y = max([i.vert_range.max for i in self.domains])
#         return Domain(Range(min_x, max_x), Range(min_y, max_y))
