from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.minimal import ROOM1


N_SURFACES_PER_CUBE = 6


## NOTE: this stuff applies to most ep objects and might be moved
def test_decompose_block_name(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    zone0 = case.zones[0]
    assert zone0.dname.plan_name == ROOM1


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    zone0 = case.zones[0]
    pass
