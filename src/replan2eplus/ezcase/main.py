from dataclasses import dataclass
from pathlib import Path
from replan2eplus.ezobjects.idf import IDF
from replan2eplus.zones.interfaces import Room
from replan2eplus.zones.presentation import create_zones


@dataclass  # TODO: is this really a dataclass? -> need to do some initialization logic, and keep track of state variables, so probably not, in the long term..
class EZCase:
    path_to_idd: Path
    path_to_initial_idf: Path


    # TODO: do these need to be initialized here?
    # path_to_weather: Path
    # path_to_analysis_period: AnalysisPeriod

    def initialize_idf(self):
        self.idf = IDF(self.path_to_idd, self.path_to_initial_idf)
        return self.idf

    def add_zones(self, rooms: list[Room]):
        # TODO - check that idf exists! 
        self.zones, self.surfaces, self.room_map = create_zones(self.idf, rooms)
        # when do constructuins, these surfaces will be updated.. 


if __name__ == "__main__":
    pass
