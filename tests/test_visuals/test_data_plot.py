from plan2eplus.visuals.simple_plots import make_pressure_plot
from plan2eplus.visuals.data.data_plot import handle_external_node_data
from plan2eplus.cli.studies.ex.paths import ExamplePaths

from plan2eplus.paths import Constants
from plan2eplus.cli.studies.ex.afn import AFNExampleCases

from plan2eplus.results.sql import get_qoi


# TODO: are these studies or actual tests?


def test_make_data_plot():
    path = ExamplePaths.afn_examples / AFNExampleCases.A_ew.name
    dp = make_pressure_plot(
        path / Constants.idf_name, path / Constants.sql_path, hour=1
    )
    # dp.show()


def test_handle_external_node_data():
    path = ExamplePaths.afn_examples / AFNExampleCases.A_ns.name
    # dp.show()
    hour = 12
    # case = EZ(path / Constants.idf_name)
    pressure = get_qoi("AFN Node Total Pressure", path / Constants.sql_path)
    data_at_noon = pressure.select_time(hour)
    handle_external_node_data(data_at_noon)


if __name__ == "__main__":
    dp = test_make_data_plot()
    # test_handle_external_node_data()
