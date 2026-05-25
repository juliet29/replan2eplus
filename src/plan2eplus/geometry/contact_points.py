from dataclasses import dataclass
from plan2eplus.geometry.coords import Coord, Coordinate3D
from typing import Literal

from plan2eplus.geometry.domain import Domain


CardinalEntries = Literal["NORTH", "EAST", "SOUTH", "WEST"]


@dataclass
class CardinalPoints:
    NORTH: Coord
    EAST: Coord
    SOUTH: Coord
    WEST: Coord

    def __getitem__(self, item: CardinalEntries) -> Coord:
        return getattr(self, item)

    @property
    def dict_(self):
        # TODO make this consistent => values or something else..
        return {
            "NORTH": self.NORTH,
            "EAST": self.EAST,
            "SOUTH": self.SOUTH,
            "WEST": self.WEST,
        }


CornerEntries = Literal["NORTH_EAST", "SOUTH_EAST", "SOUTH_WEST", "NORTH_WEST"]


@dataclass
class CornerPoints:
    NORTH_EAST: Coord
    SOUTH_EAST: Coord
    SOUTH_WEST: Coord
    NORTH_WEST: Coord

    def __getitem__(self, item: CornerEntries) -> Coord:
        return getattr(self, item)

    @property
    def coord_list(self):
        # this is clock wise not counter clockwise
        # return [self.NORTH_EAST, self.SOUTH_EAST, self.SOUTH_WEST, self.NORTH_WEST]
        return [self.NORTH_EAST, self.NORTH_WEST, self.SOUTH_WEST, self.SOUTH_EAST]

    @property
    def tuple_list(self):
        return [i.as_tuple for i in self.coord_list]


@dataclass
class CornerPoints3D:
    NORTH_EAST: Coordinate3D
    SOUTH_EAST: Coordinate3D
    SOUTH_WEST: Coordinate3D
    NORTH_WEST: Coordinate3D

    def __getitem__(self, item: CornerEntries) -> Coord:
        return getattr(self, item)

    @property
    def tuple_list(self):
        return [i.as_tuple for i in self.coord_list]


def get_domain_shortcuts(domain: Domain):
    n = domain.vert_range.max
    s = domain.vert_range.min
    e = domain.horz_range.max
    w = domain.horz_range.min
    return n, s, e, w


def calculate_corner_points(domain: Domain) -> CornerPoints:
    n, s, e, w = get_domain_shortcuts(domain)
    return CornerPoints(
        NORTH_EAST=Coord(e, n),
        SOUTH_EAST=Coord(e, s),
        SOUTH_WEST=Coord(w, s),
        NORTH_WEST=Coord(w, n),
    )


def calculate_cardinal_points(domain: Domain) -> CardinalPoints:
    n, s, e, w = get_domain_shortcuts(domain)
    mid_x = domain.horz_range.midpoint
    mid_y = domain.vert_range.midpoint
    return CardinalPoints(
        NORTH=Coord(mid_x, n),
        EAST=Coord(e, mid_y),
        SOUTH=Coord(mid_x, s),
        WEST=Coord(w, mid_y),
    )
