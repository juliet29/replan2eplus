from dataclasses import dataclass

from geomeppyupdated.idf import IDF

from plan2eplus.ops.base import IDFObject
from plan2eplus.ops.surfaces.ezobject import Surface
from plan2eplus.ops.zones.ezobject import Zone
from utils4plans.lists import chain_flatten


@dataclass
class IDFZone(IDFObject):
    Name: str = ""
    Direction_of_Relative_North: int = 0
    X_Origin: float = 0
    Y_Origin: float = 0
    Z_Origin: float = 0
    Type: int = 1
    Multiplier: int = 1
    Ceiling_Height: int | str = "autocalculate"
    Volume: int | str = "autocalculate"
    Floor_Area: int | str = "autocalculate"
    Zone_Inside_Convection_Algorithm: str = ""
    Zone_Outside_Convection_Algorithm: str = ""
    Part_of_Total_Floor_Area: str = "Yes"

    @property
    def key(self):
        return "ZONE"

    def create_ezobject(self, surfaces: list[Surface]):
        return Zone(self.Name, surfaces)

    @classmethod
    def get_zone_surfaces(cls, idf, name):
        obj = cls().get_one_idf_object(idf, name)
        return obj.zonesurfaces  # [i.Name for i in obj.zonesurfaces]

    @classmethod
    def get_zone_subsurfaces(cls, idf, name):
        zone_surfaces = cls.get_zone_surfaces(idf, name)
        subsurfaces = [
            i.subsurfaces for i in zone_surfaces
        ]  # pyright: ignore[reportAttributeAccessIssue]
        return chain_flatten(subsurfaces)

    @classmethod
    def get_zone_surface_names(cls, idf, name) -> list[str]:
        return [
            i.Name for i in cls.get_zone_surfaces(idf, name)
        ]  # pyright: ignore[reportAttributeAccessIssue]

    @classmethod
    def get_zone_subsurface_names(cls, idf, name) -> list[str]:
        return [i.Name for i in cls.get_zone_subsurfaces(idf, name)]


@dataclass
class GeomeppyBlock(IDFObject):
    name: str
    coordinates: list[tuple[float, float]]
    height: float

    def write(self, idf: IDF):
        idf.add_block(**self.values)
        return idf
