# coding: utf-8
"""
This module offers a simple, matlab-style API built on top of the gr package.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import functools
import sys
import warnings
import numpy as np
import gr
import gr3


try:
    basestring
except NameError:
    basestring = str

copy_if_needed = False
if np.lib.NumpyVersion(np.__version__) >= "2.0.0":
    copy_if_needed = None


def _close_gks_on_error(func):
    """
    Wrap an API function to make sure GKS is closed on error.

    Not closing GKS after an error occurred during plotting could lead to
    an unexpected GKS state, e.g. printing of more than one output page.

    :param func: the mlab API function to wrap
    :return: the wrapped API function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            gr.emergencyclosegks()
            raise
    return wrapper


@_close_gks_on_error
def plot(*args, **kwargs):
    """
    Draw one or more line plots.

    This function can receive one or more of the following:

    - x values and y values, or
    - x values and a callable to determine y values, or
    - y values only, with their indices as x values

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = 2*x+4
    >>> # Plot x and y
    >>> mlab.plot(x, y)
    >>> # Plot x and a callable
    >>> mlab.plot(x, lambda x: x**3 + x**2 + x)
    >>> # Plot y, using its indices for the x values
    >>> mlab.plot(y)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    if _plt.kwargs['ax']:
        _plt.args += _plot_args(args)
    else:
        _plt.args = _plot_args(args)
    return _plot_data(kind='line')


@_close_gks_on_error
def oplot(*args, **kwargs):
    """
    Draw one or more line plots over another plot.

    This function can receive one or more of the following:

    - x values and y values, or
    - x values and a callable to determine y values, or
    - y values only, with their indices as x values

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = 2*x+4
    >>> # Draw the first plot
    >>> mlab.plot(x, y)
    >>> # Plot graph over it
    >>> mlab.oplot(x, lambda x: x**3 + x**2 + x)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args += _plot_args(args)
    return _plot_data(kind='line')


@_close_gks_on_error
def step(*args, **kwargs):
    """
    Draw one or more step or staircase plots.

    This function can receive one or more of the following:

    - x values and y values, or
    - x values and a callable to determine y values, or
    - y values only, with their indices as x values

    :param args: the data to plot
    :param where: pre, mid or post, to decide where the step between two y values should be placed

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = 2*x+4
    >>> # Plot x and y
    >>> mlab.step(x, y)
    >>> # Plot x and a callable
    >>> mlab.step(x, lambda x: x**3 + x**2 + x)
    >>> # Plot y, using its indices for the x values
    >>> mlab.step(y)
    >>> # Use next y step directly after x each position
    >>> mlab.step(y, where='pre')
    >>> # Use next y step between two x positions
    >>> mlab.step(y, where='mid')
    >>> # Use next y step immediately before next x position
    >>> mlab.step(y, where='post')
    """
    global _plt
    if 'where' in kwargs:
        _plt.kwargs['step_where'] = kwargs.pop('where')
    _plt.kwargs.update(kwargs)
    if _plt.kwargs['ax']:
        _plt.args += _plot_args(args)
    else:
        _plt.args = _plot_args(args)
    return _plot_data(kind='step')


@_close_gks_on_error
def scatter(*args, **kwargs):
    """
    Draw one or more scatter plots.

    This function can receive one or more of the following:

    - x values and y values, or
    - x values and a callable to determine y values, or
    - y values only, with their indices as x values

    Additional to x and y values, you can provide values for the markers'
    size and color. Size values will determine the marker size in percent of
    the regular size, and color values will be used in combination with the
    current colormap.

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = 0.2*x+0.4
    >>> # Plot x and y
    >>> mlab.scatter(x, y)
    >>> # Plot x and a callable
    >>> mlab.scatter(x, lambda x: 0.2*x + 0.4)
    >>> # Plot y, using its indices for the x values
    >>> mlab.scatter(y)
    >>> # Plot a diagonal with increasing size and color
    >>> x = np.linspace(0, 1, 11)
    >>> y = np.linspace(0, 1, 11)
    >>> s = np.linspace(50, 400, 11)
    >>> c = np.linspace(0, 255, 11)
    >>> mlab.scatter(x, y, s, c)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyac')
    return _plot_data(kind='scatter')


@_close_gks_on_error
def quiver(x, y, u, v, **kwargs):
    """
    Draw a quiver plot.

    This function draws arrows to visualize a vector for each point of a grid.

    :param x: the X coordinates of the grid
    :param y: the Y coordinates of the grid
    :param u: the U component for each point on the grid
    :param v: the V component for each point on the grid

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-1, 1, 30)
    >>> y = np.linspace(-1, 1, 20)
    >>> u = np.repeat(x[np.newaxis, :], len(y), axis=0)
    >>> v = np.repeat(y[:, np.newaxis], len(x), axis=1)
    >>> # Draw arrows on grid
    >>> mlab.quiver(x, y, u, v)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args((x, y, u, v), fmt='xyuv')
    return _plot_data(kind='quiver')


@_close_gks_on_error
def polar(*args, **kwargs):
    """
    Draw one or more polar plots.

    This function can receive one or more of the following:

    - angle values and radius values, or
    - angle values and a callable to determine radius values

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example data
    >>> angles = np.linspace(0, 2*math.pi, 40)
    >>> radii = np.linspace(0, 2, 40)
    >>> # Plot angles and radii
    >>> mlab.polar(angles, radii)
    >>> # Plot angles and a callable
    >>> mlab.polar(angles, lambda radius: math.cos(radius)**2)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args)
    return _plot_data(kind='polar')


@_close_gks_on_error
def trisurf(*args, **kwargs):
    """
    Draw a triangular surface plot.

    This function uses the current colormap to display a series of points
    as a triangular surface plot. It will use a Delaunay triangulation to
    interpolate the z values between x and y values. If the series of points
    is concave, this can lead to interpolation artifacts on the edges of the
    plot, as the interpolation may occur in very acute triangles.

    :param x: the x coordinates to plot
    :param y: the y coordinates to plot
    :param z: the z coordinates to plot

    **Usage examples:**

    >>> # Create example point data
    >>> x = np.random.uniform(-4, 4, 100)
    >>> y = np.random.uniform(-4, 4, 100)
    >>> z = np.sin(x) + np.cos(y)
    >>> # Draw the triangular surface plot
    >>> mlab.trisurf(x, y, z)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    return _plot_data(kind='trisurf')


@_close_gks_on_error
def tricont(x, y, z, *args, **kwargs):
    """
    Draw a triangular contour plot.

    This function uses the current colormap to display a series of points
    as a triangular contour plot. It will use a Delaunay triangulation to
    interpolate the z values between x and y values. If the series of points
    is concave, this can lead to interpolation artifacts on the edges of the
    plot, as the interpolation may occur in very acute triangles.

    :param x: the x coordinates to plot
    :param y: the y coordinates to plot
    :param z: the z coordinates to plot

    **Usage examples:**

    >>> # Create example point data
    >>> x = np.random.uniform(-4, 4, 100)
    >>> y = np.random.uniform(-4, 4, 100)
    >>> z = np.sin(x) + np.cos(y)
    >>> # Draw the triangular contour plot
    >>> mlab.tricont(x, y, z)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    args = [x, y, z] + list(args)
    _plt.args = _plot_args(args, fmt='xyzc')
    return _plot_data(kind='tricont')


@_close_gks_on_error
def stem(*args, **kwargs):
    """
    Draw a stem plot.

    This function can receive one or more of the following:

    - x values and y values, or
    - x values and a callable to determine y values, or
    - y values only, with their indices as x values

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = 0.2*x+0.4
    >>> # Plot x and y
    >>> mlab.stem(x, y)
    >>> # Plot x and a callable
    >>> mlab.stem(x, lambda x: x**3 + x**2 + x + 6)
    >>> # Plot y, using its indices for the x values
    >>> mlab.stem(y)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args)
    return _plot_data(kind='stem')


def _hist(x, nbins=0, weights=None):
    x = np.array(x)
    x_min = x.min()
    x_max = x.max()
    if nbins <= 1:
        nbins = int(np.round(3.3 * np.log10(len(x)))) + 1
    binned_x = np.array(np.floor((x - x_min) / (x_max - x_min) * nbins), dtype=int)
    binned_x[binned_x == nbins] = nbins - 1
    counts = np.bincount(binned_x, weights=weights)
    edges = np.linspace(x_min, x_max, nbins + 1)
    return counts, edges


@_close_gks_on_error
def histogram(x, num_bins=0, weights=None, **kwargs):
    r"""
    Draw a histogram.

    If **num_bins** is 0, this function computes the number of
    bins as :math:`\text{round}(3.3\cdot\log_{10}(n))+1` with n as the number
    of elements in x, otherwise the given number of bins is used for the
    histogram.

    :param x: the values to draw as histogram
    :param num_bins: the number of bins in the histogram
    :param weights: weights for the x values

    **Usage examples:**

    >>> # Create example data
    >>> x = np.random.uniform(-1, 1, 100)
    >>> # Draw the histogram
    >>> mlab.histogram(x)
    >>> # Draw the histogram with 19 bins
    >>> mlab.histogram(x, num_bins=19)
    >>> # Draw the histogram with weights
    >>> weights = np.ones_like(x)
    >>> weights[x < 0] = 2.5
    >>> mlab.histogram(x, weights=weights)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    hist, bins = _hist(x, nbins=num_bins, weights=weights)
    _plt.args = [(np.array(bins), np.array(hist), None, None, "")]
    return _plot_data(kind='hist')


@_close_gks_on_error
def contour(*args, **kwargs):
    """
    Draw a contour plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a contour plot. It can receive one
    or more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a MxN grid, or
    - N x values, M y values and a callable to determine z values

    If a series of points is passed to this function, their values will be
    interpolated on a grid. For grid points outside the convex hull of the
    provided points, a value of 0 will be used.

    :param args: the data to plot
    :param levels: Number of contour lines

    **Usage examples:**

    >>> # Create example point data
    >>> x = np.random.uniform(-4, 4, 100)
    >>> y = np.random.uniform(-4, 4, 100)
    >>> z = np.sin(x) + np.cos(y)
    >>> # Draw the contour plot
    >>> mlab.contour(x, y, z)
    >>> # Create example grid data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = np.linspace(0, np.pi, 20)
    >>> z = np.sin(x[np.newaxis, :]) + np.cos(y[:, np.newaxis])
    >>> # Draw the contour plot
    >>> mlab.contour(x, y, z, levels=10)
    >>> # Draw the contour plot using a callable
    >>> mlab.contour(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    return _plot_data(kind='contour')


@_close_gks_on_error
def contourf(*args, **kwargs):
    """
    Draw a filled contour plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a filled contour plot. It can
    receive one or more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a MxN grid, or
    - N x values, M y values and a callable to determine z values

    If a series of points is passed to this function, their values will be
    interpolated on a grid. For grid points outside the convex hull of the
    provided points, a value of 0 will be used.

    :param args: the data to plot
    :param levels: Number of contour lines

    **Usage examples:**

    >>> # Create example point data
    >>> x = np.random.uniform(-4, 4, 100)
    >>> y = np.random.uniform(-4, 4, 100)
    >>> z = np.sin(x) + np.cos(y)
    >>> # Draw the filled contour plot
    >>> mlab.contourf(x, y, z)
    >>> # Create example grid data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = np.linspace(0, np.pi, 20)
    >>> z = np.sin(x[np.newaxis, :]) + np.cos(y[:, np.newaxis])
    >>> # Draw the filled contour plot
    >>> mlab.contourf(x, y, z, levels=10)
    >>> # Draw the filled contour plot using a callable
    >>> mlab.contourf(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    return _plot_data(kind='contourf')


@_close_gks_on_error
def hexbin(*args, **kwargs):
    """
    Draw a hexagon binning plot.

    This function uses hexagonal binning and the the current colormap to
    display a series of points. It  can receive one or more of the following:

    - x values and y values, or
    - x values and a callable to determine y values, or
    - y values only, with their indices as x values

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example data
    >>> x = np.random.normal(0, 1, 100000)
    >>> y = np.random.normal(0, 1, 100000)
    >>> # Draw the hexbin plot
    >>> mlab.hexbin(x, y)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args)
    return _plot_data(kind='hexbin')


@_close_gks_on_error
def heatmap(data, **kwargs):
    """
    Draw a heatmap.

    This function uses the current colormap to display a two-dimensional
    array as a heatmap. The array is drawn with its first value in the upper
    left corner, so in some cases it may be necessary to flip the columns
    (see the example below).

    By default the function will use the row and column indices for the x- and
    y-axes, so setting the axis limits is recommended. Also note that the
    values in the array must lie within the current z-axis limits so it may
    be necessary to adjust these limits or clip the range of array values.

    :param data: the heatmap data

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = np.linspace(0, np.pi, 20)
    >>> z = np.sin(x[:, np.newaxis]) + np.cos(y[np.newaxis, :])
    >>> # Draw the heatmap
    >>> mlab.heatmap(z[::-1, :], xlim=(-2, 2), ylim=(0, np.pi))
    """
    global _plt
    data = np.array(data, copy=copy_if_needed)
    if len(data.shape) != 2:
        raise ValueError('expected 2-D array')
    _plt.kwargs.update(kwargs)
    xlim = _plt.kwargs.get('xlim', None)
    ylim = _plt.kwargs.get('ylim', None)
    _plt.args = [(xlim, ylim, data, None, "")]
    return _plot_data(kind='heatmap')


@_close_gks_on_error
def polar_heatmap(data, **kwargs):
    """
    Draw a polar heatmap.

    This function uses the current colormap to display a two-dimensional
    array mapped to a disk using polar coordinates. The array is mapped
    by interpreting the rows as the angle and the columns as the radius.

    By default the function will use an inner radius of 0 and the number
    of columns as the outer radius and draw a complete circle, so setting
    the axis limits is recommended. Also note that the values in the array
    must lie within the current z-axis limits so it may be necessary to
    adjust these limits or clip the range of array values.

    :param data: the heatmap data

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 100)
    >>> y = np.linspace(0, np.pi, 200)
    >>> z = np.sin(x[:, np.newaxis]) + np.cos(y[np.newaxis, :])
    >>> # Draw the heatmap
    >>> mlab.polar_heatmap(z, rlim=(1, 10), philim=(0, np.pi / 2))
    """
    global _plt
    data = np.array(data, copy=copy_if_needed)
    if len(data.shape) != 2:
        raise ValueError('expected 2-D array')
    _plt.kwargs.update(kwargs)
    rlim = _plt.kwargs.get('rlim', None)
    philim = _plt.kwargs.get('philim', None)
    _plt.args = [(rlim, philim, data, None, "")]
    return _plot_data(kind='polar_heatmap')


