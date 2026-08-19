from geomeppyupdated import IDF
from loguru import logger
from rich.pretty import pretty_repr

from plan2eplus.errors import BadlyFormatedIDFError, IDFMisunderstandingError
from plan2eplus.ops.subsurfaces.idfobject import read_subsurfaces
from plan2eplus.ops.subsurfaces.logic.exterior import (
    create_subsurface_for_exterior_edge,
)
from plan2eplus.ops.subsurfaces.logic.interior import (
    SurfaceMatchException,
    create_subsurface_for_interior_edge,
)
from plan2eplus.ops.subsurfaces.user_interfaces import SubsurfaceInputs
from plan2eplus.ops.surfaces.ezobject import Surface
from plan2eplus.ops.surfaces.utils import update_surface_relations
from plan2eplus.ops.zones.ezobject import Zone


def create_subsurfaces(
    inputs: SubsurfaceInputs | None,
    surfaces: list[Surface],
    zones: list[Zone],
    idf: IDF,
):
    idf_subsurfaces = read_subsurfaces(idf)
    # NOTE: have not defined all the possible types of subsurfaces, so error will result if the type is of say "Window:Interzone"
    # if idf_subsurfaces:

    existing_subsurfaces = []
    if idf_subsurfaces:
        for i in idf_subsurfaces:
            res = i.create_ezobject(surfaces)
            existing_subsurfaces.append(res)
    # NOTE: dont have to update surface subsurface here bc idf already knows the relations

    if inputs:
        # interior_subsurfaces = chain_flatten(
        #     [
        #         create_subsurface_for_interior_edge(edge, detail, zones, surfaces, idf)
        #         for edge, detail in inputs.zone_pairs
        #     ]
        # )

        interior_subsurfaces = []
        for edge, detail in inputs.zone_pairs:
            try:
                res = create_subsurface_for_interior_edge(
                    edge, detail, zones, surfaces, idf
                )
            except IDFMisunderstandingError as e:
                logger.warning(
                    f"Could not make interior surfaces for {edge.as_tuple} due to {e}"
                )
                continue
            except SurfaceMatchException as e:
                logger.warning(pretty_repr(e.message()))
                continue
            interior_subsurfaces.extend(res)

        exterior_subsurfaces = []
        for edge, detail in inputs.zone_drn_pairs:
            try:
                res = create_subsurface_for_exterior_edge(
                    edge, detail, zones, surfaces, idf
                )
            except BadlyFormatedIDFError as e:
                logger.warning(
                    f"Could not make exterior surface for {edge.as_tuple} due to {e}"
                )
                continue
            exterior_subsurfaces.append(res)

        # exterior_subsurfaces =
        #     create_subsurface_for_exterior_edge(edge, detail, zones, surfaces, idf)
        #     for edge, detail in inputs.zone_drn_pairs
        # ]

        for surf in surfaces:
            # print(f"checking surf: {surf.surface_name}")
            update_surface_relations(idf, surf)

        return interior_subsurfaces + exterior_subsurfaces + existing_subsurfaces

    return existing_subsurfaces
