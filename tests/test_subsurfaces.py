# TODO should all examples live in one directory or with their creators?
from replan2eplus.examples.minimal import get_minimal_case, get_minimal_case_with_rooms
from replan2eplus.examples.minimal import test_rooms
from replan2eplus.subsurfaces.interfaces import Edge, Node, Location, Details
import pytest

from replan2eplus.subsurfaces.logic import (
    get_surface_between_zones,
    get_surface_between_zone_and_direction,
)
from replan2eplus.geometry.domain_create import Dimension



# @pytest.mark.skip("Not implemented")
# def test_create_edge_with_bad_name():
#     node_a = Node("fake_room", "Zone")
#     with pytest.raises:
#         ...
room1, room2 = test_rooms
# TODO: this can go into minimal.py -> build out a story there..
node_a = Node(room1.name, "Zone")
node_b = Node(room2.name, "Zone")
node_drn = Node("EAST", "Direction") # TODO: WEST should be outer, geometry is messed up

location = Location("mm", "SOUTH_WEST", "SOUTH_WEST")
factor = 4
dimension = Dimension(room1.domain.horz_range.size / factor, room1.domain.vert_range.size / factor)


def test_find_correct_surface_between_zones(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    
    edge = Edge(node_a, node_b)
    surf = get_surface_between_zones(edge, case.zones)
    assert surf.surface_name == "Block `room1` Storey 0 Wall 0001_1"
    assert surf.neighbor == "Block `room2` Storey 0 Wall 0003_1"


def test_find_correct_surface_between_zone_and_direction(
    get_pytest_minimal_case_with_rooms,
):
    case = get_pytest_minimal_case_with_rooms

    edge = Edge(node_a, node_drn)
    surf = get_surface_between_zone_and_direction(edge, case.zones)
    assert (
        surf.surface_name == "Block `room1` Storey 0 Wall 0003"
    )  # TODO just guessing might be wrong
    assert not surf.neighbor

def test_create_subsurface_interior(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    edge = Edge(node_a, node_b)
    subsurface, partner_suburface = create_suburface(edge, dimension, location, "Door")
    pass
    

def test_create_subsurface_exterior(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    edge = Edge(node_a, node_drn)
    surface = create_suburface(edge, dimension, location, "Window")




if __name__ == "__main__":
    # case = get_minimal_case_with_rooms()
    # node_a = Node(ROOM1_NAME, "Zone")
    # node_b = Node("WEST", "Direction")
    # edge = Edge(node_a, node_b)
    # surf = get_surface_between_zone_and_direction(edge, case.zones)
    pass
