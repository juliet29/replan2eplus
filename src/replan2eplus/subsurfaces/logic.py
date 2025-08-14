from replan2eplus.ezobjects.zone import Zone
from replan2eplus.subsurfaces.interfaces import Edge
from replan2eplus.zones.interfaces import RoomMap


def get_surface_between_zones(edge: Edge, room_map: RoomMap, zones: list[Zone]):
    names = [edge.u.name, edge.u.name]
    for name in names:
        room_map.validate_room(name)

    zones = [i for i in zones if i.room_name in names]

    # for surf in zone.surfaces.. -> how to get surfaces on zones.. 

    
    # get the zone objects/// 


def get_surfaces_for_all_edges(edges: Edge, room_map: RoomMap):
    pass
    