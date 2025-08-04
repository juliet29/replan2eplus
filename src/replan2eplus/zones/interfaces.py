from dataclasses import dataclass

from replan2eplus.geometry.domain import Domain
from replan2eplus.ezobjects.idf import EppyBlock
from typing import NamedTuple


@dataclass
class Room:
    name: str
    domain: Domain
    height: float  # TODO add default # notify that height is in meters! 

    @property
    def coords(self):
        return self.domain.create_bounds().as_pairs

    def create_geomeppy_block(self):
        return EppyBlock(
            {
                "name": self.name,
                "coordinates": self.coords,
                "height": self.height,
            }
        )
    

class RoomZonePair(NamedTuple): #TODO may already have a different implementation.. 
    room_name: str
    zone_name: str 
