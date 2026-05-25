from dataclasses import dataclass
from typing import Literal
from plan2eplus.ops.subsurfaces.interfaces import Edge, SubsurfaceType
from plan2eplus.ops.subsurfaces.utils import create_surface_domain
from plan2eplus.ops.surfaces.ezobject import Surface

# need the surface its on..

# TODO properties to add: surface, partner obj, connecting zones, "driving zones" (for the purpose of the AFN )


SubsurfaceOptions = Literal["DOOR", "WINDOW", "DOOR:INTERZONE"]


@dataclass
class Subsurface:
    subsurface_name: str
    construction_name: str
    starting_x_coordinate: float
    starting_z_coordinate: float
    length: float
    height: float
    neighbor_name_: str
    subsurface_type: SubsurfaceType
    surface: Surface

    ## :**********  Representation **********

    def __rich_repr__(self):
        yield "subsurface_name", self.subsurface_name
        yield "edge", self.edge
        # yield "domain", self.domain

    def __str__(self):
        return f"{self.subsurface_type}_{self.surface}"

    def __eq__(self, other):
        if isinstance(other, Subsurface):
            if other.edge == self.edge:
                return True
            # NOTE: this only works because assuming each surface can have only one subsurface. Later, will need to include the domain
        return False

    def __hash__(self) -> int:
        return self.edge.__hash__()

    @property
    def name(self):
        return self.subsurface_name

    @property
    def display_name(self):
        return f"{self.subsurface_type}_{self.surface.display_name}"

    @property
    def is_door(self):
        return self.subsurface_type.casefold() == "Door".casefold()

    @property
    def is_window(self):
        return self.subsurface_type.casefold() == "Window".casefold()

    ## :**********  Associaations **********

    @property
    def edge(self):
        if self.surface.boundary_condition.casefold() == "Outdoors".casefold():
            edge = (self.surface.room_name, self.surface.direction.name)
        else:
            assert (
                self.surface.room_name_of_neighbor
            ), f"Surface of subsurface `{self.subsurface_name}` has boundary condition of `{self.surface.boundary_condition}` but does not have a neighbor."
            edge = (self.surface.room_name, self.surface.room_name_of_neighbor)
        return Edge(*edge)

    @property
    def neighbor_name(self):
        return self.neighbor_name_

    ## :********** Geometry **********

    @property
    def domain(self):
        # TODO: check that this will actually work => used mostly for visualization right now..
        return create_surface_domain(
            self.surface,
            self.starting_x_coordinate,
            self.starting_z_coordinate,
            self.length,
            self.height,
        )
        # surf_domain = self.surface.domain
        # assert self.surface.surface_type.casefold() == "Wall".casefold()
        # assert isinstance(surf_domain, Domain)
        # surface_min_horz = surf_domain.horz_range.min
        # surface_min_vert = surf_domain.vert_range.min
        #
        # horz_min = surface_min_horz + float(self.starting_x_coordinate)
        # width = float(self.length)
        # if not self.starting_z_coordinate:
        #     self.starting_z_coordinate = 0  # TODO: make better solution! !, ie also check if it is a str, or for both, make sure that empty string is read in as 0..
        # vert_min = surface_min_vert + float(self.starting_z_coordinate)
        # height = float(self.height)
        #
        # horz_range = Range(horz_min, horz_min + width)
        # vert_range = Range(vert_min, vert_min + height)
        #
        # return Domain(horz_range, vert_range, surf_domain.plane)