@_close_gks_on_error
def shade(*args, **kwargs):
    """
    Draw a point or line based heatmap.

    This function uses the current colormap to display a series of points or
    polylines. For line data, NaN values can be used as separator.

    :param args: the data to plot
    :param xform: the transformation type used for color mapping

    The available transformation types are:

    +----------------+---+--------------------+
    |XFORM_BOOLEAN   |  0|boolean             |
    +----------------+---+--------------------+
    |XFORM_LINEAR    |  1|linear              |
    +----------------+---+--------------------+
    |XFORM_LOG       |  2|logarithmic         |
    +----------------+---+--------------------+
    |XFORM_LOGLOG    |  3|double logarithmic  |
    +----------------+---+--------------------+
    |XFORM_CUBIC     |  4|cubic               |
    +----------------+---+--------------------+
    |XFORM_EQUALIZED |  5|histogram equalized |
    +----------------+---+--------------------+

    **Usage examples:**

    >>> # Create point data
    >>> x = np.random.normal(size=100000)
    >>> y = np.random.normal(size=100000)
    >>> mlab.shade(x, y)
    >>> # Create line data with NaN as polyline separator
    >>> x = np.concatenate((np.random.normal(size=10000), [np.nan], np.random.normal(loc=5, size=10000)))
    >>> y = np.concatenate((np.random.normal(size=10000), [np.nan], np.random.normal(loc=5, size=10000)))
    >>> mlab.shade(x, y)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xys')
    return _plot_data(kind='shade')


@_close_gks_on_error
def wireframe(*args, **kwargs):
    """
    Draw a three-dimensional wireframe plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a wireframe plot. It can receive one
    or more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a MxN grid, or
    - N x values, M y values and a callable to determine z values

    If a series of points is passed to this function, their values will be
    interpolated on a grid. For grid points outside the convex hull of the
    provided points, a value of 0 will be used.

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example point data
    >>> x = np.random.uniform(-4, 4, 100)
    >>> y = np.random.uniform(-4, 4, 100)
    >>> z = np.sin(x) + np.cos(y)
    >>> # Draw the wireframe plot
    >>> mlab.wireframe(x, y, z)
    >>> # Create example grid data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = np.linspace(0, np.pi, 20)
    >>> z = np.sin(x[np.newaxis, :]) + np.cos(y[:, np.newaxis])
    >>> # Draw the wireframe plot
    >>> mlab.wireframe(x, y, z)
    >>> # Draw the wireframe plot using a callable
    >>> mlab.wireframe(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    return _plot_data(kind='wireframe')


@_close_gks_on_error
def surface(*args, **kwargs):
    """
    Draw a three-dimensional surface plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a surface plot. It can receive one or
    more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a MxN grid, or
    - N x values, M y values and a callable to determine z values

    If a series of points is passed to this function, their values will be
    interpolated on a grid. For grid points outside the convex hull of the
    provided points, a value of 0 will be used.

    :param args: the data to plot

    **Usage examples:**

    >>> # Create example point data
    >>> x = np.random.uniform(-4, 4, 100)
    >>> y = np.random.uniform(-4, 4, 100)
    >>> z = np.sin(x) + np.cos(y)
    >>> # Draw the surface plot
    >>> mlab.surface(x, y, z)
    >>> # Create example grid data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = np.linspace(0, np.pi, 20)
    >>> z = np.sin(x[np.newaxis, :]) + np.cos(y[:, np.newaxis])
    >>> # Draw the surface plot
    >>> mlab.surface(x, y, z)
    >>> # Draw the surface plot using a callable
    >>> mlab.surface(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    return _plot_data(kind='surface')


@_close_gks_on_error
def bar(y, *args, **kwargs):
    """
    Draw a two-dimensional bar plot.

    This function uses a list of y values to create a two dimensional bar
    plot. It can receive the following parameters:

    - a list of y values, or
    - a list of same length lists which contain y values (multiple bars)
    - a list of colors
    - one or more of the following key value pairs:
        - a parameter bar_width
        - a parameter edge_width
        - a parameter bar_color (either an int or a list of rgb values)
        - a parameter edge_color (either an int or a list of rgb values)
        - a list of xnotations
        - a list ind_bar_color, ind_edge_color which can be one color pack or
          a list with multiple ones for individual bars (color pack: first
          value: list with the indices or one index as an int, second value:
          color (rgb list))
        - a list ind_edge_width can be one width pack or a list with multiple
          ones for individual bars (width pack: first value: list with the
          indices or one index as an int, second value: width (float))
        - a style parameter (only for multi-bar)

    All parameters except for xnotations, ind_bar_color, ind_edge_color and
    ind_edge_width will be saved for the next bar plot (set to None for
    default)

    :param y: the data to plot
    :param args: the list of colors

    **Usage examples:**

    >>> # Create example data
    >>> y = np.random.uniform(0, 10, 5)
    >>> # Draw the bar plot
    >>> mlab.bar(y)
    >>> # Draw the bar plot with locations specified by x
    >>> x = ['a', 'b', 'c', 'd', 'e']
    >>> mlab.bar(y, xnotations=x)
    >>> # Draw the bar plot with different bar_width, edge_width, edge_color and bar_color
    >>> # (bar_width: float in (0;1], edge_width: float value bigger or equal to 0, color: int in [0;1255] or rgb list)
    >>> mlab.bar(y, bar_width=0.6, edge_width=2, bar_color=999, edge_color=3)
    >>> mlab.bar(y, bar_color=[0.66, 0.66, 0.66], edge_color=[0.33, 0.33, 0.33])
    >>> # Draw the bar plot with bars that have individual bar_color, edge_color, edge_with
    >>> mlab.bar(y, ind_bar_color=[1, [0.4, 0.4, 0.4]], ind_edge_color=[[1, 2], [0.66, 0.33, 0.33]], ind_edge_width=[[1, 2], 3])
    >>> # Draw the bar plot with bars that have multiple individual colors
    >>> mlab.bar(y, ind_bar_color=[[1, [1, 0.3, 0]], [[2, 3], [1, 0.5, 0]]])
    >>> # Draw the bar plot with default bar_width, edge_width, edge_color and bar_color
    >>> mlab.bar(y, bar_width=None, edge_width=None, bar_color=None, edge_color=None)
    >>> # Draw the bar plot with colorlist
    >>> mlab.bar(y, [989, 982, 980, 981, 996])
    >>> # Create example sublist data
    >>> yy = np.random.rand(3, 3)
    >>> # Draw the bar plot lined / stacked / with colorlist
    >>> mlab.bar(yy, bar_style='lined')
    >>> mlab.bar(yy, bar_style='stacked')
    >>> mlab.bar(yy, [989, 998, 994])
    """
    global _plt
    _plt.kwargs.update(kwargs)
    if 'bar_style' not in _plt.kwargs:
        _plt.kwargs['bar_style'] = 'stacked'
    if isinstance(y[0], list) or (isinstance(y, np.ndarray) and len(y.shape) == 2):
        if isinstance(y, np.ndarray) and len(y.shape) > 2:
            raise IndexError('Numpy array has to be of dimension 2 or lower!')
        _plt.kwargs['multi_bar'] = True
        if _plt.kwargs['bar_style'] == 'lined':
            new_arg = []
            for ls in y:
                new_arg.append(max(ls))
        else:
            new_arg = []
            for ls in y:
                new_arg.append(sum(ls))
        new_args = [new_arg, y]
    else:
        _plt.kwargs['multi_bar'] = False
        new_args = [y, None]

    if args:
        c = args[0]
        if not isinstance(c, list):
            raise TypeError('C has to be of type list!')
        if _plt.kwargs['multi_bar']:
            if len(c) != len(y[0]):
                raise IndexError('The length of c has to equal the length of the sublists when using a multi-bar!')
        else:
            if len(c) != len(y):
                raise IndexError('The length of c has to equal the amount of y-values!')
        for color in c:
            if isinstance(color, int):
                if color < 0:
                    raise ValueError('The values in c have to be bigger or equal to 0!')
            if isinstance(color, list):
                if len(color) != 3:
                    raise IndexError("RGB list has to contain 3 values!")
                rgb = color
                for v in rgb:
                    if v < 0 or v > 1:
                        raise ValueError('The values of a rgb color have to be in [1;0]!')
        new_args.append(c)

    _plt.args = _plot_args(new_args, fmt='y')
    return _plot_data(kind='bar')


def polar_histogram(*args, **kwargs):
    """
    Draw a polar histogram plot.

    This function uses certain input values to display a polar histogram.

    It must receive only one of the following:

    - theta: a list containing angles between 0 and 2 * pi
    - bin_counts: a list containing integer values for the height of bins

    It can also receive:

    - normalization: type of normalization in which the histogram will be displayed

        + count: the default normalization.  The height of each bar is the number of observations in each bin.
        + probability: The height of each bar is the relative number of observations,
          (number of observations in bin/total number of observations).
          The sum of the bar heights is 1.
        + countdensity: The height of each bar is the number of observations in bin/width of bin.
        + pdf: Probability density function estimate. The height of each bar is,
          (number of observations in the bin)/(total number of observations * width of bin).
          The area of each bar is the relative number of observations. The sum of the bar areas is 1
        + cumcount: The height of each bar is the cumulative number of observations in each bin and all previous bins.
          The height of the last bar is numel (theta).
        + cdf: Cumulative density function estimate. The height of each bar is equal to the cumulative relative
          number of observations in the bin and all previous bins. The height of the last bar is 1.

    - stairs: Boolean, display the histogram outline only

    - face_alpha: float value between 0 and 1 inclusive. Transparency of histogram bars. A value of 1 means fully opaque
      and 0 means completely transparent (invisible). Default is 0.75

    - face_color: Histogram bar color. Either an integer between 0 and 1008 or a list with three floats between 0 and 1
      representing an RGB Triplet

    - edge_color: Histogram bar edgecolor. Either an integer between 0 and 1008 or a list with three floats
      between 0 and 1 representing an RGB Triplet

    - num_bins: Number of bins specified as a positive integer. If no bins are given, the polarhistogram will automatically
      calculate the number of bins

    - philim: a tuple containing two angle values [min, max]. This option  plots a histogram using the input values
      (theta) that fall between min and max inclusive.

    - rlim: a tuple containing two values between 0 and 1 (min, max). This option plots a histogram with bins starting at
      min and ending at max

    - bin_edges: a list of angles between 0 and 2 * pi which specify the Edges of each bin/bar.
      NOT COMPATIBLE with bin_limits. When used with bin_counts: len(bin_edges) == len(bin_counts) + 1

    - bin_width: Width across the top of bins, specified as a float less than 2 * pi

    - colormap: A triple tuple used to create a Colormap. (x, y, size). x = index for the first Colormap. Y for the second.
      size for the size of the colormap. each component must be given! At least (None, None, None)

    - draw_edges: Boolean, draws the edges of each bin when using a colormap. Only works with a colormap

    :param args: a list


    **Usage examples:**

    >>> # create a theta list
    >>> theta = [0, 0.6, 1, 1.3, np.pi/2, np.pi, np.pi*2, np.pi*2]
    >>> polar_histogram(theta)
    >>> # create bin_counts
    >>> bc = [1, 2, 6, 9]
    >>> polar_histogram(theta, bin_counts=bc)
    >>> #create bin_edges
    >>> be = [1, 2, np.pi*1.3, np.pi]
    >>> polar_histogram(theta, bin_edges=be)
    >>> polar_histogram(theta, normalization='cdf')
    >>> polar_histogram(theta, colormap=(0,0,1000))

    """
    global _plt

    saved_ax = _plt.kwargs.get('ax', False)

    _plt.kwargs['ax'] = True
    _plt.args = _plot_args(args, fmt='xys')

    def find_max(classes, normalization):
        if normalization == 'cumcount':
            sum = 0
            for x in range(len(classes)):
                sum += len(classes[x])
            return sum

        else:
            max = len(classes[0])
            for x in range(len(classes)):
                if max < len(classes[x]):
                    max = len(classes[x])
            return max

    _plt.kwargs.update(kwargs)
    classes = []
    gr.setlinecolorind(1)
    angles = []

    # Color Map
    if _plt.kwargs.get('colormap') is not None:
        is_colormap = True
        colormap = _plt.kwargs['colormap']
        if isinstance(colormap, tuple):
            colormap = _create_colormap(colormap)
    else:
        is_colormap = False

    if _plt.kwargs.get('draw_edges') is True and not is_colormap:
        raise ValueError('draw_edges only usable with a colormap')

    # bin_edges
    if _plt.kwargs.get('bin_edges', None) is not None:
        binedges = _plt.kwargs['bin_edges']
        is_binedges = True
    else:
        is_binedges = False

    # normalization
    if _plt.kwargs.get('normalization') is not None:
        normalization = _plt.kwargs['normalization']
    else:
        normalization = 'count'
        _plt.kwargs['normalization'] = 'count'

    # Bincounts or theta
    if _plt.kwargs.get('theta') is not None:
        theta = _plt.kwargs['theta']
    else:
        theta = args[0]
    # theta check
    if len(theta) == 0:
        raise ValueError('List is empty')
    for obj in theta:
        if isinstance(obj, float):
            has_theta = True
            break
        elif isinstance(obj, int):
            has_theta = False

    if not has_theta:
        if is_binedges:
            if len(binedges) is not len(theta) + 1:
                raise ValueError('Number bin_edges must be number of Bincounts + 1')

        for x in range(len(theta)):
            classes.append([])
            if theta[x] == 0:
                classes[x].append(None)
                continue
            for y in range(theta[x]):
                classes[x].append(y)
        num_bins = len(theta)
        width = 2 * np.pi / num_bins

        if is_colormap:
            if not is_binedges:
                angles = np.linspace(0, np.pi * 2, num_bins + 1)

        # Philim for bincounts
        if _plt.kwargs.get('philim', None) is not None:
            binlimits = _plt.kwargs['philim']
            if binlimits[0] is None:
                binlimits = (0, binlimits[1])
            if binlimits[1] is None:
                binlimits = (binlimits[0], 2 * np.pi)

            if not is_binedges:
                binedges = np.linspace(binlimits[0], binlimits[1], num_bins + 1)
                is_binedges = True
                _plt.kwargs['temp_bin_edges'] = binedges
            else:
                binedges = [angle for angle in binedges if (binlimits[0] <= angle <= binlimits[1])]
                if len(binedges) != num_bins + 1:
                    raise ValueError('The given binedges is not compatible with philim since the number of angles,'
                                     ' which are in between the philims, does not equal len(bincounts) + 1 ')
                is_binedges = True
                _plt.kwargs['temp_bin_edges'] = binedges

    # No bin_counts
    else:

        # Number of bins
        if _plt.kwargs.get('num_bins', None) is not None:
            num_bins = _plt.kwargs['num_bins']
            if num_bins < 1:
                raise ValueError('Number of num_bins must be 1 or larger')
        else:
            # Auto generated num_bins
            num_bins = min(int(len(theta) / 2 - 1), 200)
            if is_binedges:
                num_bins = len(binedges) - 1

        start = 0

        # Bin Width --> will overwrite the number of bins but it will not exceed 200

        if _plt.kwargs.get('bin_width') is not None:
            width = _plt.kwargs['bin_width']
            if not width < np.pi * 2 or not width > 0:
                raise ValueError('bin_width not correct! Must be between 0 and 2*pi')
            num_bins = int(2 * np.pi / width)
            if num_bins > 200:
                num_bins = 200
                width = 2 * np.pi / num_bins
        else:
            width = 2 * np.pi / num_bins

        # Philim
        if _plt.kwargs.get('philim', None) is not None:
            is_binlimits = True
            binlimits = _plt.kwargs['philim']
            if binlimits[0] is None:
                binlimits = (0, binlimits[1])
            if binlimits[1] is None:
                binlimits = (binlimits[0], 2 * np.pi)

            if not is_binedges:
                if _plt.kwargs.get('num_bins', None) is None:
                    num_bins = max(int(num_bins * (binlimits[1] - binlimits[0]) / (np.pi * 2)), 3)

                binedges = np.linspace(binlimits[0], binlimits[1], num_bins + 1)
                is_binedges = True
                _plt.kwargs['temp_bin_edges'] = binedges
            else:
                binedges = [angle for angle in binedges if (binlimits[0] <= angle <= binlimits[1])]
                is_binedges = True
                _plt.kwargs['temp_bin_edges'] = binedges
                num_bins = len(binedges) - 1
        else:
            is_binlimits = False

        # grouping the data from given theta
        if is_binedges:
            for x in range(len(binedges)):
                start = binedges[x]
                classes.append([])
                for y in range(len(theta)):
                    try:
                        if start < theta[y] <= binedges[x + 1]:

                            if is_binlimits:
                                if binlimits[0] <= theta[y] <= binlimits[1]:
                                    classes[x].append(theta[y])
                            else:
                                classes[x].append(theta[y])
                    except Exception:
                        pass
                if len(classes[x]) == 0:
                    classes[x].append(None)
        # no Binedges
        else:
            # Optional Bin Limits
            if is_binlimits:
                theta = [angle for angle in theta if binlimits[0] <= angle <= binlimits[1]]
            interval = 2 * np.pi / num_bins
            for x in range(num_bins):
                classes.append([])
                for y in range(len(theta)):
                    if start <= theta[y] < (start + interval):
                        classes[x].append(theta[y])

                if is_colormap:
                    # angles list for colormap
                    angles.append([start, start + interval])
                if len(classes[x]) == 0:
                    classes[x].append(None)
                start += interval

    _plt.kwargs['classes'] = classes

    # calc total
    total = 0
    for temp in classes:
        total += len(temp) - temp.count(None)

    if is_binedges:
        if normalization == 'pdf':
            norm_factor = total
        elif normalization == 'countdensity':
            norm_factor = 1
        binwidths = []

        classes = [temp for temp in classes if len(temp) > 0]
        for i in range(len(binedges) - 1):
            binwidths.append(binedges[i + 1] - binedges[i])
        binwidths.append(binedges[-1] - binedges[-2])
        if normalization == 'countdensity' or normalization == 'pdf':
            bin_value = [len(x) / (norm_factor * binwidths[i]) for (i, x) in enumerate(classes)]

    exp = 0
    if normalization == 'probability' or normalization == 'pdf':
        if normalization == 'probability':
            maximum = find_max(classes, normalization) / total
        elif normalization == 'pdf':
            if is_binedges:
                maximum = max(bin_value)
            else:
                maximum = find_max(classes, normalization) / (total * width)
        exp = round(np.log10(maximum) + 0.5)
        border = round((maximum * (10 ** (abs(exp) + 1))) / (10 ** (round(abs(exp) + 1))))
        while border < maximum or border * 10 ** (abs(exp) + 2) % 4 != 0:
            border += 10 ** (exp - 1)

    elif normalization == 'cdf':
        border = 1

    else:
        # interval for x-Axis
        if is_binedges:
            if normalization == 'countdensity':
                maximum = round(max(bin_value) + 0.49)
            else:
                maximum = int(find_max(classes, normalization))
        else:
            if normalization == 'countdensity':
                maximum = int(find_max(classes, normalization) / width)
            else:
                maximum = int(find_max(classes, normalization))

        border = maximum
        outer = True
        e = 1

        while True and outer:
            if border <= 40:
                while border % 4 != 0:
                    border += 1
                break
            else:
                for x in range(9):
                    border += x * 10 ** (e - 1)
                    if border % 4 == 0:
                        outer = False
                        break
                e += 1

    # calc colormap image
    if normalization == 'probability':
        norm_factor = total
    elif normalization == 'countdensity':
        norm_factor = width
    elif normalization == 'pdf':
        norm_factor = total * width
    elif normalization == 'cdf':
        norm_factor = total
    elif normalization == 'count':
        norm_factor = 1
    elif normalization == 'cumcount':
        norm_factor = 1
    else:
        raise ValueError("Incorrect normalization Value")

    _plt.kwargs['norm_factor'] = norm_factor
    if is_colormap:

        # r_lim
        if _plt.kwargs.get('rlim', None) is not None:
            if not has_theta:
                pass
            r_lim = _plt.kwargs['rlim']
            if r_lim[0] is None:
                r_lim = (0, r_lim[1])
            if r_lim[1] is None:
                r_lim = (r_lim[0], 1)
        else:
            r_lim = (0, 1)

        height = 2000
        width = height
        center = width / 2
        cumulative = []
        length = 0

        max_radius = center * 0.8
        r_min = r_lim[0] * max_radius
        r_max = r_lim[1] * max_radius
        del max_radius

        if normalization == 'cumcount' or normalization == 'cdf':
            for temp in classes:
                if temp[0] is None:
                    if len(cumulative) > 0:
                        cumulative.append(cumulative[-1])
                    else:
                        cumulative.append(0)
                else:
                    length += len(temp) / norm_factor / border * 0.8 * center
                    cumulative.append(length)

        factor_angle_b = len(colormap[0]) / (2 * np.pi)
        Y, X = np.ogrid[:height, :width]
        radiusc = np.sqrt((X - center) ** 2 + (Y - center) ** 2)
        angle_c = np.arctan2(Y - center, X - center)
        angle_c[angle_c < 0] += 2 * np.pi
        angle_b = angle_c * factor_angle_b
        factor_radiusb2 = (len(colormap) - 1) / (center * 2 ** (1 / 2))
        radiusb2 = radiusc * factor_radiusb2
        colormap = np.array(colormap)
        lineardata = colormap[radiusb2.astype(np.int), angle_b.astype(np.int)].flatten()

        if is_binedges:
            if normalization == 'pdf':
                norm_factor = total
            if normalization == 'countdensity':
                norm_factor = 1
            binwidths = []
            for i in range(len(classes)):
                if len(classes[i]) < 1:
                    classes.pop(i)
            for i in range(len(binedges) - 1):
                binwidths.append(binedges[i + 1] - binedges[i])
            binwidths.append(binedges[-1] - binedges[-2])

            if normalization == 'countdensity' or normalization == 'pdf':
                bin_value = np.array(
                    [len(x) / (norm_factor * binwidths[i]) / border * 0.8 * center if x[0] is not None else 0
                     for (i, x) in enumerate(classes)])
            else:
                bin_value = np.array([len(x) / norm_factor / border * 0.8 * center if x[0] is not None else 0
                                      for x in classes])
        # no bin_edges
        else:
            bin_value = np.array([len(x) / norm_factor / border * 0.8 * center if x[0] is not None else 0
                                  for x in classes])

        if not is_binedges:
            if normalization == 'cdf' or normalization == 'cumcount':
                boolmap = np.zeros((height, width))
                for (angle1, angle2), radius in zip(angles, cumulative):
                    tempmap = angle1 <= angle_c
                    tempmap = np.logical_and(angle_c <= angle2, tempmap)
                    tempmap = np.logical_and(radiusc <= radius, tempmap)
                    tempmap = np.logical_and(radiusc <= r_max, tempmap)
                    tempmap = np.logical_and(r_min <= radiusc, tempmap)
                    boolmap = np.logical_or(tempmap, boolmap)

            else:
                boolmap = np.zeros((height, width))
                for (angle1, angle2), radius in zip(angles, bin_value):
                    tempmap = angle1 <= angle_c
                    tempmap = np.logical_and(angle_c <= angle2, tempmap)
                    tempmap = np.logical_and(radiusc <= radius, tempmap)
                    tempmap = np.logical_and(radiusc <= r_max, tempmap)
                    tempmap = np.logical_and(r_min <= radiusc, tempmap)
                    boolmap = np.logical_or(tempmap, boolmap)

        # Binedges
        else:
            angles = []
            for i in range(len(binedges) - 1):
                angles.append([])
                angles[i].append(binedges[i])
                angles[i].append(binedges[i + 1])

            if normalization == 'cdf' or normalization == 'cumcount':

                boolmap = np.zeros((height, width))
                for (angle1, angle2), radius in zip(angles, cumulative):
                    tempmap = angle1 <= angle_c
                    tempmap = np.logical_and(angle_c <= angle2, tempmap)
                    tempmap = np.logical_and(radiusc <= radius, tempmap)
                    tempmap = np.logical_and(radiusc <= r_max, tempmap)
                    tempmap = np.logical_and(r_min <= radiusc, tempmap)
                    boolmap = np.logical_or(tempmap, boolmap)

            else:

                boolmap = np.zeros((height, width))
                for (angle1, angle2), radius in zip(angles, bin_value):
                    tempmap = angle1 <= angle_c
                    tempmap = np.logical_and(angle_c <= angle2, tempmap)
                    tempmap = np.logical_and(radiusc <= radius, tempmap)
                    tempmap = np.logical_and(radiusc <= r_max, tempmap)
                    tempmap = np.logical_and(r_min <= radiusc, tempmap)
                    boolmap = np.logical_or(tempmap, boolmap)

        lineardata[np.logical_not(boolmap.flatten())] = 0
        _plt.kwargs['temp_colormap'] = (height, width, lineardata)

    _plt.kwargs['border_exp'] = (border, exp)

    if is_binedges:
        if _plt.kwargs['normalization'] == 'pdf':
            _plt.kwargs['norm_factor'] = total

    plt = _plot_data(kind='polar_histogram')
    _plt.kwargs['ax'] = saved_ax
    del saved_ax

    return plt


@_close_gks_on_error
def plot3(*args, **kwargs):
    """
    Draw one or more three-dimensional line plots.

    :param x: the x coordinates to plot
    :param y: the y coordinates to plot
    :param z: the z coordinates to plot

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(0, 30, 1000)
    >>> y = np.cos(x) * x
    >>> z = np.sin(x) * x
    >>> # Plot the points
    >>> mlab.plot3(x, y, z)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyac')
    return _plot_data(kind='plot3')


@_close_gks_on_error
def scatter3(x, y, z, c=None, *args, **kwargs):
    """
    Draw one or more three-dimensional scatter plots.

    Additional to x, y and z values, you can provide values for the markers'
    color. Color values will be used in combination with the current colormap.

    :param x: the x coordinates to plot
    :param y: the y coordinates to plot
    :param z: the z coordinates to plot
    :param c: the optional color values to plot

    **Usage examples:**

    >>> # Create example data
    >>> x = np.random.uniform(-1, 1, 100)
    >>> y = np.random.uniform(-1, 1, 100)
    >>> z = np.random.uniform(-1, 1, 100)
    >>> c = np.random.uniform(1, 1000, 100)
    >>> # Plot the points
    >>> mlab.scatter3(x, y, z)
    >>> # Plot the points with colors
    >>> mlab.scatter3(x, y, z, c)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    args = [x, y, z] + list(args)
    if c is not None:
        args.append(c)
    _plt.args = _plot_args(args, fmt='xyac')
    return _plot_data(kind='scatter3')


@_close_gks_on_error
def isosurface(v, **kwargs):
    """
    Draw an isosurface.

    This function can draw an isosurface from a three-dimensional numpy array.
    Values greater than the isovalue will be seen as outside the isosurface,
    while values less than the isovalue will be seen as inside the isosurface.

    :param v: the volume data
    :param isovalue: the isovalue

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-1, 1, 40)[:, np.newaxis, np.newaxis]
    >>> y = np.linspace(-1, 1, 40)[np.newaxis, :, np.newaxis]
    >>> z = np.linspace(-1, 1, 40)[np.newaxis, np.newaxis, :]
    >>> v = 1-(x**2 + y**2 + z**2)**0.5
    >>> # Draw the isosurace.
    >>> mlab.isosurface(v, isovalue=0.2)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = [(None, None, v, None, '')]
    return _plot_data(kind='isosurface')


