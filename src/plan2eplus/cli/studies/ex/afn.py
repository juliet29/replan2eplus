from typing import NamedTuple

from plan2eplus.cli.studies.ex.rooms import Rooms
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs
from dataclasses import dataclass
from plan2eplus.cli.studies.ex.subsurfaces import details


r1 = Rooms.r1.name
r2 = Rooms.r2.name
N, E, S, W = "north east south west".upper().split()


class AFNEdgeGroups:
    A_ns = [
        EdgeGroup.from_tuple_edges(
            [
                (r1, N),
                (r1, S),
                (r2, N),
                (r2, S),
            ],
            "door",
            "Zone_Direction",
        ),
    ]
    A_ew = [
        EdgeGroup.from_tuple_edges(
            [(W, r1), (r2, E)],
            "door",
            "Zone_Direction",
        ),
        EdgeGroup.from_tuple_edges([(r1, r2)], "door", "Zone_Zone"),
    ]
    B_ne = [
        EdgeGroup.from_tuple_edges(
            [(W, r1), (N, r1), (N, r2)],
            "door",
            "Zone_Direction",
        )
    ]
    C_n = [
        EdgeGroup.from_tuple_edges(
            [
                (r1, N),
            ],
            "door",
            "Zone_Direction",
        ),
        EdgeGroup.from_tuple_edges([(r1, r2)], "door", "Zone_Zone"),
    ]
    D = [
        EdgeGroup.from_tuple_edges(
            [],
            "door",
            "Zone_Direction",
        )
    ]


@dataclass
class AFNCaseDefinition:
    name: str
    edge_groups: list[EdgeGroup]
    n_zones_with_two_plus_valid_surfaces: int
    n_surfaces_in_avail_zones: int
    n_surfaces_after_check_nbs: int
    n_zones_in_afn: int
    n_surfs_in_afn: int

    @property
    def case_with_subsurfaces(self):
        base_case = EZ().add_zones(Rooms().two_room_list)
        return base_case.add_subsurfaces(SubsurfaceInputs(self.edge_groups, details))


A_ns = AFNCaseDefinition("A_ns", AFNEdgeGroups.A_ns, 2, 4, 4, 2, 4)
A_ew = AFNCaseDefinition("A_ew", AFNEdgeGroups.A_ew, 2, 4, 4, 2, 4)
B_ne = AFNCaseDefinition("B_ne", AFNEdgeGroups.B_ne, 1, 2, 2, 1, 2)
C_n = AFNCaseDefinition("C_n", AFNEdgeGroups.C_n, 1, 2, 1, 0, 0)
D = AFNCaseDefinition("D", AFNEdgeGroups.D, 0, 0, 0, 0, 0)


class AFNExampleCases:
    # avail zones, afn zone
    # A -> 2 avail zones, 2 afn zones
    # B -> 1 avail zones, 1 afn zone
    # C -> 1 avail zones, 0 afn zones
    # D -> 0 avail zones, 0 afn zones

    A_ns = A_ns
    A_ew = A_ew
    B_ne = B_ne
    C_n = C_n
    D = D

    @property
    def list(self):
        return [self.A_ns, self.A_ew, self.B_ne, self.C_n, self.D]


# TODO make edge groupds more ergonomic => dont require to spec which is which kind of edge -> figure it out! only details should hamper..
# also, can specify edges using north on an interior object.. but i guess thing getting edges from wont do this.. but shouldnt assume is exterior
