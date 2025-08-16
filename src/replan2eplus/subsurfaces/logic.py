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
    # TODO check the plan name is valid!
    return candidates[0]


def get_surface_between_zones(edge: Edge, zones: list[Zone]):
    zone_a = get_zones_by_plan_name(edge.u.name, zones)
    zone_b = get_zones_by_plan_name(edge.v.name, zones)

    candidates: list[Surface] = []

    for surface in zone_a.surfaces:
        if surface.neighbor and surface.neighbor in zone_b.surface_names:
            candidates.append(surface)

    # TODO this is a repeating pattern -> can just pass the messages!
    if len(candidates) == 0:
        raise IDFMisunderstandingError(
            f"Could not find any surfaces  between zones. {zone_a.zone_name} and {zone_b.zone_name} may not be neighbors!"
        )
    if len(candidates) > 1:
        raise BadlyFormatedIDFError(
            f"Should not have more than one shared wall between zones. Between {zone_a.zone_name} and {zone_b.zone_name}, have {len(candidates)} walls: `{candidates}` "
        )
    return candidates[0]


def get_surface_between_zone_and_direction(edge: Edge, zones: list[Zone]):
    zone_a = get_zones_by_plan_name(edge.u.name, zones)
    direction = edge.v.name

    candidates = zone_a.directed_surfaces[direction]

    if len(candidates) == 0:
        raise BadlyFormatedIDFError(
            f"Could not find any surfaces on the `{direction}` side of the zone `{zone_a.zone_name}`"
        )
    if len(candidates) > 1:
        raise NotImplementedError(
            f"For now, assuming that edges between a zone and a direction are for placing external subsurfaces. There should only be one external subsurface on each facade. Instead found {len(candidates)} surfaces on the {direction} facade of {zone_a.zone_name} "
        )
    return candidates[0] #TODO in line with above assumption, should make sure all candidates do not have neigboriing surfaces


def get_surfaces_for_all_edges(edges: Edge, room_map: RoomMap):
    pass # TODO: turn this into an edgelist.. 