@_close_gks_on_error
def volume(v, **kwargs):
    """
    Draw a volume.

    This function can draw a three-dimensional numpy array using volume rendering.
    The volume data is reduced to a two-dimensional image using an emission or
    absorption model or by a maximum intensity projection. After the projection
    the current colormap is applied to the result.

    :param v: the volume data
    :param algorithm: the algorithm used to reduce the volume data.
                      Available algorithms are "maximum", "emission" and "absorption".
    :param dmin: the minimum data value when applying the colormap
    :param dmax: the maximum data value when applying the colormap

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-1, 1, 40)[:, np.newaxis, np.newaxis]
    >>> y = np.linspace(-1, 1, 40)[np.newaxis, :, np.newaxis]
    >>> z = np.linspace(-1, 1, 40)[np.newaxis, np.newaxis, :]
    >>> v = 1 - (x**2 + y**2 + z**2)**0.5 - np.random.uniform(0, 0.25, (40, 40, 40))
    >>> # Draw the 3d volume data
    >>> mlab.volume(v)
    >>> # Draw the 3d volume data using an emission model
    >>> mlab.volume(v, algorithm='emission', dmin=0.1, dmax=0.4)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    nz, ny, nx = v.shape
    _plt.args = [(np.arange(nx + 1), np.arange(nz + 1), np.arange(ny + 1), v, '')]
    return _plot_data(kind='volume')


@_close_gks_on_error
def imshow(image, **kwargs):
    """
    Draw an image.

    This function can draw an image either from reading a file or using a
    two-dimensional array and the current colormap.

    :param image: an image file name or two-dimensional array

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = np.linspace(0, np.pi, 20)
    >>> z = np.sin(x[np.newaxis, :]) + np.cos(y[:, np.newaxis])
    >>> # Draw an image from a 2d array
    >>> mlab.imshow(z)
    >>> # Draw an image from a file
    >>> mlab.imshow("example.png")
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = [(None, None, image, None, "")]
    return _plot_data(kind='imshow')


@_close_gks_on_error
def size(*size):
    """
    Set the size of the output window.

    The size can be passed in several formats, allowing both pixel sizes and
    metric sizes, as well as mixes of those. If nothing is passed to this
    function, the default of 600 by 450 pixels is restored.

    :param size: aseries of values or a tuple containing:
        - two numbers (width and height as pixels), or
        - two strings (width and height as another unit), or
        - two numbers and a string (width, height and their unit), or
        - a number, a string, another number and another string (width and
            height, along with their units)

    **Usage examples:**

    >>> # Set the size to 640 by 480 pixels
    >>> mlab.size(600, 450)
    >>> # Set the size to 640 by 480 pixels using a tuple
    >>> mlab.size((600, 450))
    >>> # Reset size to its default of 600 by 450 pixels
    >>> mlab.size()
    >>> # Set the size to 6 centimeters by 200 pixels
    >>> mlab.size("6cm", 200)
    >>> # Set the size to 120 millimeters by 9 centimeters
    >>> mlab.size("120mm", "9cm")
    >>> # Set the size to 4 by 3 inches
    >>> mlab.size(4, 3, "in")
    >>> # Set the size to 0.5 feet by 0.1 meters
    >>> mlab.size(0.5, "ft", 0.1, "m")
    """
    if len(size) == 1 and hasattr(size[0], '__getitem__'):
        size = size[0]
    if len(size) == 0:
        size = (600, 450)
    return _plot_data(size=size)


@_close_gks_on_error
def title(title=""):
    """
    Set the plot title.

    The plot title is drawn using the extended text function
    :py:func:`gr.textext`. You can use a subset of LaTeX math syntax, but will
    need to escape certain characters, e.g. parentheses. For more information
    see the documentation of :py:func:`gr.textext`.

    :param title: the plot title

    **Usage examples:**

    >>> # Set the plot title to "Example Plot"
    >>> mlab.title("Example Plot")
    >>> # Clear the plot title
    >>> mlab.title()
    """
    return _plot_data(title=title)


@_close_gks_on_error
def xlabel(x_label=""):
    """
    Set the x-axis label.

    The axis labels are drawn using the extended text function
    :py:func:`gr.textext`. You can use a subset of LaTeX math syntax, but will
    need to escape certain characters, e.g. parentheses. For more information
    see the documentation of :py:func:`gr.textext`.

    :param x_label: the x-axis label

    **Usage examples:**

    >>> # Set the x-axis label to "x"
    >>> mlab.xlabel("x")
    >>> # Clear the x-axis label
    >>> mlab.xlabel()
    """
    return _plot_data(xlabel=x_label)


@_close_gks_on_error
def ylabel(y_label=""):
    r"""
    Set the y-axis label.

    The axis labels are drawn using the extended text function
    :py:func:`gr.textext`. You can use a subset of LaTeX math syntax, but will
    need to escape certain characters, e.g. parentheses. For more information
    see the documentation of :py:func:`gr.textext`.

    :param y_label: the y-axis label

    **Usage examples:**

    >>> # Set the y-axis label to "y\(x\)"
    >>> mlab.ylabel("y\(x\)")
    >>> # Clear the y-axis label
    >>> mlab.ylabel()
    """
    return _plot_data(ylabel=y_label)


@_close_gks_on_error
def zlabel(z_label=""):
    r"""
    Set the z-axis label.

    The axis labels are drawn using the extended text function
    :py:func:`gr.textext`. You can use a subset of LaTeX math syntax, but will
    need to escape certain characters, e.g. parentheses. For more information
    see the documentation of :py:func:`gr.textext`.

    :param z_label: the z-axis label

    **Usage examples:**

    >>> # Set the z-axis label to "z(x, y)"
    >>> mlab.zlabel("z\(x, y\)")
    >>> # Clear the z-axis label
    >>> mlab.zlabel()
    """
    return _plot_data(zlabel=z_label)


@_close_gks_on_error
def dlabel(d_label=""):
    r"""
    Set the volume intensity label.

    This label is drawn using the extended text function
    :py:func:`gr.textext`. You can use a subset of LaTeX math syntax, but will
    need to escape certain characters, e.g. parentheses. For more information
    see the documentation of :py:func:`gr.textext`.

    :param d_label: the volume intensity label

    **Usage examples:**

    >>> # Set the volume intensity label to "Intensity"
    >>> mlab.dlabel("Intensity")
    >>> # Clear the volume intensity label
    >>> mlab.dlabel()
    """
    return _plot_data(dlabel=d_label)


@_close_gks_on_error
def xlim(x_min=None, x_max=None, adjust=True):
    """
    Set the limits for the x-axis.

    The x-axis limits can either be passed as individual arguments or as a
    tuple of (**x_min**, **x_max**). Setting either limit to **None** will
    cause it to be automatically determined based on the data, which is the
    default behavior.

    :param x_min:
        - the x-axis lower limit, or
        - **None** to use an automatic lower limit, or
        - a tuple of both x-axis limits
    :param x_max:
        - the x-axis upper limit, or
        - **None** to use an automatic upper limit, or
        - **None** if both x-axis limits were passed as first argument
    :param adjust: whether or not the limits may be adjusted

    **Usage examples:**

    >>> # Set the x-axis limits to -1 and 1
    >>> mlab.xlim(-1, 1)
    >>> # Set the x-axis limits to -1 and 1 using a tuple
    >>> mlab.xlim((-1, 1))
    >>> # Reset the x-axis limits to be determined automatically
    >>> mlab.xlim()
    >>> # Reset the x-axis upper limit and set the lower limit to 0
    >>> mlab.xlim(0, None)
    >>> # Reset the x-axis lower limit and set the upper limit to 1
    >>> mlab.xlim(None, 1)
    """
    if x_max is None and x_min is not None:
        try:
            x_min, x_max = x_min
        except TypeError:
            pass
    return _plot_data(xlim=(x_min, x_max), adjust_xlim=adjust)


@_close_gks_on_error
def ylim(y_min=None, y_max=None, adjust=True):
    """
    Set the limits for the y-axis.

    The y-axis limits can either be passed as individual arguments or as a
    tuple of (**y_min**, **y_max**). Setting either limit to **None** will
    cause it to be automatically determined based on the data, which is the
    default behavior.

    :param y_min:
        - the y-axis lower limit, or
        - **None** to use an automatic lower limit, or
        - a tuple of both y-axis limits
    :param y_max:
        - the y-axis upper limit, or
        - **None** to use an automatic upper limit, or
        - **None** if both y-axis limits were passed as first argument
    :param adjust: whether or not the limits may be adjusted

    **Usage examples:**

    >>> # Set the y-axis limits to -1 and 1
    >>> mlab.ylim(-1, 1)
    >>> # Set the y-axis limits to -1 and 1 using a tuple
    >>> mlab.ylim((-1, 1))
    >>> # Reset the y-axis limits to be determined automatically
    >>> mlab.ylim()
    >>> # Reset the y-axis upper limit and set the lower limit to 0
    >>> mlab.ylim(0, None)
    >>> # Reset the y-axis lower limit and set the upper limit to 1
    >>> mlab.ylim(None, 1)
    """
    if y_max is None and y_min is not None:
        try:
            y_min, y_max = y_min
        except TypeError:
            pass
    return _plot_data(ylim=(y_min, y_max), adjust_ylim=adjust)


@_close_gks_on_error
def zlim(z_min=None, z_max=None, adjust=True):
    """
    Set the limits for the z-axis.

    The z-axis limits can either be passed as individual arguments or as a
    tuple of (**z_min**, **z_max**). Setting either limit to **None** will
    cause it to be automatically determined based on the data, which is the
    default behavior.

    :param z_min:
        - the z-axis lower limit, or
        - **None** to use an automatic lower limit, or
        - a tuple of both z-axis limits
    :param z_max:
        - the z-axis upper limit, or
        - **None** to use an automatic upper limit, or
        - **None** if both z-axis limits were passed as first argument
    :param adjust: whether or not the limits may be adjusted

    **Usage examples:**

    >>> # Set the z-axis limits to -1 and 1
    >>> mlab.zlim(-1, 1)
    >>> # Set the z-axis limits to -1 and 1 using a tuple
    >>> mlab.zlim((-1, 1))
    >>> # Reset the z-axis limits to be determined automatically
    >>> mlab.zlim()
    >>> # Reset the z-axis upper limit and set the lower limit to 0
    >>> mlab.zlim(0, None)
    >>> # Reset the z-axis lower limit and set the upper limit to 1
    >>> mlab.zlim(None, 1)
    """
    if z_max is None and z_min is not None:
        try:
            z_min, z_max = z_min
        except TypeError:
            pass
    return _plot_data(zlim=(z_min, z_max), adjust_zlim=adjust)


@_close_gks_on_error
def rlim(r_min=None, r_max=None, adjust=True):
    """
    Set the limits for the radii in polar plots.

    The inner and outer radius can either be passed as individual arguments
    or as a tuple of (**r_min**, **r_max**). Setting either limit to **None**
    will cause it to be automatically determined based on the data, which is the
    default behavior. **r_min** and **r_max** must both be greater or equal 0.

    :param r_min:
        - the inner radius, or
        - **None** to use an automatic inner radius, or
        - a tuple of both radii
    :param r_max:
        - the outer radius, or
        - **None** to use an automatic outer radius, or
        - **None** if both radii were passed as first argument
    :param adjust: whether or not the radii may be adjusted

    **Usage examples:**

    >>> # Set the radii in polar plots to 0 and 1
    >>> mlab.rlim(0, 1)
    >>> # Set the radii in polar plots to 0 and 1 using a tuple
    >>> mlab.rlim((0, 1))
    >>> # Reset the radii to be determined automatically
    >>> mlab.rlim()
    >>> # Reset the outer radius and set the inner radius to 0
    >>> mlab.rlim(0, None)
    >>> # Reset the inner radius and set the outer radius to 1
    >>> mlab.rlim(None, 1)
    """
    if r_max is None and r_min is not None:
        try:
            r_min, r_max = r_min
        except TypeError:
            pass
    return _plot_data(rlim=(r_min, r_max), adjust_rlim=adjust)


@_close_gks_on_error
def philim(phi_min=None, phi_max=None, adjust=True):
    """
    Set the start and end angle for polar plots in radians.

    The angles can either be passed as individual arguments or as a tuple
    of (**phi_min**, **phi_max**). Setting either angle to **None** will
    cause it to be automatically determined based on the data, which is the
    default behavior.

    :param phi_min:
        - the start angle in radians, or
        - **None** to use an automatic start angle, or
        - a tuple of both angles
    :param phi_max:
        - the end angle in radians, or
        - **None** to use an automatic end angle, or
        - **None** if both angles were passed as first argument
    :param adjust: whether or not the angles may be adjusted

    **Usage examples:**

    >>> # Set the angle limits to 0 and 2 Pi
    >>> mlab.philim(0, 2*np.pi)
    >>> # Set the angle limits to 0 and 2 Pi using a tuple
    >>> mlab.philim((0, 2*np.pi))
    >>> # Reset the angle limits to be determined automatically
    >>> mlab.philim()
    >>> # Reset the end angle and set the start angle to 0
    >>> mlab.philim(0, None)
    >>> # Reset the start angle and set end angle to 2 Pi
    >>> mlab.philim(None, 2*np.pi)
    """
    if phi_max is None and phi_min is not None:
        try:
            phi_min, phi_max = phi_min
        except TypeError:
            pass
    return _plot_data(philim=(phi_min, phi_max), adjust_philim=adjust)


@_close_gks_on_error
def xlog(xlog=True):
    """
    Enable or disable a logarithmic scale for the x-axis.

    :param xlog: whether or not the x-axis should be logarithmic

    **Usage examples:**

    >>> # Enable a logarithic x-axis
    >>> mlab.xlog()
    >>> # Disable it again
    >>> mlab.xlog(False)
    """
    return _plot_data(xlog=xlog)


@_close_gks_on_error
def ylog(ylog=True):
    """
    Enable or disable a logarithmic scale for the y-axis.

    :param ylog: whether or not the y-axis should be logarithmic

    **Usage examples:**

    >>> # Enable a logarithic y-axis
    >>> mlab.ylog()
    >>> # Disable it again
    >>> mlab.ylog(False)
    """
    return _plot_data(ylog=ylog)


@_close_gks_on_error
def zlog(zlog=True):
    """
    Enable or disable a logarithmic scale for the z-axis.

    :param zlog: whether or not the z-axis should be logarithmic

    **Usage examples:**

    >>> # Enable a logarithic z-axis
    >>> mlab.zlog()
    >>> # Disable it again
    >>> mlab.zlog(False)
    """
    return _plot_data(zlog=zlog)


@_close_gks_on_error
def xflip(xflip=True):
    """
    Enable or disable x-axis flipping/reversal.

    :param xflip: whether or not the x-axis should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the x-axis
    >>> mlab.xflip()
    >>> # Restores the x-axis
    >>> mlab.xflip(False)
    """
    return _plot_data(xflip=xflip)


@_close_gks_on_error
def yflip(yflip=True):
    """
    Enable or disable y-axis flipping/reversal.

    :param yflip: whether or not the y-axis should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the y-axis
    >>> mlab.yflip()
    >>> # Restores the y-axis
    >>> mlab.yflip(False)
    """
    return _plot_data(yflip=yflip)


@_close_gks_on_error
def zflip(zflip=True):
    """
    Enable or disable z-axis flipping/reversal.

    :param zflip: whether or not the z-axis should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the z-axis
    >>> mlab.zflip()
    >>> # Restores the z-axis
    >>> mlab.zflip(False)
    """
    return _plot_data(zflip=zflip)


@_close_gks_on_error
def rflip(rflip=True):
    """
    Enable or disable flipping/reversal of the radius.

    :param rflip: whether or not the inner and outer radius should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the inner and outer radius
    >>> mlab.rflip()
    >>> # Restores the radius
    >>> mlab.rflip(False)
    """
    return _plot_data(rflip=rflip)


@_close_gks_on_error
def phiflip(phiflip=True):
    """
    Enable or disable flipping/reversal of the polar angles.

    :param zflip: whether or not the start and end angle should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the start and end angle
    >>> mlab.phiflip()
    >>> # Restores the angles
    >>> mlab.phiflip(False)
    """
    return _plot_data(phiflip=phiflip)


@_close_gks_on_error
def colormap(colormap=''):
    """
    Get or set the colormap for the current plot or enable manual colormap control.

    :param colormap:
        - The name of a gr colormap
        - One of the gr colormap constants (**gr.COLORMAP_...**)
        - A list of red-green-blue tuples as colormap
        - A dict mapping a normalized position to the corresponding red-green-blue tuple
        - **None**, if the colormap should use the current colors set by
          :py:func:`gr.setcolorrep`
        - No parameter or an empty string (default) to get the colormap as a
          list of red-green-blue tuples

    **Usage examples:**

    >>> # Use one of the built-in colormap names
    >>> mlab.colormap('viridis')
    >>> # Use one of the built-in colormap constants
    >>> mlab.colormap(gr.COLORMAP_BWR)
    >>> # Use a list of red-green-blue tuples as colormap
    >>> mlab.colormap([(0, 0, 1), (1, 1, 1), (1, 0, 0)])
    >>> # Use a dict mapping a normalized position to the corresponding red-green-blue tuple as colormap
    >>> mlab.colormap({0.0: (0, 0, 1), 0.25: (1, 1, 1), 1.0: (1, 0, 0)})
    >>> # Use a custom colormap using gr.setcolorrep directly
    >>> for i in range(256):
    ...     gr.setcolorrep(1.0-i/255.0, 1.0, i/255.0)
    ...
    >>> mlab.colormap(None)
    >>> # Get the current colormap as list of red-green-blue tuples
    >>> colormap = mlab.colormap()
    """
    if colormap == '':
        _set_colormap()
        return [(c[0], c[1], c[2]) for c in _colormap()]
    return _plot_data(colormap=colormap)


@_close_gks_on_error
def field_of_view(field_of_view):
    """
    Set the vertical field of view of the current 3D plot.

    Depending on how the field of view is set, a different projection will be
    used for 3D plots. Setting field of view to a value between 0 and 180
    degrees (exclusively) will use a perspective projection with the given
    vertical field of view. Setting field of view to 0 or NaN will use an
    orthographic projection and setting Field of view to None will use a
    custom projection with limited camera positioning.

    By default, a field of view set to None will be assumed.

    :param field_of_view: the vertical field of view or None

    **Usage examples:**

    >>> # Create example data
    >>> x = np.random.uniform(0, 1, 100)
    >>> y = np.random.uniform(0, 1, 100)
    >>> z = np.random.uniform(0, 1, 100)
    >>> # Set the field of view to 20 degrees and draw an example plot
    >>> mlab.field_of_view(20)
    >>> mlab.plot3(x, y, z)
    >>> # Select an orthographic projection instead
    >>> mlab.field_of_view(0)
    >>> mlab.plot3(x, y, z)
    >>> # Restore the default projection
    >>> mlab.field_of_view(None)
    >>> mlab.plot3(x, y, z)
    """
    return _plot_data(field_of_view=field_of_view)


@_close_gks_on_error
def tilt(tilt):
    """
    Set the 3d axis tilt of the current plot.

    How the tilt is interpreted depends on the current field_of_view setting.
    For the default projection, with field_of_view set to None, the tilt can
    be any value between 0 and 90, and controls the angle between the viewer
    and the X-Y-plane. For the orthographic or perspective projection, with
    field_of_view set to a value between 0 and 180 or to NaN, the tilt can
    be any value between 0 and 180 and controls the angle between the viewer
    and the z-axis.

    :param tilt: the 3d axis tilt

    **Usage examples:**

    >>> # Create example data
    >>> x = np.random.uniform(0, 1, 100)
    >>> y = np.random.uniform(0, 1, 100)
    >>> z = np.random.uniform(0, 1, 100)
    >>> # Set the tilt and draw an example plot
    >>> mlab.tilt(45)
    >>> mlab.plot3(x, y, z)
    """
    return _plot_data(tilt=tilt)


@_close_gks_on_error
def rotation(rotation):
    """
    Set the 3d axis rotation of the current plot.

    The rotation controls the angle between the viewer projected onto the
    X-Y-plane and the x-axis, setting the camera position for 3D plots in
    combination with the tilt setting.

    The range of values for the rotation depends on the current field_of_view
    setting. For the default projection, with field_of_view set to None, the
    rotation can be any value between 0 and 90 degrees. For the orthographic
    or perspective projection, with field_of_view set to a value between 0 and
    180 or to NaN, the rotation can be any value between 0 and 360 degrees.

    :param rotation: the 3d axis rotation

    **Usage examples:**

    >>> # Create example data
    >>> x = np.random.uniform(0, 1, 100)
    >>> y = np.random.uniform(0, 1, 100)
    >>> z = np.random.uniform(0, 1, 100)
    >>> # Set the rotation and draw an example plot
    >>> mlab.rotation(45)
    >>> mlab.plot3(x, y, z)
    """
    return _plot_data(rotation=rotation)


@_close_gks_on_error
def legend(*labels, **kwargs):
    r"""
    Set the labels and location for the legend of the current plot.

    The labels for the legend are drawn using the extended text function
    :py:func:`gr.textext`. You can use a subset of LaTeX math syntax, but will
    need to escape certain characters, e.g. parentheses. For more information
    see the documentation of :py:func:`gr.textext`.

    :param labels: the labels for each graph in the current plot
    :param location: the location of the legend (from 1 to 10)

    **Usage examples:**

    >>> # Set the labels for the two graphs "f(x)" and "g(x)"
    >>> mlab.legend("f\(x\)", "g\(x\)")
    >>> # Set the labels and draws the legend in the lower right corner
    >>> mlab.legend("f\(x\)", "g\(x\)", location=4)
    >>> # Resets the legend
    >>> mlab.legend()
    """
    if not all(isinstance(label, basestring) for label in labels):
        raise TypeError('list of strings expected')
    return _plot_data(labels=labels, **kwargs)


@_close_gks_on_error
def savefig(filename):
    """
    Save the current figure to a file.

    This function draw the current figure using one of GR's workstation types
    to create a file of the given name. Which file types are supported depends
    on the installed workstation types, but GR usually is built with support
    for .png, .jpg, .pdf, .ps, .gif and various other file formats.

    :param filename: the filename the figure should be saved to

    **Usage examples:**

    >>> # Create a simple plot
    >>> mlab.plot(range(100), lambda x: 1/(x+1))
    >>> # Save the figure to a file
    >>> mlab.savefig("example.png")
    """
    gr.beginprint(filename)
    _plot_data()
    gr.endprint()


