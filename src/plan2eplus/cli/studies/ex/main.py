from plan2eplus.cli.studies.ex.materials import ConstructionExamples, MaterialExamples
from plan2eplus.cli.studies.ex.rooms import Rooms
from plan2eplus.cli.studies.ex.subsurfaces import SubsurfaceInputExamples

from plan2eplus.eppaths.logic import EpPaths
from plan2eplus.ezcase.ez import EZ


# hellpp//
class Interfaces:
    rooms = Rooms()
    subsurfaces = SubsurfaceInputExamples()
    materials = MaterialExamples()
    constructions = ConstructionExamples()


# TODO -> move to their own places.., also link to eplus data set is a bit fragile for testing => have local copies in case things change..  /static folder that is a part of the source
class EpAFNCase:
    # NOTE: draw back of this case is that it uses ONLY fenestration subsurfaces -> not ideal since this code avoids this.. reasonable enough for enough for materials though
    name = "AirflowNetwork3zVent.idf"
    ep_paths = EpPaths()
    path = ep_paths.example_files / name
    # case = EZ(path)
    basic_material_names = [
        "A1 - 1 IN STUCCO",
        "C4 - 4 IN COMMON BRICK",
        "E1 - 3 / 4 IN PLASTER OR GYP BOARD",
        "C6 - 8 IN CLAY TILE",
        "C10 - 8 IN HW CONCRETE",
        "E2 - 1 / 2 IN SLAG OR STONE",
        "E3 - 3 / 8 IN FELT AND MEMBRANE",
        "B5 - 1 IN DENSE INSULATION",
        "C12 - 2 IN HW CONCRETE",
        "1.375in-Solid-Core",
    ]
    window_glazing_material_names = ["WIN-LAY-GLASS-LIGHT"]
    mixed_subset_materials = basic_material_names[0:4] + window_glazing_material_names
    constructions = [
        "DOOR-CON",
        "EXTWALL80",
        "PARTITION06",
        "FLOOR SLAB 8 IN",
        "ROOF34",
        "WIN-CON-LIGHT",
    ]


class EpFourZoneCase:
    name = "4ZoneWithShading_Simple_2.idf"
    ep_paths = EpPaths()
    path = ep_paths.example_files / name
    # case = EZ(path)

    subsurface_names = [
        "Zn001:Wall001:Win001",
        "Zn002:Wall001:Win001",
        "Zn002:Wall001:Win002",
        "Zn003:Wall001:Win001",
        "Zn004:Wall001:Win001",
        "Zn001:Wall001:Door002",
        "Zn003:Wall004:Door001",
    ]


class Cases:
    ui = Interfaces()

    @property
    def base(self):
        return EZ()

    @property
    def ep_afn(self):
        return EpAFNCase

    @property
    def ep_four_zone(self):
        return EpFourZoneCase

    @property
    def two_room(self):
        case = self.base
        case.add_zones(self.ui.rooms.two_room_list)
        return case

    @property
    def subsurfaces_simple(self):
        case = self.two_room
        case.add_subsurfaces(Interfaces.subsurfaces.simple)
        return case

    @property
    def sample(self):
        pass
