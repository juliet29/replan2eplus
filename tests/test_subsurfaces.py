# TODO should all examples live in one directory or with their creators?
from replan2eplus.examples.minimal import get_minimal_case
from replan2eplus.examples.minimal import TEST_ROOMS, ROOM2, ROOM1
from replan2eplus.subsurfaces.interfaces import Edge, Node
import pytest

from replan2eplus.subsurfaces.logic import get_surface_between_zones


@pytest.mark.skip("Not implemented")
def test_create_edge_with_bad_name():
    node_a = Node("fake_room", "Zone")
    with pytest.raises:
        ...


def test_find_correct_surface_between_zones(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    # TODO: this can go into minimal.py -> build out a story there..
    node_a = Node(ROOM1, "Zone")
    node_b = Node(ROOM2, "Zone")
    edge = Edge(node_a, node_b)
    surf = get_surface_between_zones(edge, case.zones)
    assert surf.surface_name == "Block `room1` Storey 0 Wall 0001_1"
    assert surf.neighbor == "Block `room2` Storey 0 Wall 0003_1"


def test_find_correct_surface_between_zone_and_direction(
    get_pytest_minimal_case_with_rooms,
):
    case = get_pytest_minimal_case_with_rooms
    # TODO: this can go into minimal.py -> build out a story there..
    node_a = Node(ROOM1, "Zone")
    node_b = Node("WEST", "Direction")
    edge = Edge(node_a, node_b)
    surf = get_surface_between_zone_and_direction(edge, case.zones)
    assert surf.surface_name == "Block `room1` Storey 0 Wall 0004" #TODO just guessing might be wrong 
    assert not  surf.neighbor 


if __name__ == "__main__":
    case = get_minimal_case()
    case.add_zones(TEST_ROOMS)
    print(case.surfaces)
    pass
