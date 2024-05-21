"""
This module provides access to the various plotting-related functions.
"""
from typing import overload, Union, Mapping, Iterable, Optional
from ctypes import c_int, c_char_p, c_void_p, c_uint
from gr import _require_runtime_version, _RUNTIME_VERSION

from . import _grm, _encode_str_to_char_p, args


@overload
def plot(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]]
) -> bool:
    ...


@overload
def plot(
        args_container: None = None,
        *,
        append_plots: args._ElemType = ...,
        hold_plots: args._ElemType = ...,
        plots: args._ElemType = ...,
        clear: args._ElemType = ...,
        figsize: args._ElemType = ...,
        raw: args._ElemType = ...,
        size: args._ElemType = ...,
        subplots: args._ElemType = ...,
        update: args._ElemType = ...,
        accelerate: args._ElemType = ...,
        adjust_xlim: args._ElemType = ...,
        adjust_ylim: args._ElemType = ...,
        adjust_zlim: args._ElemType = ...,
        alpha: args._ElemType = ...,
        angle_ticks: args._ElemType = ...,
        backgroundcolor: args._ElemType = ...,
        bar_color: args._ElemType = ...,
        bar_width: args._ElemType = ...,
        colormap: args._ElemType = ...,
        font_precision: args._ElemType = ...,
        font: args._ElemType = ...,
        grplot: args._ElemType = ...,
        ind_bar_color: args._ElemType = ...,
        ind_edge_color: args._ElemType = ...,
        ind_edge_width: args._ElemType = ...,
        keep_aspect_ratio: args._ElemType = ...,
        kind: args._ElemType = ...,
        labels: args._ElemType = ...,
        levels: args._ElemType = ...,
        location: args._ElemType = ...,
        marginal_heatmap_kind: args._ElemType = ...,
        normalization: args._ElemType = ...,
        orientation: args._ElemType = ...,
        panzoom: args._ElemType = ...,
        phiflip: args._ElemType = ...,
        resample_method: args._ElemType = ...,
        reset_ranges: args._ElemType = ...,
        rings: args._ElemType = ...,
        rotation: args._ElemType = ...,
        series: args._ElemType = ...,
        style: args._ElemType = ...,
        subplot: args._ElemType = ...,
        tilt: args._ElemType = ...,
        title: args._ElemType = ...,
        xbins: args._ElemType = ...,
        xflip: args._ElemType = ...,
        xform: args._ElemType = ...,
        xgrid: args._ElemType = ...,
        xind: args._ElemType = ...,
        xlabel: args._ElemType = ...,
        xlim: args._ElemType = ...,
        xlog: args._ElemType = ...,
        xticklabels: args._ElemType = ...,
        ybins: args._ElemType = ...,
        yflip: args._ElemType = ...,
        ygrid: args._ElemType = ...,
        yind: args._ElemType = ...,
        ylabel: args._ElemType = ...,
        ylim: args._ElemType = ...,
        ylog: args._ElemType = ...,
        zflip: args._ElemType = ...,
        zgrid: args._ElemType = ...,
        zlabel: args._ElemType = ...,
        zlim: args._ElemType = ...,
        zlog: args._ElemType = ...,
        a: args._ElemType = ...,
        algorithm: args._ElemType = ...,
        bin_counts: args._ElemType = ...,
        bin_edges: args._ElemType = ...,
        bin_width: args._ElemType = ...,
        c_dims: args._ElemType = ...,
        c: args._ElemType = ...,
        crange: args._ElemType = ...,
        dmax: args._ElemType = ...,
        dmin: args._ElemType = ...,
        draw_edges: args._ElemType = ...,  # bool?
        edge_color: args._ElemType = ...,
        edge_width: args._ElemType = ...,
        error: args._ElemType = ...,
        face_color: args._ElemType = ...,
        foreground_color: args._ElemType = ...,
        indices: args._ElemType = ...,
        inner_series: args._ElemType = ...,
        isovalue: args._ElemType = ...,
        markertype: args._ElemType = ...,
        nbins: args._ElemType = ...,
        philim: args._ElemType = ...,
        rgb: args._ElemType = ...,
        rlim: args._ElemType = ...,
        spec: args._ElemType = ...,
        stairs: args._ElemType = ...,
        step_where: args._ElemType = ...,
        u: args._ElemType = ...,
        v: args._ElemType = ...,
        weights: args._ElemType = ...,
        x: args._ElemType = ...,
        xcolormap: args._ElemType = ...,
        xrange: args._ElemType = ...,
        y: args._ElemType = ...,
        ycolormap: args._ElemType = ...,
        ylabels: args._ElemType = ...,
        yrange: args._ElemType = ...,
        z_dims: args._ElemType = ...,
        z: args._ElemType = ...,
        zrange: args._ElemType = ...,
        **kwargs: args._ElemType
) -> bool:
    ...


