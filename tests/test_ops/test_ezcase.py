import pytest

from plan2eplus.cli.studies.ex.afn import AFNEdgeGroups as AFNEdgeGroups, AFNExampleCases
from plan2eplus.cli.studies.ex.make import make_test_case
from plan2eplus.cli.studies.ex.make import airboundary_edges

from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.afn.create import AFNInput
from plan2eplus.ops.afn.utils.venting import AFNVentingInput
from plan2eplus.ops.schedules.interfaces.year import create_year_from_single_value
from plan2eplus.cli.studies.ex.paths import ExamplePaths
from plan2eplus.cli.studies.ex.schedule import ExampleYear
from plan2eplus.results.sql import get_qoi
import numpy as np
from plan2eplus.paths import Constants
from utils4plans.logs import logset


@pytest.mark.slow
def test_case_basic():
    case = make_test_case(AFNEdgeGroups.A_ew)
    case.save_and_run(run=True)
    assert 1


@pytest.mark.slow
def test_case_airboudary():
    case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges)
    case.save_and_run(run=True)
    assert 1


@pytest.mark.slow
def test_case_airboundary_afn():
    case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges, afn=True)
    case.save_and_run(run=True)
    assert 1


@pytest.mark.slow
def test_run_case_without_reading():
    output_path = ExamplePaths.THROWAWAY_PATH  # TODO: move this to static
    path = ExamplePaths.afn_examples / AFNExampleCases.A_ew.name / Constants.idf_name
    case = EZ(path, read_existing=False)
    case.save_and_run(output_path=output_path, run=True)
    assert 1


# TODO: this seems like a different set of tests -> having to do with schedules?

QUANTILES = [0.1, 0.25, 0.75, 0.9]


def test_case_with_default_venting():
    opath = ExamplePaths.ts_open
    case = make_test_case(AFNEdgeGroups.A_ns, afn=True, output_path=opath)
    # TODO: this is getting stale qoi data because not being run again?
    case.save_and_run(run=False)

    res2 = get_qoi(
        "AFN Surface Venting Availability Status", opath / Constants.sql_path
    )

    quantiles = res2.data_arr.mean("space_names").quantile(q=QUANTILES)
    assert np.unique(quantiles.data) == np.array(1)


def test_case_with_afn_venting():
    opath = ExamplePaths.ts_dynamic
    venting_input = AFNVentingInput("Doors", ExampleYear().year)
    case = make_test_case(
        AFNEdgeGroups.A_ns,
        afn=True,
        output_path=opath,
        afn_input=AFNInput([venting_input]),
    )
    case.save_and_run(run=False, output_path=opath)
    res2 = get_qoi(
        "AFN Surface Venting Availability Status", opath / Constants.sql_path
    )

    quantiles = res2.data_arr.mean("space_names").quantile(q=QUANTILES)
    assert np.array_equal(np.unique(quantiles.data), np.array([0, 1]))


def test_case_with_afn_no_venting():
    opath = ExamplePaths.ts_closed
    closed_year = create_year_from_single_value(0)
    venting_input = AFNVentingInput("Doors", closed_year)
    case = make_test_case(
        AFNEdgeGroups.A_ns,
        afn=True,
        output_path=opath,
        afn_input=AFNInput([venting_input]),
    )
    case.save_and_run(run=False, output_path=opath)
    res2 = get_qoi(
        "AFN Surface Venting Availability Status", opath / Constants.sql_path
    )

    # assert 1
    quantiles = res2.data_arr.mean("space_names").quantile(q=QUANTILES)
    assert np.unique(quantiles.data) == np.array(0)


# TODO!
# ortho domains..
# running from an existing idf -> to run don't need to read an idf really, that is just needed for graphing.. so maybe reading existing objects is a flag that can get turned on or off.. if adding new things, should read ..


if __name__ == "__main__":
    logset()
    test_run_case_without_reading()

    # case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges, afn=True)
    # r = test_case_with_default_venting()
    # t = test_case_with_afn_venting()
    # y = test_case_with_afn_no_venting()
    # print(r, t[0], t[1], y)
    # arr = t[2].data_arr
    # print(np.unique(arr.data))
    #
    # # case.save_and_run(run=True)
