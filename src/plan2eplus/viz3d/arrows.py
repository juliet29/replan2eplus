import math
from pathlib import Path
import xarray as xr

from loguru import logger
from plan2eplus.ezcase.ez import EZ
from plan2eplus.geometry.contact_points import CardinalPoints, calculate_cardinal_points
from plan2eplus.geometry.domain import (
    Domain,
)
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.zones.ezobject import Zone
from plan2eplus.results.sql import get_qoi
from plan2eplus.visuals.data.colorbars import data_norm
from plan2eplus.visuals.domains import compute_multidomain, expand_domain
from plan2eplus.visuals.transforms import subsurface_to_points
from plan2eplus.viz3d.arrow_mesh import create_segmented_arrow


# TODO: dont think a cylinder is needed.. maybe better to do flat shape if possible ? or rectnagle => decrease the resolution..
#
def get_arrow_coords(
    domain: Domain,
    edge: Edge,
    zones: list[Zone],
    cardinal_coords: CardinalPoints,
    arrow_height: float,
):

    points = subsurface_to_points(domain, edge, zones, cardinal_coords)
    return [(*p.as_tuple, arrow_height) for p in points]


def handle_colors(data: xr.DataArray):
    cmap, norm = data_norm(abs(data).values)
    value_signs = [int(math.copysign(1, i)) for i in data.values]

    colors = cmap(norm(data))
    logger.debug(colors)
    return cmap, norm, value_signs


def gather_data(case: EZ, sql_path: Path, hour: int):
    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate", sql_path)
    flow_21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate", sql_path)
    combined_flow = flow_12.select_time(hour) - flow_21.select_time(hour)
    data_subsurfaces = [
        i
        for i in case.objects.subsurfaces
        if i.subsurface_name.upper() in combined_flow.space_names.values
    ]

    return combined_flow, data_subsurfaces


def make_case_arrows(case: EZ, sql_path: Path):
    # TODO: the case should passed in as path..
    cardinal_expansion_factor = 1.2

    data, data_subsurfaces = gather_data(case, sql_path, 12)  # TODO: unhardcode this..
    cmap, norm, value_signs = handle_colors(data)

    zones = case.objects.zones
    z0 = zones[0]
    surf = [i for i in z0.surfaces if i.surface_type == "wall"][0]
    assert isinstance(surf.domain, Domain)
    height = surf.domain.vert_range.max
    logger.debug(height)
    arrow_height = (
        height / 2
    )  # TODO: dummy height for now -> needs to go through subsurfaces

    total_domain = compute_multidomain([i.domain for i in zones])
    cardinal_domain = expand_domain(total_domain, cardinal_expansion_factor)
    cardinal_points = calculate_cardinal_points(cardinal_domain)

    # subsurfs = case.objects.subsurfaces
    # surf0 = subsurfs[0]
    coords = [
        get_arrow_coords(surf.domain, surf.edge, zones, cardinal_points, arrow_height)
        for surf in data_subsurfaces
    ]
    logger.debug(coords)
    # coords0 = get_arrow_coords(
    #     surf0.domain, surf0.edge, zones, cardinal_points, arrow_height
    # )
    # logger.debug(coords0)

    arrows = [create_segmented_arrow(*c, radius=0.05) for c in coords]
    logger.debug(arrows)
    return arrows
