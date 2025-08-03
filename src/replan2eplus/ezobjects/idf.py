from dataclasses import dataclass
from eppy.bunch_subclass import EpBunch

from eppy.modeleditor import IDF


@dataclass
class EZIDF:
    idf: IDF

    # Eppy functions
    def print_idf(self):
        self.idf.printidf()

    # My functions : )
    def get_zones(self) -> list[EpBunch]:
        return [
            i for i in self.idf.idfobjects["ZONE"]
        ]  # TODO could put EzBunch on top here.. => maybe if things get out of hand..

    def get_surfaces(self) -> list[EpBunch]:
        return [i for i in self.idf.idfobjects["BUILDINGSURFACE:DETAILED"]]