@_close_gks_on_error
def figure(**kwargs):
    """
    Create a new figure with the given settings.

    Settings like the current colormap, title or axis limits as stored in the
    current figure. This function creates a new figure, restores the default
    settings and applies any settings passed to the function as keyword
    arguments.

    **Usage examples:**

    >>> # Restore all default settings
    >>> mlab.figure()
    >>> # Restore all default settings and set the title
    >>> mlab.figure(title="Example Figure")
    """
    global _plt
    _plt = _Figure()
    _plt.kwargs.update(kwargs)
    return _plt


@_close_gks_on_error
def hold(flag):
    """
    Set the hold flag for combining multiple plots.

    The hold flag prevents drawing of axes and clearing of previous plots, so
    that the next plot will be drawn on top of the previous one.

    :param flag: the value of the hold flag

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(0, 1, 100)
    >>> # Draw the first plot
    >>> mlab.plot(x, lambda x: x**2)
    >>> # Set the hold flag
    >>> mlab.hold(True)
    >>> # Draw additional plots
    >>> mlab.plot(x, lambda x: x**4)
    >>> mlab.plot(x, lambda x: x**8)
    >>> # Reset the hold flag
    >>> mlab.hold(False)
    """
    global _plt
    _plt.kwargs['ax'] = flag
    _plt.kwargs['clear'] = not flag


@_close_gks_on_error
def subplot(num_rows, num_columns, subplot_indices):
    """
    Set current subplot index.

    By default, the current plot will cover the whole window. To display more
    than one plot, the window can be split into a number of rows and columns,
    with the current plot covering one or more cells in the resulting grid.

    Subplot indices are one-based and start at the upper left corner, with a
    new row starting after every **num_columns** subplots.

    :param num_rows: the number of subplot rows
    :param num_columns: the number of subplot columns
    :param subplot_indices:
        - the subplot index to be used by the current plot
        - a pair of subplot indices, setting which subplots should be covered
          by the current plot

    **Usage examples:**

    >>> # Set the current plot to the second subplot in a 2x3 grid
    >>> mlab.subplot(2, 3, 2)
    >>> # Set the current plot to cover the first two rows of a 4x2 grid
    >>> mlab.subplot(4, 2, (1, 4))
    >>> # Use the full window for the current plot
    >>> mlab.subplot(1, 1, 1)
    """
    global _plt
    x_min = y_min = 1
    x_max = y_max = 0
    if isinstance(subplot_indices, int):
        subplot_indices = (subplot_indices,)
    for subplot_index in subplot_indices:
        row = num_rows - (subplot_index - 1.0) // num_columns
        column = (subplot_index - 1.0) % num_columns + 1
        x_min = min(x_min, (column - 1) / num_columns)
        x_max = max(x_max, column / num_columns)
        y_min = min(y_min, (row - 1) / num_rows)
        y_max = max(y_max, row / num_rows)
    _plt.kwargs['subplot'] = [x_min, x_max, y_min, y_max]
    _plt.kwargs['clear'] = (subplot_indices[0] == 1)
    _plt.kwargs['update'] = (subplot_indices[-1] == num_rows * num_columns)


class _Figure(object):
    def __init__(self, width=600, height=450):
        self.args = []
        self.kwargs = {
            'size': (width, height),
            'ax': False,
            'subplot': [0, 1, 0, 1],
            'clear': True,
            'update': True
        }


_plt = _Figure()


_gr3_available = None


def _gr3_is_available():
    global _gr3_available
    if _gr3_available is None:
        try:
            gr3.init()
        except gr3.GR3_Exception:
            _gr3_available = False
        else:
            _gr3_available = True
    return _gr3_available


def _colormap():
    rgba = np.ones((256, 4), np.float32)
    for color_index in range(256):
        color = gr.inqcolor(1000 + color_index)
        rgba[color_index, 0] = (color % 256) / 255.0
        rgba[color_index, 1] = ((color >> 8) % 256) / 255.0
        rgba[color_index, 2] = ((color >> 16) % 256) / 255.0
    return rgba


def _set_colormap():
    global _plt
    if 'cmap' in _plt.kwargs:
        warnings.warn('The parameter "cmap" has been replaced by "colormap". The value of "cmap" will be ignored.', stacklevel=3)
    colormap = _plt.kwargs.get('colormap', gr.COLORMAP_VIRIDIS)
    if colormap is None:
        return
    if isinstance(colormap, int):
        gr.setcolormap(colormap)
        return
    if hasattr(colormap, 'upper'):
        colormap_name = 'COLORMAP_' + colormap.upper()
        colormap = getattr(gr, colormap_name)
        gr.setcolormap(colormap)
        return
    if isinstance(colormap, dict):
        positions, colors = zip(*sorted(list(colormap.items())))
    if isinstance(colormap, tuple):

        if isinstance(colormap[0], int):
            gr.setcolormap(colormap[0])
        elif isinstance(colormap[1], int):
            gr.setcolormap(colormap[1])
        else:
            gr.setcolormap(1)
        return
    else:
        positions = None
        colors = colormap
    gr.setcolormapfromrgb(colors, positions)


def _interpret_size(size, dpi, default_size=(600, 450)):
    units = {
        'px': (1, 0),
        'in': (0, 1),
        '"': (0, 1),
        'ft': (0, 12),
        '\'': (0, 12),
        'mm': (0, 0.1 / 2.54),
        'cm': (0, 1 / 2.54),
        'dm': (0, 10 / 2.54),
        'm': (0, 100 / 2.54)
    }

    def pixels_per_unit(unit, dpi):
        return units[unit][0] + units[unit][1] * dpi

    def interpret_length(length, dpi, default_length):
        if length is None:
            return default_length
        if is_floatish(length):
            return float(length)
        if hasattr(length, 'endswith'):
            for unit in units:
                if length.endswith(unit) and is_floatish(length[:-len(unit)]):
                    length_value = float(length[:-len(unit)])
                    return length_value * pixels_per_unit(unit, dpi)
        print("Unable to interpret length '{}', falling back to default value: {} pixels".format(length, default_length), file=sys.stderr)
        return default_length

    def is_floatish(number):
        try:
            float(number)
            return True
        except ValueError:
            return False
        except TypeError:
            return False

    if len(size) == 2:
        width = interpret_length(size[0], dpi, default_size[0])
        height = interpret_length(size[1], dpi, default_size[1])
        return width, height
    if len(size) == 3 and is_floatish(size[0]) and is_floatish(size[1]) and size[2] in units:
        width_value = float(size[0])
        height_value = float(size[1])
        unit = size[2]
        width = width_value * pixels_per_unit(unit, dpi)
        height = height_value * pixels_per_unit(unit, dpi)
        return width, height
    if len(size) == 4 and is_floatish(size[0]) and size[1] in units and is_floatish(size[2]) and size[3] in units:
        width_value = float(size[0])
        unit = size[1]
        width = width_value * pixels_per_unit(unit, dpi)
        height_value = float(size[2])
        unit = size[3]
        height = height_value * pixels_per_unit(unit, dpi)
        return width, height
    print("Unable to interpret size '{}', falling back to default size: {} x {} pixels".format(repr(size), default_size[0], default_size[1]), file=sys.stderr)
    return default_size


def _set_viewport(kind, subplot):
    global _plt
    metric_width, metric_height, pixel_width, pixel_height = gr.inqdspsize()
    if 'figsize' in _plt.kwargs:
        horizontal_pixels_per_inch = pixel_width * 0.0254 / metric_width
        vertical_pixels_per_inch = pixel_height * 0.0254 / metric_height
        width = _plt.kwargs['figsize'][0] * horizontal_pixels_per_inch
        height = _plt.kwargs['figsize'][1] * vertical_pixels_per_inch
    else:
        dpi = pixel_width / metric_width * 0.0254
        width, height = _interpret_size(_plt.kwargs['size'], dpi)

    viewport = [0, 0, 0, 0]
    vp = subplot[:]
    if width > height:
        aspect_ratio = height / width
        metric_size = metric_width * width / pixel_width
        gr.setwsviewport(0, metric_size, 0, metric_size * aspect_ratio)
        gr.setwswindow(0, 1, 0, aspect_ratio)
        vp[2] *= aspect_ratio
        vp[3] *= aspect_ratio
    else:
        aspect_ratio = width / height
        metric_size = metric_height * height / pixel_height
        gr.setwsviewport(0, metric_size * aspect_ratio, 0, metric_size)
        gr.setwswindow(0, aspect_ratio, 0, 1)
        vp[0] *= aspect_ratio
        vp[1] *= aspect_ratio

    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf', 'volume'):
        if kind in ('surface', 'trisurf', 'volume'):
            extent = min(vp[1] - vp[0] - 0.1, vp[3] - vp[2])
        else:
            extent = min(vp[1] - vp[0], vp[3] - vp[2])
        vp0 = 0.5 * (vp[0] + vp[1] - extent)
        vp1 = 0.5 * (vp[0] + vp[1] + extent)
        vp2 = 0.5 * (vp[2] + vp[3] - extent)
        vp3 = 0.5 * (vp[2] + vp[3] + extent)
        vp = (vp0, vp1, vp2, vp3)

    viewport[0] = vp[0] + 0.125 * (vp[1] - vp[0])
    viewport[1] = vp[0] + 0.925 * (vp[1] - vp[0])
    viewport[2] = vp[2] + 0.125 * (vp[3] - vp[2])
    viewport[3] = vp[2] + 0.925 * (vp[3] - vp[2])

    if width > height:
        viewport[2] += (1 - (subplot[3] - subplot[2])**2) * 0.02
    colorbar = _plt.kwargs.get('colorbar', None)
    if colorbar or kind in ('contour', 'contourf', 'heatmap', 'polar_heatmap', 'hexbin', 'quiver'):
        viewport[1] -= 0.1
    gr.setviewport(*viewport)
    _plt.kwargs['viewport'] = viewport
    _plt.kwargs['vp'] = vp
    _plt.kwargs['ratio'] = aspect_ratio

    if 'backgroundcolor' in _plt.kwargs:
        gr.savestate()
        gr.selntran(0)
        gr.setfillintstyle(gr.INTSTYLE_SOLID)
        gr.setfillcolorind(_plt.kwargs['backgroundcolor'])
        if width > height:
            gr.fillrect(subplot[0], subplot[1],
                        subplot[2] * aspect_ratio, subplot[3] * aspect_ratio)
        else:
            gr.fillrect(subplot[0] * aspect_ratio, subplot[1] * aspect_ratio,
                        subplot[2], subplot[3])
        gr.selntran(1)
        gr.restorestate()

    if kind == 'polar':
        x_min, x_max, y_min, y_max = viewport
        x_center = 0.5 * (x_min + x_max)
        y_center = 0.5 * (y_min + y_max)
        r = 0.5 * min(x_max - x_min, y_max - y_min)
        gr.setviewport(x_center - r, x_center + r, y_center - r, y_center + r)


def _fix_minmax(v_min, v_max):
    if v_min == v_max:
        if v_min == 0:
            v_min -= 0.1
            v_max += 0.1
        else:
            v_min -= 0.1 * np.abs(v_min)
            v_max += 0.1 * np.abs(v_max)
    return v_min, v_max


def _minmax(kind=None):
    global _plt
    x_min = y_min = z_min = float('infinity')
    x_max = y_max = z_max = float('-infinity')
    x_step = y_step = float('-infinity')

    for x, y, z, c, spec in _plt.args:
        if x is None and kind in ('heatmap',):
            x_min = -0.5
            x_max = z.shape[1] - 0.5
        elif x is None and kind in ('polar_heatmap',):
            x_min = 0
            x_max = z.shape[0]
        else:
            x_min = min(np.nanmin(x), x_min)
            x_max = max(np.nanmax(x), x_max)
        if y is None and kind in ('heatmap',):
            y_min = -0.5
            y_max = z.shape[0] - 0.5
        elif y is None and kind in ('polar_heatmap',):
            y_min = 0
            y_max = z.shape[1]
        else:
            y_min = min(np.nanmin(y), y_min)
            y_max = max(np.nanmax(y), y_max)
        if z is not None and kind not in ('bar', ):
            z_min = min(np.nanmin(z), z_min)
            z_max = max(np.nanmax(z), z_max)
        if kind in ('quiver',):
            if len(x) > 1:
                x_step = max(np.abs(x[1:] - x[:-1]).max(), x_step)
            if len(y) > 1:
                y_step = max(np.abs(y[1:] - y[:-1]).max(), y_step)

    if kind in ('quiver',):
        if x_step is not None and x_step > 0:
            x_min -= x_step
            x_max += x_step
        if y_step is not None and y_step > 0:
            y_min -= y_step
            y_max += y_step
        # Use vector length for colormap
        x, y, u, v, spec = _plt.args[0]
        lengths_squared = u**2 + v**2
        z_min = np.sqrt(np.min(lengths_squared))
        z_max = np.sqrt(np.max(lengths_squared))
    if kind in ('bar'):
        x_min -= 1
        x_max += 1
    else:
        x_min, x_max = _fix_minmax(x_min, x_max)
    y_min, y_max = _fix_minmax(y_min, y_max)
    z_min, z_max = _fix_minmax(z_min, z_max)
    x_range = _plt.kwargs.get('xlim', (x_min, x_max))
    y_range = _plt.kwargs.get('ylim', (y_min, y_max))
    z_range = _plt.kwargs.get('zlim', (z_min, z_max))
    r_range = _plt.kwargs.get('rlim', (0, y_max))
    phi_range = _plt.kwargs.get('philim', (None, None))

    # Replace None with values determined above
    if x_range[0] is None:
        x_range = (x_min, x_range[1])
    if x_range[1] is None:
        x_range = (x_range[0], x_max)
    if y_range[0] is None:
        y_range = (y_min, y_range[1])
    if y_range[1] is None:
        y_range = (y_range[0], y_max)
    if z_range[0] is None:
        z_range = (z_min, z_range[1])
    if z_range[1] is None:
        z_range = (z_range[0], z_max)
    if r_range[0] is None:
        r_range = (0, r_range[1])
    if r_range[1] is None:
        r_range = (r_range[0], y_max)
    if phi_range[0] is None:
        phi_range = (0, phi_range[1])
    else:
        phi_range = (np.degrees(phi_range[0]), phi_range[1])
    if phi_range[1] is None:
        phi_range = (phi_range[0], 360)
    else:
        phi_range = (phi_range[0], np.degrees(phi_range[1]))

    _plt.kwargs['xrange'] = x_range
    _plt.kwargs['yrange'] = y_range
    _plt.kwargs['zrange'] = z_range
    _plt.kwargs['rrange'] = r_range
    _plt.kwargs['phirange'] = phi_range


def _set_window(kind):
    global _plt
    scale = 0
    if kind != 'polar':
        scale |= gr.OPTION_X_LOG if _plt.kwargs.get('xlog', False) else 0
        scale |= gr.OPTION_Y_LOG if _plt.kwargs.get('ylog', False) else 0
        scale |= gr.OPTION_Z_LOG if _plt.kwargs.get('zlog', False) else 0
        scale |= gr.OPTION_FLIP_X if _plt.kwargs.get('xflip', False) else 0
        scale |= gr.OPTION_FLIP_Y if _plt.kwargs.get('yflip', False) else 0
        scale |= gr.OPTION_FLIP_Z if _plt.kwargs.get('zflip', False) else 0

    _minmax(kind)
    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'polar', 'trisurf', 'volume'):
        major_count = 2
    else:
        major_count = 5

    x_min, x_max = _plt.kwargs['xrange']
    if not scale & gr.OPTION_X_LOG:
        if _plt.kwargs.get('adjust_xlim', 'xlim' not in _plt.kwargs) and kind not in ('heatmap',):
            x_min, x_max = gr.adjustlimits(x_min, x_max)
        if kind in ('bar'):
            x_tick = 1
            if 'xnotations' in _plt.kwargs:
                x_major_count = 0
            else:
                x_major_count = 1
        else:
            x_major_count = major_count
            x_tick = gr.tick(x_min, x_max) / x_major_count
    else:
        x_tick = x_major_count = 1
    if not scale & gr.OPTION_FLIP_X:
        xorg = (x_min, x_max)
    else:
        xorg = (x_max, x_min)
    _plt.kwargs['xaxis'] = x_tick, xorg, x_major_count

    y_min, y_max = _plt.kwargs['yrange']
    if kind in ('hist', 'bar') and 'ylim' not in _plt.kwargs:
        if scale & gr.OPTION_Y_LOG:
            y_min = 1
        else:
            y_min = 0
    if not scale & gr.OPTION_Y_LOG:
        if _plt.kwargs.get('adjust_ylim', 'ylim' not in _plt.kwargs) and kind not in ('heatmap',):
            y_min, y_max = gr.adjustlimits(y_min, y_max)
        y_major_count = major_count
        y_tick = gr.tick(y_min, y_max) / y_major_count
    else:
        y_tick = y_major_count = 1
    if not scale & gr.OPTION_FLIP_Y:
        yorg = (y_min, y_max)
    else:
        yorg = (y_max, y_min)
    _plt.kwargs['yaxis'] = y_tick, yorg, y_major_count

    _plt.kwargs['window'] = (x_min, x_max, y_min, y_max)
    if kind in ('polar', 'polar_heatmap'):
        phi_min, phi_max = _phase_wrapped_philim(adjust=_plt.kwargs.get('adjust_philim', True))
        r_min, r_max = _plt.kwargs['rrange']
        if _plt.kwargs.get('adjust_rlim', True):
            r_min, r_max = gr.adjustlimits(r_min, r_max)
        r_rrel_min = r_min / r_max
        angles = [a for a in (0, 90, 180, 270, 360) if phi_min < a < phi_max] + [phi_min, phi_max]
        bbox = [1, -1, 1, -1]
        for angle in angles:
            sinf = np.sin(np.radians(angle))
            cosf = np.cos(np.radians(angle))
            min_x = min(cosf * 1.12, r_rrel_min * cosf)
            max_x = max(cosf * 1.12, r_rrel_min * cosf)
            min_y = min(sinf * 1.12, r_rrel_min * sinf)
            max_y = max(sinf * 1.12, r_rrel_min * sinf)
            bbox[0] = min(bbox[0], min_x)
            bbox[1] = max(bbox[1], max_x)
            bbox[2] = min(bbox[2], min_y)
            bbox[3] = max(bbox[3], max_y)
        viewport = _plt.kwargs['viewport']
        vp = _plt.kwargs['vp']
        viewport_aspect = (viewport[1] - viewport[0]) / (viewport[3] - viewport[2])
        vp_aspect = (vp[1] - vp[0]) / (vp[3] - vp[2])
        vp_aspect = vp_aspect / viewport_aspect
        width = (bbox[1] - bbox[0]) / vp_aspect
        height = bbox[3] - bbox[2]
        aspect = width / height
        if aspect > 1:
            d = (width - height) / 2
            bbox[3] += d
            bbox[2] -= d
        else:
            d = (height - width) / 2
            bbox[1] += d
            bbox[0] -= d
        gr.setwindow(*bbox)
    else:
        gr.setwindow(x_min, x_max, y_min, y_max)

    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf', 'volume'):
        z_min, z_max = _plt.kwargs['zrange']
        if not scale & gr.OPTION_Z_LOG:
            if _plt.kwargs.get('adjust_zlim', 'zlim' not in _plt.kwargs):
                z_min, z_max = gr.adjustlimits(z_min, z_max)
            z_major_count = major_count
            z_tick = gr.tick(z_min, z_max) / z_major_count
        else:
            z_tick = z_major_count = 1
        if not scale & gr.OPTION_FLIP_Z:
            zorg = (z_min, z_max)
        else:
            zorg = (z_max, z_min)
        _plt.kwargs['zaxis'] = z_tick, zorg, z_major_count
        rotation = _plt.kwargs.get('rotation', 40)
        tilt = _plt.kwargs.get('tilt', 70)
        gr.setspace(z_min, z_max, rotation, tilt)
        fov = _plt.kwargs.get('field_of_view', None)
        if fov is not None:
            gr.setwindow3d(x_min, x_max, y_min, y_max, z_min, z_max)
            gr.setwindow(-1, 1, -1, 1)
            rotation %= 360
            tilt %= 180
            tilt = min(max(tilt, 0), 180)
            gr.setspace3d(-rotation, tilt, fov, 0)

    _plt.kwargs['scale'] = scale
    gr.setscale(scale)


def _phase_wrapped_philim(phirange=None, adjust=False):
    if phirange is None:
        phi_min, phi_max = _plt.kwargs.get('phirange', (0, 360))
    else:
        phi_min, phi_max = phirange
    if phi_min == 0 and phi_max == 360:
        return phi_min, phi_max
    phi_min -= np.floor(phi_min / 360.) * 360
    phi_max -= np.floor(phi_max / 360.) * 360
    if abs(phi_min - phi_max) < 1e-6:
        phi_max += 360
    if phi_min > phi_max:
        phi_max, phi_min = phi_min, phi_max
    if adjust:
        phi_min, phi_max = gr.adjustlimits(phi_min / 3., phi_max / 3.)
        phi_min *= 3
        phi_max *= 3
    if phi_max > 360:
        phi_max = 360
    if phi_min > 360:
        phi_min = 360
    return phi_min, phi_max


