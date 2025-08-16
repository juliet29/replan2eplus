from replan2eplus.ezobjects.surface import Surface
import replan2eplus.epnames.keys as keys
from replan2eplus.examples.existing import get_example_idf


# TODO: test init surface! 


def test_assign_surface_conditions(get_pytest_example_idf):
    idf = get_pytest_example_idf
    surfaces = idf.get_surfaces()
    outward_surfaces = [
        i for i in surfaces if i.Outside_Boundary_Condition == "outdoors"
    ]
    s1 = Surface(outward_surfaces[0], keys.SURFACE)
    assert s1.boundary_condition == "outdoors"


def test_get_surface_neighbor(get_pytest_example_idf):
    idf = get_pytest_example_idf
    surfaces = [Surface(i, keys.SURFACE) for i in idf.get_surfaces()]
    indoor_surfaces = [i for i in surfaces if i.boundary_condition == "surface"]

    assert indoor_surfaces[0].neighbor


if __name__ == "__main__":
    idf = get_example_idf()
    surfaces = idf.get_surfaces()
    s = Surface(surfaces[0], expected_key=keys.SURFACE)
    print(surfaces[0])
