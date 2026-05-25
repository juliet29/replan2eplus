from dataclasses import dataclass

from expression.collections import Seq
from geomeppyupdated.idf import IDF
from geomeppyupdated.geom.polygons import Polygon3D
from loguru import logger
from utils4plans.lists import chain_flatten, get_unique_one

from plan2eplus.errors import InvalidObjectError, NonExistentEpBunchTypeError
from plan2eplus.ops.base import IDFObject
from plan2eplus.ops.init.idfobject import GlobalGeometryRules
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.subsurfaces.interfaces import SubsurfaceType
from plan2eplus.ops.surfaces.ezobject import Surface


@dataclass
class IDFSubsurfaceBase(IDFObject):
    Name: str = ""
    Building_Surface_Name: str = ""
    Construction_Name: str = ""
    Starting_X_Coordinate: float = 0
    Starting_Z_Coordinate: float = 0
    Length: float = 0
    Height: float = 0
    Polygon: Polygon3D | None = None

    @property
    def type_(self) -> SubsurfaceType: ...

    def get_surface(self, surfaces: list[Surface]):
        try:
            return get_unique_one(
                surfaces, lambda x: x.surface_name == self.Building_Surface_Name
            )
        except AssertionError:
            raise Exception(
                f"Error when trying to get matching surface for {self.Building_Surface_Name}. Input surfaces are: {surfaces}  "
            )

    @property
    def empty_boundary_condition_object(self):
        return ""

    def create_ezobject(self, surfaces: list[Surface]) -> Subsurface:
        return Subsurface(
            self.Name,
            self.Construction_Name,
            self.Starting_X_Coordinate,
            self.Starting_Z_Coordinate,
            self.Length,
            self.Height,
            self.empty_boundary_condition_object,
            self.type_,  # this will map to the key
            self.get_surface(surfaces),
        )

    def write_subsurface(self, idf: IDF):
        vals = {k: v for k, v in self.values.items() if v}
        logger.debug(vals)
        polygon = vals.pop("Polygon")
        logger.debug(polygon)
        logger.debug(vals)
        # raise Exception("bye")

        obj = idf.newidfobject(self.key, **vals)

        ggr = GlobalGeometryRules().get_idf_objects(idf)
        obj.setcoords(polygon, ggr=None)

        # TODO: add get a polygon and set the values..
        return idf


@dataclass
class IDFWindow(IDFSubsurfaceBase):
    Frame_and_Divider_Name: str = ""
    Multiplier: float = 1

    @property
    def key(self):
        return "WINDOW"

    @property
    def type_(self) -> SubsurfaceType:
        return "Window"


@dataclass
class IDFDoor(IDFSubsurfaceBase):
    Multiplier: float = 1

    @property
    def key(self):
        return "DOOR"

    @property
    def type_(self) -> SubsurfaceType:
        return "Door"


@dataclass
class IDFDoorInterzone(IDFSubsurfaceBase):
    Outside_Boundary_Condition_Object: str = ""
    Multiplier: float = 1

    @property
    def key(self):
        return "DOOR:INTERZONE"

    @property
    def type_(self) -> SubsurfaceType:
        return "Door"

    def create_ezobject(self, surfaces: list[Surface]) -> Subsurface:
        return Subsurface(
            self.Name,
            self.Construction_Name,
            self.Starting_X_Coordinate,
            self.Starting_Z_Coordinate,
            self.Length,
            self.Height,
            self.Outside_Boundary_Condition_Object,
            self.type_,  # this will map to the key
            self.get_surface(surfaces),
        )


subsurface_objects: list[type[IDFSubsurfaceBase]] = [
    IDFWindow,
    IDFDoor,
    IDFDoorInterzone,
]


def read_subsurfaces(idf: IDF, names: list[str] = []):
    k = Seq(subsurface_objects).map(lambda x: x.read(idf, names)).pipe(chain_flatten)
    return k


def update_subsurface(idf: IDF, name: str, param: str, new_value: str):
    for obj in subsurface_objects:
        try:
            # NOTE: this assumes that object names are NOT shared across different types of subsurface objects
            # TODO check this when reading in ..
            obj().update(idf, name, param, new_value)
            return
        except (InvalidObjectError, NonExistentEpBunchTypeError):
            pass
    # if we get here then not objects matched.
    raise Exception(
        f"Unable to update subsurface: no matching subsurface for subsurface named : {name}"
    )