@overload
def plot(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        *,
        append_plots: args._ElemType = ...,
        hold_plots: args._ElemType = ...,
        plots: args._ElemType = ...,
        clear: args._ElemType = ...,
        figsize: args._ElemType = ...,
        raw: args._ElemType = ...,
        size: args._ElemType = ...,
        subplots: args._ElemType = ...,
        update: args._ElemType = ...,
        accelerate: args._ElemType = ...,
        adjust_xlim: args._ElemType = ...,
        adjust_ylim: args._ElemType = ...,
        adjust_zlim: args._ElemType = ...,
        alpha: args._ElemType = ...,
        angle_ticks: args._ElemType = ...,
        backgroundcolor: args._ElemType = ...,
        bar_color: args._ElemType = ...,
        bar_width: args._ElemType = ...,
        colormap: args._ElemType = ...,
        font_precision: args._ElemType = ...,
        font: args._ElemType = ...,
        grplot: args._ElemType = ...,
        ind_bar_color: args._ElemType = ...,
        ind_edge_color: args._ElemType = ...,
        ind_edge_width: args._ElemType = ...,
        keep_aspect_ratio: args._ElemType = ...,
        kind: args._ElemType = ...,
        labels: args._ElemType = ...,
        levels: args._ElemType = ...,
        location: args._ElemType = ...,
        marginal_heatmap_kind: args._ElemType = ...,
        normalization: args._ElemType = ...,
        orientation: args._ElemType = ...,
        panzoom: args._ElemType = ...,
        phiflip: args._ElemType = ...,
        resample_method: args._ElemType = ...,
        reset_ranges: args._ElemType = ...,
        rings: args._ElemType = ...,
        rotation: args._ElemType = ...,
        series: args._ElemType = ...,
        style: args._ElemType = ...,
        subplot: args._ElemType = ...,
        tilt: args._ElemType = ...,
        title: args._ElemType = ...,
        xbins: args._ElemType = ...,
        xflip: args._ElemType = ...,
        xform: args._ElemType = ...,
        xgrid: args._ElemType = ...,
        xind: args._ElemType = ...,
        xlabel: args._ElemType = ...,
        xlim: args._ElemType = ...,
        xlog: args._ElemType = ...,
        xticklabels: args._ElemType = ...,
        ybins: args._ElemType = ...,
        yflip: args._ElemType = ...,
        ygrid: args._ElemType = ...,
        yind: args._ElemType = ...,
        ylabel: args._ElemType = ...,
        ylim: args._ElemType = ...,
        ylog: args._ElemType = ...,
        zflip: args._ElemType = ...,
        zgrid: args._ElemType = ...,
        zlabel: args._ElemType = ...,
        zlim: args._ElemType = ...,
        zlog: args._ElemType = ...,
        a: args._ElemType = ...,
        algorithm: args._ElemType = ...,
        bin_counts: args._ElemType = ...,
        bin_edges: args._ElemType = ...,
        bin_width: args._ElemType = ...,
        c_dims: args._ElemType = ...,
        c: args._ElemType = ...,
        crange: args._ElemType = ...,
        dmax: args._ElemType = ...,
        dmin: args._ElemType = ...,
        draw_edges: args._ElemType = ...,  # bool?
        edge_color: args._ElemType = ...,
        edge_width: args._ElemType = ...,
        error: args._ElemType = ...,
        face_color: args._ElemType = ...,
        foreground_color: args._ElemType = ...,
        indices: args._ElemType = ...,
        inner_series: args._ElemType = ...,
        isovalue: args._ElemType = ...,
        markertype: args._ElemType = ...,
        nbins: args._ElemType = ...,
        philim: args._ElemType = ...,
        rgb: args._ElemType = ...,
        rlim: args._ElemType = ...,
        spec: args._ElemType = ...,
        stairs: args._ElemType = ...,
        step_where: args._ElemType = ...,
        u: args._ElemType = ...,
        v: args._ElemType = ...,
        weights: args._ElemType = ...,
        x: args._ElemType = ...,
        xcolormap: args._ElemType = ...,
        xrange: args._ElemType = ...,
        y: args._ElemType = ...,
        ycolormap: args._ElemType = ...,
        ylabels: args._ElemType = ...,
        yrange: args._ElemType = ...,
        z_dims: args._ElemType = ...,
        z: args._ElemType = ...,
        zrange: args._ElemType = ...,

        # append_plots: bool = ...,
        # hold_plots: bool = ...,
        # plots: args._ElemType = ...,
        # clear: bool = ...,
        # figsize: Iterable[float] = ...,
        # raw: str = ...,
        # size: Union[Iterable[float], Iterable[int], Mapping[str, args._ElemType], args._ArgumentContainer] = ...,
        # subplots: args._ElemType = ...,
        # update: bool = ...,
        # accelerate: bool = ...,
        # adjust_xlim: bool = ...,
        # adjust_ylim: bool = ...,
        # adjust_zlim: bool = ...,
        # alpha: float = ...,
        # angle_ticks: int = ...,
        # backgroundcolor: int = ...,
        # bar_color: Union[Iterable[float], int] = ...,
        # bar_width: float = ...,
        # colormap: int = ...,
        # font_precision: int = ...,
        # font: int = ...,
        # grplot: int = ...,
        # ind_bar_color: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        # ind_edge_color: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        # ind_edge_width: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        # keep_aspect_ratio: bool = ...,
        # kind: str = ...,
        # labels: Iterable[str] = ...,
        # levels: int = ...,
        # location: int = ...,
        # marginalheatmap_kind: str = ...,
        # normalization: str = ...,
        # orientation: str = ...,
        # panzoom: Iterable[float] = ...,
        # phiflip: bool = ...,
        # resample_method: Union[str, int] = ...,
        # reset_ranges: bool = ...,
        # rings: int = ...,
        # rotation: float = ...,
        # series: args._ElemType = ...,
        # style: str = ...,
        # subplot: Iterable[float] = ...,
        # tilt: float = ...,
        # title: str = ...,
        # xbins: int = ...,
        # xflip: bool = ...,
        # xform: int = ...,
        # xgrid: int = ...,
        # xind: int = ...,
        # xlabel: str = ...,
        # xlim: Iterable[float] = ...,
        # xlog: bool = ...,
        # xticklabels: args._ElemType = ...,
        # ybins: int = ...,
        # yflip: bool = ...,
        # ygrid: int = ...,
        # yind: int = ...,
        # ylabel: str = ...,
        # ylim: Iterable[float] = ...,
        # ylog: bool = ...,
        # zflip: bool = ...,
        # zgrid: int = ...,
        # zlabel: str = ...,
        # zlim: Iterable[float] = ...,
        # zlog: bool = ...,
        # a: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        # algorithm: Union[str, int] = ...,
        # bin_counts: int = ...,
        # bin_edges: Iterable[float] = ...,
        # bin_width: float = ...,
        # c_dims: Iterable[int] = ...,
        # c: Union[Iterable[float], Iterable[int]] = ...,
        # crange: Iterable[float] = ...,
        # dmax: float = ...,
        # dmin: float = ...,
        # draw_edges: int = ...,  # bool?
        # edge_color: Union[Iterable[float], int] = ...,
        # edge_width: float = ...,
        # error: Union[Mapping[str, args._ElemType], args._ArgumentContainer] = ...,
        # face_color: int = ...,
        # foreground_color: Iterable[float] = ...,
        # indices: Iterable[int] = ...,
        # inner_series: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        # isovalue: float = ...,
        # markertype: int = ...,
        # nbins: int = ...,
        # philim: Iterable[float] = ...,
        # rgb: Iterable[float] = ...,
        # rlim: Iterable[float] = ...,
        # spec: str = ...,
        # stairs: int = ...,
        # step_where: str = ...,
        # u: Iterable[float] = ...,
        # v: Iterable[float] = ...,
        # weights: Iterable[float] = ...,
        # x: Union[Iterable[int], Iterable[float]] = ...,
        # xcolormap: int = ...,
        # xrange: Iterable[float] = ...,
        # y: Iterable[float] = ...,
        # ycolormap: int = ...,
        # ylabels: Iterable[str] = ...,
        # yrange: Iterable[float] = ...,
        # z_dims: Iterable[int] = ...,
        # z: Iterable[float] = ...,
        # zrange: Iterable[float] = ...,
        **kwargs: args._ElemType
) -> bool:
    ...


