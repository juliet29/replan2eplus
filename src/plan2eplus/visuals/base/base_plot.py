from dataclasses import dataclass
from typing import Sequence

from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from plan2eplus.ops.afn.ezobject import AirflowNetwork
from plan2eplus.ops.airboundary.ezobject import Airboundary
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.surfaces.ezobject import Surface
from plan2eplus.ops.zones.ezobject import Zone
from plan2eplus.geometry.domain import Domain
from plan2eplus.visuals.domains import (
    compute_multidomain,
)
from plan2eplus.geometry.contact_points import calculate_cardinal_points
from plan2eplus.visuals.axes import (
    AnnotationPair,
    LineStyles,
    add_annotations,
    add_connection_lines,
    add_polygons,
    add_surface_lines,
)
from plan2eplus.visuals.domains import expand_domain
from plan2eplus.visuals.organize import (
    organize_connections,
    organize_subsurfaces_and_surfaces,
    get_domains,
    get_edges,
)
from plan2eplus.visuals.styles.artists import (
    AnnotationStyles,
    ConnectionStyles,
    PolygonStyles,
    SurfaceStyles,
)
from plan2eplus.visuals.transforms import (
    EXPANSION_FACTOR,
)  # TODO move this to a config!


@dataclass
class BasePlot:
    zones: list[Zone]
    cardinal_expansion_factor: float = EXPANSION_FACTOR
    extents_expansion_factor: float = EXPANSION_FACTOR

    def __post_init__(self):
        self.fig, self.axes = plt.subplots(figsize=(12, 8))
        self.total_domain = compute_multidomain([i.domain for i in self.zones])

        self.cardinal_domain = expand_domain(
            self.total_domain, self.cardinal_expansion_factor
        )
        self.extents = expand_domain(
            self.cardinal_domain, self.extents_expansion_factor
        )

    def plot_zones(self, style=PolygonStyles()):
        add_polygons(
            [i.domain for i in self.zones], [style], self.axes
        )  # TODO if pass a list of styles, then apply each differently -> when are doing values .. or just have different function for if have values..
        return self

    def plot_zone_names(self, style=AnnotationStyles()):
        add_annotations(
            [AnnotationPair(i.domain.centroid, i.room_name) for i in self.zones],
            style,
            self.axes,
        )
        return self

    def plot_cardinal_names(self, style=AnnotationStyles()):
        cardinal_points = calculate_cardinal_points(self.cardinal_domain)
        add_annotations(
            [
                AnnotationPair(value, key)
                for key, value in cardinal_points.dict_.items()
            ],
            style,
            self.axes,
        )
        return self

    # NOTE: ASSUMING THAT ALL SUBSURFACES / SURFACES ARE WALLS. then will not have an ortho domain. When incorporate multilievels, will need to plot differently

    def plot_subsurfaces_and_surfaces(
        self,
        afn: AirflowNetwork,
        airboundaries: list[Airboundary],
        subsurfaces: list[Subsurface],
        style=SurfaceStyles(),
    ):
        surface_org = organize_subsurfaces_and_surfaces(afn, airboundaries, subsurfaces)

        def add(items: Sequence[Airboundary | Subsurface | Surface], style: LineStyles):
            add_surface_lines(get_domains(items), style, self.axes)

        add(
            surface_org.non_afn_surfaces,
            style.non_afn_surfaces,
        )
        add(
            surface_org.windows,
            style.windows,
        )
        add(
            surface_org.doors,
            style.doors,
        )

        add(
            surface_org.airboundaries,
            style.airboundaries,
        )
        return self

    def plot_connections(
        self,
        afn: AirflowNetwork,
        airboundaries: list[Airboundary],
        subsurfaces: list[Subsurface],
        style=ConnectionStyles(),
    ):
        def add(items: Sequence[Airboundary | Subsurface], style: LineStyles):
            add_connection_lines(
                get_domains(items),
                get_edges(items),
                self.zones,
                cardinal_points,
                [style],
                self.axes,
            )

        connections_org = organize_connections(afn, airboundaries, subsurfaces)

        cardinal_points = calculate_cardinal_points(self.cardinal_domain)

        add(connections_org.baseline, style.baseline)
        add(connections_org.baseline, style.afn)

        return self

    def finalize(self):
        self.axes.set_xlim(self.extents.horz_range.as_tuple)
        self.axes.set_ylim(self.extents.vert_range.as_tuple)
        self.axes.legend()
        return self

    def show(self):
        self.finalize()
        plt.show()
