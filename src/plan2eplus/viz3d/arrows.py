import math
from matplotlib.colors import Colormap, Normalize
import xarray as xr

from loguru import logger
from plan2eplus.ezcase.ez import EZ
from plan2eplus.geometry.contact_points import CardinalPoints, calculate_cardinal_points
from plan2eplus.geometry.domain import (
    Domain,
)
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.zones.ezobject import Zone
from plan2eplus.visuals.data.colorbars import data_norm
from plan2eplus.visuals.domains import compute_multidomain, expand_domain
from plan2eplus.visuals.transforms import subsurface_to_points
from plan2eplus.viz3d.arrow_curve import ArrowHeadLoc, create_segmented_arrow


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
    point_names = ["p_start", "p_mid", "p_end"]
    return {name: (*p.as_tuple, arrow_height) for name, p in zip(point_names, points)}


def make_colormaps(data: xr.DataArray):
    cmap, norm = data_norm(abs(data).values)
    return cmap, norm


def gather_data(case: EZ, data: xr.DataArray):
    data_subsurfaces = [
        i
        for i in case.objects.subsurfaces
        if i.subsurface_name.upper() in data.space_names.values
    ]

    return data_subsurfaces


def color_and_drn(
    data: xr.DataArray, subsurface_name: str, cmap: Colormap, norm: Normalize
):
    value = data.sel(space_names=subsurface_name.upper())
    norm_val = norm(abs(value))
    logger.debug(norm_val)
    color = cmap(norm_val)
    direction = ArrowHeadLoc(int(math.copysign(1, value)))

    def remap(value, lo=0.08, hi=0.15):
        return lo + (hi - lo) * value

    radius = remap(norm_val)
    logger.debug(radius)
    # "radius": norm_val
    return {
        "color": color,
        "arrow_loc": direction,
        "radius": radius,
        # "radius": remap()
    }


def make_cardinal_points(zones: list[Zone]):
    cardinal_expansion_factor = 1.4
    total_domain = compute_multidomain([i.domain for i in zones])
    cardinal_domain = expand_domain(total_domain, cardinal_expansion_factor)
    cardinal_points = calculate_cardinal_points(cardinal_domain)
    return cardinal_points


def make_case_arrows(case: EZ, data: xr.DataArray):
    # TODO: the case should passed in as path..

    data_subsurfaces = gather_data(case, data)  # TODO: unhardcode this..
    cmap, norm = make_colormaps(data)

    zones = case.objects.zones
    cardinal_points = make_cardinal_points(zones)

    coords = [
        get_arrow_coords(
            surf.domain,
            surf.edge,
            zones,
            cardinal_points,
            surf.domain.vert_range.midpoint,
        )
        for surf in data_subsurfaces
    ]

    arrows = [
        create_segmented_arrow(
            **c, **color_and_drn(data, v.subsurface_name, cmap, norm)
        )
        for c, v in zip(coords, data_subsurfaces)
    ]
    return arrows
