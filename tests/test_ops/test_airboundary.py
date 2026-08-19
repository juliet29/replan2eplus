import pytest
from plan2eplus.errors import IDFMisunderstandingError
from plan2eplus.cli.studies.ex.subsurfaces import SubsurfaceInputOutputExamples, e0, zone_edge
from plan2eplus.ezcase.ez import EZ
from plan2eplus.ops.airboundary.create import update_airboundary_constructions
from plan2eplus.ops.subsurfaces.logic.interior import (
    create_subsurface_for_interior_edge,
)
from plan2eplus.cli.studies.ex.subsurfaces import door_details
from plan2eplus.cli.studies.ex.main import Cases
from plan2eplus.cli.studies.ex.paths import ExamplePaths
from plan2eplus.paths import Constants


def test_add_airboundary():
    case = Cases().two_room
    airboundaries = update_airboundary_constructions(
        case.idf, [e0], case.objects.zones, case.objects.surfaces
    )
    assert len(airboundaries) == 2
    for boundary in airboundaries:
        assert "Airboundary" in boundary.surface.construction_name
        assert (
            boundary.edge.space_a == e0.space_a and boundary.edge.space_b == e0.space_b
        )
    # ab = airboundaries[0]


# TODO -> test update construction set after airboudnaries are added.. -> make sure that they dont get overwritten..


def test_cant_add_subsurfacae_on_airboundary():
    case = Cases().two_room
    update_airboundary_constructions(
        case.idf, [e0], case.objects.zones, case.objects.surfaces
    )
    with pytest.raises(IDFMisunderstandingError):
        create_subsurface_for_interior_edge(
            zone_edge, door_details, case.objects.zones, case.objects.surfaces, case.idf
        )


def test_read_airboundary_from_existing_case():
    example = SubsurfaceInputOutputExamples.airboundary
    output_path = ExamplePaths.airboundary_examples / example.info.name
    case = EZ(idf_path=output_path / Constants.idf_name)
    assert len(case.objects.airboundaries) == 1 * 2


if __name__ == "__main__":
    test_read_airboundary_from_existing_case()
