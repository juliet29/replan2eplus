from dataclasses import dataclass
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.range import Range
from replan2eplus.geometry.contact_points import (
    CardinalEntries,
    CornerEntries,
    CornerPoints,
    Nonant,
    NonantEntries,
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
    def corner(self):  # TODO should these be anscestors?
        return calculate_corner_points(self)  # TODO

    @property
    def nonant(self):
        return Nonant(self.horz_range.trirange, self.vert_range.trirange)  # TODO


# TODO should this be a class method yay or nay?
def create_domain_for_nonant(domain: Domain, loc: NonantEntries):
    coord = domain.nonant[loc]
    horz_dist = domain.nonant.horz_trirange.dist_between
    vert_dist = domain.nonant.vert_trirange.dist_between
    horz_range = Range(coord.x, coord.x + horz_dist)
    vert_range = Range(coord.y, coord.y + vert_dist)
    return Domain(horz_range, vert_range)

    # TODO return buffer of self..

# all this goes elsewhere.. 
class Dimension(NamedTuple):
    width: float
    height: float


ContactEntries = Union[CornerEntries, CardinalEntries, Literal["centroid"]]


def create_domain_from_corner_point(
    coord: Coord, point_name: CornerEntries, dimensions: Dimension
):
    match point_name:
        case "NORTH_EAST":
            horz_range = Range(coord.x - dimensions.width, coord.x)
            vert_range = Range(coord.y - dimensions.height, coord.y)
        case "SOUTH_EAST":
            horz_range = Range(coord.x - dimensions.width, coord.x)
            vert_range = Range(coord.y, coord.y + dimensions.height)
        case "SOUTH_WEST":
            horz_range = Range(coord.x, coord.x + dimensions.width)
            vert_range = Range(coord.y, coord.y + dimensions.height)
        case "NORTH_WEST":
            horz_range = Range(coord.x, coord.x + dimensions.width)
            vert_range = Range(coord.y - dimensions.height, coord.y)
        case _:
            raise Exception("Invalid corner point!")

    return Domain(horz_range, vert_range)


def create_domain_from_contact_point_and_dimensions(
    coord: Coord, point_name: ContactEntries, dimensions: Dimension
):#TODO rename to contact_loc
    """
    coord => nonant loc  
    point_name => for the subsurface..  
    """
    match point_name:
        case "NORTH_EAST" | "SOUTH_EAST" | "SOUTH_WEST" | "NORTH_WEST":
            return create_domain_from_corner_point(coord, point_name, dimensions)
        # TODO case centroid 
        case _:
            raise Exception("Invalid point")

def place_domain(base_domain: Domain, nonant_loc: NonantEntries, nonant_contact_loc: CornerEntries, subsurface_contact_loc: CornerEntries, dimension: Dimension):
    nonant_domain = create_domain_for_nonant(base_domain, nonant_loc)
    nonant_coord = nonant_domain.corner[nonant_contact_loc] # TODO note this is a restriction and will need a match case here eventually.. 
    subsurf_domain = create_domain_from_contact_point_and_dimensions( nonant_coord, subsurface_contact_loc, dimension)
    return subsurf_domain



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
