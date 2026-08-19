import pytest

from plan2eplus.cli.studies.ex.main import Cases, Interfaces
from plan2eplus.cli.studies.ex.subsurfaces import (
    door_details,
    window_details,
    zone_drn_edge,
    zone_edge,
)
from plan2eplus.geometry.directions import WallNormal
from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.range import Range
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.subsurfaces.interfaces import Dimension
from plan2eplus.ops.subsurfaces.logic.exterior import (
    create_subsurface_for_exterior_edge,
)
from plan2eplus.ops.subsurfaces.logic.interior import (
    create_subsurface_for_interior_edge,
)
from plan2eplus.ops.subsurfaces.logic.prepare import (
    compare_and_maybe_change_dimensions,
    compare_domain,
)
from plan2eplus.ops.subsurfaces.logic.select import (
    get_surface_between_zone_and_direction,
    get_surface_between_zones,
)
from plan2eplus.ops.subsurfaces.config import DOMAIN_SHRINK_FACTOR
from plan2eplus.ops.subsurfaces.user_interfaces import (
    Detail,
)


def test_find_correct_surface_between_zones():
    case = Cases().two_room
    surf, nb = get_surface_between_zones(zone_edge, case.objects.zones)
    assert surf.direction == WallNormal.EAST
    assert nb.direction == WallNormal.WEST


def test_find_correct_surface_between_zone_and_direction():
    case = Cases().two_room
    surf = get_surface_between_zone_and_direction(zone_drn_edge, case.objects.zones)
    assert surf.direction == WallNormal.WEST
    assert not surf.neighbor_name

    # Geomeppy IDF doesnt check for valididty, but this method should.. -> ie that the surface matches a zone..


def test_create_subsurface_interior():
    case = Cases().two_room
    subsurface, partner_suburface = create_subsurface_for_interior_edge(
        zone_edge, door_details, case.objects.zones, case.objects.surfaces, case.idf
    )
    assert Interfaces.rooms.r1.name in subsurface.subsurface_name
    assert Interfaces.rooms.r2.name in partner_suburface.subsurface_name


def test_create_subsurface_exterior():
    case = Cases().two_room
    subsurface = create_subsurface_for_exterior_edge(
        zone_drn_edge,
        window_details,
        case.objects.zones,
        case.objects.surfaces,
        case.idf,
    )
    assert Interfaces.rooms.r1.name in subsurface.subsurface_name


def test_too_large_dimension():
    detail = Detail(Dimension(10, 2), window_details.location, window_details.type_)

    domain = Domain(Range(0, 3), Range(0, 3))
    new_detail = compare_and_maybe_change_dimensions(detail, domain)
    expected_detail = Detail(
        Dimension(3 * DOMAIN_SHRINK_FACTOR, 2),
        window_details.location,
        window_details.type_,
    )
    assert new_detail == expected_detail


@pytest.mark.parametrize("horz_range", [Range(5, 10), Range(5, 25), Range(15, 22)])
def test_bad_subsurface_location(horz_range):
    subsurf_domain = Domain(horz_range, Range(10, 20))
    main_surface_domain = Domain(Range(10, 20), Range(10, 20))
    with pytest.raises(Exception):
        compare_domain(main_surface_domain, subsurf_domain)


def test_sorting_directed_edges():
    edge = Edge("EAST", Interfaces.rooms.r1.name)
    expected_edge = (Interfaces.rooms.r1.name, WallNormal.EAST)
    assert expected_edge == edge.sorted_directed_edge


if __name__ == "__main__":
    detail = Detail(Dimension(10, 2), window_details.location, window_details.type_)
    domain = Domain(Range(0, 3), Range(0, 3))
    new_detail = compare_and_maybe_change_dimensions(detail, domain)
    expected_detail = Detail(
        Dimension(3 * DOMAIN_SHRINK_FACTOR, 2),
        window_details.location,
        window_details.type_,
    )
    assert new_detail == expected_detail


# TEST subsurface location