def _draw_axes(kind, pass_=1):
    global _plt
    viewport = _plt.kwargs['viewport']
    vp = _plt.kwargs['vp']
    x_tick, x_org, x_major_count = _plt.kwargs['xaxis']
    y_tick, y_org, y_major_count = _plt.kwargs['yaxis']
    # enforce uniform axis labels for logarithmic labels
    # otherwise the labels will switch between decimal and exponential notation
    if _plt.kwargs['scale'] & gr.OPTION_X_LOG:
        x_tick = 10
    if _plt.kwargs['scale'] & gr.OPTION_Y_LOG:
        y_tick = 10

    gr.setlinecolorind(1)
    gr.setlinewidth(1)
    diag = ((viewport[1] - viewport[0])**2 + (viewport[3] - viewport[2])**2)**0.5
    charheight = max(0.018 * diag, 0.012)
    gr.setcharheight(charheight)
    ticksize = 0.0075 * diag
    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf', 'volume'):
        z_tick, z_org, z_major_count = _plt.kwargs['zaxis']
        fov = _plt.kwargs.get('field_of_view', None)
        if fov is None:
            if pass_ == 1:
                gr.grid3d(x_tick, 0, z_tick, x_org[0], y_org[1], z_org[0], 2, 0, 2)
                gr.grid3d(0, y_tick, 0, x_org[0], y_org[1], z_org[0], 0, 2, 0)
            else:
                gr.axes3d(x_tick, 0, z_tick, x_org[0], y_org[0], z_org[0], x_major_count, 0, z_major_count, -ticksize)
                gr.axes3d(0, y_tick, 0, x_org[1], y_org[0], z_org[0], 0, y_major_count, 0, ticksize)
        else:
            rotation = _plt.kwargs.get('rotation', 40)
            tilt = _plt.kwargs.get('tilt', 70)
            rotation %= 360
            tilt %= 180
            tilt = min(max(tilt, 0), 180)
            zi = 0 if 0 <= tilt <= 90 else 1
            if pass_ == 1:
                if 0 <= rotation < 90:
                    gr.grid3d(x_tick, 0, z_tick, x_org[0], y_org[1], z_org[zi], 2, 0, 2)
                    gr.grid3d(0, y_tick, 0, x_org[0], y_org[1], z_org[zi], 0, 2, 0)
                elif 90 <= rotation < 180:
                    gr.grid3d(x_tick, 0, z_tick, x_org[1], y_org[1], z_org[zi], 2, 0, 2)
                    gr.grid3d(0, y_tick, 0, x_org[1], y_org[1], z_org[zi], 0, 2, 0)
                elif 180 <= rotation < 270:
                    gr.grid3d(x_tick, 0, z_tick, x_org[1], y_org[0], z_org[zi], 2, 0, 2)
                    gr.grid3d(0, y_tick, 0, x_org[1], y_org[0], z_org[zi], 0, 2, 0)
                else:
                    gr.grid3d(x_tick, 0, z_tick, x_org[0], y_org[0], z_org[0], 2, 0, 2)
                    gr.grid3d(0, y_tick, 0, x_org[0], y_org[0], z_org[zi], 0, 2, 0)
            else:
                if 0 <= rotation < 90:
                    gr.axes3d(x_tick, 0, z_tick, x_org[0], y_org[0], z_org[zi], x_major_count, 0, z_major_count, -ticksize)
                    gr.axes3d(0, y_tick, 0, x_org[1], y_org[0], z_org[zi], 0, y_major_count, 0, ticksize)
                elif 90 <= rotation < 180:
                    gr.axes3d(0, 0, z_tick, x_org[0], y_org[1], z_org[zi], 0, 0, z_major_count, -ticksize)
                    gr.axes3d(x_tick, y_tick, 0, x_org[0], y_org[0], z_org[zi], x_major_count, y_major_count, 0, -ticksize)
                elif 180 <= rotation < 270:
                    gr.axes3d(x_tick, 0, z_tick, x_org[1], y_org[1], z_org[zi], x_major_count, 0, z_major_count, ticksize)
                    gr.axes3d(0, y_tick, 0, x_org[0], y_org[0], z_org[zi], 0, y_major_count, 0, -ticksize)
                else:
                    gr.axes3d(0, 0, z_tick, x_org[1], y_org[0], z_org[zi], 0, 0, z_major_count, -ticksize)
                    gr.axes3d(x_tick, y_tick, 0, x_org[1], y_org[1], z_org[zi], x_major_count, y_major_count, 0, ticksize)
    else:
        if kind in ('heatmap', 'shade'):
            ticksize = -ticksize
        if kind not in ('shade',):
            gr.grid(x_tick, y_tick, 0, 0, x_major_count, y_major_count)
        gr.axes(x_tick, y_tick, x_org[0], y_org[0], x_major_count, y_major_count, ticksize)
        gr.axes(x_tick, y_tick, x_org[1], y_org[1], -x_major_count, -y_major_count, -ticksize)

    if 'title' in _plt.kwargs:
        gr.savestate()
        gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_TOP)
        gr.textext(0.5 * (viewport[0] + viewport[1]), vp[3], _plt.kwargs['title'])
        gr.restorestate()

    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf', 'volume'):
        x_label = _plt.kwargs.get('xlabel', '')
        y_label = _plt.kwargs.get('ylabel', '')
        z_label = _plt.kwargs.get('zlabel', '')
        gr.titles3d(x_label, y_label, z_label)
    else:
        if 'xlabel' in _plt.kwargs:
            gr.savestate()
            gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_BOTTOM)
            gr.textext(0.5 * (viewport[0] + viewport[1]), vp[2] + 0.5 * charheight, _plt.kwargs['xlabel'])
            gr.restorestate()
        if 'ylabel' in _plt.kwargs:
            gr.savestate()
            gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_TOP)
            gr.setcharup(-1, 0)
            gr.textext(vp[0] + 0.5 * charheight, 0.5 * (viewport[2] + viewport[3]), _plt.kwargs['ylabel'])
            gr.restorestate()

    if kind in ('bar'):
        if 'xnotations' in _plt.kwargs:
            x_notations = _plt.kwargs.pop('xnotations')
            yval = _plt.args[0][2] if _plt.kwargs['multi_bar'] else _plt.args[0][1]
            if len(x_notations) == len(yval):
                window = _plt.kwargs['window']
                gr.setcharheight(charheight)
                gr.settextalign(2, 1)
                for i in range(1, len(x_notations) + 1):
                    x = viewport[0] + ((viewport[1] - viewport[0]) * i) / (window[1] - window[0])
                    y = viewport[2] - 0.5 * charheight
                    gr.textext(x, y, x_notations[i - 1])
            else:
                raise IndexError('The length of xnotations has to equal the amount of y-values!')


def _draw_polar_axes():
    global _plt
    viewport = _plt.kwargs['viewport']
    diag = ((viewport[1] - viewport[0])**2 + (viewport[3] - viewport[2])**2)**0.5
    charheight = max(0.018 * diag, 0.012)

    r_min, r_max = _plt.kwargs['rrange']
    if _plt.kwargs.get('adjust_rlim', True):
        r_min, r_max = gr.adjustlimits(r_min, r_max)

    phi_min, phi_max = _phase_wrapped_philim(adjust=_plt.kwargs.get('adjust_philim', True))

    gr.savestate()
    gr.setcharheight(charheight)
    gr.setlinetype(gr.LINETYPE_SOLID)
    tick = gr.tick(phi_min / 6., phi_max / 6.) * 1.5
    n = int(round((phi_max - phi_min) / tick + 0.5))
    for i in range(n + 1):
        angle_label = phi_min + i * tick
        if _plt.kwargs.get('phiflip', False):
            angle = phi_max - i * tick
        else:
            angle = angle_label
        sinf = np.sin(np.radians(angle))
        cosf = np.cos(np.radians(angle))
        pline = np.array([r_min / r_max, 1])
        if phi_min <= angle <= phi_max:
            if i % 2 == 0 and not (i == n and phi_max % 360 == phi_min % 360):
                gr.setlinecolorind(88)
                gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_HALF)
                x, y = gr.wctondc(1.1 * cosf, 1.1 * sinf)
                gr.textext(x, y, "%g\xb0" % angle_label)
            else:
                gr.setlinecolorind(90)
        else:
            angle = np.clip(angle, phi_min, phi_max)
            gr.setlinecolorind(88)
            sinf = np.sin(np.radians(angle))
            cosf = np.cos(np.radians(angle))
        gr.polyline(cosf * pline, sinf * pline)
    tick = 0.5 * gr.tick(r_min, r_max)
    n = int(round((r_max - r_min) / tick + 0.5))
    for i in range(n + 1):
        r = (r_min + i * tick) / r_max
        gr.setlinecolorind(88)
        r = np.clip(r, 0, 1)
        if i % 2 == 1 and r <= 1:
            gr.setlinecolorind(90)
        gr.drawarc(-r, r, -r, r, phi_min, phi_max)
        if i % 2 == 0 and not r > 1:
            gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_HALF)
            sinf = np.sin(np.radians(phi_min))
            cosf = np.cos(np.radians(phi_min))
            x, y = gr.wctondc(r * cosf + sinf * 0.05, r * sinf - cosf * 0.05)
            if _plt.kwargs.get('rflip', False):
                r_label = r_max - i * tick
            else:
                r_label = r_min + i * tick
            gr.text(x, y, "%g" % r_label)

    gr.restorestate()


def _draw_legend():
    global _plt
    viewport = _plt.kwargs['viewport']
    num_labels = len(_plt.kwargs['labels'])
    location = _plt.kwargs.get('location', 1)
    gr.savestate()
    gr.selntran(0)
    gr.setscale(0)
    w = 0
    for label in _plt.kwargs['labels']:
        tbx, tby = gr.inqtextext(0, 0, label)
        w = max(w, tbx[2])

    num_lines = len(_plt.args)
    h = (num_lines + 1) * 0.03
    if location in (8, 9, 10):
        px = 0.5 * (viewport[0] + viewport[1] - w)
    elif location in (2, 3, 6):
        px = viewport[0] + 0.11
    else:
        px = viewport[1] - 0.05 - w
    if location in (5, 6, 7, 10):
        py = 0.5 * (viewport[2] + viewport[3] + h) - 0.03
    elif location in (3, 4, 8):
        py = viewport[2] + h
    else:
        py = viewport[3] - 0.06

    gr.setfillintstyle(gr.INTSTYLE_SOLID)
    gr.setfillcolorind(0)
    gr.fillrect(px - 0.08, px + w + 0.02, py + 0.03, py - 0.03 * num_lines)
    gr.setlinetype(gr.LINETYPE_SOLID)
    gr.setlinecolorind(1)
    gr.setlinewidth(1)
    gr.drawrect(px - 0.08, px + w + 0.02, py + 0.03, py - 0.03 * num_lines)
    i = 0
    gr.uselinespec(" ")
    for (x, y, z, c, spec) in _plt.args:
        gr.savestate()
        mask = gr.uselinespec(spec)
        if mask in (0, 1, 3, 4, 5):
            gr.polyline([px - 0.07, px - 0.01], [py, py])
        if mask & 2:
            gr.polymarker([px - 0.06, px - 0.02], [py, py])
        gr.restorestate()
        gr.settextalign(gr.TEXT_HALIGN_LEFT, gr.TEXT_VALIGN_HALF)
        if i < num_labels:
            gr.textext(px, py, _plt.kwargs['labels'][i])
            i += 1
        py -= 0.03
    gr.selntran(1)
    gr.restorestate()


def _colorbar(off=0.0, colors=256, label_name='zlabel'):
    global _plt
    gr.savestate()
    viewport = _plt.kwargs['viewport']
    zmin, zmax = _plt.kwargs['zrange']
    zlog = _plt.kwargs.get('zlog', None)

    gr.setviewport(viewport[1] + 0.02 + off, viewport[1] + 0.05 + off,
                   viewport[2], viewport[3])
    gr.setwindow(0, 1, 0, 1)

    if colors == 1:
        data = [1000]
    else:
        data = [1000 + int(255 * i / (colors - 1)) for i in range(colors)]

    gr.setlinecolorind(1)
    gr.setscale(0)
    if _plt.kwargs['scale'] & gr.OPTION_FLIP_Z:
        gr.cellarray(0, 1, 0, 1, 1, colors, data)
    else:
        gr.cellarray(0, 1, 1, 0, 1, colors, data)
    diag = ((viewport[1] - viewport[0]) ** 2 + (viewport[3] - viewport[2]) ** 2) ** 0.5
    charheight = max(0.016 * diag, 0.012)
    gr.setcharheight(charheight)

    if 0 < zmin < zmax and zlog:
        gr.setwindow(0, 1, zmin, zmax)
        if _plt.kwargs['scale'] & gr.OPTION_FLIP_Z:
            gr.setscale(gr.OPTION_Y_LOG | gr.OPTION_FLIP_Y)
        else:
            gr.setscale(gr.OPTION_Y_LOG)
        gr.axes(0, 2, 1, zmin, 0, 1, 0.005)
    elif zmin <= zmax and not zlog:
        if _plt.kwargs['scale'] & gr.OPTION_FLIP_Z:
            gr.setscale(gr.OPTION_FLIP_Y)
        else:
            gr.setscale(0)
        ztick = 0.5 * gr.tick(zmin, zmax)
        gr.setwindow(0, 1, zmin, zmax)
        gr.axes(0, ztick, 1, zmin, 0, 1, 0.005)
    else:
        if zmin == float('inf') and zmax != float('-inf') and not (zmax < 0 and zlog):
            labels = ("min", str(zmax))
        elif zmax == float('-inf') and zmin != float('inf') and not (zmin < 0 and zlog):
            labels = (str(zmin), "max")
        else:
            labels = ("min", "max")

        def axeslbl_callback(x, y, svalue, value, labels=labels):
            gr.text(x, y, labels[int(value)])
        if _plt.kwargs['scale'] & gr.OPTION_FLIP_Z:
            gr.setscale(gr.OPTION_FLIP_Y)
        else:
            gr.setscale(0)
        gr.axeslbl(0, 1, 1, 0, 0, 1, 0.005, 0, axeslbl_callback)

    label = _plt.kwargs.get(label_name, None)
    if label:
        diag = ((viewport[1] - viewport[0])**2 + (viewport[3] - viewport[2])**2)**0.5
        charheight = max(0.018 * diag, 0.012)
        gr.setcharheight(charheight)
        gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_BASE)
        gr.textext(viewport[1] + 0.035 + off, viewport[3] + 0.01, label)
    gr.restorestate()


def _plot_data(**kwargs):
    global _plt
    _plt.kwargs.update(kwargs)
    colorbar = _plt.kwargs.get('colorbar', None)
    if not _plt.args:
        return
    kind = _plt.kwargs.get('kind', 'line')
    if _plt.kwargs['clear']:
        gr.clearws()
    if kind in ('imshow', 'isosurface'):
        _set_viewport(kind, _plt.kwargs['subplot'])
    elif not _plt.kwargs['ax']:
        _set_viewport(kind, _plt.kwargs['subplot'])
        _set_window(kind)
        if kind == 'polar':
            _draw_polar_axes()
        elif kind == 'polar_heatmap':
            pass
        else:
            _draw_axes(kind)
    elif kind in ('polar', 'polar_heatmap'):
        _set_viewport(kind, _plt.kwargs['subplot'])
        _set_window(kind)

    _set_colormap()
    if colorbar and kind not in ('quiver', 'hexbin', 'contour', 'contourf', 'surface', 'trisurf', 'heatmap', 'volume' 'polar_heatmap'):
        _colorbar()
    gr.uselinespec(" ")
    for x, y, z, c, spec in _plt.args:
        gr.savestate()
        if 'alpha' in _plt.kwargs:
            gr.settransparency(_plt.kwargs['alpha'])
        if kind == 'line':
            mask = gr.uselinespec(spec)
            if mask in (0, 1, 3, 4, 5):
                gr.polyline(x, y)
            if mask & 2:
                gr.polymarker(x, y)
        if kind == 'step':
            mask = gr.uselinespec(spec)
            if mask in (0, 1, 3, 4, 5):
                where = _plt.kwargs.get('step_where', 'mid')
                if where == 'pre':
                    n = len(x)
                    x_step_boundaries = np.zeros(2 * n - 1)
                    y_step_values = np.zeros(2 * n - 1)
                    x_step_boundaries[0] = x[0]
                    x_step_boundaries[1::2] = x[:-1]
                    x_step_boundaries[2::2] = x[1:]
                    y_step_values[0] = y[0]
                    y_step_values[1::2] = y[1:]
                    y_step_values[2::2] = y[1:]
                elif where == 'post':
                    n = len(x)
                    x_step_boundaries = np.zeros(2 * n - 1)
                    y_step_values = np.zeros(2 * n - 1)
                    x_step_boundaries[0::2] = x
                    x_step_boundaries[1::2] = x[1:]
                    x_step_boundaries[-1] = x[-1]
                    y_step_values[0::2] = y
                    y_step_values[1::2] = y[:-1]
                    y_step_values[-1] = y[-1]
                else:
                    n = len(x)
                    x_step_boundaries = np.zeros(2 * n)
                    x_step_boundaries[0] = x[0]
                    x_step_boundaries[1:-1][0::2] = (x[1:] + x[:-1]) / 2
                    x_step_boundaries[1:-1][1::2] = (x[1:] + x[:-1]) / 2
                    x_step_boundaries[-1] = x[-1]
                    y_step_values = np.zeros(2 * n)
                    y_step_values[0::2] = y
                    y_step_values[1::2] = y
                gr.polyline(x_step_boundaries, y_step_values)
            if mask & 2:
                gr.polymarker(x, y)
        elif kind == 'scatter':
            gr.setmarkertype(gr.MARKERTYPE_SOLID_CIRCLE)
            if z is not None or c is not None:
                if c is not None:
                    c_min = c.min()
                    c_ptp = c.ptp()
                for i in range(len(x)):
                    if z is not None:
                        gr.setmarkersize(z[i] / 100.0)
                    if c is not None:
                        c_index = 1000 + int(255 * (c[i] - c_min) / c_ptp)
                        gr.setmarkercolorind(c_index)
                    gr.polymarker([x[i]], [y[i]])
            else:
                gr.polymarker(x, y)
        elif kind == 'bar':
            _plot_bar()
        elif kind == 'polar_histogram':
            _plot_polar_histogram()
        elif kind == 'quiver':
            u = z
            v = c
            gr.quiver(len(x), len(y), x, y, u, v, True)
            if colorbar or colorbar is None:
                _colorbar(0.05)
        elif kind == 'stem':
            gr.setlinecolorind(1)
            gr.polyline(_plt.kwargs['window'][:2], [0, 0])
            gr.setmarkertype(gr.MARKERTYPE_SOLID_CIRCLE)
            gr.uselinespec(spec)
            for xi, yi in zip(x, y):
                gr.polyline([xi, xi], [0, yi])
            gr.polymarker(x, y)
        elif kind == 'hist':
            y_min = _plt.kwargs['window'][2]
            for i in range(1, len(y) + 1):
                gr.setfillcolorind(989)
                gr.setfillintstyle(gr.INTSTYLE_SOLID)
                gr.fillrect(x[i - 1], x[i], y_min, y[i - 1])
                gr.setfillcolorind(1)
                gr.setfillintstyle(gr.INTSTYLE_HOLLOW)
                gr.fillrect(x[i - 1], x[i], y_min, y[i - 1])
        elif kind == 'contour':
            z_min, z_max = _plt.kwargs['zrange']
            gr.setspace(z_min, z_max, 0, 90)
            num_levels = _plt.kwargs.get('levels', 20)
            if x.shape == y.shape == z.shape:
                x, y, z = gr.gridit(x, y, z, 200, 200)
                z = np.array(z)
                z_min, z_max = _plt.kwargs.get('zlim', (np.min(z), np.max(z)))
            else:
                z = np.ascontiguousarray(z)
            if _plt.kwargs['scale'] & gr.OPTION_Z_LOG:
                h = [np.exp(np.log(z_min) + i / num_levels * (np.log(z_max) - np.log(z_min))) for i in range(num_levels)]
            else:
                h = [z_min + i / num_levels * (z_max - z_min) for i in range(num_levels)]
            z.shape = np.prod(z.shape)
            gr.contour(x, y, h, z, 1000)
            if colorbar or colorbar is None:
                _colorbar(colors=num_levels)
        elif kind == 'contourf':
            z_min, z_max = _plt.kwargs['zrange']
            gr.setspace(z_min, z_max, 0, 90)
            scale = _plt.kwargs['scale']
            num_levels = _plt.kwargs.get('levels', 20)
            gr.setscale(scale)
            if x.shape == y.shape == z.shape:
                x, y, z = gr.gridit(x, y, z, 200, 200)
                z = np.array(z)
                z_min, z_max = _plt.kwargs.get('zlim', (np.min(z), np.max(z)))
            else:
                z = np.ascontiguousarray(z)
            if _plt.kwargs['scale'] & gr.OPTION_Z_LOG:
                h = [np.exp(np.log(z_min) + i / num_levels * (np.log(z_max) - np.log(z_min))) for i in range(num_levels)]
            else:
                h = [z_min + i / num_levels * (z_max - z_min) for i in range(num_levels)]
            z.shape = np.prod(z.shape)
            if colorbar or colorbar is None:
                _colorbar(colors=num_levels)
            gr.setlinecolorind(1)
            gr.contourf(x, y, h, z, 0)
        elif kind == 'hexbin':
            nbins = _plt.kwargs.get('nbins', 40)
            cntmax = gr.hexbin(x, y, nbins)
            if cntmax > 0:
                _plt.kwargs['zrange'] = (0, cntmax)
                if colorbar or colorbar is None:
                    _colorbar()
        elif kind == 'heatmap':
            x_min, x_max, y_min, y_max = _plt.kwargs['window']
            if x is not None:
                x_min, x_max = x
            if y is not None:
                y_min, y_max = y
            height, width = z.shape
            cmap = _colormap()
            icmap = np.zeros(256, np.uint32)
            for i in range(256):
                r, g, b, a = cmap[i]
                icmap[i] = (int(r * 255) << 0) + (int(g * 255) << 8) + (int(b * 255) << 16) + (int(a * 255) << 24)
            z_min, z_max = _plt.kwargs.get('zlim', (np.min(z), np.max(z)))
            if z_max < z_min:
                z_max, z_min = z_min, z_max
            if _plt.kwargs.get('zlog', False):
                z = np.log(z)
                z_min = np.log(z_min)
                z_max = np.log(z_max)
            if z_max > z_min:
                data = (z - z_min) / (z_max - z_min) * 255
            else:
                data = np.zeros((height, width))
            rgba = np.zeros((height, width), np.uint32)
            for x in range(width):
                for y in range(height):
                    if 0 <= data[y, x] <= 255:
                        rgba[y, x] = icmap[int(data[y, x])]
                    else:
                        # make invalid values transparent
                        rgba[y, x] = 0
            y_min, y_max = y_max, y_min
            gr.drawimage(x_min, x_max, y_min, y_max, width, height, rgba)
            if colorbar or colorbar is None:
                _colorbar()
        elif kind == 'polar_heatmap':
            height, width = z.shape
            z_min, z_max = _plt.kwargs.get('zlim', (np.min(z), np.max(z)))
            if z_max < z_min:
                z_max, z_min = z_min, z_max
            if _plt.kwargs.get('zlog', False):
                z = np.log(z)
                z_min = np.log(z_min)
                z_max = np.log(z_max)
            if z_max > z_min:
                data = (1000 + (z - z_min) / (z_max - z_min) * 255).astype(np.int)
            else:
                data = np.zeros((height, width), dtype=np.int)
            if y is not None:
                phi_range = np.degrees(y)
            else:
                phi_range = None
            phi_min, phi_max = _phase_wrapped_philim(phi_range)
            if _plt.kwargs.get('phiflip', False):
                phi_min_adj, phi_max_adj = _phase_wrapped_philim(adjust=_plt.kwargs.get('adjust_philim', True))
                phi_offset = phi_max_adj + phi_min_adj - phi_max - phi_min
                phi_min, phi_max = phi_max + phi_offset, phi_min + phi_offset
            if x is not None:
                r_range = np.array(x)
            else:
                r_range = np.array(_plt.kwargs['rrange'])
            r_min, r_max = _plt.kwargs['rrange']
            relative_r_min = r_min / r_max
            r_range = ((r_range - r_min) / (r_max - r_min) * (1 - relative_r_min)) + relative_r_min
            if _plt.kwargs.get('rflip', False):
                r_range = 1 + relative_r_min - r_range
            gr.polarcellarray(0, 0, phi_min, phi_max, r_range[0], r_range[1], width, height, data)
            _draw_polar_axes()
            if colorbar or colorbar is None:
                _colorbar()
        elif kind == 'wireframe':
            if x.shape == y.shape == z.shape:
                x, y, z = gr.gridit(x, y, z, 50, 50)
                z = np.array(z)
            else:
                z = np.ascontiguousarray(z)
            z.shape = np.prod(z.shape)
            gr.setfillcolorind(0)
            gr.surface(x, y, z, gr.OPTION_FILLED_MESH)
            _draw_axes(kind, 2)
        elif kind == 'surface':
            if x.shape == y.shape == z.shape:
                x, y, z = gr.gridit(x, y, z, 200, 200)
                z = np.array(z)
            else:
                z = np.ascontiguousarray(z)
            z.shape = np.prod(z.shape)
            if _plt.kwargs.get('accelerate', True) and _gr3_is_available():
                gr3.clear()
                gr3.surface(x, y, z, gr.OPTION_COLORED_MESH)
            else:
                gr.surface(x, y, z, gr.OPTION_COLORED_MESH)
            _draw_axes(kind, 2)
            if colorbar or colorbar is None:
                _colorbar(0.05)
        elif kind == 'plot3':
            gr.polyline3d(x, y, z)
            _draw_axes(kind, 2)
        elif kind == 'scatter3':
            gr.setmarkertype(gr.MARKERTYPE_SOLID_CIRCLE)
            if c is not None:
                c_min = c.min()
                c_ptp = c.ptp()
                for i in range(len(x)):
                    c_index = 1000 + int(255 * (c[i] - c_min) / c_ptp)
                    gr.setmarkercolorind(c_index)
                    gr.polymarker3d([x[i]], [y[i]], [z[i]])
            else:
                gr.polymarker3d(x, y, z)
            _draw_axes(kind, 2)
        elif kind == 'imshow':
            _plot_img(z)
        elif kind == 'isosurface':
            _plot_iso(z)
        elif kind == 'volume':
            algorithm = _plt.kwargs.get('algorithm', 'maximum').lower()
            if algorithm == 'emission':
                _algorithm = 0
            elif algorithm == 'absorption':
                _algorithm = 1
            elif algorithm in ('mip', 'maximum'):
                _algorithm = 2
            else:
                raise ValueError('Invalid volume algorithm. Use "emission", "absorption" or "maximum".')
            dmin = _plt.kwargs.get('dmin', -1)
            dmax = _plt.kwargs.get('dmax', -1)
            if dmin is None:
                dmin = -1
            if dmax is None:
                dmax = -1
            width, height, device_pixel_ratio = gr.inqvpsize()
            gr.setpicturesizeforvolume(int(width * device_pixel_ratio), int(height * device_pixel_ratio))
            dmin, dmax = gr.volume(c, algorithm=_algorithm, dmin=dmin, dmax=dmax)
            _draw_axes(kind, 2)
            prev_zrange = _plt.kwargs.get('zrange', None)
            _plt.kwargs['zrange'] = (dmin, dmax)
            if colorbar or colorbar is None:
                _colorbar(0.05, label_name='dlabel')
            _plt.kwargs['zrange'] = prev_zrange
        elif kind == 'polar':
            gr.uselinespec(spec)
            _plot_polar(x, y)
        elif kind == 'trisurf':
            gr.trisurface(x, y, z)
            _draw_axes(kind, 2)
            if colorbar or colorbar is None:
                _colorbar(0.05)
        elif kind == 'tricont':
            zmin, zmax = _plt.kwargs['zrange']
            levels = np.linspace(zmin, zmax, 20)
            gr.tricontour(x, y, z, levels)
        elif kind == 'shade':
            xform = _plt.kwargs.get('xform', 5)
            if np.any(np.isnan(x)):
                gr.shadelines(x, y, xform=xform)
            else:
                gr.shadepoints(x, y, xform=xform)
        gr.restorestate()
    if kind in ('line', 'step', 'scatter', 'stem') and 'labels' in _plt.kwargs:
        _draw_legend()

    if _plt.kwargs['update']:
        gr.updatews()
        if gr.isinline():
            return gr.show()


