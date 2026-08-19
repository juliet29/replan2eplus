from plan2eplus.campaigns.decorator2 import DataDict
from plan2eplus.examples.cases.minimal import test_rooms
from plan2eplus.cli.studies.ex.subsurfaces import edge_groups

from plan2eplus.ops.subsurfaces.interfaces import Dimension

case = {
    "rooms": {
        "A": test_rooms,
        "B": test_rooms,
    },
    "connections": {
        "A": edge_groups["ns_windows"] + edge_groups["door"],
        "B": edge_groups["windows"] + edge_groups["door"],
    },
}


# TODO: probably going to be strings. especially if using a config file..
mods = {
    "window_dimension": {
        "-50%": Dimension(0.5, 2),
        "standard": Dimension(1, 2),
        "+50%": Dimension(1.5, 2),
    },
    # "door": {
    #     "-50%": Dimension(0.5, 2),
    #     "standard": Dimension(1, 2),
    #     "+50%": Dimension(1.5, 2),
    # },
}


def make_data_dict():
    return DataDict(case, mods)
