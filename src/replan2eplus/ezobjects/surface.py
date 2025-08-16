from replan2eplus.ezobjects.object2D import EZObject2D
from dataclasses import dataclass
import replan2eplus.epnames.keys as keys
from enum import StrEnum, Enum
from typing import Literal
from replan2eplus.errors import IDFMisunderstandingError, BadlyFormatedIDFError

from replan2eplus.geometry.directions import WallNormal


# NOTE: this code showcases what could be a recurring pattern for wrapping geomeppy/eppy outputs -> has to be returned in an enum, but then can access using string literals and get hints
# This is safe if a type checker is being used and makes coding easier, but then literals are floating everywhere, pros + cons..


SurfaceBoundaryCondition = StrEnum(
    "SurfaceBoundaryCondition", "surface ground outdoors"
)
SurfaceBoundaryConditionNames = Literal["surface", "ground", "outdoors"]

# StrEnum()

SurfaceType = StrEnum("SurfaceType", "floor roof wall")
SurfaceTypeNames = Literal["floor", "roof", "wall"]


@dataclass
class Surface(EZObject2D):
    # TODO turn to class (instead of) if have to init later..?  / read python docs..
    def __post_init__(self):
        assert self.expected_key == keys.SURFACE

    @property
    def surface_name(self):
        return self.idf_name

    @property
    def zone_name(self):
        return self.epbunch.Zone_Name

    @property
    def type_(self) -> SurfaceTypeNames:
        return SurfaceType(self.epbunch.Surface_Type).name

    @property
    def azimuth(self):
        return round(float(self.epbunch.azimuth))

    @property
    def direction(self):
        match self.type_:
            case "floor":
                return WallNormal.DOWN
            case "roof":
                return WallNormal.UP
            case "wall":
                return WallNormal(self.azimuth)
            case _:
                raise BadlyFormatedIDFError("Invalid surface type!")

    @property
    def boundary_condition(self) -> SurfaceBoundaryConditionNames:
        return SurfaceBoundaryCondition(self.epbunch.Outside_Boundary_Condition).name

    @property
    def neighbor(self):
        if self.boundary_condition == "surface":
            return str(self.epbunch.Outside_Boundary_Condition_Object)  #
        else:
            return None
            # raise IDFMisunderstandingError(
            #     "This surface has no neighbor!"
            # )  # maybe better to return the direction? ->
            # # TODO could have a neighbor in a multistory situation though..
