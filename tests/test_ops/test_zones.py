import pytest

from plan2eplus.cli.studies.ex.main import Cases
from plan2eplus.cli.studies.ex.main import Interfaces as UI

from plan2eplus.ops.base import get_names_of_idf_objects
from plan2eplus.ops.zones.create import create_zones
from plan2eplus.ops.zones.idfobject import IDFZone
from plan2eplus.ezcase.ez import EZ

N_SURFACES_PER_CUBE = 6


def test_zone_names():
    case = Cases().two_room
    zones = case.objects.zones
    assert set([i.room_name for i in zones]) == set(
        [i.name for i in UI.rooms.two_room_list]
    )


def test_add_zones():
    case = Cases().base
    zones, *_ = create_zones(case.idf, UI.rooms.two_room_list)
    assert len(zones) == len(UI.rooms.two_room_list)


def test_add_surfaces_with_zones():
    case = Cases().base
    _, surfaces = create_zones(case.idf, UI.rooms.two_room_list)
    assert len(surfaces) == len(UI.rooms.two_room_list) * N_SURFACES_PER_CUBE


@pytest.mark.xfail()  # TODO replace with own example
def test_read():
    case = EZ(Cases().ep_four_zone.path)
    n_zones = len(case.objects.zones)
    assert n_zones == 3


def test_read_from_idf_with_keys_not_implemented():
    with pytest.raises(Exception):
        _ = EZ(Cases().ep_four_zone.path)


# @pytest.mark.xfail()
# def test_get_zone_subsurfaces(get_pytest_minimal_case_with_subsurfaces):
#     case = get_pytest_minimal_case_with_subsurfaces
#     zone = case.zones[0]
#     assert len(zone.subsurface_names) == 2


def test_update_zone_name():
    case = Cases().two_room
    zone_name = "Block `room1` Storey 0"
    test_name = "test_name"
    IDFZone().update(case.idf, zone_name, "Name", test_name)
    new_zones = IDFZone().read(case.idf)
    assert test_name in get_names_of_idf_objects(new_zones)
    # zone1 = true_zones[0]
    # zone1["Name"] =


# TODO separate the idf tests from the pure zone tests
def test_get_one_idf_object():
    case = Cases().two_room
    zone_name = "Block `room1` Storey 0"
    res = IDFZone().get_one_idf_object(case.idf, zone_name)
    assert res.Name == zone_name


def test_get_idf_zone_surfaces():
    case = Cases().two_room
    zone_name = "Block `room1` Storey 0"
    res = IDFZone.get_zone_surface_names(case.idf, zone_name)
    assert len(res) == N_SURFACES_PER_CUBE


def test_get_idf_zone_subsurfaces():
    case = Cases().subsurfaces_simple
    zone_name = "Block `room1` Storey 0"
    res = IDFZone.get_zone_subsurface_names(case.idf, zone_name)
    assert len(res) == 2
    # assert len(res) == N_SURFACES_PER_CUBE


if __name__ == "__main__":
    case = Cases().subsurfaces_simple
    zone_name = "Block `room1` Storey 0"
    res = IDFZone().get_one_idf_object(case.idf, zone_name)

    # zones = IDFZone.read(case.idf)[0]
    # test_get_zone_subsurfaces()
    # case = EZ()
    # rooms = [UI.rooms.r1, UI.rooms.r2]
    # zones = create_zones(case.idf, rooms)

    # ss = z.subsurface_names
    # print(ss)
    # idf = get_minimal_idf()
    # zones, surfaces = create_zones(idf, test_rooms)
    # print(surfaces)
    # # EZObject2D(epbunch=)
