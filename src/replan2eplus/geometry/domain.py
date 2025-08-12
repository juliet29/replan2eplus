from dataclasses import dataclass
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.range import Range
from replan2eplus.geometry.contact_points import CardinalPoints, Nonant
from typing import Literal, NamedTuple
from replan2eplus.geometry.domain_calcs import (
    BaseDomain,
    calculate_cardinal_points,
    calculate_corner_points,
)

AXIS = Literal["X", "Y", "Z"]


class Plane(NamedTuple):
    axis: AXIS
    location: float


# TODO domain calcs will live in a separate file..


@dataclass(frozen=True)
class Domain(BaseDomain):
    # horz_range: Range
    # vert_range: Range
    plane: Plane | None = None

    # @classmethod
    # def from_coords_list(cls, coords: list[Coord]):
    #     # TODO can it be > 4 coords?
    #     xs = sorted(set([i.x for i in coords]))
    #     ys = sorted(set([i.y for i in coords]))
    #     horz_range = Range(xs[0], xs[-1])
    #     vert_range = Range(ys[0], ys[-1])
    #     return cls(horz_range, vert_range)

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
    def corner(self):
        return calculate_corner_points(self)  # TODO

    @property
    def nonant(self):
        return Nonant(self.horz_range.trirange, self.vert_range.trirange)  # TODO

    # TODO return buffer of self..


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
