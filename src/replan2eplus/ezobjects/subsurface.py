from replan2eplus.ezobjects.object2D import EZObject2D
from dataclasses import dataclass


@dataclass
class Subsurface(EZObject2D):
    # expected_key =
    @property
    def name(self):
        return self._epbunch.Name

    # TODO properties to add: surface, partner obj, connecting zones, "driving zones" (for the purpose of the AFN )
