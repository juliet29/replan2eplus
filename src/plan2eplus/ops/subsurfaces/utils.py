# functions used in other parts of the code!

# def filter_subsurfaces():
#     # TODO: for now use dummy hash, later add some sort of ordering..
#     # do want to keep in the edge order though..
#     pass
from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.range import Range
from plan2eplus.ops.surfaces.ezobject import Surface


def create_surface_domain(
    surface: Surface,
    starting_x_coordinate: float,
    starting_z_coordinate: float,
    length: float,
    height: float,
):
    surf_domain = surface.domain
    assert surface.surface_type.casefold() == "Wall".casefold()
    assert isinstance(surf_domain, Domain)
    surface_min_horz = surf_domain.horz_range.min
    surface_min_vert = surf_domain.vert_range.min

    horz_min = surface_min_horz + float(starting_x_coordinate)
    width = float(length)
    if not starting_z_coordinate:
        starting_z_coordinate = 0  # TODO: make better solution! !, ie also check if it is a str, or for both, make sure that empty string is read in as 0..
    vert_min = surface_min_vert + float(starting_z_coordinate)
    height = float(height)

    horz_range = Range(horz_min, horz_min + width)
    vert_range = Range(vert_min, vert_min + height)

    return Domain(horz_range, vert_range, surf_domain.plane)


def create_surface_coords():
    pass
