from dataclasses import dataclass
from pathlib import Path
from typing import Literal, NamedTuple

from utils4plans.io import write_json
from utils4plans.lists import chain_flatten
from utils4plans.sets import set_intersection

from plan2eplus.geometry.directions import WallNormalNamesList
from plan2eplus.ops.subsurfaces.interfaces import (
    Dimension,
    Edge,
    Location,
    SubsurfaceType,
    ZoneDirectionEdge,
    ZoneEdge,
)

EdgeGroupType = Literal["Zone_Direction", "Zone_Zone"]


class Detail(NamedTuple):
    dimension: Dimension
    location: Location
    type_: SubsurfaceType


@dataclass
class EdgeGroup:
    edges: list[Edge]
    detail: str | Detail
    type_: EdgeGroupType

    def __post_init__(self):
        self.edges_match_type_()

    @classmethod
    def from_tuple_edges(
        cls,
        edges_: list[tuple[str, str]],
        detail: str | Detail,
        type_: EdgeGroupType,
    ):
        edges = [Edge(*i) for i in edges_]
        return cls(edges, detail, type_)

    # these should all have the same type of edges => either zone_edge or zone_direction edges..
    def edges_match_type_(self):
        for edge in self.edges:
            if self.type_ == "Zone_Direction":
                assert (
                    len(set_intersection(edge.as_upper_tuple, WallNormalNamesList)) == 1
                ), f"Invalid `Zone_Direction` Edge: {edge}"
            else:
                assert (
                    len(set_intersection(edge.as_upper_tuple, WallNormalNamesList)) == 0
                ), f"Invalid `Zone_Zone` Edge: {edge}"

    def write(self, path: Path):
        assert isinstance(self.detail, str)
        edges = list(map(lambda x: x.as_tuple, self.edges))
        data = {"edges": edges, "detail": self.detail, "type_": self.type_}
        write_json(data, path)


@dataclass
class SubsurfaceInputs:
    edge_groups: list[EdgeGroup]
    details: dict[str, Detail] | None = None

    def get_detail(self, edge_group: EdgeGroup):
        if isinstance(edge_group.detail, Detail):
            return edge_group.detail
        else:
            assert self.details
            return self.details[edge_group.detail]

    @property
    def zone_pairs(self) -> list[tuple[ZoneEdge, Detail]]:
        return chain_flatten(
            [
                self.make_edge_group_edges(i)
                for i in self.edge_groups
                if i.type_ == "Zone_Zone"
            ]
        )  # type: ignore

    @property
    def zone_drn_pairs(self) -> list[tuple[ZoneDirectionEdge, Detail]]:
        return chain_flatten(
            [
                self.make_edge_group_edges(i)
                for i in self.edge_groups
                if i.type_ == "Zone_Direction"
            ]
        )  # type: ignore

    def make_edge_group_edges(self, edge_group: EdgeGroup):
        detail = self.get_detail(edge_group)
        if edge_group.type_ == "Zone_Direction":
            return [
                (
                    ZoneDirectionEdge(*i.sorted_directed_edge),
                    detail,
                )
                for i in edge_group.edges
            ]
        else:
            return [(ZoneEdge(*i), detail) for i in edge_group.edges]
