from dataclasses import dataclass

from geomeppyupdated.idf import IDF
from loguru import logger

from plan2eplus.ops.base import IDFObject
from plan2eplus.ops.init.idfobject import GlobalGeometryRules


@dataclass
class IDFFenestrationObject(IDFObject):
    Name: str = ""
    Building_Surface_Name: str = ""
    Construction_Name: str = ""

    # Starting_X_Coordinate: float = 0
    # Starting_Z_Coordinate: float = 0
    # Length: float = 0
    # Height: float = 0
    # Polygon: Polygon3D | None = None
    #
    # @property
    # def type_(self) -> SubsurfaceType: ...
    #
    # def get_surface(self, surfaces: list[Surface]):
    #     try:
    #         return get_unique_one(
    #             surfaces, lambda x: x.surface_name == self.Building_Surface_Name
    #         )
    #     except AssertionError:
    #         raise Exception(
    #             f"Error when trying to get matching surface for {self.Building_Surface_Name}. Input surfaces are: {surfaces}  "
    #         )
    #
    # @property
    # def empty_boundary_condition_object(self):
    #     return ""
    #
    # def create_ezobject(self, surfaces: list[Surface]) -> Subsurface:
    #     return Subsurface(
    #         self.Name,
    #         self.Construction_Name,
    #         self.Starting_X_Coordinate,
    #         self.Starting_Z_Coordinate,
    #         self.Length,
    #         self.Height,
    #         self.empty_boundary_condition_object,
    #         self.type_,  # this will map to the key
    #         self.get_surface(surfaces),
    #     )
    #
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
