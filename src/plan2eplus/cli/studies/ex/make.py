from pathlib import Path

from plan2eplus.cli.studies.ex.rooms import Rooms
from plan2eplus.cli.studies.ex.subsurfaces import details

from plan2eplus.eppaths.logic import EpPaths
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.afn.user_interface import AFNInput
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs

r1, r2 = Rooms().two_room_list
airboundary_edges = [Edge(r1.name, r2.name)]


def make_test_case(
    edge_groups: list[EdgeGroup],
    airboundary_edges: list[Edge] = [],
    output_path: Path | None = None,
    afn: bool = False,
    rooms=Rooms().two_room_list,
    afn_input: AFNInput = AFNInput(),
):
    case = (
        EZ()
        .add_zones(rooms)
        .add_subsurfaces(SubsurfaceInputs(edge_groups, details), airboundary_edges)
        .add_constructions()
    )
    if afn:
        case.add_airflow_network(afn_input)
    if output_path:
        case.output_path = output_path
    ep_paths = EpPaths()
    case.epw_path = ep_paths.default_weather

    return case
