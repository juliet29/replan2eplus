from dataclasses import dataclass, field
from pathlib import Path

from eppy.modeleditor import IDDAlreadySetError
from geomeppyupdated.idf import IDF

from plan2eplus.ops.init.create import add_init_objects
from plan2eplus.ops.run_settings.defaults import default_analysis_period
from plan2eplus.ops.run_settings.user_interfaces import AnalysisPeriod
from plan2eplus.paths import Constants


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


def initialize_idd(idd_path: Path):
    try:
        IDF.setiddname(idd_path)
    except IDDAlreadySetError:
        pass


@dataclass
class RunSettings:
    output_path: Path | None = None
    epw_path: Path | None = None
    analysis_period: AnalysisPeriod = field(
        default_factory=lambda: default_analysis_period
    )

    def output_root(self) -> Path:
        assert (
            self.output_path
        ), "No output_path set on the case's run_settings - don't know where to write outputs."
        return self.output_path

    @property
    def output_idf_path(self) -> Path:
        return self.output_root() / Constants.idf_name

    @property
    def output_results_path(self) -> Path:
        return self.output_root() / Constants.results_location

    @property
    def output_schedules_path(self) -> Path:
        return self.output_root() / Constants.schedule_location
