from geomeppyupdated import IDF
from utils4plans.sets import set_equality

from plan2eplus.cli.studies.ex.main import Cases, EpAFNCase, Interfaces
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.base import get_names_of_idf_objects
from plan2eplus.ops.materials.idfobject import IDFMaterial
from plan2eplus.ops.materials.utils import (
    read_materials,
    read_materials_from_many_idf,
)
from plan2eplus.eppaths.logic import EpPaths


def test_read_material_of_type_a_from_idf():
    case = EZ(
        Cases().ep_afn.path
    )  # TODO replace with own example once get materials working
    materials = IDFMaterial.read(case.idf)
    found_material_names = [i.Name for i in materials]
    assert set_equality(found_material_names, EpAFNCase.basic_material_names)


def test_read_materials_from_idf_by_name():
    case = EZ(Cases().ep_afn.path)
    found_materials = read_materials(case.idf, EpAFNCase.mixed_subset_materials)
    assert set_equality(
        get_names_of_idf_objects(found_materials), EpAFNCase.mixed_subset_materials
    )
    # TODO test reading bad materials -> at least create a log..


def test_read_many_materials_from_many_idfs():
    materials = Interfaces.materials.materials_across_idfs
    ep_paths = EpPaths()
    found_materials = read_materials_from_many_idf(ep_paths.material_idfs, materials)
    assert set_equality(get_names_of_idf_objects(found_materials), materials)


def test_write_material():
    source_case = EZ(Cases().ep_afn.path)
    source_materials = IDFMaterial.read(source_case.idf)
    destination_case = Cases().base
    new_idf = source_materials[0].write(destination_case.idf)
    new_materials = IDFMaterial.read(new_idf)
    assert new_materials[0].Name == source_materials[0].Name


def test_write_materials():
    source_case = EZ(Cases().ep_afn.path)
    source_materials = IDFMaterial.read(source_case.idf)
    destination_case = Cases().base
    new_idf = IDF()
    for material in source_materials:
        new_idf = material.write(destination_case.idf)
    new_materials = IDFMaterial.read(new_idf)
    assert set_equality(
        get_names_of_idf_objects(new_materials),
        get_names_of_idf_objects(source_materials),
    )


if __name__ == "__main__":
    test_read_material_of_type_a_from_idf()
