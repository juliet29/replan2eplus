from dataclasses import dataclass
from eppy.bunch_subclass import EpBunch
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from replan2eplus.errors import InvalidEpBunchException
from replan2eplus.ezobjects.name import decompose_idf_name

@dataclass
class EZObject:
    epbunch: EpBunch
    expected_key: str 
    # TODO idf name stuff

    def __post_init__(self):
        actual_key = get_epbunch_key(self.epbunch)
        try:
            assert actual_key == self.expected_key
        except AssertionError:
            raise InvalidEpBunchException(self.expected_key, actual_key)
        

    @property
    def idf_name(self):
        return str(self.epbunch.Name)
    
    @property
    def dname(self):
        return decompose_idf_name(self.idf_name)







