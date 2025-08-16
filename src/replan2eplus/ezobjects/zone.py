from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass, field
from replan2eplus.ezobjects.base import EZObject

import replan2eplus.epnames.keys as epkeys
from replan2eplus.ezobjects.surface import Surface


@dataclass
class Zone(EZObject):
    epbunch: EpBunch
    expected_key: str = epkeys.ZONE
    surfaces: list[Surface] = field(default_factory=list)


    @property
    def room_name(self):
        return self.dname.plan_name
    
    @property
    def zone_name(self): # idf name?
        return self.idf_name



# TODO create a parent class, but figure out visuals first..
