from geomeppyupdated import IDF
from loguru import logger
from rich import print

from plan2eplus.errors import IDFMisunderstandingError
from plan2eplus.geometry.domain import Domain
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.subsurfaces.interfaces import ZoneEdge
from plan2eplus.ops.subsurfaces.logic.placement import place_domain
from plan2eplus.ops.subsurfaces.logic.prepare import (
    compare_and_maybe_change_dimensions,
    prepare_object,
)
from plan2eplus.ops.subsurfaces.logic.select import get_surface_between_zones
from plan2eplus.ops.subsurfaces.user_interfaces import Detail
from plan2eplus.ops.zones.ezobject import Zone
from plan2eplus.ops.surfaces.ezobject import Surface


def check_for_airboundaries(main_surface, nb_surface):
    if main_surface.is_airboundary or nb_surface.is_airboundary:
        main_name = f"Main: {main_surface.surface_name}"
        nb_name = f"Nb: {nb_surface.surface_name}"
        assert (
            main_surface.is_airboundary and nb_surface.is_airboundary
        ), f"Matching surfaces should be airboundaries!!! \n {main_name}' constr: {main_surface.construction_name}\n {nb_name}' constr: {nb_surface.construction_name}"
        raise IDFMisunderstandingError(
            f"{main_name} and {nb_name} are airboundaries! They cannot have surfaces placed on them! "
        )


class SurfaceMatchException(Exception):
    def __init__(self, s1: Surface, s2: Surface) -> None:
        self.s1 = s1
        self.s2 = s2

    def message(self):

        def make(s: Surface):
            return {
                "display": s.display_name,
                "true": s.surface_name,
                "neigbor": s.neighbor_name,
                "domain": str(s.domain),
                "domain_raw": s.domain,
            }

        s = "[red]Neigboring surfaces should have matching domains."
        d = {
            "Error": s,
            "Main surface": make(self.s1),
            "Neigboring surf": make(self.s2),
        }
        return d


def create_subsurface_for_interior_edge(
    edge: ZoneEdge,
    detail_: Detail,
    zones: list[Zone],
    surfaces: list[Surface],
    idf: IDF,
) -> tuple[Subsurface, Subsurface]:
    main_surface, nb_surface = get_surface_between_zones(edge, zones, edge.index)

    with logger.contextualize(s1=main_surface.display_name, s2=nb_surface.display_name):
        if main_surface.domain != nb_surface.domain:
            raise SurfaceMatchException(main_surface, nb_surface)

    check_for_airboundaries(main_surface, nb_surface)

    assert isinstance(main_surface.domain, Domain)

    # TODO check dimensions!
    detail = compare_and_maybe_change_dimensions(detail_, main_surface.domain)

    subsurf_domain = place_domain(
        main_surface.domain, *detail.location, detail.dimension
    )

    main_obj = prepare_object(
        main_surface.surface_name,
        subsurf_domain,
        main_surface.domain,
        detail,
        nb_surface.surface_name,
        True,
    )
    nb_obj = prepare_object(
        nb_surface.surface_name,
        subsurf_domain,
        main_surface.domain,
        detail,
        main_surface.surface_name,
        True,
    )

    # main_obj.write(idf)
    try:
        main_obj.write(idf)
    except AttributeError:
        # TODO -> do this with loguru
        print(main_obj.values)
        raise Exception("Problem writing Subusrface Object!")

    try:
        nb_obj.write(idf)
    except AttributeError:
        print(nb_obj.values)
        raise Exception("Problem writing Subusrface Object!")

    # nb_obj.write(idf)

    ez_surf_main = main_obj.create_ezobject(surfaces)
    ez_surf_nb = nb_obj.create_ezobject(surfaces)

    return ez_surf_main, ez_surf_nb
