from plan2eplus.cli.studies.ex.subsurfaces import details, e0
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.base import get_names_of_idf_objects
from plan2eplus.ops.subsurfaces.idfobject import IDFSubsurfaceBase, read_subsurfaces
from plan2eplus.ops.subsurfaces.logic.prepare import create_ss_name
from plan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs
import pytest
from plan2eplus.cli.studies.ex.main import Cases, Interfaces, EpFourZoneCase
from plan2eplus.ops.subsurfaces.create import create_subsurfaces
from plan2eplus.ops.zones.idfobject import IDFZone
from plan2eplus.ops.surfaces.idfobject import IDFSurface
from rich import print

from utils4plans.sets import set_equality


def test_init_edge_group():
    edges = [("a", "NORTH"), ("b", "SOUTH")]
    eg = EdgeGroup.from_tuple_edges(edges, "", "Zone_Direction")
    assert eg


def test_init_edge_group_zones():
    edges = [("a", "0"), ("b", "1")]
    eg = EdgeGroup.from_tuple_edges(edges, "", "Zone_Zone")
    assert eg


def test_bad_init_edge_group():
    edges = [("a", "0"), ("b", "1")]
    with pytest.raises(AssertionError):
        EdgeGroup.from_tuple_edges(edges, "", "Zone_Direction")


# def test_read_subsurfaces_from_():
#     case = EZ(Cases().ep_four_zone.path)
#     subsurfaces = read_subsurfaces(case.idf)
#     names = get_names_of_idf_objects(subsurfaces)
#     assert set_equality(names, EpFourZoneCase.subsurface_names)


def test_simple_subsurface_desc():
    case = Cases().two_room
    input = SubsurfaceInputs(
        [EdgeGroup.from_tuple_edges([e0], details["door"], "Zone_Zone")]
    )
    subsurfaces = create_subsurfaces(
        input, case.objects.surfaces, case.objects.zones, case.idf
    )
    print(subsurfaces)
    assert len(subsurfaces) == 2


def test_creating_subsurfaces_simple():
    case = Cases().two_room
    subsurfaces = create_subsurfaces(
        Interfaces.subsurfaces.simple,
        case.objects.surfaces,
        case.objects.zones,
        case.idf,
    )
    assert len(subsurfaces) == 3


def test_creating_subsurfaces_three_details():
    case = Cases().two_room
    subsurfaces = create_subsurfaces(
        Interfaces.subsurfaces.three_details,
        case.objects.surfaces,
        case.objects.zones,
        case.idf,
    )
    assert len(subsurfaces) == 5


def test_creating_interior_subsurface():
    case = Cases().two_room
    subsurfaces = create_subsurfaces(
        Interfaces.subsurfaces.interior,
        case.objects.surfaces,
        case.objects.zones,
        case.idf,
    )
    assert len(subsurfaces) == 2
    ss1 = subsurfaces[0]
    ss2 = subsurfaces[1]
    assert ss2.surface.neighbor_name
    assert ss1.subsurface_name == create_ss_name(
        ss2.surface.neighbor_name, details["door"]
    )


def test_subsurface_equality():
    case = Cases().two_room
    subsurfaces = create_subsurfaces(
        Interfaces.subsurfaces.interior,
        case.objects.surfaces,
        case.objects.zones,
        case.idf,
    )
    ss1 = subsurfaces[0]
    ss2 = subsurfaces[1]
    assert ss1 == ss2
    assert len(set([ss1, ss2])) == 1


if __name__ == "__main__":
    ex = Cases().ep_four_zone
    case = EZ(ex.path)