@_require_runtime_version(0, 47, 0)
def plot(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    """
    Update the internal data container with the given data and draw the plot after it.

    :param args_container: The container with the data to merge and plot

    :raises TypeError: if the args_container is not a valid :class:`grm.args._ArgumentContainer`
    """
    if args_container is None:
        if kwargs:
            a = args.new(kwargs)
            return bool(_grm.grm_plot(a.ptr))
        return bool(_grm.grm_plot(c_void_p(0x0)))
    if isinstance(args_container, args._ArgumentContainer):
        for key in kwargs:
            args_container.push(key, kwargs[key])
        return bool(_grm.grm_plot(args_container.ptr))
    elif isinstance(args_container, dict):
        args_container = args_container | kwargs
        a = args.new(args_container)
        return bool(_grm.grm_plot(a.ptr))
    else:
        raise TypeError('args_container is not a valid args._argumentConainer or dict')
        # adjust_xlim: bool = ...,
        # adjust_ylim: bool = ...,
        # alpha: float = ...,
        # append_plots: bool = ...,
        # backgroundcolor: int = ...,
        # clear: bool = ...,
        # colormap: int = ...,
        # figsize: Iterable[float] = ...,
        # font: int = ...,
        # font_precision: int = ...,
        # hold_plots: bool = ...,
        # keep_aspect_ratio: bool = ...,
        # panzoom: Iterable[float] = ...,
        # resample_method: Union[str, int] = ...,
        # reset_ranges: bool = ...,
        # size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        # subplot: Iterable[float] = ...,
        # title: str = ...,
        # update: bool = ...,
        # xflip: bool = ...,
        # xlabel: str = ...,
        # xlim: Iterable[float] = ...,
        # xlog: bool = ...,
        # xrange: Iterable[float] = ...,
        # yflip: bool = ...,
        # ylabel: str = ...,
        # ylim: Iterable[float] = ...,
        # ylog: bool = ...,
        # yrange: Iterable[float] = ...


@overload
def barplot(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def barplot(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        bar_color: Union[Iterable[float], int] = ...,
        bar_width: float = ...,
        c: Union[Iterable[float], Iterable[int]] = ...,
        edge_color: Union[Iterable[float], int] = ...,
        edge_width: float = ...,
        error: Union[Mapping[str, args._ElemType], args._ArgumentContainer] = ...,
        ind_bar_color: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        ind_edge_color: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        ind_edge_width: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        indices: Iterable[int] = ...,
        inner_series: Union[Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        orientation: str = ...,
        rgb: Iterable[float] = ...,
        style: str = ...,
        xgrid: int = ...,
        xticklabels: args._ElemType = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        ylabels: Iterable[str] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def barplot(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def barplot(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="barplot", **kwargs)


@overload
def contour(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def contour(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        levels: int = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zgrid: int = ...,
        zlabel: str = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def contour(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def contour(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="contour", **kwargs)


@overload
def contourf(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def contourf(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        levels: int = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zgrid: int = ...,
        zlabel: str = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def contourf(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def contourf(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="contourf", **kwargs)


@overload
def heatmap(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def heatmap(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        crange: Iterable[float] = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        z_dims: Iterable[int] = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="heatmap", **kwargs)


@overload
def nonuniformheatmap(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def nonuniformheatmap(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        crange: Iterable[float] = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z_dims: Iterable[int] = ...,
        zlog: bool = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def nonuniformheatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def nonuniformheatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="nonuniformheatmap", **kwargs)


@overload
def hexbin(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def hexbin(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        nbins: int = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def hexbin(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def hexbin(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="hexbin", **kwargs)


@overload
def hist(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def hist(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        bar_color: Union[Iterable[float], int] = ...,
        edge_color: Union[Iterable[float], int] = ...,
        orientation: str = ...,
        weights: Iterable[float] = ...,
        xgrid: int = ...,
        xind: int = ...,
        ygrid: int = ...,
        yind: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def hist(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def hist(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="hist", **kwargs)


@overload
def imshow(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def imshow(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        c: Union[Iterable[float], Iterable[int]] = ...,
        c_dims: Iterable[int] = ...,
        xflip: bool = ...,
        yflip: bool = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        # xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        # yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def imshow(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def imshow(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="imshow", **kwargs)


@overload
def isosurface(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def isosurface(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        c: Union[Iterable[float], Iterable[int]] = ...,
        c_dims: Iterable[int] = ...,
        foreground_color: Iterable[float] = ...,
        isovalue: float = ...,
        rotation: float = ...,
        tilt: float = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def isosurface(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def isosurface(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="isosurface", **kwargs)


@overload
def line(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def line(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        labels: Iterable[str] = ...,
        location: int = ...,
        markertype: int = ...,
        orientation: str = ...,
        spec: str = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def line(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def line(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="line", **kwargs)


@overload
def marginal_heatmap(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def marginal_heatmap(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        algorithm: Union[int, str] = ...,
        marginal_heatmap_kind: str = ...,
        orientation: str = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xflip: bool = ...,
        xgrid: int = ...,
        xind: int = ...,
        y: Iterable[float] = ...,
        yflip: bool = ...,
        ygrid: int = ...,
        yind: int = ...,
        z: Iterable[float] = ...,
        zgrid: int = ...,
        zlabel: str = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        # xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        # yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def marginal_heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def marginal_heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="marginal_heatmap", **kwargs)


@overload
def pie(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def pie(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        labels: Iterable[str] = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def pie(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def pie(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="pie", **kwargs)


@overload
def plot3(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def plot3(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        adjust_zlim: bool = ...,
        rotation: float = ...,
        tilt: float = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zflip: bool = ...,
        zgrid: int = ...,
        zlabel: str = ...,
        zlim: Iterable[float] = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def plot3(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def plot3(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="plot3", **kwargs)


@overload
def polar(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def polar(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        angle_ticks: int = ...,
        rings: int = ...,
        spec: str = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def polar(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def polar(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="polar", **kwargs)


@overload
def polar_heatmap(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def polar_heatmap(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        crange: Iterable[float] = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        y: Iterable[float] = ...,
        z: Iterable[float] = ...,
        z_dims: Iterable[int] = ...,
        zlabel: str = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def polar_heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def polar_heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="polar_heatmap", **kwargs)


@overload
def nonuniformpolar_heatmap(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def nonuniformpolar_heatmap(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        crange: Iterable[float] = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        y: Iterable[float] = ...,
        z: Iterable[float] = ...,
        z_dims: Iterable[int] = ...,
        zlabel: str = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def nonuniformpolar_heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def nonuniformpolar_heatmap(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="nonuniformpolar_heatmap", **kwargs)


@overload
def polar_histogram(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def polar_histogram(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        x: Iterable[float] = ...,
        angle_ticks: int = ...,
        bin_counts: int = ...,
        bin_edges: Iterable[float] = ...,
        bin_width: float = ...,
        draw_edges: int = ...,
        edge_color: Union[Iterable[float], int] = ...,
        face_alpha: float = ...,
        face_color: int = ...,
        nbins: int = ...,
        normalization: str = ...,
        phiflip: bool = ...,
        philim: Iterable[float] = ...,
        rings: int = ...,
        rlim: Iterable[float] = ...,
        stairs: int = ...,
        xcolormap: int = ...,
        xgrid: int = ...,
        ycolormap: int = ...,
        ygrid: int = ...,
        zgrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def polar_histogram(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def polar_histogram(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="polar_histogram", **kwargs)


@overload
def quiver(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def quiver(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        u: Iterable[float] = ...,
        v: Iterable[float] = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def quiver(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def quiver(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="quiver", **kwargs)


@overload
def scatter(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def scatter(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        c: Union[Iterable[float], Iterable[int]] = ...,
        labels: Iterable[str] = ...,
        location: int = ...,
        markertype: int = ...,
        orientation: str = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zgrid: int = ...,
        zlabel: str = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def scatter(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def scatter(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="scatter", **kwargs)


@overload
def scatter3(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def scatter3(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        adjust_zlim: bool = ...,
        c: Union[Iterable[float], Iterable[int]] = ...,
        rotation: float = ...,
        tilt: float = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zflip: bool = ...,
        zgrid: int = ...,
        zlabel: str = ...,
        zlim: Iterable[float] = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def scatter3(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def scatter3(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="scatter3", **kwargs)


@overload
def shade(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def shade(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        x: Union[Iterable[float], Iterable[int]] = ...,
        xbins: int = ...,
        xform: int = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ybins: int = ...,
        ygrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def shade(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def shade(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="shade", **kwargs)


@overload
def stairs(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def stairs(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        labels: Iterable[str] = ...,
        location: int = ...,
        orientation: str = ...,
        step_where: str = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def stairs(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def stairs(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="stairs", **kwargs)


@overload
def stem(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def stem(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        labels: Iterable[str] = ...,
        location: int = ...,
        orientation: str = ...,
        spec: str = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def stem(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def stem(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="stem", **kwargs)


@overload
def surface(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def surface(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        accelerate: bool = ...,
        adjust_zlim: bool = ...,
        rotation: float = ...,
        tilt: float = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        z_dims: Iterable[int] = ...,
        zflip: bool = ...,
        zgrid: int = ...,
        zlabel: str = ...,
        zlim: Iterable[float] = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def surface(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def surface(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="surface", **kwargs)


@overload
def tricont(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def tricont(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        levels: int = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zgrid: int = ...,
        zlabel: str = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def tricont(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def tricont(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="tricont", **kwargs)


@overload
def trisurf(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def trisurf(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        adjust_zlim: bool = ...,
        rotation: float = ...,
        tilt: float = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zflip: bool = ...,
        zgrid: int = ...,
        zlabel: str = ...,
        zlim: Iterable[float] = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def trisurf(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def trisurf(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="trisurf", **kwargs)


@overload
def volume(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def volume(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        adjust_zlim: bool = ...,
        algorithm: Union[int, str] = ...,
        c: Union[Iterable[float], Iterable[int]] = ...,
        c_dims: Iterable[int] = ...,
        dmax: float = ...,
        dmin: float = ...,
        rotation: float = ...,
        tilt: float = ...,
        xgrid: int = ...,
        ygrid: int = ...,
        zflip: bool = ...,
        zgrid: int = ...,
        zlim: Iterable[float] = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def volume(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def volume(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="volume", **kwargs)


@overload
def wireframe(
        args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]
) -> bool:
    ...


@overload
def wireframe(
        *,
        plots: args._ElemType = ...,
        subplots: args._ElemType = ...,
        series: args._ElemType = ...,

        adjust_zlim: bool = ...,
        rotation: float = ...,
        tilt: float = ...,
        x: Union[Iterable[float], Iterable[int]] = ...,
        xgrid: int = ...,
        y: Iterable[float] = ...,
        ygrid: int = ...,
        z: Iterable[float] = ...,
        zflip: bool = ...,
        zgrid: int = ...,
        zlabel: str = ...,
        zlim: Iterable[float] = ...,
        zlog: bool = ...,
        zrange: Iterable[float] = ...,

        adjust_xlim: bool = ...,
        adjust_ylim: bool = ...,
        alpha: float = ...,
        append_plots: bool = ...,
        backgroundcolor: int = ...,
        clear: bool = ...,
        colormap: int = ...,
        figsize: Iterable[float] = ...,
        font: int = ...,
        font_precision: int = ...,
        hold_plots: bool = ...,
        keep_aspect_ratio: bool = ...,
        panzoom: Iterable[float] = ...,
        resample_method: Union[str, int] = ...,
        reset_ranges: bool = ...,
        size: Union[Iterable[float], Iterable[int], Iterable[Mapping[str, args._ElemType]], Iterable[args._ArgumentContainer]] = ...,
        subplot: Iterable[float] = ...,
        title: str = ...,
        update: bool = ...,
        xflip: bool = ...,
        xlabel: str = ...,
        xlim: Iterable[float] = ...,
        xlog: bool = ...,
        xrange: Iterable[float] = ...,
        yflip: bool = ...,
        ylabel: str = ...,
        ylim: Iterable[float] = ...,
        ylog: bool = ...,
        yrange: Iterable[float] = ...
) -> bool:
    ...


@overload
def wireframe(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]],
        **kwargs: args._ElemType
) -> bool:
    ...


def wireframe(
        args_container: Optional[Union[Mapping[str, args._ElemType], args._ArgumentContainer]] = None,
        **kwargs: args._ElemType
) -> bool:
    return plot(args_container, kind="wireframe", **kwargs)


@_require_runtime_version(0, 47, 0)
def clear() -> bool:
    """
    Clear all plots.
    """
    return bool(_grm.grm_clear())


@_require_runtime_version(0, 47, 0)
def max_plotid() -> int:
    """
    Index of the highest active plot.
    """
    return int(_grm.grm_max_plotid())


@_require_runtime_version(0, 47, 0)
def merge(args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]) -> bool:
    """
    Store the args_container into the internal, possibly clearing the internal values.

    :param args_container: The container with the data to merge

    :raises TypeError: if the args_container is not a valid :class:`grm.args._ArgumentContainer`
    """
    if isinstance(args_container, dict):
        a = args.new(args_container)
        return bool(_grm.grm_merge(a.ptr))
    elif isinstance(args_container, args._ArgumentContainer):
        return bool(_grm.grm_merge(args_container.ptr))
    else:
        raise TypeError("The given parameter is not a valid ArgumentContainer or Dict")


@_require_runtime_version(0, 47, 0)
def merge_extended(args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer], hold: bool, identificator: str) -> bool:
    """
    Merge the args_container into the internal, like merge_named, but hold specifies if the internal container should not be cleared.

    :param args_container: The argument container with the data to merge
    :param hold: When True, does not clear the internal data.
    :param identificator: The identificator to pass to the MERGE_END event

    :raises TypeError: if the arguments passed are not the expected type
    """
    if isinstance(args_container, dict):
        args_container = args.new(args_container)
    if (
        not isinstance(args_container, args._ArgumentContainer)
        or not isinstance(hold, int)  # noqa W503
        or not isinstance(identificator, str)  # noqa W503
    ):
        raise TypeError("The given parameters do not match the types required.")

    return bool(_grm.grm_merge_extended(args_container.ptr, c_int(1 if hold else 0), _encode_str_to_char_p(identificator)))


@_require_runtime_version(0, 47, 0)
def merge_hold(args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer]) -> bool:
    """
    Merge the container while preserving the internally stored values.

    :param args_container: The argument container with the data to merge

    :raises TypeError: if the args_container is not a valid :class:`grm.args._ArgumentContainer`
    """
    if isinstance(args_container, dict):
        args_container = args.new(args_container)
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer.")
    return bool(_grm.grm_merge_hold(args_container.ptr))


@_require_runtime_version(0, 47, 0)
def merge_named(args_container: Union[Mapping[str, args._ElemType], args._ArgumentContainer], identificator: str) -> bool:
    """
    Merge the container, and the MERGE_END event is called with identificator set to the argument.

    :param args_container: The argument container with the data to merge
    :param identificator: The identificator to pass to the MERGE_END event

    :raises TypeError: if the args_container is not a valid :class:`grm.args._ArgumentContainer`, or the
        identificator is not a string
    """
    if isinstance(args_container, dict):
        args_container = args.new(args_container)
    if not isinstance(args_container, args._ArgumentContainer):
        raise TypeError("The given parameter is not a valid ArgumentContainer.")
    if not isinstance(identificator, str):
        raise TypeError("The given identificator is not a valid string.")

    return bool(_grm.grm_merge_named(args_container.ptr, _encode_str_to_char_p(identificator)))


@_require_runtime_version(0, 47, 0)
def switch(plot_id: int) -> bool:
    """
    Switches the default plot id.

    :param plot_id: The plot id to switch to.

    :raises TypeError: if plot_id is not an unsigned int.
    """
    if not isinstance(plot_id, int):
        raise TypeError("Given parameter is not a valid integer!")
    if plot_id < 0:
        raise TypeError("Given parameter is not unsigned.")
    return bool(_grm.grm_switch(c_uint(plot_id)))


@_require_runtime_version(0, 47, 0)
def finalize() -> None:
    """
    Finalize the grm framework and frees resources.
    """
    _grm.grm_finalize()


if _RUNTIME_VERSION >= (0, 47, 0, 0):
    _grm.grm_plot.argtypes = [c_void_p]
    _grm.grm_plot.restype = c_int

    _grm.grm_clear.argtypes = []
    _grm.grm_clear.restype = c_int

    _grm.grm_max_plotid.argtypes = []
    _grm.grm_max_plotid.restype = c_uint

    _grm.grm_merge.argtypes = [c_void_p]
    _grm.grm_merge.restype = c_int

    _grm.grm_merge_extended.argtypes = [c_void_p, c_int, c_char_p]
    _grm.grm_merge_extended.restype = c_int

    _grm.grm_merge_hold.argtypes = [c_void_p]
    _grm.grm_merge_hold.restype = c_int

    _grm.grm_merge_named.argtypes = [c_void_p, c_char_p]
    _grm.grm_merge_named.restype = c_int

    _grm.grm_switch.argtypes = [c_uint]
    _grm.grm_switch.restype = c_int

    _grm.grm_finalize.argtypes = []
    _grm.grm_finalize.restype = None

__all__ = ["plot", "clear", "max_plotid", "merge", "merge_extended", "merge_hold", "merge_named", "switch", "finalize"]
