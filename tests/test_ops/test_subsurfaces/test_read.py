import pytest
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.subsurfaces.idfobject import read_subsurfaces
from plan2eplus.cli.studies.ex.paths import ExamplePaths
from plan2eplus.cli.studies.ex.subsurfaces import (
    SubsurfaceInputOutput,
    SubsurfaceInputOutputExamples,
)
from plan2eplus.paths import Constants


def prep_test_read_subsurfaces(example: SubsurfaceInputOutput):
    input_path = ExamplePaths.subsurface_examples / example.info.name
    case = EZ(input_path / Constants.idf_name)
    subsurfs = read_subsurfaces(case.idf)
    assert len(subsurfs) == example.info.sum_subsurfaces


@pytest.mark.parametrize("example", SubsurfaceInputOutputExamples().list_examples)
def test_read_subsurfaces(example):
    prep_test_read_subsurfaces(example)


def prep_test_autoread_subsurfaces(example: SubsurfaceInputOutput):
    input_path = ExamplePaths.subsurface_examples / example.info.name
    case = EZ(input_path / Constants.idf_name)
    assert len(case.objects.subsurfaces) == example.info.sum_subsurfaces


@pytest.mark.parametrize("example", SubsurfaceInputOutputExamples().list_examples)
def test_autoread_subsurfaces(example):
    prep_test_autoread_subsurfaces(example)


if __name__ == "__main__":
    examples = SubsurfaceInputOutputExamples()
    for ex in examples.list_examples:
        # for ex in examples.list_examples:
        prep_test_autoread_subsurfaces(ex)
