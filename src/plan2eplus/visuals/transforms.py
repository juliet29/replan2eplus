from dataclasses import dataclass
from typing import NamedTuple

from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle

from plan2eplus.errors import IDFMisunderstandingError
from plan2eplus.geometry.contact_points import CardinalPoints, calculate_corner_points
from plan2eplus.geometry.coords import Coord
from plan2eplus.geometry.directions import WallNormalNamesList
from plan2eplus.geometry.domain import (
    Domain,
)
from plan2eplus.geometry.ortho_domain import OrthoDomain
from plan2eplus.geometry.plane import Plane
from plan2eplus.geometry.range import Range
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.zones.ezobject import Zone, get_zones

EXPANSION_FACTOR = 1.1


class MPlData(NamedTuple):
    xdata: list[float]
    ydata: list[float]


def split_coords(coords: list[Coord]):
    return MPlData([i.x for i in coords], [i.y for i in coords])


@dataclass
class Line:
    # TODO feels like this logic should be in geometry folder
    start: Coord
    end: Coord
    plane: Plane

    @property
    def to_line2D(self):
        return Line2D(*split_coords([self.start, self.end]))

    @property
    def centroid(self):
        return (
            Range(self.start.x, self.end.x).midpoint,
            Range(self.start.y, self.end.y).midpoint,
        )


def domain_to_mpl_polygon(domain: Domain | OrthoDomain):
    if isinstance(domain, Domain):
        coords = calculate_corner_points(domain)
        # TODO is fill = false needed?
        return Polygon(coords.tuple_list)
    else:
        return Polygon(domain.tuple_list)


def domain_to_line(domain: Domain):
    assert domain.plane
    plane = domain.plane
    if plane.axis == "Z":
        raise IDFMisunderstandingError("Can't flatten a domain in the Z Plane!")
    else:
        # TODO if is ORTHODomain, use bounding box
        min_ = domain.horz_range.min
        max_ = domain.horz_range.max
    if plane.axis == "X":
        start = Coord(plane.location, min_)
        end = Coord(plane.location, max_)
    else:
        assert plane.axis == "Y"
        start = Coord(min_, plane.location)
        end = Coord(max_, plane.location)
    return Line(start, end, plane)


# this is a pretty generic fx -> utils4plans -> filter, get1 throw error
def subsurface_to_connection_line(
    domain: Domain,
    edge: Edge,
    zones: list[Zone],
    cardinal_coords: CardinalPoints,
):
    space_a, space_b = edge.space_a, edge.space_b

    middle_coord = Coord(*domain_to_line(domain).centroid)

    zone_a = get_zones(space_a, zones)
    # TODO define centroid as centroid of bounding box..
    coord_a = zone_a.domain.centroid
    if space_b in WallNormalNamesList:
        coord_b = cardinal_coords.dict_[space_b]
    else:
        zone_b = get_zones(space_b, zones)
        coord_b = zone_b.domain.centroid

    points = [coord_a, middle_coord, coord_b]
    return Line2D(*split_coords(points))


# TODO this is kind of its own thing!