def _plot_img(image):
    global _plt

    if isinstance(image, basestring):
        width, height, data = gr.readimage(image)
        if width == 0 or height == 0:
            return
    else:
        image = np.array(image)
        height, width = image.shape
        data = np.array(1000 + (1.0 * image - image.min()) / image.ptp() * 255, np.int32)

    if _plt.kwargs['clear']:
        gr.clearws()

    if not _plt.kwargs['ax']:
        _set_viewport('line', _plt.kwargs['subplot'])

    viewport = _plt.kwargs['viewport']
    vp = _plt.kwargs['vp']

    if width * (viewport[3] - viewport[2]) < height * (viewport[1] - viewport[0]):
        w = width / height * (viewport[3] - viewport[2])
        x_min = max(0.5 * (viewport[0] + viewport[1] - w), viewport[0])
        x_max = min(0.5 * (viewport[0] + viewport[1] + w), viewport[1])
        y_min = viewport[2]
        y_max = viewport[3]
    else:
        h = height / width * (viewport[1] - viewport[0])
        x_min = viewport[0]
        x_max = viewport[1]
        y_min = max(0.5 * (viewport[3] + viewport[2] - h), viewport[2])
        y_max = min(0.5 * (viewport[3] + viewport[2] + h), viewport[3])

    _set_colormap()
    gr.selntran(0)
    if isinstance(image, basestring):
        gr.drawimage(x_min, x_max, y_min, y_max, width, height, data)
    else:
        gr.cellarray(x_min, x_max, y_min, y_max, width, height, data)

    if 'title' in _plt.kwargs:
        gr.savestate()
        gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_TOP)
        gr.textext(0.5 * (viewport[0] + viewport[1]), vp[3], _plt.kwargs['title'])
        gr.restorestate()
    gr.selntran(1)


def _plot_iso(v):
    global _plt
    if not _gr3_is_available():
        raise RuntimeError("Unable to initialize GR3, please ensure that your system supports OpenGL")
    viewport = _plt.kwargs['viewport']
    if viewport[3] - viewport[2] < viewport[1] - viewport[0]:
        width = viewport[3] - viewport[2]
        center_x = 0.5 * (viewport[0] + viewport[1])
        x_min = max(center_x - 0.5 * width, viewport[0])
        x_max = min(center_x + 0.5 * width, viewport[1])
        y_min = viewport[2]
        y_max = viewport[3]
    else:
        height = viewport[1] - viewport[0]
        center_y = 0.5 * (viewport[2] + viewport[3])
        x_min = viewport[0]
        x_max = viewport[1]
        y_min = max(center_y - 0.5 * height, viewport[2])
        y_max = min(center_y + 0.5 * height, viewport[3])

    gr.selntran(0)
    usable_vs = v[np.abs(v) != np.inf]
    if np.prod(usable_vs.shape) == 0:
        return
    v_max = usable_vs.max()
    v_min = usable_vs.min()
    if v_min == v_max:
        return
    uint16_max = np.iinfo(np.uint16).max
    if v.dtype == np.uint16:
        isovalue = int(_plt.kwargs.get('isovalue', 0.5 * uint16_max))
    else:
        isovalue = _plt.kwargs.get('isovalue', 0.5)
        isovalue = int((isovalue - v_min) / (v_max - v_min) * uint16_max)
    v = (np.clip(v, v_min, v_max) - v_min) / (v_max - v_min) * uint16_max
    values = v.astype(np.uint16)
    nx, ny, nz = v.shape
    rotation = np.radians(_plt.kwargs.get('rotation', 40))
    tilt = np.radians(_plt.kwargs.get('tilt', 70))
    gr3.clear()
    mesh = gr3.createisosurfacemesh(values, (2 / (nx - 1), 2 / (ny - 1), 2 / (nz - 1)),
                                    (-1., -1., -1.), isovalue)
    color = _plt.kwargs.get('color', (0.0, 0.5, 0.8))
    gr3.setbackgroundcolor(1, 1, 1, 0)
    gr3.drawmesh(mesh, 1, (0, 0, 0), (0, 0, 1), (0, 1, 0), color, (1, 1, 1))
    r = 2.5
    if tilt != 0:
        up = (0, 1, 0)
    else:
        up = (0, 0, 1)
    gr3.cameralookat(
        r * np.sin(tilt) * np.sin(rotation), r * np.cos(tilt), r * np.sin(tilt) * np.cos(rotation),
        0, 0, 0,
        up[0], up[1], up[2]
    )
    gr3.drawimage(x_min, x_max, y_min, y_max, 500, 500, gr3.GR3_Drawable.GR3_DRAWABLE_GKS)
    gr3.deletemesh(mesh)
    gr.selntran(1)


def _plot_polar(phi, rho):
    global _plt
    r_min, r_max = _plt.kwargs['rrange']
    if _plt.kwargs.get('adjust_rlim', True):
        r_min, r_max = gr.adjustlimits(r_min, r_max)
    phi_min, phi_max = np.radians(_phase_wrapped_philim(adjust=_plt.kwargs.get('adjust_philim', True)))
    phi = np.fmod(phi, 2 * np.pi)
    split_rho = np.logical_or(rho < r_min, rho > r_max)
    split_phi = np.logical_or(phi < phi_min, phi > phi_max)
    split = np.where(np.logical_or(split_phi, split_rho))[0].astype(np.int)
    relative_r_min = r_min / r_max
    rho = ((rho - r_min) / (r_max - r_min) * (1 - relative_r_min)) + relative_r_min
    if _plt.kwargs.get('rflip', False):
        rho = 1 + relative_r_min - rho
    if _plt.kwargs.get('phiflip', False):
        phi = phi_max + phi_min - phi
    for r, a in zip(np.split(rho, split), np.split(phi, split)):
        if not len(r) > 1:
            continue
        x = r * np.cos(a)
        y = r * np.sin(a)
        gr.polyline(x, y)


def _convert_to_array(obj, may_be_2d=False, xvalues=None, always_flatten=False):
    global _plt
    if callable(obj):
        if xvalues is None:
            raise TypeError('object is callable, but xvalues is None')
        if len(xvalues.shape) == 1:
            a = np.fromiter((obj(x) for x in xvalues), np.float64)
        else:
            a = np.fromiter((obj(x, y) for x, y in xvalues), np.float64)
    else:
        a = obj
        try:
            if obj.__iter__() is obj:
                a = np.fromiter(obj, np.float64, len(xvalues))
        except (AttributeError, TypeError):
            pass
    try:
        a = np.array(a, copy=copy_if_needed)
    except TypeError:
        raise TypeError("expected a sequence, but got '{}'".format(type(obj)))
    if always_flatten:
        # Only contiguous arrays can be flattened this way
        a = np.ascontiguousarray(a)
        a.shape = np.prod(a.shape)
    # Ensure a shape of (n,) or (n, 2) if may_be_2d is True
    dimension = sum(i != 1 for i in a.shape)
    if may_be_2d and dimension > 2:
        raise TypeError("expected a 1d- or 2d-sequence, but got shape {}".format(a.shape))
    if not may_be_2d and dimension > 1:
        raise TypeError("expected a 1d-sequence, but got shape {}".format(a.shape))
    if dimension == 0:
        dimension = 1
        a.shape = [1]
    else:
        a.shape = [i for i in a.shape if i != 1]
    if dimension == 2:
        if 2 not in a.shape:
            raise TypeError("expected a sequence of pairs, but got shape {}".format(a.shape))
        if a.shape[0] == 2 and a.shape[1] != 2:
            a = a.T
    n = len(a)
    assert a.shape == (n,) or a.shape == (n, 2)

    if a.dtype == complex:
        if dimension != 1:
            raise TypeError("expected a sequence of complex values, but got shape {}".format(a.shape))
        a = np.hstack((np.real(a), np.imag(a)))
        dimension = 2
    elif a.dtype != np.float64:
        try:
            a = a.astype(np.float64)
        except (TypeError, ValueError):
            raise TypeError("expected a sequence of real values, but got '{}'".format(a.dtype))
    return a


def _plot_bar():
    global _plt
    kwargs = _plt.kwargs
    args = _plt.args[0]
    multi_bar = kwargs['multi_bar']
    style = kwargs['bar_style']

    # Default
    bar_width = 1
    edgewidth = 1
    edgecolor = [0, 0, 0]
    std_colors = [989, 982, 980, 981, 996, 983, 995, 988, 986, 990, 991, 984, 992, 993, 994, 987, 985, 997, 998, 999]
    color = std_colors[0]
    color_save_spot = 1000

    # Args
    if multi_bar:
        y_values = args[2]
        colorlist = args[3]
    else:
        y_values = args[1]
        colorlist = args[3]

    # Width
    if kwargs.get('bar_width'):
        bar_width = kwargs['bar_width']
        if not isinstance(bar_width, (int, float)):
            raise TypeError('Bar_width has to be an int or float!')
        elif bar_width > 1 or bar_width <= 0:
            raise ValueError('Bar_width has to be in (0;1]!')

    # Color
    if kwargs.get('bar_color'):
        color = kwargs['bar_color']
        if isinstance(kwargs['bar_color'], int):
            if not color >= 0 or not color < 1256:
                raise ValueError('Bar_color has to be in [0;1256)!')
        elif isinstance(kwargs['bar_color'], list) and len(kwargs['bar_color']) == 3:
            for c in color:
                if c < 0 or c > 1:
                    raise ValueError('The values of bar_color have to be in [1;0]!')
        else:
            raise TypeError('Bar_color has to be an int or list of RGB values!')

    # EdgeColor
    if kwargs.get('edge_color'):
        edgecolor = kwargs['edge_color']
        if isinstance(kwargs['edge_color'], int):
            if not edgecolor >= 0 or not edgecolor < 1256:
                raise ValueError('Edge_color has to be in [0;1256)!')
        elif isinstance(kwargs['edge_color'], list) and len(kwargs['edge_color']) == 3:
            for c in edgecolor:
                if c < 0 or c > 1:
                    raise ValueError('The values of edge_color have to be in [1;0]!')
        else:
            raise TypeError('Edge_color has to be an int or list of RGB values!')

    # EdgeWidth
    if kwargs.get('edge_width'):
        if not isinstance(kwargs['edge_width'], (float, int)):
            raise TypeError('Edge_width has to be of type int or float')
        edgewidth = kwargs['edge_width']
        if edgewidth < 0:
            raise ValueError('Edge_width has to be bigger or equal to 0!')

    # Change individual color
    pos_indcolor = []
    changecolor = False
    indcolors = [None for i in range(len(y_values) + 1)]
    if 'ind_bar_color' in kwargs:
        changecolor = True
        indcolor = kwargs.pop('ind_bar_color')
        if not isinstance(indcolor, list):
            raise TypeError('Ind_bar_color has to be a list!')
        if not indcolor:
            raise IndexError('Ind_bar_color can`t be empty!')
        if isinstance(indcolor[0], list) and not indcolor[0]:
            raise IndexError('Ind_bar_color[0] can`t be empty!')
        try:
            if isinstance(indcolor[0], list) and isinstance(indcolor[0][1], int) or isinstance(indcolor[0], int):
                has_pairs = False
            elif isinstance(indcolor[0], list) and isinstance(indcolor[0][1], list):
                has_pairs = True
            else:
                raise TypeError('Ind_bar_color[0] has to be an int or list!')
        except IndexError:
            raise IndexError('Ind_bar_color[0] has to be a colorpack, a list bigger than 1 or an int!')
        if not has_pairs:
            indcolor = [indcolor]
        for colorpack in indcolor:
            if not isinstance(colorpack[0], (list, int)) or not isinstance(colorpack[1], list):
                raise TypeError('Colorpack[0] has to be an int or list and colorpack[1] has to be a list!')
            if not len(colorpack[1]) == 3:
                raise IndexError('Colorpack[1] has to be of length 3!')
            for c in colorpack[1]:
                if c < 0 or c > 1:
                    raise ValueError('The values in colorpack[1] have to be in [0;1]!')
            indcolor_rgb = [colorpack[1][0], colorpack[1][1], colorpack[1][2]]
            if isinstance(colorpack[0], list):
                pos_indcolor.extend(colorpack[0])
                for index in colorpack[0]:
                    indcolors[index] = indcolor_rgb
            elif isinstance(colorpack[0], int):
                pos_indcolor.append(colorpack[0])
                indcolors[colorpack[0]] = indcolor_rgb

    # Change individual edgecolor
    pos_indedgecolor = []
    changeedgecolor = False
    indedgecolors = [None for i in range(len(y_values) + 1)]
    if 'ind_edge_color' in kwargs:
        changeedgecolor = True
        indedgecolor = kwargs.pop('ind_edge_color')
        if not isinstance(indedgecolor, list):
            raise TypeError('Ind_edge_color has to be a list!')
        try:
            if isinstance(indedgecolor[0], list) and isinstance(indedgecolor[0][1], int) or isinstance(indedgecolor[0], int):
                has_pairs = False
            elif isinstance(indedgecolor[0], list) and isinstance(indedgecolor[0][1], list):
                has_pairs = True
            else:
                raise TypeError('Ind_edge_color[0] has to be an int or list!')
        except IndexError:
            raise IndexError('Ind_edge_color[0] has to be a colorpack, a list bigger than 1 or an int!')
        if not has_pairs:
            indedgecolor = [indedgecolor]
        for colorpack in indedgecolor:
            if not isinstance(colorpack[0], (list, int)):
                raise TypeError('Colorpack[0] has to be an int or list!')
            if not isinstance(colorpack[1], list):
                raise TypeError('Colorpack[1] has to be a list!')
            if len(colorpack[1]) != 3:
                raise IndexError('Colorpack[1] has to be of length 3!')
            for c in colorpack[1]:
                if c < 0 or c > 1:
                    raise ValueError('The values in colorpack[1] have to be in [0;1]!')
            indedgecolor_rgb = [colorpack[1][0], colorpack[1][1], colorpack[1][2]]
            if isinstance(colorpack[0], list):
                pos_indedgecolor.extend(colorpack[0])
                for index in colorpack[0]:
                    indedgecolors[index] = indedgecolor_rgb
            elif isinstance(colorpack[0], int):
                pos_indedgecolor.append(colorpack[0])
                indedgecolors[colorpack[0]] = indedgecolor_rgb

    # Change individual edge width
    pos_indedgewidth = []
    changeedgewidth = False
    indedgewidths = [None for i in range(len(y_values) + 1)]
    if 'ind_edge_width' in kwargs:
        indedgewidth = kwargs.pop('ind_edge_width')
        if not isinstance(indedgewidth, list):
            raise TypeError('Ind_edge_width has to be of type list!')
        if isinstance(indedgewidth[1], (float, int)) and isinstance(indedgewidth[0], (int, list)):
            has_pairs = False
        elif isinstance(indedgewidth[1], list):
            has_pairs = True
        else:
            raise TypeError('Ind_edge_width[0] has to be of type int or list and Ind_edge_width[1] of type int '
                            'or float!')
        if not has_pairs:
            indedgewidth = [indedgewidth]
        for widthpack in indedgewidth:
            if isinstance(widthpack[1], (float, int)) and isinstance(widthpack[0], (int, list)):
                if not widthpack[1] >= 0:
                    raise ValueError('Widthpack[1] has to be bigger or equal to 0!')
                changeedgewidth = True
                ind_edgewidth = widthpack[1]
                if isinstance(widthpack[0], list):
                    pos_indedgewidth.extend(widthpack[0])
                    for index in widthpack[0]:
                        indedgewidths[index] = ind_edgewidth
                elif isinstance(widthpack[0], int):
                    pos_indedgewidth.append(widthpack[0])
                    indedgewidths[widthpack[0]] = ind_edgewidth

    # Draw bars
    wfac = bar_width * 0.8
    gr.setfillintstyle(1)
    for a, y in enumerate(y_values):
        x = a + 1
        if style == 'stacked' and multi_bar:
            c = 0
            for i in range(0, len(y), 1):
                if changecolor and (i + 1 in pos_indcolor):
                    current_rgb = indcolors[i + 1]
                    gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                    gr.setfillcolorind(color_save_spot)
                else:
                    if colorlist:
                        if isinstance(colorlist[i], int):
                            gr.setfillcolorind(colorlist[i])
                        else:
                            current_rgb = colorlist[i]
                            gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                            gr.setfillcolorind(color_save_spot)
                    else:
                        gr.setfillcolorind(std_colors[i % len(std_colors)])
                gr.fillrect((x - 0.5 * bar_width), (x + 0.5 * bar_width),
                            c, (y[i] + c))
                c = y[i] + c
        elif style == 'lined' and multi_bar:
            bar_width = wfac / (len(y))
            for i in range(0, len(y), 1):
                if changecolor and (i + 1 in pos_indcolor):
                    current_rgb = indcolors[i + 1]
                    gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                    gr.setfillcolorind(color_save_spot)
                else:
                    if colorlist:
                        if isinstance(colorlist[i], int):
                            gr.setfillcolorind(colorlist[i])
                        else:
                            current_rgb = colorlist[i]
                            gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                            gr.setfillcolorind(color_save_spot)
                    else:
                        gr.setfillcolorind(std_colors[i % len(std_colors)])
                gr.fillrect((x - 0.5 * wfac + bar_width * i),
                            (x - 0.5 * wfac + bar_width + bar_width * i), 0,
                            y[i])
        else:
            if changecolor and (x in pos_indcolor):
                current_rgb = indcolors[x]
                gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                gr.setfillcolorind(color_save_spot)
            else:
                if colorlist:
                    if isinstance(colorlist[a], int):
                        gr.setfillcolorind(colorlist[a])
                    else:
                        current_rgb = colorlist[a]
                        gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                        gr.setfillcolorind(color_save_spot)
                else:
                    if isinstance(color, int):
                        gr.setfillcolorind(color)
                    else:
                        current_rgb = color
                        gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                        gr.setfillcolorind(color_save_spot)
            gr.fillrect((x - 0.5 * bar_width), (x + 0.5 * bar_width), 0, y)

    # Draw edges
    gr.setfillintstyle(0)
    for a, y in enumerate(y_values):
        x = a + 1
        if style == 'stacked' and multi_bar:
            c = 0
            for i in range(0, len(y), 1):
                if changeedgecolor and (i + 1 in pos_indedgecolor):
                    current_rgb = indedgecolors[i + 1]
                    gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                    gr.setlinecolorind(color_save_spot)
                else:
                    if isinstance(edgecolor, int):
                        gr.setlinecolorind(edgecolor)
                    else:
                        current_rgb = edgecolor
                        gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                        gr.setlinecolorind(color_save_spot)
                if changeedgewidth and (i + 1 in pos_indedgewidth):
                    gr.setlinewidth(indedgewidths[i + 1])
                else:
                    gr.setlinewidth(edgewidth)
                gr.drawrect((x - 0.5 * bar_width), (x + 0.5 * bar_width),
                            c, (y[i] + c))
                c = y[i] + c
        elif style == 'lined' and multi_bar:
            bar_width = wfac / (len(y))
            for i in range(0, len(y), 1):
                if changeedgecolor and (i + 1 in pos_indedgecolor):
                    current_rgb = indedgecolors[i + 1]
                    gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                    gr.setlinecolorind(color_save_spot)
                else:
                    if isinstance(edgecolor, int):
                        gr.setlinecolorind(edgecolor)
                    else:
                        current_rgb = edgecolor
                        gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                        gr.setlinecolorind(color_save_spot)
                if changeedgewidth and (i + 1 in pos_indedgewidth):
                    gr.setlinewidth(indedgewidths[i + 1])
                else:
                    gr.setlinewidth(edgewidth)
                gr.drawrect((x - 0.5 * wfac + bar_width * i),
                            (x - 0.5 * wfac + bar_width + bar_width * i), 0,
                            y[i])
        else:
            if changeedgecolor and (x in pos_indedgecolor):
                current_rgb = indedgecolors[x]
                gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                gr.setlinecolorind(color_save_spot)
            else:
                if isinstance(edgecolor, int):
                    gr.setlinecolorind(edgecolor)
                else:
                    current_rgb = edgecolor
                    gr.setcolorrep(color_save_spot, current_rgb[0], current_rgb[1], current_rgb[2])
                    gr.setlinecolorind(color_save_spot)
            if changeedgewidth and (x in pos_indedgewidth):
                gr.setlinewidth(indedgewidths[x])
            else:
                gr.setlinewidth(edgewidth)
            gr.drawrect((x - 0.5 * bar_width), (x + 0.5 * bar_width), 0, y)


