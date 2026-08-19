from plan2eplus.cli.studies.ex.afn import AFNExampleCases, AFNCaseDefinition
from plan2eplus.ezcase.ez import EZ
from plan2eplus.cli.studies.ex.paths import ExamplePaths
from plan2eplus.paths import Constants

from plan2eplus.cli.studies.ex.main import Interfaces
from plan2eplus.ops.afn.logic import (
    check_surfaces_for_nbs,
    determine_afn_objects,
    get_avail_surfaces,
    get_avail_zones,
)
import pytest
from rich import print

from plan2eplus.ops.afn.create import create_afn_objects, select_afn_objects
from plan2eplus.ops.afn.interfaces import IDFAFNSurface, IDFAFNZone


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_get_avail_zones(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    zones = get_avail_zones(active_case.objects.zones)

    assert len(zones) == case.n_zones_with_two_plus_valid_surfaces


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_get_avail_subsurfaces(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    avail_zones = get_avail_zones(active_case.objects.zones)
    avail_subsurfaces = get_avail_surfaces(active_case.objects.subsurfaces, avail_zones)
    assert len(avail_subsurfaces.to_list()) == case.n_surfaces_in_avail_zones


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_filter_subsurfaces(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    avail_zones = get_avail_zones(active_case.objects.zones)
    res = get_avail_surfaces(active_case.objects.subsurfaces, avail_zones).pipe(
        check_surfaces_for_nbs
    )
    assert len(res) == case.n_surfaces_after_check_nbs


@pytest.mark.parametrize("case_", AFNExampleCases().list)
def test_get_afn_objects(case_: AFNCaseDefinition):
    case = case_.case_with_subsurfaces
    zones, surfs = determine_afn_objects(case.objects.zones, case.objects.subsurfaces)
    assert len(zones) == case_.n_zones_in_afn
    assert len(surfs) == case_.n_surfs_in_afn


def test_selecting_afn_zones():
    case_ = AFNExampleCases().B_ne
    case = case_.case_with_subsurfaces
    afn = select_afn_objects(case.objects.zones, case.objects.subsurfaces, [])
    assert len(afn.zones) == case_.n_zones_in_afn
    assert afn.zones[0].room_name == Interfaces.rooms.r1.name


@pytest.mark.xfail()  #
def test_selecting_afn_surfaces():
    case_ = AFNExampleCases().B_ne
    case = case_.case_with_subsurfaces
    afn = select_afn_objects(case.objects.zones, case.objects.subsurfaces, [])
    assert len(afn.subsurfaces) == case_.n_surfs_in_afn


def test_adding_afn_objects():
    case_ = AFNExampleCases().B_ne
    case = case_.case_with_subsurfaces
    _ = create_afn_objects(case.idf, case.objects.zones, case.objects.subsurfaces, [])
    print(case.idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"])
    # TOOD -> do more ioobjects need this?
    surfs = IDFAFNSurface.read_and_filter(case.idf)
    assert len(surfs) == case_.n_surfs_in_afn

    zones = IDFAFNZone.read_and_filter(case.idf)
    assert len(zones) == case_.n_zones_in_afn


def test_reading_existing_afn():
    # NOTE: the afn should be the same given the same input of zones, subsurfaces, and airboundaries..

    case_ = AFNExampleCases().B_ne
    output_path = ExamplePaths.afn_examples / case_.name
    case = EZ(idf_path=output_path / Constants.idf_name)

    assert len(case.objects.airflow_network.afn_surfaces) == case_.n_surfs_in_afn

    assert len(case.objects.airflow_network.zones) == case_.n_zones_in_afn


def reg_test():
    def study(case_: AFNCaseDefinition):
        print(case_.name)
        case = case_.case_with_subsurfaces
        zones, surfs = determine_afn_objects(
            case.objects.zones, case.objects.subsurfaces
        )

        print(f"found_zones: {[i.room_name for i in zones]}")

    for case in AFNExampleCases().list:
        study(case)


if __name__ == "__main__":
    test_reading_existing_afn()
