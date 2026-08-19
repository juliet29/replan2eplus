import pytest
from rich import print

from plan2eplus.cli.studies.ex.main import Cases
from plan2eplus.cli.studies.ex.rooms import Rooms
from plan2eplus.geometry.directions import WallNormalLiteral
from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.plane import Plane
from plan2eplus.geometry.range import Range

# from plan2eplus.examples.cases.minimal import get_minimal_case_with_rooms
# from plan2eplus.cli.studies.ex.subsurfaces import (
#     Rooms.r1,
#     Rooms.r2,
# )
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.subsurfaces.interfaces import Dimension, Location
from plan2eplus.ops.subsurfaces.create import create_subsurfaces
from plan2eplus.ops.subsurfaces.user_interfaces import (
    Detail,
    EdgeGroup,
    SubsurfaceInputs,
)

# TODO clean up + test throwing error if the dimensions are too large..
dimension = Dimension(width=1 / 3, height=1)
mm_nw = Location("mm", "NORTH_WEST", "NORTH_WEST")

x_edge_detail_groups: list[tuple[WallNormalLiteral, float]] = [
    ("SOUTH", 0),
    ("NORTH", 1),
]


# @pytest.mark.skip()
@pytest.mark.parametrize("direction, plane_loc", x_edge_detail_groups)
def test_subsurface_x_plane(direction, plane_loc):
    edge = Edge(Rooms.r2.name, direction)
    detail = Detail(dimension, mm_nw, "Window")
    domain = Domain(
        Range(1 + dimension.width, 1 + (2 * dimension.width)),
        Range(1, 2),
        Plane("Y", plane_loc),
    )
    case = Cases().two_room
    input = SubsurfaceInputs([EdgeGroup([edge], detail, "Zone_Direction")])
    subsurface = create_subsurfaces(
        input, case.objects.surfaces, case.objects.zones, case.idf
    )[0]
    assert subsurface.domain == domain


y_edge_detail_groups: list[tuple[Edge, float]] = [
    (Edge(Rooms.r1.name, "WEST"), 0),
    (Edge(Rooms.r2.name, "EAST"), 2),
]


@pytest.mark.parametrize("edge, plane_loc", y_edge_detail_groups)
def test_subsurface_y_plane(edge, plane_loc):
    detail = Detail(dimension, mm_nw, "Window")
    domain = Domain(
        Range(dimension.width, (2 * dimension.width)),
        Range(1, 2),
        Plane("X", plane_loc),
    )
    case = Cases().two_room

    input = SubsurfaceInputs([EdgeGroup([edge], detail, "Zone_Direction")])
    subsurface = create_subsurfaces(
        input, case.objects.surfaces, case.objects.zones, case.idf
    )[0]
    assert subsurface.domain == domain


def test_subsurface_equality():
    # NOTE: THIS IS NOT CHECKING THE ORDER OF THE SUBSURFACE EDGES! SEEMS LIKE THIS IS SOMETHING THAT NEEDS TO BE REIMPLEMENTED!! 10/22/25
    case = Cases().subsurfaces_simple
    eq_subsurfaces = [
        i for i in case.objects.subsurfaces if Rooms.r2.name in list(i.edge.as_tuple)
    ]
    assert len(eq_subsurfaces) == 2
    ss1, ss2 = eq_subsurfaces
    assert ss1 == ss2


if __name__ == "__main__":
    test_subsurface_equality()
    # case = get_minimal_case_with_rooms()
    # edge, detail, domain = (
    #     Edge(Rooms.r2.name, "EAST"),
    #     Detail(dimension, mm_nw, "Window"),
    #     Domain(
    #         Range(1 + dimension.width, 1 + (2 * dimension.width)),
    #         Range(1, 2),
    #         Plane("X", 2),
    #     ),
    # )
    # input = SubsurfaceInputExample(edges=[edge], details=[detail], map_={0: [0]}).inputs
    # subsurface = create_subsurfaces(input, case.zones, case.idf)[0]
    # print(subsurface.domain)
    # print(subsurface)


# TODO! stronger checks on tehse? rn just checking that get the right number of subsurfaces.. are they on the right faces?
