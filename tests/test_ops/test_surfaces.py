from plan2eplus.cli.studies.ex.main import Cases
from plan2eplus.ops.surfaces.idfobject import IDFSurface

from rich import print

# TODO: test init surface!


def test_surface_idf():
    case = Cases().two_room
    surfaces = IDFSurface.read(case.idf)
    assert len(surfaces) == 6 * 2


def test_assign_surface_conditions():
    case = Cases().two_room
    surfaces = IDFSurface.read(case.idf)
    outward_surfaces = [
        i for i in surfaces if i.Outside_Boundary_Condition.casefold() == "outdoors"
    ]
    s1 = outward_surfaces[0].create_ezobject()
    assert s1.boundary_condition == "outdoors"


def test_get_surface_neighbor():
    case = Cases().two_room
    surfaces = [i.create_ezobject() for i in IDFSurface.read(case.idf)]
    indoor_surfaces = [
        i for i in surfaces if i.boundary_condition.casefold() == "surface"
    ]

    assert indoor_surfaces[0].neighbor_name


def test_get_idf_surface_subsurfaces():
    case = Cases().subsurfaces_simple
    zone_surfaces = case.objects.zones[0].surface_names
    print(case.objects.surfaces)

    n_surfs = 0
    for surf in zone_surfaces:
        res = IDFSurface.get_surface_subsurfaces(case.idf, surf)
        n_surfs += len(res)

    assert n_surfs == 2


if __name__ == "__main__":
    case = Cases().subsurfaces_simple
    zone_surfaces = case.objects.zones[0].surface_names
    print(case.objects.surfaces)
    # print(d)
