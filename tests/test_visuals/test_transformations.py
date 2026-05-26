import pytest
from plan2eplus.ops.airboundary.create import update_airboundary_constructions
from plan2eplus.visuals.domains import calculate_cardinal_domain
from plan2eplus.geometry.contact_points import calculate_cardinal_points
from plan2eplus.visuals.transforms import (
    subsurface_to_mpl_connection_line,
)
from plan2eplus.ex.subsurfaces import e0

pytest.skip(allow_module_level=True)


def test_transform_subsurface_to_connection(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    cardinal_domain = calculate_cardinal_domain([i.domain for i in case.zones])
    subsurface = case.subsurfaces[0]

    subsurface_to_mpl_connection_line(
        subsurface.domain,
        subsurface.edge,
        case.zones,
        calculate_cardinal_points(cardinal_domain),
    )


def test_transform_airboundary_to_connection(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    airboundaries = update_airboundary_constructions(case.idf, [e0], case.zones)
    cardinal_domain = calculate_cardinal_domain([i.domain for i in case.zones])
    airboundary = airboundaries[0]
    subsurface_to_mpl_connection_line(
        airboundary.domain,
        airboundary.edge,
        case.zones,
        calculate_cardinal_points(cardinal_domain),
    )
