from plan2eplus.cli.studies.ex.afn import AFNExampleCases
from plan2eplus.ops.afn.create import create_afn_objects
from plan2eplus.ops.afn.idfobject import IDFAFNSurface


def test_ammend_afn_surface():
    case_ = AFNExampleCases.A_ew
    case = case_.case_with_subsurfaces
    afn = create_afn_objects(
        case.idf,
        case.objects.zones,
        case.objects.subsurfaces,
        case.objects.airboundaries,
    )
    surf = afn.subsurfaces[0]
    param = "External_Node_Name"
    new_value ="new external node" 
    IDFAFNSurface.update_afn_surface(
        case.idf,
        surf.subsurface_name,
        param=param,
        new_value=new_value

    )
    updated_surf = IDFAFNSurface().get_one_idf_object(
        case.idf, surf.name, identifier_name="Surface_Name"
    )
    assert updated_surf[param] == new_value



if __name__ == "__main__":
    test_ammend_afn_surface()
