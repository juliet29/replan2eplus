from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass
from replan2eplus.ezobjects.base import EZObject

import replan2eplus.epnames.keys as epkeys


@dataclass
class Zone(EZObject):
    epbunch: EpBunch
    expected_key: str = epkeys.ZONE

    @property
    def room_name(self):
        return self.dname.plan_name
    
    @property
    def zone_name(self):
        return self.dname.zone_name



# TODO create a parent class, but figure out visuals first..
