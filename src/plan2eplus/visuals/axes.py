from typing import NamedTuple

from matplotlib.axes import Axes

from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.zones.ezobject import Zone
from plan2eplus.geometry.contact_points import CardinalPoints
from plan2eplus.geometry.coords import Coord
from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.ortho_domain import OrthoDomain
from plan2eplus.visuals.transforms import (
    domain_to_line,
    domain_to_mpl_polygon,
    subsurface_to_mpl_connection_line,
)
from plan2eplus.visuals.styles.artists import (
    LineStyles,
    PolygonStyles,
    AnnotationStyles,
)


def add_polygons(
    domains: list[Domain | OrthoDomain], styles: list[PolygonStyles], axes: Axes
):
    def update(domain, style):
        polygon = domain_to_mpl_polygon(domain)
        polygon.set(**style.values)
        axes.add_artist(polygon)

    if len(styles) == 1:
        style = styles[0]
        for domain in domains:
            update(domain, style)
    elif len(styles) > 1:
        assert len(styles) == len(domains)
        for domain, style in zip(domains, styles):
            update(domain, style)
    else:
        raise Exception(
            f"Invalid length of styles! Expected 1 or {len(domains)} to match the number of domains. Instead got {len(styles)}"
        )

    return axes


def add_surface_lines(domains: list[Domain], style: LineStyles, axes: Axes):
    for ix, domain in enumerate(domains):
        if ix != 0:
            style.label = ""
        line = domain_to_line(domain).to_line2D
        line.set(**style.values)
        axes.add_artist(line)
    return axes


def add_connection_lines(
    domains: list[Domain],
    edges: list[Edge],
    zones: list[Zone],
    cardinal_coords: CardinalPoints,
    styles: list[LineStyles],
    axes: Axes,
):
    def update(domain, edge, style):
        line = subsurface_to_mpl_connection_line(domain, edge, zones, cardinal_coords)
        line.set(**style.values)
        axes.add_artist(line)
        return line

    lines = []
    if len(styles) == 1:
        style = styles[0]
        for domain, edge in zip(domains, edges):
            line = update(domain, edge, style)
            lines.append(line)
    elif len(styles) > 1:
        assert len(styles) == len(domains)
        for (
            domain,
            edge,
            style,
        ) in zip(
            domains,
            edges,
            styles,
        ):
            line = update(domain, edge, style)
            lines.append(line)
    else:
        raise Exception(
            f"Invalid length of styles! Expected 1 or {len(domains)} to match the number of domains. Instead got {len(styles)}"
        )

    return axes, lines


class AnnotationPair(NamedTuple):
    coord: Coord
    name: str


def add_annotations(
    annotation_pairs: list[AnnotationPair],
    styles: AnnotationStyles | list[AnnotationStyles],
    axes: Axes,
):
    if not isinstance(styles, list):
        for coord, name in annotation_pairs:
            axes.text(*coord.as_tuple, s=name, **styles.values)
        return axes
    else:
        assert len(styles) == len(annotation_pairs)
        for pair, style in zip(annotation_pairs, styles):
            coord, name = pair
            axes.text(*coord.as_tuple, s=name, **style.values)
        return axes
