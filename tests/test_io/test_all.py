from plan2eplus.io.edges import create_edge_inputs
from plan2eplus.cli.studies.ex.paths import ProjectPaths


def test_read_edges_config():
    path = ProjectPaths.input_config.edges
    res = create_edge_inputs(path)
    assert len(res) == 3
