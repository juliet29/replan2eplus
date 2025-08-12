from dataclasses import dataclass
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.range import Range
from typing import Literal, NamedTuple

AXIS = Literal["X", "Y", "Z"]

class Plane(NamedTuple):
    axis: AXIS
    location: float
    


@dataclass(frozen=True)
class Domain:
    horz_range: Range
    vert_range: Range
    plane: Plane | None = None

    @classmethod
    def from_coords_list(cls, coords: list[Coord]):
        # TODO can it be > 4 coords?
        xs = sorted(set([i.x for i in coords]))
        ys = sorted(set([i.y for i in coords]))
        horz_range = Range(xs[0], xs[-1])
        vert_range = Range(ys[0], ys[-1])
        return cls(horz_range, vert_range)


    @property
    def centroid(self):
        return Coord(self.horz_range.midpoint, self.vert_range.midpoint)

    @property
    def area(self):
        return self.horz_range.size * self.vert_range.size

    @property
    def aspect_ratio(self):
        return self.horz_range.size / self.vert_range.size



@dataclass
class MultiDomain:
    domains: list[Domain]

    @property
    def total_domain(self):
        min_x = min([i.horz_range.min for i in self.domains])
        max_x = max([i.horz_range.max for i in self.domains])
        min_y = min([i.vert_range.min for i in self.domains])
        max_y = max([i.vert_range.max for i in self.domains])
        return Domain(Range(min_x, max_x), Range(min_y, max_y))


