from replan2eplus.zones.interfaces import Room
from replan2eplus.ezobjects.idf import IDF
from replan2eplus.ezobjects.zone import Zone, Surface

# Tests to do on rooms -> no duplicates..
# -> Domains should be hashed -> no dup domains,
# no duplicate room names..

# TODO make presentation


def create_zones(idf: IDF, rooms: list[Room]):
    for room in rooms:
        idf.add_eppy_block(room.create_geomeppy_block())
    idf.print_idf()

    # now get the zones from the idf..
    zones = [Zone(i) for i in idf.get_zones()]
    surfaces = [Surface(i) for i in idf.get_surfaces()]

    return zones, surfaces
