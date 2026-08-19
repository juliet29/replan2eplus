from plan2eplus.cli.studies.ex.afn import AFNEdgeGroups as AFNEdgeGroups

from plan2eplus.cli.studies.ex.make import make_test_case
from plan2eplus.visuals.simple_plots import make_base_plot


def test_make_base_plot():
    case = make_test_case(AFNEdgeGroups.A_ew, afn=True)
    make_base_plot(case)
    assert 1
    # TODO -> make better tests, check the matplotlib axes..


# def test_make_ortho_plot():
#     case = create_ortho_case()
#     make_base_plot(case)
#     assert 1


if __name__ == "__main__":
    case = make_test_case(AFNEdgeGroups.D, afn=True)
    bp = make_base_plot(case)
    bp.show()
