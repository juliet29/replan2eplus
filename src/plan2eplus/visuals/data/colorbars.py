from typing import Callable, Literal

import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar
from matplotlib.colors import Colormap, Normalize, TwoSlopeNorm

PotentialColorMaps = Literal["YlOrRd_r", "RdYlBu", "RdYlBu_r", "managua"]

ColorBarFx = Callable[
    [list[float] | np.ndarray, Axes],
    tuple[tuple[Colorbar], Colormap, Normalize | TwoSlopeNorm],
]


def is_greater_than_zero(num: float):
    return True if num > 0 else False


def pressure_colorbar(
    data: list[float] | np.ndarray,
    ax: Axes,
    single_colormap: PotentialColorMaps = "YlOrRd_r",
    diverging_colormap: PotentialColorMaps = "RdYlBu_r",
    min_: float | None = None,
    max_: float | None = None,
    show_bar=True,
):
    expansion = 1.3
    if len(data) == 1:
        res = data[0]
        norm = Normalize(vmin=res - expansion, vmax=res + expansion)
        cmap = mpl.colormaps[single_colormap]

    else:
        if not (min_ and max_):
            min_, max_ = (
                min(data),  # * expansion,
                max(data),  # * expansion,
            )  # TODO come up with a better way of doing this expansion thing / figuring out the limits of data to show..
            # TODO reverse colors for pressure!
            # sign_min = math.copysign(1, min_)
            # sign_max = math.copysign(1, max_)

        same_sign = is_greater_than_zero(min_) and is_greater_than_zero(max_)

        if max_ <= 0:
            norm = Normalize(vmin=min_, vmax=max_)
            cmap = mpl.colormaps[single_colormap]
        elif same_sign:
            norm = Normalize(vmin=min_, vmax=max_)
            cmap = mpl.colormaps[single_colormap]
        else:
            center = 0

            norm = TwoSlopeNorm(vmin=min_, vcenter=center, vmax=max_)

            cmap = mpl.colormaps[diverging_colormap]

    if not show_bar:
        return "", cmap, norm

    bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation="vertical",
            label="Total Pressure [Pa]",
            ax=ax,
            # shrink=0.5
            # TODO pass in the label
        ),
    )
    return bar, cmap, norm


def temperature_colorbar(data: list[float] | np.ndarray, ax: Axes):
    cmap = mpl.colormaps["YlOrRd"]
    min_, max_ = min(data), max(data)
    norm = Normalize(vmin=min_, vmax=max_)
    bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation="vertical",
            label="Temperature [ºC]",
            ax=ax,
        ),
    )
    return bar, cmap, norm


def flow_colorbar(data: list[float] | np.ndarray, ax: Axes):
    cmap = mpl.colormaps["PuBu"]
    min_, max_ = min(data), max(data)
    norm = Normalize(vmin=min_, vmax=max_)
    bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation="vertical",
            label="Volume Flow Rate [m3/s]",
            ax=ax,
        ),
    )
    return bar, cmap, norm


def data_norm(data: list[float] | np.ndarray):
    cmap = mpl.colormaps["PuBu"]
    min_, max_ = min(data), max(data)
    norm = Normalize(vmin=min_, vmax=max_)
    return cmap, norm


def assemble_components():
    pass
