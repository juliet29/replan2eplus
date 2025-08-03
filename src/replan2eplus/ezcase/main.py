from dataclasses import dataclass
from eppy.modeleditor import IDF, IDDAlreadySetError
from ladybug.analysisperiod import AnalysisPeriod
from pathlib import Path
from replan2eplus.ezcase.defaults import PATH_TO_IDF, PATH_TO_IDD
from rich import print as rprint
from replan2eplus.ezobjects.idf import EZIDF


@dataclass  # TODO: is this really a dataclass? -> need to do some initialization logic, and keep track of state variables, so probably not, in the long term..
class EZCase:
    path_to_idd: Path
    path_to_initial_idf: Path

    # TODO: do these need to be initialized here?
    # path_to_weather: Path
    # path_to_analysis_period: AnalysisPeriod

    def initialize_idf(self):
        try:
            IDF.setiddname(self.path_to_idd)
        except IDDAlreadySetError:
            pass  # TODO log IDD already set, especially if the one they try to set is different..

        idf =  IDF(idfname=self.path_to_initial_idf)
        return EZIDF(idf)
    


def get_test_idf():
    case = EZCase(PATH_TO_IDD, PATH_TO_IDF)
    return case.initialize_idf()



if __name__ == "__main__":
    case = EZCase(PATH_TO_IDD, PATH_TO_IDF)
    idf = case.initialize_idf()
    rprint(idf.print_idf())
