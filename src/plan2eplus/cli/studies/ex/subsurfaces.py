from typing import NamedTuple
from plan2eplus.geometry.directions import WallNormal
from plan2eplus.geometry.domain import Domain
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.subsurfaces.interfaces import (
    Dimension,
    Location,
    ZoneDirectionEdge,
    ZoneEdge,
)
from plan2eplus.ops.subsurfaces.user_interfaces import (
    Detail,
    EdgeGroup,
    SubsurfaceInputs,
)
from plan2eplus.cli.studies.ex.rooms import Rooms

FACTOR = 4

val = 0.5
random_surface_name = "Block `room1` Storey 0 Wall 0003"
# subsurface_object = IDFSubsurface("Test", random_surface_name, val, val, val, val)


# TODO probably a good idea to put these in classes..?
zone_edge = ZoneEdge(Rooms.r1.name, Rooms.r2.name)
zone_drn_edge = ZoneDirectionEdge(Rooms.r1.name, WallNormal.WEST)
zone_drn_edge_room2 = ZoneDirectionEdge(Rooms.r2.name, WallNormal.EAST)

location = Location("mm", "SOUTH_WEST", "SOUTH_WEST")
location_bl = Location("bm", "WEST", "WEST")

domain = Rooms.r1.domain
assert isinstance(domain, Domain)
dimension = Dimension(domain.horz_range.size / FACTOR, domain.vert_range.size / FACTOR)

door_details = Detail(dimension, location, "Door")
window_details = Detail(dimension, location, "Window")
window_details_bl = Detail(dimension, location_bl, "Window")

details = {
    "door": Detail(dimension, location, "Door"),
    "window": Detail(dimension, location_bl, "Window"),
    "window_bl": Detail(dimension, location_bl, "Window"),
}


e0 = Edge(Rooms.r1.name, Rooms.r2.name)
e1 = Edge(Rooms.r1.name, "WEST")
e2 = Edge(Rooms.r1.name, "NORTH")
e3 = Edge(Rooms.r1.name, "SOUTH")


# TODO: think about how to input edge groups with combined types..
class EdgeGroups:
    door = [EdgeGroup.from_tuple_edges([e0], "door", "Zone_Zone")]
    window = [
        EdgeGroup.from_tuple_edges(
            [e1],
            "window",
            "Zone_Direction",
        )
    ]
    ns_windows = [EdgeGroup.from_tuple_edges([e2, e3], "window", "Zone_Direction")]
    windows = [EdgeGroup.from_tuple_edges([e1, e2, e3], "window", "Zone_Direction")]
    window_bl = [EdgeGroup.from_tuple_edges([e1], "window_bl", "Zone_Direction")]


class SubsurfaceEdgeGroups:
    interior = EdgeGroups.door
    simple = EdgeGroups.door + EdgeGroups.window
    airboundary =  EdgeGroups.ns_windows
    three_details = EdgeGroups.door + EdgeGroups.window_bl + EdgeGroups.ns_windows


class SubsurfaceInputExamples:  #  TODO: this is a bit redundant, but not a huge issue..
    interior = SubsurfaceInputs(
        EdgeGroups.door,
        details,
    )
    simple = SubsurfaceInputs(EdgeGroups.door + EdgeGroups.window, details)
    airboundary = SubsurfaceInputs(EdgeGroups.door + EdgeGroups.ns_windows, details)
    three_details = SubsurfaceInputs(
        EdgeGroups.door + EdgeGroups.window_bl + EdgeGroups.ns_windows,
        details,
    )


class SubsurfaceInfo(NamedTuple):
    name: str
    n_external_windows: int
    n_external_doors: int
    n_internal_doors: int

    @property
    def sum_subsurfaces(self):
        return self.n_external_windows + self.n_external_doors + self.n_internal_doors*2

class SubsurfaceInputOutput(NamedTuple):
    edge_groups: list[EdgeGroup]
    info: SubsurfaceInfo



class SubsurfaceInputOutputExamples:
    interior = SubsurfaceInputOutput(
        SubsurfaceEdgeGroups.interior, SubsurfaceInfo("interior", 0, 0, 1)
    )
    simple = SubsurfaceInputOutput(
        SubsurfaceEdgeGroups.simple, SubsurfaceInfo("simple", 1, 0, 1)
    )
    airboundary = SubsurfaceInputOutput(
        SubsurfaceEdgeGroups.airboundary, SubsurfaceInfo("airboundary", 2, 0, 1)
    )
    three_details = SubsurfaceInputOutput(
        SubsurfaceEdgeGroups.three_details, SubsurfaceInfo("three_details", 3, 0, 1)
    )

    @property
    def list_examples(self):
        return [self.interior, self.simple, self.airboundary, self.three_details]


# def get_minimal_case_with_subsurfaces():
#     case = get_minimal_case_with_rooms()
#     case.add_subsurfaces(subsurface_inputs_dict["simple"])
#     return case
