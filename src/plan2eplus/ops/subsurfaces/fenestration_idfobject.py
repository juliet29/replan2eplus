from dataclasses import dataclass

from typing import Literal

from geomeppyupdated.geom.polygons import Polygon3D
from geomeppyupdated.idf import IDF
from loguru import logger

from plan2eplus.ops.base import IDFObject


@dataclass
class IDFFenestrationObject(IDFObject):
    Name: str = ""
    Surface_Type: Literal[
        "Window", "Door", "GlassDoor", "TubularDaylightDome", "TubularDaylightDiffuser"
    ] = "Window"
    Construction_Name: str = ""
    Building_Surface_Name: str = ""
    Outside_Boundary_Condition_Object: str = ""
    View_Factor_to_Ground: str = "autocalculate"
    Frame_and_Divider_Name: str = ""
    Multiplier: float = 1.0
    Number_of_Vertices: str = "autocalculate"
    Vertex_1_X_coordinate: float = 0.0
    Vertex_1_Y_coordinate: float = 0.0
    Vertex_1_Z_coordinate: float = 0.0
    Vertex_2_X_coordinate: float = 0.0
    Vertex_2_Y_coordinate: float = 0.0
    Vertex_2_Z_coordinate: float = 0.0
    Vertex_3_X_coordinate: float = 0.0
    Vertex_3_Y_coordinate: float = 0.0
    Vertex_3_Z_coordinate: float = 0.0
    Vertex_4_X_coordinate: float = 0.0
    Vertex_4_Y_coordinate: float = 0.0
    Vertex_4_Z_coordinate: float = 0.0
    Polygon: Polygon3D | None = None

    @property
    def key(self):
        return "FENESTRATIONSURFACE:DETAILED"

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
    def write(self, idf: IDF):
        vals = {k: v for k, v in self.values.items() if v}
        logger.debug(vals)
        polygon = vals.pop("Polygon")
        logger.debug(polygon)
        # remove vertex values -> have these be set as coords..
        vertex_keys = [i for i in vals.keys() if "Vertex" in i]
        for k in vertex_keys:
            vals.pop(k)
        logger.debug(vals)
        # raise Exception("bye")

        obj = idf.newidfobject(self.key, **vals)

        # ggr = GlobalGeometryRules().get_idf_objects(idf)
        obj.setcoords(polygon, ggr=None)

        # TODO: add get a polygon and set the values..
        return idf
