from replan2eplus.geometry.coords import Coordinate3D
from replan2eplus.geometry.domain import Domain, Plane, AXIS


def get_plane_axis_location(plane: AXIS, coords: list[Coordinate3D]):
    plane_locs = [coord.get_plane_axis_location(plane.lower()) for coord in coords]
    unique_loc = set(plane_locs)
    assert len(unique_loc) == 1
    return plane_locs[0]


def create_domain_from_coords(normal_axis: AXIS, coords: list[Coordinate3D]):
    match normal_axis:
        case "X":
            pair = ("x", "z")
            fixed_plane = "Y"


        case "Y":
            pair = ("y", "z")
            fixed_plane = "X"

        case "Z":
            pair = ("x", "y")
            fixed_plane = "Z"
        case _:
            raise Exception("Invalid Direction!")

    def get_2D_coords(l1, l2):
        return [coord.get_pair(l1, l2) for coord in coords]


    plane_location = get_plane_axis_location(fixed_plane, coords)

    coords_2D = get_2D_coords(*pair)
    domain = Domain.from_coords_list(coords_2D) 
    return Domain(
        domain.horz_range, domain.vert_range, plane=Plane(fixed_plane, plane_location)
    )
