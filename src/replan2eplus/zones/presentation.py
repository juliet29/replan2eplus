from replan2eplus.zones.interfaces import Room
from replan2eplus.ezobjects.idf import IDF
from replan2eplus.ezobjects.zone import Zone, Surface

# TODO: logic! 
# Tests to do on rooms -> no duplicates..
# -> Domains should be hashed -> no dup domains,
# no duplicate room names..



def create_zones(idf: IDF, rooms: list[Room]):
    # TODO move to logic! 
    for room in rooms:
        idf.add_eppy_block(room.create_geomeppy_block())

    
    idf.intersect_match()
    # now get the zones from the idf..
    zones = [Zone(i) for i in idf.get_zones()]
    surfaces = [Surface(i) for i in idf.get_surfaces()]

    return zones, surfaces
