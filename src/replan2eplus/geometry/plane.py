from geomeppy.geom.polygons import Polygon3D
from replan2eplus.geometry.coords import Coordinate3D
from replan2eplus.geometry.domain import Domain, Plane, AXIS


def get_location_of_fixed_plane(plane: AXIS, coords: list[Coordinate3D]):
    plane_locs = [coord.get_plane_axis_location(plane.lower()) for coord in coords]
    unique_loc = set(plane_locs)
    assert len(unique_loc) == 1
    return plane_locs[0]


def create_domain_from_coords(normal_axis: AXIS, coords: list[Coordinate3D]):
    match normal_axis:
        case "X":
            pair = ("y", "z")

        case "Y":
            pair = ("x", "z")

        case "Z":
            pair = ("x", "y")
        case _:
            raise Exception("Invalid Direction!")

    def get_2D_coords(l1, l2):
        return [coord.get_pair(l1, l2) for coord in coords]

    location_of_fixed_plane = get_location_of_fixed_plane(normal_axis, coords)

    coords_2D = get_2D_coords(*pair)
    domain = Domain.from_coords_list(coords_2D)
    return Domain(
        domain.horz_range,
        domain.vert_range,
        plane=Plane(normal_axis, location_of_fixed_plane),
    )


# def compute_unit_normal(surface: EpBunch) -> AXIS:

#     vector_map: dict[tuple[int, int, int], AXIS] = {
#         (1, 0, 0): "X",
#         (0, 1, 0): "Y",
#         (0, 0, 1): "Z",
#     }
#     polygon = Polygon3D(surface.coords)
#     print(polygon)
#     normal_vector = polygon.normal_vector
#     nv = tuple([abs(int(i)) for i in normal_vector])
#     assert len(nv) == 3
#     return vector_map[nv]


def compute_unit_normal_coords(coords: list[tuple[float, float, float]]) -> AXIS:
    vector_map: dict[tuple[int, int, int], AXIS] = {
        (1, 0, 0): "X",
        (0, 1, 0): "Y",
        (0, 0, 1): "Z",
    }
    polygon = Polygon3D(coords)
    print(polygon.vertices)
    normal_vector = polygon.normal_vector
    nv = tuple([abs(int(i)) for i in normal_vector])
    assert len(nv) == 3
    return vector_map[nv]
