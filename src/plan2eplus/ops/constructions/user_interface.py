from pathlib import Path
from typing import NamedTuple

from plan2eplus.eppaths.logic import EpPaths
from plan2eplus.ops.constructions.interfaces import (
    BaseConstructionSet,
    EPConstructionSet,
)


class ConstructionInput(NamedTuple):
    const_idf_paths: list[Path]
    mat_idf_paths: list[Path]
    construction_set: EPConstructionSet


# TODO: move all defaults right next to ezcase
default_construction_set = EPConstructionSet(
    # interior then exterior
    # TODO should be able to specify a tuple, and just one object if its the same.., trim white space
    wall=BaseConstructionSet("Medium Partitions", "Medium Exterior Wall"),
    floor=BaseConstructionSet("Medium Floor", "Medium Floor"),
    roof=BaseConstructionSet("Medium Roof/Ceiling", "Medium Roof/Ceiling"),
    window=BaseConstructionSet("Sgl Clr 6mm", "Sgl Clr 6mm"),
    door=BaseConstructionSet("Medium Furnishings", "Medium Furnishings"),
)  # TODO -> could one quicly change the names of these?


def default_construction_input(ep_paths: EpPaths):
    return ConstructionInput(
        ep_paths.construction_idfs,
        ep_paths.material_idfs,
        default_construction_set,
    )
