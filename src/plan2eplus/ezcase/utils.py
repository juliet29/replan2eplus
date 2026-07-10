from dataclasses import dataclass
from eppy.modeleditor import IDDAlreadySetError
from geomeppyupdated.idf import IDF


from pathlib import Path

from plan2eplus.io.files import get_or_make_folder_path


from plan2eplus.ops.init.create import add_init_objects
from plan2eplus.ops.run_settings.defaults import default_analysis_period
from plan2eplus.ops.run_settings.user_interfaces import AnalysisPeriod
from plan2eplus.paths import Constants
from plan2eplus.ep_paths import ep_paths


def open_idf(idf_path: Path | None = None):
    if idf_path:
        assert idf_path.exists(), f"Invalid idf path: {idf_path}"
        return IDF(idf_path)
    idf = IDF()
    idf.initnew(None)
    add_init_objects(
        idf
    )  # TODO: ordinarily, need to do some checking to ensure that these objects dont already exist.., but they are not part of the ezobjects
    return idf


def initialize_idd():
    try:
        IDF.setiddname(ep_paths.idd_path)
    except IDDAlreadySetError:
        pass


# TODO: should probably be in interfaces or something like this?
@dataclass
class RunVariablesInput:
    # OUTPUTS
    output_idf_path: Path | None = None
    output_results_path: Path | None = None
    output_schedules_path: Path | None = None
    # INPUTS
    epw_path: Path | None = None
    analysis_period: AnalysisPeriod | None = None


@dataclass
class RunVariablesOutput:
    # OUTPUTS
    output_idf_path: Path
    output_results_path: Path
    output_schedules_path: Path
    # INPUTS
    epw_path: Path
    analysis_period: AnalysisPeriod


def no_path_spec_message(name: str):
    return f"No output path specified for {name} and not output_path specified for the case"


def handle_run_variables(
    v: RunVariablesInput,
    case_output_path: Path | None,
):
    # NOTE: when using defaults, this function will take care of creating the directories if they dont already exist, for non-EnergyPlus writes. Otherwise, the calling function should take care of this.

    if not v.output_idf_path:
        assert case_output_path, no_path_spec_message("the IDF")
        v.output_idf_path = case_output_path / Constants.idf_name

    if not v.output_results_path:
        assert case_output_path, no_path_spec_message("the results")
        v.output_results_path = case_output_path / Constants.results_location

    if not v.output_schedules_path:
        assert case_output_path, no_path_spec_message("the schedules")
        sched_path = case_output_path / Constants.schedule_location
        get_or_make_folder_path(sched_path)
        v.output_schedules_path = sched_path

    # NOTE: not going to change Case variables when do the run..
    if not v.epw_path:
        v.epw_path = ep_paths.default_weather

    # ANALYSIS PERIOD
    if not v.analysis_period:
        v.analysis_period = default_analysis_period

    return RunVariablesOutput(**v.__dict__)
