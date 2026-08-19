from plan2eplus.cli.studies.ex.afn import AFNExampleCases
from plan2eplus.ops.afn.create import create_afn_objects
from plan2eplus.ops.afn.idfobject import IDFAFNSurface
from plan2eplus.cli.studies.ex.afn import AFNEdgeGroups as AFNEdgeGroups, AFNExampleCases
from plan2eplus.cli.studies.ex.make import make_test_case
from plan2eplus.ops.afn.utils.coefficients import assign_external_nodes


def test_match_external_nodes():
    case = make_test_case(AFNEdgeGroups.A_ew, afn=True)
    assign_external_nodes(case.idf, case.objects.airflow_network.subsurfaces)


if __name__ == "__main__":
    test_match_external_nodes()
