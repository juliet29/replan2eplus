from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.contact_points import calculate_corner_points
from plan2eplus.ops.subsurfaces.interfaces import Dimension
from plan2eplus.geometry.range import Range
from plan2eplus.ops.subsurfaces.idfobject import (
    IDFDoor,
    IDFDoorInterzone,
    IDFSubsurfaceBase,
    IDFWindow,
)
from plan2eplus.ops.subsurfaces.config import DOMAIN_SHRINK_FACTOR
from plan2eplus.ops.subsurfaces.user_interfaces import Detail


def compare_and_maybe_change_dimensions(detail: Detail, domain: Domain):
    def compare_and_maybe_change_dimension(
        dimension: float, range_: Range, shrink_factor=DOMAIN_SHRINK_FACTOR
    ):
        if dimension >= range_.size:
            return range_.size * shrink_factor
        return dimension

    dimension = detail.dimension
    width = compare_and_maybe_change_dimension(dimension.width, domain.horz_range)
    height = compare_and_maybe_change_dimension(dimension.height, domain.vert_range)
    return Detail(Dimension(width, height), detail.location, detail.type_)


def compare_range(range_: Range, subsurf_range_: Range):
    if subsurf_range_.min < range_.min or subsurf_range_.max > range_.max:
        raise Exception(
            f"Arrangement is invalid! Domain range: {range_}. Subsurface range: {subsurf_range_}"
        )  # TODO add more contxt!


def compare_domain(domain: Domain, subsurf_domain: Domain):
    compare_range(domain.horz_range, subsurf_domain.horz_range)
    compare_range(domain.vert_range, subsurf_domain.vert_range)


def create_ss_name(surface_name: str, detail: Detail):
    if surface_name:
        return f"{detail.type_}__{surface_name}"
    else:
        return ""


def get_idf_subsurface_object(detail: Detail, is_interior: bool):
    match detail.type_.lower(), is_interior:
        case "door", True:
            return IDFDoorInterzone
        case "door", False:
            return IDFDoor
        case "window", False:
            return IDFWindow
        case "window", True:
            raise NotImplementedError("Have not considered interior windows!")
        case _:
            raise Exception(
                f"Invalid entries: detail_type should be window or door but is {detail.type_} | is_interior should be bool but is {is_interior}"
            )


# def prepare_geometry(surface: Surface, )
# TODO this goes to logic! TODO number files in logic _04_indiv_subsurf
def prepare_object(
    surface_name: str,
    subsurf_domain: Domain,
    main_surface_domain: Domain,
    detail: Detail,
    nb_surface_name: str,
    is_interior,
):

    # HERE CHECK SUBSURF DOMAINS..
    compare_domain(main_surface_domain, subsurf_domain)
    # polygon_coords = calculate_corner_points(subsurf_domain).tuple_list
    # polygon = Polygon3D(polygon_coords)
    # with logger.contextualize(loc="Checking createio of coords, wll 2D work?"):
    #     coords = calculate_corner_points(subsurf_domain).tuple_list
    #     logger.debug(coords)
    #     p = Polygon3D(coords)
    #     logger.debug(p)
    # raise Exception("Done with Coords")
    #
    subsurf_coord = calculate_corner_points(subsurf_domain).SOUTH_WEST
    surf_coord = calculate_corner_points(main_surface_domain).SOUTH_WEST
    # TODO: this should be in its own function..
    coords = (
        subsurf_coord.x - surf_coord.x,
        subsurf_coord.y - surf_coord.y,
    )  # need to subtract the surface corner..
    dims = detail.dimension.as_tuple

    # empty when created, has to be updated later via construction set
    construction_name = ""

    idfobject = get_idf_subsurface_object(detail, is_interior)
    # TODO consider making this a typed dict?
    values = IDFSubsurfaceBase(
        create_ss_name(surface_name, detail),
        surface_name,
        construction_name,
        *coords,
        *dims,
        # Polygon=polygon,
    ).values

    if hasattr(idfobject, "Outside_Boundary_Condition_Object"):
        return idfobject(
            **values,
            Outside_Boundary_Condition_Object=create_ss_name(
                nb_surface_name, detail
            ),  # pyright: ignore[reportCallIssue]
        )
    else:
        return idfobject(**values)
