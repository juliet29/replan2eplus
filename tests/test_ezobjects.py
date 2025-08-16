from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.minimal import test_rooms


N_SURFACES_PER_CUBE = 6

room1, _ = test_rooms


## NOTE: this stuff applies to most ep objects and might be moved
def test_decompose_block_name(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    zone0 = case.zones[0]
    assert zone0._dname.plan_name == room1.name


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    zone0 = case.zones[0]
    pass
