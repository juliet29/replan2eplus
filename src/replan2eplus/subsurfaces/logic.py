from replan2eplus.errors import BadlyFormatedIDFError, IDFMisunderstandingError
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.subsurfaces.interfaces import Edge
from replan2eplus.zones.interfaces import RoomMap


def get_zones_by_plan_name(room_name: str, zones: list[Zone]):
    candidates = [i for i in zones if i.room_name in room_name]
    assert len(candidates) == 1, BadlyFormatedIDFError(
        f"More than one zone with the room name: `{room_name}`: {candidates}"
    )
    return candidates[0]


def get_surface_between_zones(edge: Edge, room_map: RoomMap, zones: list[Zone]):
    # names = [edge.u.name, edge.u.name]
    # for name in names:
    #     room_map.validate_room(
    #         name
    #     )  # TODO: can clean this up by having validate_room return the name

    zone_a = get_zones_by_plan_name(edge.u.name, zones)
    zone_b = get_zones_by_plan_name(edge.v.name, zones)

    candidates:list[Surface] = []

    for surface in zone_a.surfaces:
        if surface.neighbor and surface.neighbor in zone_b.surface_names:
            candidates.append(surface)

    # TODO this can be shared
    if len(candidates) == 0:
        raise IDFMisunderstandingError(
            f"Could not find any surfaces  between zones. {zone_a.zone_name} and {zone_b.zone_name} may not be neighbors!"
        )
    if len(candidates) > 1:
        raise BadlyFormatedIDFError(
            f"Should not have more than one shared wall between zones. Between {zone_a.zone_name} and {zone_b.zone_name}, have {len(candidates)} walls: `{candidates}` "
        )

    return candidates[0]

    # for surf in zone.surfaces.. -> how to get surfaces on zones..

    # get the zone objects///


def get_surfaces_for_all_edges(edges: Edge, room_map: RoomMap):
    pass
