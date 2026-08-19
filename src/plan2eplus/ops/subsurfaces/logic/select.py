import rich
from loguru import logger

from plan2eplus.errors import BadlyFormatedIDFError, IDFMisunderstandingError
from plan2eplus.ops.subsurfaces.interfaces import ZoneDirectionEdge, ZoneEdge
from plan2eplus.ops.surfaces.ezobject import Surface
from plan2eplus.ops.zones.ezobject import Zone


def keep_rich():
    rich.print("hi")


# TODO : use get unique here...
def get_zones_by_plan_name(room_name: str, zones: list[Zone]):
    candidates = [i for i in zones if i.room_name == room_name]
    assert len(candidates) == 1, BadlyFormatedIDFError(
        f"More than one zone with the room name: `{room_name}`: {candidates}"
    )
    # TODO check the plan name is valid!
    return candidates[0]


def get_surface_between_zones(edge: ZoneEdge, zones: list[Zone], index: int = 0):
    zone_a = get_zones_by_plan_name(edge.space_a, zones)
    zone_b = get_zones_by_plan_name(edge.space_b, zones)

    candidates: list[Surface] = []

    for surface in zone_a.surfaces:
        if surface.neighbor_name and surface.neighbor_name in zone_b.surface_names:
            candidates.append(surface)

    # TODO this is a repeating pattern -> can just pass the messages!
    if len(candidates) == 0:
        raise IDFMisunderstandingError(
            f"Could not find any surfaces between zones. {zone_a.zone_name} and {zone_b.zone_name} may not be neighbors!"
        )
    if index >= len(candidates):
        raise IDFMisunderstandingError(
            f"Requested shared wall #{index} between {zone_a.zone_name} and "
            f"{zone_b.zone_name}, but they share only {len(candidates)} wall(s)."
        )
    if len(candidates) > 1:
        candidate_names = [i.surface_name for i in candidates]
        logger.warning(
            f"More than one shared wall between {zone_a.zone_name} and {zone_b.zone_name}: {len(candidates)} shared walls `{candidate_names}`. Choosing #{index}: {candidate_names[index]}"
        )
    surf = candidates[index]
    assert surf.neighbor_name
    neighbor = [i for i in zone_b.surfaces if i.surface_name == surf.neighbor_name]
    assert len(neighbor) == 1
    return surf, neighbor[0]


def get_surface_between_zone_and_direction(edge: ZoneDirectionEdge, zones: list[Zone]):
    zone_a = get_zones_by_plan_name(edge.space_a, zones)
    direction = edge.space_b.name

    directed_surfaces = zone_a.directed_surfaces[direction]

    candidates = list(filter(lambda x: x.is_external, directed_surfaces))

    if len(candidates) == 0:
        for i in directed_surfaces:
            logger.debug(
                (
                    i.display_name,
                    i.direction.name,
                    i.boundary_condition,
                    i.boundary_condition_object,
                )
            )
        raise BadlyFormatedIDFError(
            f"Could not find any surfaces on the `{direction}` side of the zone `{zone_a.zone_name}` with external boundary condition."
        )

    if len(candidates) > 1:
        candidate_names = [i.surface_name for i in candidates]
        logger.warning(
            f"For now, assuming that edges between a zone and a direction are for placing external subsurfaces. There should only be one external subsurface on each facade. Instead found {len(candidates)} surfaces on the {direction} facade of {zone_a.zone_name}: Choosing {candidate_names[0]}.... "
        )
    surf = candidates[0]
    assert not surf.neighbor_name
    return surf  # TODO in line with above assumption, should make sure all candidates do not have neigboriing surfaces


# def get_surfaces_for_all_edges(edges: Edge, room_map: RoomMap):
#     pass # TODO: turn this into an edgelist..
