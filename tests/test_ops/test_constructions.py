from geomeppyupdated import IDF
from rich import print
from utils4plans.lists import chain_flatten
from utils4plans.sets import set_equality

from plan2eplus.cli.studies.ex.main import Cases, EpAFNCase, Interfaces
from plan2eplus.cli.studies.ex.materials import SAMPLE_CONSTRUCTION_SET
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.base import get_names_of_idf_objects
from plan2eplus.ops.constructions.create import create_constructions
from plan2eplus.ops.constructions.idfobject import IDFConstruction
from plan2eplus.ops.constructions.utils import (
    read_constructions_and_assoc_materials,
    read_constructions_by_name_from_many_idfs,
    read_materials_for_construction,
)
from plan2eplus.ops.subsurfaces.create import read_subsurfaces
from plan2eplus.ops.surfaces.idfobject import IDFSurface
from plan2eplus.ep_paths import ep_paths


def test_read_constructions():
    case = EZ(Cases().ep_afn.path)
    constructions = IDFConstruction.read(case.idf)
    const_names = get_names_of_idf_objects(constructions)
    assert set_equality(const_names, EpAFNCase.constructions)


def test_read_construction_by_name():
    case = EZ(Cases().ep_afn.path)
    name = EpAFNCase.constructions[0]
    constructions = IDFConstruction.read_by_name(case.idf, [name])
    const_names = get_names_of_idf_objects(constructions)
    assert set_equality(const_names, [name])


def test_read_material_based_on_construction():
    case = EZ(Cases().ep_afn.path)
    assert case.idf_path
    name = EpAFNCase.constructions[0]
    construction = IDFConstruction.read_by_name(
        case.idf, [name]
    )  # TODO special handling if its just one object
    assert len(construction) == 1

    found_materials = read_materials_for_construction([case.idf_path], construction[0])
    assert set_equality(
        get_names_of_idf_objects(found_materials), construction[0].materials
    )


def test_read_construction_across_idfs():
    names = Interfaces.constructions.constructions_across_idfs
    found_constructions = read_constructions_by_name_from_many_idfs(
        ep_paths.construction_idfs, names
    )
    print(chain_flatten([i.materials for i in found_constructions]))
    assert set_equality(get_names_of_idf_objects(found_constructions), names)


def test_read_constructions_and_materials_across_idfs():
    const_names = Interfaces.constructions.constructions_across_idfs
    results = read_constructions_and_assoc_materials(
        ep_paths.construction_idfs, ep_paths.material_idfs, const_names
    )
    result_names = get_names_of_idf_objects(results.constructions + results.materials)
    mat_names = Interfaces.constructions.materials_for_const_across_idfs
    assert set_equality(result_names, mat_names + const_names)


def test_write_constructions():
    source_case = EZ(Cases().ep_afn.path)
    source_constructions = IDFConstruction.read(source_case.idf)
    destination_case = Cases().base
    new_idf = IDF()
    for construction in source_constructions:
        new_idf = construction.write(destination_case.idf)

    new_constructions = IDFConstruction.read(new_idf)
    print(new_constructions)
    print(IDFConstruction().get_idf_objects(new_idf))
    print(IDFConstruction().get_idf_objects(source_case.idf))
    assert set_equality(
        get_names_of_idf_objects(new_constructions),
        get_names_of_idf_objects(source_constructions),
    )


def test_write_ep_construction_set():
    case = Cases().subsurfaces_simple
    create_constructions(
        case.idf,
        ep_paths.construction_idfs,
        ep_paths.material_idfs,
        SAMPLE_CONSTRUCTION_SET,
        case.objects.surfaces,
        case.objects.subsurfaces,
    )
    surface_consts = [i.Construction_Name for i in IDFSurface.read(case.idf)]
    subsurface_consts = [i.Construction_Name for i in read_subsurfaces(case.idf)]
    assert set_equality(
        surface_consts + subsurface_consts, SAMPLE_CONSTRUCTION_SET.names
    )


if __name__ == "__main__":
    test_write_constructions()
