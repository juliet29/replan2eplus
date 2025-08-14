from typing import NamedTuple, Literal
from dataclasses import dataclass
from utils4plans.sets import set_difference


class Node(NamedTuple):
    name: str # needs to be in zone_plan_dict.. => so either post init or validate later..
    type_: Literal["Zone", "Direction"]


class Edge(NamedTuple):
    u: Node
    v: Node


@dataclass
class Edges:
    edges: list[Edge]

    @property
    def zone_edges(self):
        return [i for i in self.edges if i.u.type_ == "Zone" and i.v.type_ == "Zone"]

    @property
    def zone_drn_edges(self):
        return set_difference(self.edges, self.zone_edges)