def _create_colormap(tup):

    if len(tup) != 3:
        raise ValueError('colormap must be a triple tuple!')

    if tup[2] is None:
        size = 700
    else:
        size = tup[2]

    if tup[0] is None and tup[1] is None:
        gr.setcolormap(0)
        COLORMAP_Y = np.array(_colormap() * 255, dtype=int)
        COLORMAP_X = np.zeros((256, 4))
        factor = 1

    elif tup[0] is not None and tup[1] is None:
        if isinstance(tup[0], int):
            gr.setcolormap(tup[0])
        elif isinstance(tup[0], str):
            gr.setcolormap(gr.COLORMAPS[tup[0]])
        else:
            raise ValueError('Invalid colormap parameter')

        COLORMAP_X = np.array(_colormap() * 255, dtype=int)
        COLORMAP_Y = np.zeros((256, 4))
        factor = 1

    elif tup[0] is None and tup[1] is not None:
        if isinstance(tup[1], int):
            gr.setcolormap(tup[1])
        elif isinstance(tup[1], str):
            gr.setcolormap(gr.COLORMAPS[tup[1]])
        else:
            raise ValueError('Invalid colormap parameter')
        COLORMAP_X = np.zeros((256, 4))
        COLORMAP_Y = np.array(_colormap() * 255, dtype=int)
        factor = 1

    else:
        if isinstance(tup[0], int):
            gr.setcolormap(tup[0])
        elif isinstance(tup[0], str):
            gr.setcolormap(gr.COLORMAPS[tup[0]])
        else:
            raise ValueError('Invalid colormap parameter')
        COLORMAP_X = np.array(_colormap() * 255, dtype=int)

        if isinstance(tup[1], int):
            gr.setcolormap(tup[1])
        elif isinstance(tup[1], str):
            gr.setcolormap(gr.COLORMAPS[tup[1]])
        else:
            raise ValueError('Invalid colormap parameter')
        COLORMAP_Y = np.array(_colormap() * 255, dtype=int)
        factor = 2

    size_range = range(256)
    lins_float = np.linspace(0, 255, num=size)

    r1 = np.array(np.interp(lins_float, size_range, COLORMAP_X[size_range, 0])).reshape(1, -1)
    r2 = np.array(np.interp(lins_float, size_range, COLORMAP_Y[size_range, 0])).reshape(-1, 1)
    r12 = np.array((r1 + r2) / factor, dtype=np.int)

    g1 = np.array(np.interp(lins_float, size_range, COLORMAP_X[size_range, 1])).reshape(1, -1)
    g2 = np.array(np.interp(lins_float, size_range, COLORMAP_Y[size_range, 1])).reshape(-1, 1)
    g12 = np.left_shift(np.array((g1 + g2) / factor, dtype=np.int), 8)

    b1 = np.array(np.interp(lins_float, size_range, COLORMAP_X[size_range, 2])).reshape(1, -1)
    b2 = np.array(np.interp(lins_float, size_range, COLORMAP_Y[size_range, 2])).reshape(-1, 1)
    b12 = np.left_shift(np.array((b1 + b2) / factor, dtype=np.int), 16)

    a1 = np.array(np.interp(lins_float, size_range, COLORMAP_X[size_range, 3])).reshape(1, -1)
    a2 = np.array(np.interp(lins_float, size_range, COLORMAP_Y[size_range, 3])).reshape(-1, 1)
    a12 = np.left_shift(np.array((a1 + a2) / factor, dtype=np.int), 24)

    pixmap = np.array(r12 | g12 | b12 | a12)

    return np.ascontiguousarray(pixmap)


