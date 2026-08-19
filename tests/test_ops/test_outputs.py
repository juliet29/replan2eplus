from utils4plans.sets import set_intersection
from plan2eplus.cli.studies.ex.main import Cases
from plan2eplus.ops.output.defaults import default_variables
from plan2eplus.ops.output.create import add_output_variables
from plan2eplus.ops.output.idfobject import IDFOutputVariable


def test_add_outputs():
    case = Cases().two_room
    test_vars = ["AFN Node Total Pressure", "Site Wind Direction"]
    add_output_variables(case.idf)
    assert set_intersection(
        IDFOutputVariable().get_existing_output_variable_names(case.idf), test_vars
    )


def test_add_default_variables():
    case = Cases().two_room
    add_output_variables(case.idf)
    test_vars = [
        "AFN Linkage Node 1 to Node 2 Volume Flow Rate",
        "AFN Zone Mixing Volume",
        "Site Wind Direction",
    ]
    assert set_intersection(
        IDFOutputVariable().get_existing_output_variable_names(case.idf), test_vars
    )


if __name__ == "__main__":
    print(default_variables)
    # case = get_minimal_case_with_rooms()
    # test_vars = ["AFN Node Total Pressure", "Site Wind Direction"]
    # case.idf.add_output_variables(test_vars)
    # print(case.idf.get_output_variables())
    # assert set_intersection(case.idf.get_output_variables(), test_vars)
