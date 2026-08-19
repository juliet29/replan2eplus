from pathlib import Path
from geomeppyupdated import IDF
from ladybug.epw import EPW as LBEPW
from dataclasses import dataclass

from plan2eplus.ops.run_settings.idfobject import IDFLocation, IDFRunPeriod


@dataclass
class AnalysisPeriod:
    name: str
    st_month: int
    end_month: int
    st_day: int
    end_day: int

    def create_idf_object(self):
        return IDFRunPeriod(
            self.name, self.st_month, self.end_month, self.st_day, self.end_day
        )


@dataclass
class EPW:
    path: Path

    def create_idf_object(self):
        epw = LBEPW(self.path)
        loc = epw.location

        return IDFLocation(
            loc.city, loc.latitude, loc.longitude, loc.time_zone, loc.elevation
        )


def write_run_period_and_location(
    idf: IDF, analysis_period: AnalysisPeriod, epw_path: Path
):
    ap_object = analysis_period.create_idf_object()
    ap_object.overwrite(idf)

    location_object = EPW(epw_path).create_idf_object()
    location_object.overwrite(idf)
