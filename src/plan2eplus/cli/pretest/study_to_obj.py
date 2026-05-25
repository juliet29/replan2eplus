from loguru import logger
from geomeppyupdated.geom.polygons import Polygon3D
from plan2eplus.ezcase.ez import EZ
from geomeppyupdated.idf import IDF
from plan2eplus.geometry.contact_points import calculate_corner_points
from plan2eplus.geometry.domain import Domain
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.subsurfaces.fenestration_idfobject import IDFFenestrationObject
from plan2eplus.ops.subsurfaces.idfobject import subsurface_objects


def get_subsurface_epbunches(idf: IDF):
    epbunches = []
    for object_type in subsurface_objects:
        objects = idf.idfobjects[object_type().key]
        epbunches.extend(objects)
    return epbunches


def prep_to_obj(case: EZ):
    # TODO: need to make sure dont change underlying IDF! In case need to use again..  test the eppy copy method will work.. may need to re-init as a geomeppy IDF
    # case = deepcopy(case_)  # will make changes to copy of idf
    idf = case.idf

    def subsurface_to_fenestration_object(surf: Subsurface):
        domain = surf.domain
        assert isinstance(domain, Domain)
        polygon_coords = calculate_corner_points(domain).tuple_list
        polygon = Polygon3D(polygon_coords)

        logger.debug(surf.subsurface_type)

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
    logger.debug(subsurfaces)

    fen_objects = [subsurface_to_fenestration_object(i) for i in subsurfaces]
    logger.debug(idf.idfobjects["FENESTRATIONSURFACE:DETAILED"])
    # logger.debug(fen_objects)

    # delete all subsurfaces..
    epbunches = get_subsurface_epbunches(idf)

    logger.debug(epbunches)
    for ep in epbunches:
        idf.removeidfobject(ep)

    obj = idf.to_obj("test.obj")
