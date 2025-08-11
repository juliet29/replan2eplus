import replan2eplus.epnames.keys as epkeys
from replan2eplus.errors import InvalidEpBunchException
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from replan2eplus.ezobjects.object2D import EZObject2D
from replan2eplus.epnames.keys import SURFACE
from dataclasses import dataclass


from eppy.bunch_subclass import EpBunch
from rich import print as rprint





# TODO intermediate class shared w subsurface? 
@dataclass
class Surface(EZObject2D): 
    @property
    def name(self):
        return self.epbunch.Name
    
    