def _plot_polar_histogram():
    def moivre(r, x, n):
        list1 = [1, 0]
        if n != 0:
            list1[0] = r ** (1 / n) * (np.cos((2 * x * np.pi) / n))
            list1[1] = r ** (1 / n) * (np.sin((2 * x * np.pi) / n))
        return list1

    global _plt

    edgecolor = 1
    facecolor = 989
    facealpha = 0.75
    temp_face = None
    temp_edge = None

    vp = _plt.kwargs['subplot']
    if vp[1] - vp[0] > 0.99 and vp[3] - vp[2] > 0.99:
        if 'title' in _plt.kwargs:
            gr.savestate()
            gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_TOP)
            gr.textext(0.5 * (vp[0] + vp[1]), 0.95, _plt.kwargs['title'])
            gr.restorestate()

        vp = [0.1, 0.9, 0.1, 0.9]

    else:
        vp[3] = vp[2] + vp[1] - vp[0]
        _set_viewport('polar_histogram', vp)
        vp = gr.inqviewport()
        vp[3] = vp[2] + vp[1] - vp[0]
        temp_add = (vp[1] - vp[0]) * 0.25

        if 'title' in _plt.kwargs:
            factor = 0.3
            vp[0] += temp_add * 2 * factor
            vp[1] -= temp_add * 2 * factor
            gr.savestate()
            gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_TOP)
            gr.textext(0.5 * (vp[0] + vp[1]), vp[3] - temp_add * 4 * 0.25, _plt.kwargs['title'])
            gr.restorestate()

            vp[3] -= temp_add * 4 * factor
            del factor
        else:
            vp[1] -= temp_add
            vp[3] -= temp_add

        del temp_add

    gr.setviewport(vp[0], vp[1], vp[2], vp[3])
    gr.setlinewidth(1)
    gr.setwindow(0, 1, 0, 1)

    convert = 180 / np.pi
    norm_factor = _plt.kwargs['norm_factor']
    normalization = _plt.kwargs['normalization']

    classes = _plt.kwargs['classes']
    del _plt.kwargs['classes']

    if _plt.kwargs.get('bin_edges', None) is not None:
        is_binedges = True
        binedges = _plt.kwargs['bin_edges']
    else:
        is_binedges = False

    if _plt.kwargs.get('temp_bin_edges', None) is not None:
        is_binedges = True
        binedges = _plt.kwargs['temp_bin_edges']
        del _plt.kwargs['temp_bin_edges']

    temp = _plt.kwargs['border_exp']
    border = temp[0]
    exp = temp[1]
    del temp
    del _plt.kwargs['border_exp']

    gr.settransparency(0.8)

    num_bins = len(classes)

    if _plt.kwargs.get('rlim', None) is not None:
        r_min = _plt.kwargs['rlim']
        r_max = r_min[1]
        r_min = r_min[0]
        is_rlim = True
    else:
        is_rlim = False

    # face_color either a number or an rgb triplet [x,y,z]
    if 'face_color' in _plt.kwargs:
        facecolor = _plt.kwargs['face_color']
        if isinstance(facecolor, list):
            if len(facecolor) == 3:
                temp_face = gr.inqcolor(1004)
                gr.setcolorrep(1004, facecolor[0], facecolor[1], facecolor[2])
                facecolor = 1004
            else:
                raise ValueError('RGB Triplet not correct')
        elif not isinstance(facecolor, int):
            raise ValueError('face_color not correct')

    # face_alpha
    if 'face_alpha' in _plt.kwargs:
        facealpha = _plt.kwargs['face_alpha']
        if not (0 <= facealpha <= 1):
            raise ValueError('face_alpha not correct')

    # edge_color
    if 'edge_color' in _plt.kwargs:
        edgecolor = _plt.kwargs['edge_color']
        if isinstance(edgecolor, list):
            if len(edgecolor) == 3:
                temp_edge = gr.inqcolor(1005)
                gr.setcolorrep(1005, edgecolor[0], edgecolor[1], edgecolor[2])
                edgecolor = 1005
        elif not isinstance(edgecolor, int):
            raise ValueError('Incorrect Color Value. Either Integer or rgb triplet in a list')

    # drawing the circles + x-Axis numbers
    gr.settextalign(1, 1)
    window_width = (vp[1] - vp[0])
    center_x = window_width / 2 + vp[0]
    center_y = (vp[3] - vp[2]) / 2 + vp[2]

    for x in range(4):
        gr.drawarc((0.1 + x * 0.1), (0.9 - 0.1 * x), (0.1 + x * 0.1), (0.9 - 0.1 * x), 0, 360)
        if normalization == 'count' or normalization == 'cumcount':
            gr.text(center_x * 1.02, center_y + (x + 1) * window_width * 0.8 / 2 / 4, str(int((x + 1) * border / 4)))
        else:
            if normalization == 'probability':
                gr.text(center_x * 1.02, center_y + (x + 1) * window_width * 0.8 / 2 / 4,
                        str(round(((x + 1) * border / 4) * 10 ** (exp + 2 + int(num_bins / 25))) / 10 ** (
                            exp + 2 + int(num_bins / 25))))
            else:
                gr.text(center_x * 1.02, center_y + (x + 1) * window_width * 0.8 / 2 / 4,
                        str(round(((x + 1) * border / 4) * 10 ** (exp + 3)) / 10 ** (exp + 3)))

    # drawinng lines + angle
    number = 0
    gr.settextalign(2, 3)
    for x in range(12):
        liste = moivre(0.4 ** 12, x, 12)
        gr.polyline([0.5, 0.5 + (1 * liste[0])], [0.5, 0.5 + (1 * liste[1])])
        gr.text(center_x + (liste[0]) * window_width * 1.15, center_y + liste[1] * window_width * 1.15, str(number))
        number += 30

    gr.settransparency(facealpha)
    length = 0

    # colormap
    if 'temp_colormap' in _plt.kwargs:
        triple = _plt.kwargs['temp_colormap']
        del _plt.kwargs['temp_colormap']
        gr.drawimage(0, 1, 1, 0, triple[0], triple[1], triple[2])

        # draw_edges for Colormap: if draw_edges is given, the edges will be drawn
        if 'draw_edges' in _plt.kwargs:
            if _plt.kwargs['draw_edges'] is True:
                gr.setlinecolorind(edgecolor)
                gr.setlinewidth(1.5)

                if is_binedges:
                    if normalization == 'countdensity':
                        norm_factor = 1

                    if normalization == 'countdensity' or normalization == 'pdf':
                        binwidths = []
                        classes = [temp for temp in classes if len(temp) > 0]

                        for i in range(len(binedges) - 1):
                            binwidths.append(binedges[i + 1] - binedges[i])
                        binwidths.append(binedges[-1] - binedges[-2])

                        bin_value = [len(x) / (norm_factor * binwidths[i]) if x[0] is not None else 0
                                     for (i, x) in enumerate(classes)]
                    else:
                        bin_value = [len(x) / (norm_factor) if x[0] is not None else 0
                                     for (i, x) in enumerate(classes)]

                else:
                    bin_value = [len(x) / norm_factor if x is not None else 0 for x in classes]

                length = 0
                mlist = []

                for x in range(len(classes)):
                    if normalization == 'cumcount' or normalization == 'cdf':
                        if classes[x][0] is None:
                            pass
                        else:
                            length = len(classes[x]) / norm_factor + length
                    elif classes[x][0] is None:
                        continue
                    elif normalization == 'pdf' or normalization == 'countdensity':
                        length = bin_value[x]

                    else:
                        length = len(classes[x]) / norm_factor

                    r = (length / border * 0.4) ** (num_bins * 2)
                    liste = moivre(r, (2 * x), num_bins * 2)
                    rect = np.sqrt(liste[0] ** 2 + liste[1] ** 2)

                    if is_rlim:

                        liste2 = moivre(r, (2 * x + 2), (num_bins * 2))
                        mlist.append(liste)
                        mlist.append(liste2)
                        r_min_list = moivre((r_min * 0.4) ** (num_bins * 2), (x * 2), num_bins * 2)
                        r_min_list2 = moivre((r_min * 0.4) ** (num_bins * 2), (x * 2 + 2), num_bins * 2)

                        for kaman in (-1, -2):
                            temporary = abs(np.sqrt(mlist[kaman][0]**2 + mlist[kaman][1]**2))
                            if temporary > (r_max * 0.4):
                                factor = abs(r_max * 0.4 / temporary)
                                mlist[kaman][0] *= factor
                                mlist[kaman][1] *= factor
                        del temporary

                    gr.settransparency(1)
                    gr.setfillintstyle(0)
                    gr.setfillcolorind(edgecolor)

                    if is_binedges:

                        if is_rlim:

                            rect = int(rect * 10000)
                            rect = rect / 10000

                            if round(rect, 3) > r_min * 0.4:
                                try:
                                    gr.drawarc(0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                               0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                               binedges[x] * convert,
                                               binedges[x + 1] * convert)

                                    gr.drawarc(0.5 - r_min * 0.4, 0.5 + r_min * 0.4, 0.5 - r_min * 0.4, 0.5 + r_min * 0.4,
                                               binedges[x] * convert,
                                               binedges[x + 1] * convert)

                                    gr.polyline([0.5 + r_min * 0.4 * np.cos(binedges[x]), 0.5 + min(rect, r_max * 0.4) * np.cos(binedges[x])],
                                                [0.5 + r_min * 0.4 * np.sin(binedges[x]), 0.5 + min(rect, r_max * 0.4) * np.sin(binedges[x])])

                                    gr.polyline([0.5 + r_min * 0.4 * np.cos(binedges[x + 1]),
                                                 0.5 + min(rect, r_max * 0.4) * np.cos(binedges[x + 1])],
                                                [0.5 + r_min * 0.4 * np.sin(binedges[x + 1]),
                                                 0.5 + min(rect, r_max * 0.4) * np.sin(binedges[x + 1])])

                                except Exception:
                                    pass
                        # no rlim
                        else:

                            try:
                                gr.fillarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, binedges[x] * convert,
                                           binedges[x + 1] * convert)

                            except Exception:
                                pass

                    # no binedges
                    else:
                        if is_rlim:
                            rect = int(rect * 10000)
                            rect = rect / 10000

                            if round(rect, 3) > r_min * 0.4:
                                gr.drawarc(0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                           0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                           x * (360 / num_bins),
                                           (x + 1) * (360 / num_bins))
                                gr.drawarc(0.5 - r_min * 0.4, 0.5 + r_min * 0.4, 0.5 - r_min * 0.4, 0.5 + r_min * 0.4,
                                           x * (360 / num_bins), (x + 1) * (360 / num_bins))

                                gr.polyline([0.5 + r_min_list[0], 0.5 + mlist[2 * x][0]],
                                            [0.5 + r_min_list[1], 0.5 + mlist[2 * x][1]])

                                gr.polyline([0.5 + r_min_list2[0], 0.5 + mlist[2 * x + 1][0]],
                                            [0.5 + r_min_list2[1], 0.5 + mlist[2 * x + 1][1]])

                        # Normal (no rlim)
                        else:
                            gr.fillarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, x * (360 / num_bins),
                                       (x + 1) * (360 / num_bins))
                del mlist

    # No Colormap
    else:
        if is_binedges:
            if normalization == 'pdf':
                pass
            elif normalization == 'countdensity':
                norm_factor = 1
            binwidths = []
            classes = [bin for bin in classes if len(bin) > 0]
            for i in range(len(binedges) - 1):
                binwidths.append(binedges[i + 1] - binedges[i])
            binwidths.append(binedges[-1] - binedges[-2])

            if normalization == 'countdensity' or normalization == 'pdf':
                bin_value = [len(x) / (norm_factor * binwidths[i]) for (i, x) in enumerate(classes)]

            else:
                bin_value = [len(x) / norm_factor if x[0] is not None else 0 for x in classes]

        # No binedges
        else:
            if normalization == 'countdensity':
                bin_value = [len(x) / norm_factor if x[0] is not None else 0 for x in classes]

            elif normalization == 'pdf':
                bin_value = [len(x) / (norm_factor) if x[0] is not None else 0 for x in classes]

            else:
                bin_value = [len(x) / norm_factor if x[0] is not None else 0 for x in classes]

        # no stairs
        if _plt.kwargs.get('stairs', False) is False:

            mlist = []

            for x in range(len(classes)):

                if normalization == 'cumcount' or normalization == 'cdf':
                    if classes[x][0] is None:
                        pass
                    else:
                        length = len(classes[x]) / norm_factor + length
                elif normalization == 'pdf' or normalization == 'countdensity':
                    length = bin_value[x]
                elif classes[x][0] is None:
                    continue
                else:
                    length = len(classes[x]) / norm_factor

                r = (length / border * 0.4) ** (num_bins * 2)
                liste = moivre(r, (2 * x), num_bins * 2)
                rect = np.sqrt(liste[0] ** 2 + liste[1] ** 2)

                gr.setfillcolorind(facecolor)
                gr.settransparency(facealpha)
                gr.setfillintstyle(1)

                if is_rlim:
                    liste2 = moivre(r, (2 * x + 2), (num_bins * 2))
                    mlist.append(liste)
                    mlist.append(liste2)
                    r_min_list = moivre((r_min * 0.4) ** (num_bins * 2), (x * 2), num_bins * 2)
                    r_min_list2 = moivre((r_min * 0.4) ** (num_bins * 2), (x * 2 + 2), num_bins * 2)

                    for kaman in (-1, -2):
                        temporary = abs(np.sqrt(mlist[kaman][0] ** 2 + mlist[kaman][1] ** 2))
                        if temporary > (r_max * 0.4):
                            factor = abs(r_max * 0.4 / temporary)
                            mlist[kaman][0] *= factor
                            mlist[kaman][1] *= factor
                    del temporary

                    r = length / border * 0.4
                    if r > r_max * 0.4:
                        r = r_max * 0.4

                if is_binedges:

                    if is_rlim:
                        try:

                            if r > r_min * 0.4:

                                start_angle = binedges[x]
                                end_angle = binedges[x + 1]

                                diff_angle = end_angle - start_angle
                                num_angle = int(diff_angle / (0.2 / convert)) * 1j
                                phi_array = np.array(
                                    np.ogrid[start_angle: end_angle:num_angle], dtype=np.float)

                                arc_1_x = [r * np.cos(phi) + 0.5 for phi in phi_array]
                                arc_1_y = [r * np.sin(phi) + 0.5 for phi in phi_array]

                                arc_2_x = [r_min * 0.4 * np.cos(phi) + 0.5 for phi in phi_array]
                                arc_2_y = [r_min * 0.4 * np.sin(phi) + 0.5 for phi in phi_array]

                                line_1_x = [0.5 + r_min * 0.4 * np.cos(binedges[x]),
                                            0.5 + min(rect, r_max * 0.4) * np.cos(binedges[x])]
                                line_1_y = [0.5 + r_min * 0.4 * np.sin(binedges[x]),
                                            0.5 + min(rect, r_max * 0.4) * np.sin(binedges[x])]

                                line_2_x = [0.5 + r_min * 0.4 * np.cos(binedges[x + 1]),
                                            0.5 + min(rect, r_max * 0.4) * np.cos(binedges[x + 1])]
                                line_2_y = [0.5 + r_min * 0.4 * np.sin(binedges[x + 1]),
                                            0.5 + min(rect, r_max * 0.4) * np.sin(binedges[x + 1])]

                                gr.setfillintstyle(1)
                                gr.fillarea(np.hstack((
                                    line_1_x, arc_1_x, line_2_x[::-1], arc_2_x[::-1],)),
                                    np.hstack((
                                        line_1_y, arc_1_y, line_2_y[::-1], arc_2_y[::-1],))
                                )

                                gr.setfillintstyle(0)
                                gr.setfillcolorind(edgecolor)
                                gr.fillarea(np.hstack((
                                    line_1_x, arc_1_x, line_2_x[::-1], arc_2_x[::-1],)),
                                    np.hstack((
                                        line_1_y, arc_1_y, line_2_y[::-1], arc_2_y[::-1],))
                                )

                        except Exception:
                            pass

                        pass

                    else:
                        try:
                            gr.fillarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, binedges[x] * convert,
                                       binedges[x + 1] * convert)

                        except Exception:
                            pass

                        gr.settransparency(1)
                        gr.setfillintstyle(0)
                        gr.setfillcolorind(edgecolor)
                        try:
                            gr.fillarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, binedges[x] * convert,
                                       binedges[x + 1] * convert)
                        except Exception:
                            pass
                # no binedges
                else:
                    if is_rlim:

                        try:

                            if r > r_min * 0.4:

                                start_angle = x * (360 / num_bins) / convert
                                end_angle = (x + 1) * (360 / num_bins) / convert

                                diff_angle = end_angle - start_angle
                                num_angle = int(diff_angle / (0.2 / convert)) * 1j
                                phi_array = np.array(
                                    np.ogrid[start_angle: end_angle:num_angle], dtype=np.float)

                                arc_1_x = [r * np.cos(phi) + 0.5 for phi in phi_array]
                                arc_1_y = [r * np.sin(phi) + 0.5 for phi in phi_array]

                                arc_2_x = [r_min * 0.4 * np.cos(phi) + 0.5 for phi in phi_array]
                                arc_2_y = [r_min * 0.4 * np.sin(phi) + 0.5 for phi in phi_array]

                                line_1_x = [0.5 + r_min_list[0], 0.5 + mlist[2 * x][0]]
                                line_1_y = [0.5 + r_min_list[1], 0.5 + mlist[2 * x][1]]

                                line_2_x = [0.5 + r_min_list2[0], 0.5 + mlist[2 * x + 1][0]]
                                line_2_y = [0.5 + r_min_list2[1], 0.5 + mlist[2 * x + 1][1]]

                                gr.setfillintstyle(1)
                                gr.fillarea(np.hstack((
                                    line_1_x, arc_1_x, line_2_x[::-1], arc_2_x[::-1],)),
                                    np.hstack((
                                        line_1_y, arc_1_y, line_2_y[::-1], arc_2_y[::-1],))
                                )

                                gr.setfillintstyle(0)
                                gr.setfillcolorind(edgecolor)
                                gr.fillarea(np.hstack((
                                    line_1_x, arc_1_x, line_2_x[::-1], arc_2_x[::-1],)),
                                    np.hstack((
                                        line_1_y, arc_1_y, line_2_y[::-1], arc_2_y[::-1],))
                                )

                        except Exception:
                            pass

                    # no rlim
                    else:
                        gr.fillarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, x * (360 / num_bins),
                                   (x + 1) * (360 / num_bins))

                        gr.settransparency(1)
                        gr.setfillintstyle(0)
                        gr.setfillcolorind(edgecolor)

                        gr.fillarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, x * (360 / num_bins),
                                   (x + 1) * (360 / num_bins))

        # stairs
        else:
            gr.setlinewidth(2.3)
            gr.setlinecolorind(edgecolor)

            # With given bin_edges
            if is_binedges:

                mlist = []
                rectlist = []

                for x in range(len(classes)):
                    if normalization == 'cumcount' or normalization == 'cdf':
                        if classes[x][0] is None:
                            pass
                        else:
                            length = len(classes[x]) / norm_factor + length
                    elif normalization == 'pdf' or normalization == 'countdensity':
                        length = bin_value[x]
                    elif classes[x][0] is None:
                        length = 0
                    else:
                        length = len(classes[x]) / norm_factor

                    r = (length / border * 0.4) ** (num_bins * 2)
                    liste = moivre(r, (2 * x), num_bins * 2)
                    liste2 = moivre(r, (2 * x + 2), (num_bins * 2))
                    mlist.append(liste)
                    mlist.append(liste2)

                    rect = np.sqrt(liste[0] ** 2 + liste[1] ** 2)

                    if is_rlim:

                        for kaman in (-1, -2):
                            temporary = abs(np.sqrt(mlist[kaman][0]**2 + mlist[kaman][1]**2))
                            if temporary > (r_max * 0.4):
                                factor = abs(r_max * 0.4 / temporary)
                                mlist[kaman][0] *= factor
                                mlist[kaman][1] *= factor
                        del temporary

                        if rect < r_min * 0.4:
                            rectlist.append(r_min * 0.4)
                        elif rect > r_max * 0.4:
                            rectlist.append(r_max * 0.4)
                        else:
                            rectlist.append(rect)
                    else:
                        rectlist.append(rect)

                    if is_rlim:

                        rect = int(rect * 10000)
                        rect = rect / 10000

                        if round(rect, 3) > r_min * 0.4:
                            try:
                                gr.drawarc(0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                           0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                           binedges[x] * convert,
                                           binedges[x + 1] * convert)

                                gr.drawarc(0.5 - r_min * 0.4, 0.5 + r_min * 0.4, 0.5 - r_min * 0.4, 0.5 + r_min * 0.4,
                                           binedges[x] * convert,
                                           binedges[x + 1] * convert)

                            except Exception:
                                pass
                    else:
                        try:
                            gr.drawarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, binedges[x] * convert,
                                       binedges[x + 1] * convert)
                        except Exception:
                            pass

                if is_rlim:
                    startx = max(rectlist[0] * np.cos(binedges[0]), r_min * 0.4 * np.cos(binedges[0]))
                    starty = max(rectlist[0] * np.sin(binedges[0]), r_min * 0.4 * np.sin(binedges[0]))

                    for x in range(len(binedges)):

                        if not (binedges[0] == 0 and binedges[len(binedges) - 1] == 2 * np.pi and (
                                x == len(binedges) - 1 or x == 0)):
                            try:
                                gr.polyline([0.5 + startx, 0.5 + rectlist[x] * np.cos(binedges[x])],
                                            [0.5 + starty, 0.5 + rectlist[x] * np.sin(binedges[x])])
                            except Exception:
                                pass
                        try:
                            startx = (rectlist[x] * np.cos(binedges[x + 1]))
                            starty = (rectlist[x] * np.sin(binedges[x + 1]))
                        except Exception:
                            pass

                    gr.polyline([0.5 + r_min * 0.4 * np.cos(binedges[0]),
                                 0.5 + rectlist[0] * np.cos(binedges[0])],
                                [0.5 + r_min * 0.4 * np.sin(binedges[0]),
                                 0.5 + rectlist[0] * np.sin(binedges[0])])

                    gr.polyline([0.5 + r_min * 0.4 * np.cos(binedges[-1]),
                                 0.5 + rectlist[-1] * np.cos(binedges[-1])],
                                [0.5 + r_min * 0.4 * np.sin(binedges[-1]),
                                 0.5 + rectlist[-1] * np.sin(binedges[-1])])
                # no rlim
                else:
                    startx = 0
                    starty = 0
                    for x in range(len(binedges)):
                        pass
                        try:
                            gr.polyline([0.5 + startx, 0.5 + rectlist[x] * np.cos(binedges[x])],
                                        [0.5 + starty, 0.5 + rectlist[x] * np.sin(binedges[x])])
                            startx = (rectlist[x] * np.cos(binedges[x + 1]))
                            starty = (rectlist[x] * np.sin(binedges[x + 1]))
                        except Exception:
                            pass

                    if binedges[0] == 0 and binedges[-1] == 2 * np.pi:
                        gr.polyline([0.5 + rectlist[0] * np.cos(binedges[0]), 0.5 + startx],
                                    [0.5 + rectlist[0] * np.sin(binedges[0]), 0.5 + starty])
                    else:
                        gr.polyline([0.5 + rectlist[-1] * np.cos(binedges[-1]), 0.5],
                                    [0.5 + rectlist[-1] * np.sin(binedges[-1]), 0.5])

            # Normal stairs (no bin_edges)
            else:

                mlist = []
                for x in range(len(classes)):

                    if normalization == 'cumcount' or normalization == 'cdf':
                        if classes[x][0] is None:
                            pass
                        else:
                            length = length + len(classes[x]) / norm_factor
                    elif classes[x][0] is None:
                        length = 0
                    else:
                        length = len(classes[x]) / norm_factor

                    r = (length / border * 0.4) ** (num_bins * 2)
                    liste = moivre(r, (2 * x), num_bins * 2)
                    liste2 = moivre(r, (2 * x + 2), (num_bins * 2))
                    mlist.append(liste)
                    mlist.append(liste2)

                    rect = np.sqrt(liste[0] ** 2 + liste[1] ** 2)

                    gr.setfillcolorind(edgecolor)

                    if is_rlim:

                        for kaman in (-1, -2):
                            temporary = abs(np.sqrt(mlist[kaman][0] ** 2 + mlist[kaman][1] ** 2))
                            if temporary > (r_max * 0.4):
                                factor = abs(r_max * 0.4 / temporary)
                                mlist[kaman][0] *= factor
                                mlist[kaman][1] *= factor
                        del temporary

                        rect = int(rect * 10000)
                        rect = rect / 10000

                        if round(rect, 3) > r_min * 0.4:
                            gr.drawarc(0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                       0.5 - min(rect, r_max * 0.4), 0.5 + min(rect, r_max * 0.4),
                                       x * (360 / num_bins),
                                       (x + 1) * (360 / num_bins))
                            gr.drawarc(0.5 - r_min * 0.4, 0.5 + r_min * 0.4, 0.5 - r_min * 0.4, 0.5 + r_min * 0.4,
                                       x * (360 / num_bins),
                                       (x + 1) * (360 / num_bins))
                    # no rlim
                    else:
                        gr.drawarc(0.5 - rect, 0.5 + rect, 0.5 - rect, 0.5 + rect, x * (360 / num_bins),
                                   (x + 1) * (360 / num_bins))
                if is_rlim:
                    for x in range(len(classes) * 2):
                        if x > 1 and x % 2 == 0:
                            rect1 = np.sqrt(mlist[x][0]**2 + mlist[x][1]**2)
                            rect1 = round(int(rect1 * 10000) / 10000, 3)
                            rect2 = np.sqrt(mlist[x - 1][0]**2 + mlist[x - 1][1]**2)
                            rect2 = round(int(rect2 * 10000) / 10000, 3)

                            if rect1 < (r_min * 0.4) and rect2 < (r_min * 0.4):
                                continue
                            if rect1 < r_min * 0.4:
                                mlist[x][0] = r_min * 0.4 * np.cos(np.pi / len(classes) * x)
                                mlist[x][1] = r_min * 0.4 * np.sin(np.pi / len(classes) * x)

                            if rect2 < r_min * 0.4:
                                mlist[x - 1][0] = r_min * 0.4 * np.cos(np.pi / len(classes) * x)
                                mlist[x - 1][1] = r_min * 0.4 * np.sin(np.pi / len(classes) * x)

                            gr.polyline([0.5 + mlist[x][0], 0.5 + mlist[x - 1][0]],
                                        [0.5 + mlist[x][1], 0.5 + mlist[x - 1][1]])

                    mlist[-1][0] = max(mlist[-1][0], r_min * 0.4 * np.cos(0))
                    mlist[-1][1] = max(mlist[-1][1], r_min * 0.4 * np.sin(0))
                    mlist[0][0] = max(mlist[0][0], r_min * 0.4 * np.cos(0))
                    mlist[0][1] = max(mlist[0][1], r_min * 0.4 * np.sin(0))

                    gr.polyline([0.5 + mlist[-1][0], 0.5 + mlist[0][0]],
                                [0.5 + mlist[-1][1], 0.5 + mlist[0][1]])

                else:
                    for x in range(len(classes) * 2):
                        if x > 1 and x % 2 == 0:
                            gr.polyline([0.5 + mlist[x][0], 0.5 + mlist[x - 1][0]],
                                        [0.5 + mlist[x][1], 0.5 + mlist[x - 1][1]])
                    gr.polyline([0.5 + mlist[-1][0], 0.5 + mlist[0][0]],
                                [0.5 + mlist[-1][1], 0.5 + mlist[0][1]])

    if temp_edge is not None:
        red = (temp_edge % 256) / 255
        green = ((temp_edge >> 8) % 256) / 255
        blue = ((temp_edge >> 16) % 256) / 255
        gr.setcolorrep(1004, red, green, blue)

    if temp_face is not None:
        red = (temp_face % 256) / 255
        green = ((temp_face >> 8) % 256) / 255
        blue = ((temp_face >> 16) % 256) / 255
        gr.setcolorrep(1004, red, green, blue)

    gr.updatews()


def _plot_args(args, fmt='xys'):
    global _plt
    args = list(args)
    parsed_args = []
    column = 0
    while args or column > 0:
        # Try to read x, y, z and c
        x = y = z = c = None
        if fmt == 'xyuv':
            if len(args) == 4:
                x, y, u, v = args
                x = _convert_to_array(x)
                y = _convert_to_array(y)
                u = _convert_to_array(u, always_flatten=True)
                v = _convert_to_array(v, always_flatten=True)
                if u.shape != (len(x) * len(y),):
                    raise TypeError('expected an array of len(y) * len(x) u values')
                if v.shape != (len(x) * len(y),):
                    raise TypeError('expected an array of len(y) * len(x) v values')
                parsed_args.append((x, y, u.reshape(len(y), len(x)), v.reshape(len(y), len(x)), ""))
                break
            else:
                raise TypeError('expected x, y, u and v')
        if fmt == 'xyzc' and len(args) == 1:
            try:
                a = np.array(args[0])
                if max(a.shape) == 1:
                    a.shape = [1, 1]
                else:
                    a.shape = [i for i in a.shape if i != 1]
                if len(a.shape) == 1:
                    a.shape = [len(a), 1]
                if a.dtype == complex:
                    raise TypeError()
                x = np.arange(1, a.shape[1] + 1)
                y = np.arange(1, a.shape[0] + 1)
                z = a.astype(np.float64)
                args.pop(0)
            except TypeError:
                x = y = z = c = None

        if x is None or column > 0:
            if column == 0:
                a = np.array(args[0])
                args.pop(0)
            if len(a.shape) == 2 and a.shape[0] == 2:
                x, y = a[0, :], a[1, :]
            else:
                if fmt == 'xys':
                    if len(a.shape) == 2:
                        x = np.arange(1, a.shape[1] + 1)
                        y = a[column, :]
                        if column + 1 < a.shape[0]:
                            column += 1
                        else:
                            column = 0
                            break
                    else:
                        a = _convert_to_array(args.pop(0), may_be_2d=True)
                        try:
                            x = a
                            y = _convert_to_array(args[0], xvalues=x)
                            args.pop(0)
                        except (TypeError, IndexError):
                            y = a
                            x = np.arange(1, len(a) + 1)
                elif fmt == 'y':
                    y = a
                    x = np.arange(1, len(a) + 1)
                elif fmt == 'xyac' or fmt == 'xyzc':
                    try:
                        x = a
                        if fmt == 'xyac' and len(args) >= 1:
                            y = _convert_to_array(args[0], xvalues=x)
                        if len(args) >= 2:
                            y = _convert_to_array(args[0])
                            xy_y, xy_x = np.meshgrid(y, x)
                            xy_x.shape = np.prod(xy_x.shape)
                            xy_y.shape = np.prod(xy_y.shape)
                            xy = np.stack((xy_x, xy_y), axis=1)
                            if fmt == 'xyzc':
                                z = _convert_to_array(args[1], xvalues=xy, always_flatten=True)
                                if z.shape != x.shape or z.shape != y.shape:
                                    z.shape = (len(y), len(x))
                            else:
                                z = _convert_to_array(args[1], xvalues=x)
                        if len(args) >= 3:
                            if fmt == 'xyzc':
                                c = _convert_to_array(args[2], xvalues=xy, always_flatten=True)
                                c.shape = (len(y), len(x))
                            else:
                                c = _convert_to_array(args[2], xvalues=x)
                    except TypeError:
                        pass
                    if y is None:
                        raise TypeError('expected callable or sequence of real values')
                    for v in (y, z, c):
                        if v is None:
                            break
                        args.pop(0)
                else:
                    raise TypeError("Invalid format: '{}'".format(fmt))

        # Remove unused values
        if z is None:
            if len(x) > len(y):
                x = x[:len(y)]
            elif len(x) < len(y):
                y = y[:len(x)]
        else:
            if fmt == 'xyzc':
                if z.shape[0] > len(y):
                    z = z[:len(y), :]
                elif z.shape[0] < len(y):
                    y = y[:z.shape[0]]
                if len(z.shape) > 1 and z.shape[1] > len(x):
                    z = z[:, len(x)]
                elif len(z.shape) > 1 and z.shape[1] < len(x):
                    x = x[:z.shape[1]]
                if c is not None:
                    if c.shape[0] > len(y):
                        c = c[:len(y), :]
                    elif c.shape[0] < len(y):
                        y = y[:c.shape[0]]
                        z = z[:c.shape[0], 0]
                    if c.shape[1] > len(x):
                        c = c[:, len(x)]
                    elif c.shape[1] < len(x):
                        x = x[:c.shape[1]]
                        z = z[:, :c.shape[1]]
                if z is not None:
                    z = np.ascontiguousarray(z)
                if c is not None:
                    c = np.ascontiguousarray(c)
            else:
                if len(x) > len(y):
                    x = x[:len(y)]
                else:
                    y = y[:len(x)]
                if len(z) > len(x):
                    z = z[:len(x)]
                else:
                    x = x[:len(z)]
                    y = y[:len(z)]
                if c is not None:
                    if len(c) > len(z):
                        c = c[:len(z)]
                    else:
                        x = x[:len(c)]
                        y = y[:len(c)]
                        z = z[:len(c)]
        # Try to read the spec if available
        spec = ""
        if fmt == 'xys' and len(args) > 0 and isinstance(args[0], basestring):
            spec = args.pop(0)
        if fmt == 'y' and args:
            z = args.pop(0)
            if args:
                c = args.pop(0)
        parsed_args.append((x, y, z, c, spec))
    return parsed_args
