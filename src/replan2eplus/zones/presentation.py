from replan2eplus.ezobjects.surface import Surface
from replan2eplus.subsurfaces.logic import RoomMap
from replan2eplus.zones.interfaces import Room, RoomZonePair
from replan2eplus.ezobjects.idf import IDF
from replan2eplus.ezobjects.zone import Zone
import replan2eplus.epnames.keys as keys
# from replan2eplus.ezcase.examples import get_minimal_idf

# TODO: logic!
# Tests to do on rooms -> no duplicates..
# -> Domains should be hashed -> no dup domains,
# no duplicate room names..


def create_zones(idf: IDF, rooms: list[Room]):
    # TODO move to logic!
    for room in rooms:
        idf.add_geomeppy_block(room.geomeppy_block())

    idf.intersect_match()
    # now get the zones from the idf..
    zones = [Zone(i) for i in idf.get_zones()]
    surfaces = [
        Surface(i, keys.SURFACE) for i in idf.get_surfaces()
    ]  # TODO can this be done automatically?, ie dont have to declare surface?
    room_map = RoomMap([RoomZonePair(i.room_name, i.zone_name) for i in zones])
    return zones, surfaces, room_map
