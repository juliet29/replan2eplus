from pathlib import Path
from loguru import logger
from geomeppyupdated.geom.polygons import Polygon3D
from rich.pretty import pretty_repr
from plan2eplus.errors import IDFMisunderstandingError
from plan2eplus.ezcase.ez import EZ
from geomeppyupdated.idf import IDF
from plan2eplus.geometry.contact_points import CornerPoints3D
from plan2eplus.geometry.coords import Coordinate3D
from plan2eplus.geometry.domain import Domain
from plan2eplus.ops.init.idfobject import GlobalGeometryRules
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.subsurfaces.fenestration_idfobject import IDFFenestrationObject
from plan2eplus.ops.subsurfaces.idfobject import subsurface_objects


def get_subsurface_epbunches(idf: IDF):
    epbunches = []
    for object_type in subsurface_objects:
        objects = idf.idfobjects[object_type().key]
        epbunches.extend(objects)
    return epbunches


def domain_to_3D_coords(domain: Domain, idf: IDF):
    ggr = GlobalGeometryRules().read(idf)[0]
    assert ggr.Starting_Vertex_Position == "UpperLeftCorner"
    assert ggr.Vertex_Entry_Direction == "CounterClockwise"
    assert domain.plane
    plane = domain.plane
    # TODO: make sure is not ortho domain..
    if plane.axis == "Z":
        raise IDFMisunderstandingError("Unexpected subsurface with Z Normal axis")
    else:
        hr = domain.horz_range
        vr = domain.vert_range
    if plane.axis == "X":
        res = CornerPoints3D(
            NORTH_EAST=Coordinate3D(plane.location, hr.max, vr.max),
            SOUTH_EAST=Coordinate3D(plane.location, hr.max, vr.min),
            SOUTH_WEST=Coordinate3D(plane.location, hr.min, vr.min),
            NORTH_WEST=Coordinate3D(plane.location, hr.min, vr.max),
        )

    else:
        assert plane.axis == "Y"

        res = CornerPoints3D(
            NORTH_EAST=Coordinate3D(hr.max, plane.location, vr.max),
            SOUTH_EAST=Coordinate3D(hr.max, plane.location, vr.min),
            SOUTH_WEST=Coordinate3D(hr.min, plane.location, vr.min),
            NORTH_WEST=Coordinate3D(hr.min, plane.location, vr.max),
        )
    arr = [res.NORTH_WEST, res.SOUTH_WEST, res.SOUTH_EAST, res.NORTH_EAST]
    coords = [i.as_three_tuple for i in arr]
    return coords


def prep_to_obj(idf_path: Path, obj_path: Path):
    case = EZ(idf_path)
    # TODO: need to make sure dont change underlying IDF! In case need to use again..  test the eppy copy method will work.. may need to re-init as a geomeppy IDF
    # case = deepcopy(case_)  # will make changes to copy of idf
    idf = case.idf

    def subsurface_to_fenestration_object(surf: Subsurface):
        domain = surf.domain
        assert isinstance(domain, Domain)
        logger.debug(domain.plane)
        polygon_coords = domain_to_3D_coords(domain, case.idf)
        polygon = Polygon3D(polygon_coords)

        logger.debug(pretty_repr(polygon_coords))
        # raise Exception("check polygon")

        fen = IDFFenestrationObject(
            Name=surf.subsurface_name,
            Surface_Type=surf.subsurface_type,
            Construction_Name=surf.construction_name,
            Building_Surface_Name=surf.surface.surface_name,
            Outside_Boundary_Condition_Object=surf.neighbor_name_,
            Polygon=polygon,
        )
        fen.write(idf)
        return fen
        # return fen

    pass
    # change all subsurface to fenestration objects..
    subsurfaces = case.objects.subsurfaces
    # logger.debug(subsurfaces)

    fen_objects = [subsurface_to_fenestration_object(i) for i in subsurfaces]
    logger.debug(idf.idfobjects["FENESTRATIONSURFACE:DETAILED"])
    # logger.debug(fen_objects)

    # delete all subsurfaces..
    epbunches = get_subsurface_epbunches(idf)

    for ep in epbunches:
        idf.removeidfobject(ep)

    obj = idf.to_obj(str(obj_path))
    # TODO: add path as a variable..
    # TODO: should clear IDF as a sign that can't use it again => now corruped untill inocorporate Fenestration method fully..
