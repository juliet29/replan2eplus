from dataclasses import dataclass

from plan2eplus.ops.base import IDFObject


@dataclass
class Version(IDFObject):
    Version_Identifier: float = 22.2  # TODO get from config

    @property
    def key(self):
        return "VERSION"


@dataclass
class Timestep(IDFObject):
    Number_of_Timesteps_per_Hour: int = 4

    @property
    def key(self):
        return "TIMESTEP"


@dataclass
class Building(IDFObject):
    Name: str = ""
    North_Axis: int = 0
    Terrain: str = "Suburbs"  # TODO enum
    Loads_Convergence_Tolerance_Value: float = 0.04
    Temperature_Convergence_Tolerance_Value: float = 0.40
    Solar_Distribution: str = "FullInteriorAndExterior"
    Maximum_Number_of_Warmup_Days: int = 25
    Minimum_Number_of_Warmup_Days: int = 6

    @property
    def key(self):
        return "BUILDING"


@dataclass
class GlobalGeometryRules(IDFObject):
    Starting_Vertex_Position: str = "UpperLeftCorner"
    Vertex_Entry_Direction: str = "CounterClockwise"
    Coordinate_System: str = "World"
    Daylighting_Reference_Point_Coordinate_System: str = ""
    Rectangular_Surface_Coordinate_System: str = ""

    @property
    def key(self):
        return "GLOBALGEOMETRYRULES"


@dataclass
class SimulationControl(IDFObject):
    Do_Zone_Sizing_Calculation: str = "No"
    Do_System_Sizing_Calculation: str = "No"
    Do_Plant_Sizing_Calculation: str = "No"
    Run_Simulation_for_Sizing_Periods: str = "No"
    Run_Simulation_for_Weather_File_Run_Periods: str = "Yes"
    Do_HVAC_Sizing_Simulation_for_Sizing_Periods: str = "No"
    Maximum_Number_of_HVAC_Sizing_Simulation_Passes: int = 1

    @property
    def key(self):
        return "SIMULATIONCONTROL"
