from geomeppyupdated.idf import IDF
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.subsurfaces.idfobject import subsurface_objects


def get_subsurface_epbunches(idf: IDF):
    epbunches = []
    for object_type in subsurface_objects:
        objects = idf.idfobjects[object_type().key]
        epbunches.extend(epbunches)
    return epbunches


def prep_to_obj(case: EZ):
    def subsurface_to_fenestration_objects():
        pass

    pass
    # change all subsurface to fenestration objects..
    subsurfaces = case.objects.subsurfaces

    # delete all subsurfaces..
    epbunches = get_subsurface_epbunches(case.idf)
