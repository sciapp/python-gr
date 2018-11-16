# coding: utf-8
"""
This module offers a simple, matlab-style API built on top of the gr package.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import functools
import warnings
import numpy as np
import gr
import gr3


try:
    basestring
except NameError:
    basestring = str


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
    >>> mlab.plot(x, lambda x: x: x**3 + x**2 + x)
    >>> # Plot y, using its indices for the x values
    >>> mlab.plot(y)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    if _plt.kwargs['ax']:
        _plt.args += _plot_args(args)
    else:
        _plt.args = _plot_args(args)
    _plot_data(kind='line')


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
    _plot_data(kind='line')


@_close_gks_on_error
def step(*args, **kwargs):
    """
    Draw one or more step or staircase plots.

    This function can receive one or more of the following:

    - x values and y values, or
    - x values and a callable to determine y values, or
    - y values only, with their indices as x values

    :param args: the data to plot
    :param where: pre, mid or post, to decide where the step between to y values should be placed

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = 2*x+4
    >>> # Plot x and y
    >>> mlab.step(x, y)
    >>> # Plot x and a callable
    >>> mlab.step(x, lambda x: x: x**3 + x**2 + x)
    >>> # Plot y, using its indices for the x values
    >>> mlab.step(y)
    >>> # Use next y step directly after x each position
    >>> mlab.step(y, where='pre')
    >>> # Use next y step between two x positions
    >>> mlab.step(y, where='pre')
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
    _plot_data(kind='step')


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
    _plot_data(kind='scatter')


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
    >>> mlab.quiver(x, y, u, b)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args((x, y, u, v), fmt='xyuv')
    _plot_data(kind='quiver')


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
    _plot_data(kind='polar')


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
    _plot_data(kind='trisurf')


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
    _plot_data(kind='tricont')


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
    _plot_data(kind='stem')


def _hist(x, nbins=0):
    x = np.array(x)
    x_min = x.min()
    x_max = x.max()
    if nbins <= 1:
        nbins = int(np.round(3.3 * np.log10(len(x)))) + 1
    binned_x = np.array(np.floor((x - x_min) / (x_max - x_min) * nbins), dtype=int)
    binned_x[binned_x == nbins] = nbins - 1
    counts = np.bincount(binned_x)
    edges = np.linspace(x_min, x_max, nbins + 1)
    return counts, edges


@_close_gks_on_error
def histogram(x, num_bins=0, **kwargs):
    r"""
    Draw a histogram.

    If **num_bins** is 0, this function computes the number of
    bins as :math:`\text{round}(3.3\cdot\log_{10}(n))+1` with n as the number
    of elements in x, otherwise the given number of bins is used for the
    histogram.

    :param x: the values to draw as histogram
    :param num_bins: the number of bins in the histogram

    **Usage examples:**

    >>> # Create example data
    >>> x = np.random.uniform(-1, 1, 100)
    >>> # Draw the histogram
    >>> mlab.histogram(x)
    >>> # Draw the histogram with 19 bins
    >>> mlab.histogram(x, num_bins=19)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    hist, bins = _hist(x, num_bins)
    _plt.args = [(np.array(bins), np.array(hist), None, None, "")]
    _plot_data(kind='hist')


@_close_gks_on_error
def contour(*args, **kwargs):
    """
    Draw a contour plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a contour plot. It can receive one
    or more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a NxM grid, or
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
    >>> z = np.sin(x[:, np.newaxis]) + np.cos(y[np.newaxis, :])
    >>> # Draw the contour plot
    >>> mlab.contour(x, y, z, levels=10)
    >>> # Draw the contour plot using a callable
    >>> mlab.contour(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    _plot_data(kind='contour')


@_close_gks_on_error
def contourf(*args, **kwargs):
    """
    Draw a filled contour plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a filled contour plot. It can
    receive one or more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a NxM grid, or
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
    >>> z = np.sin(x[:, np.newaxis]) + np.cos(y[np.newaxis, :])
    >>> # Draw the filled contour plot
    >>> mlab.contourf(x, y, z, levels=10)
    >>> # Draw the filled contour plot using a callable
    >>> mlab.contourf(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    _plot_data(kind='contourf')


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
    _plot_data(kind='hexbin')


@_close_gks_on_error
def heatmap(data, **kwargs):
    """
    Draw a heatmap.

    This function uses the current colormap to display a two-dimensional
    array as a heatmap. The array is drawn with its first value in the upper
    left corner, so in some cases it may be neccessary to flip the columns
    (see the example below).

    By default the function will use the row and column indices for the x- and
    y-axes, so setting the axis limits is recommended. Also note that the
    values in the array must lie within the current z-axis limits so it may
    be neccessary to adjust these limits or clip the range of array values.

    :param data: the heatmap data

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-2, 2, 40)
    >>> y = np.linspace(0, np.pi, 20)
    >>> z = np.sin(x[np.newaxis, :]) + np.cos(y[:, np.newaxis])
    >>> # Draw the heatmap
    >>> mlab.heatmap(z[::-1, :], xlim=(-2, 2), ylim=(0, np.pi))
    """
    global _plt
    data = np.array(data, copy=False)
    if len(data.shape) != 2:
        raise ValueError('expected 2-D array')
    height, width = data.shape
    _plt.kwargs.update(kwargs)
    _plt.args = [(np.arange(width), np.arange(height), data, None, "")]
    _plot_data(kind='heatmap')


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
    _plot_data(kind='shade')


@_close_gks_on_error
def wireframe(*args, **kwargs):
    """
    Draw a three-dimensional wireframe plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a wireframe plot. It can receive one
    or more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a NxM grid, or
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
    >>> z = np.sin(x[:, np.newaxis]) + np.cos(y[np.newaxis, :])
    >>> # Draw the wireframe plot
    >>> mlab.wireframe(x, y, z)
    >>> # Draw the wireframe plot using a callable
    >>> mlab.wireframe(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    _plot_data(kind='wireframe')


@_close_gks_on_error
def surface(*args, **kwargs):
    """
    Draw a three-dimensional surface plot.

    This function uses the current colormap to display a either a series of
    points or a two-dimensional array as a surface plot. It can receive one or
    more of the following:

    - x values, y values and z values, or
    - N x values, M y values and z values on a NxM grid, or
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
    >>> z = np.sin(x[:, np.newaxis]) + np.cos(y[np.newaxis, :])
    >>> # Draw the surface plot
    >>> mlab.surface(x, y, z)
    >>> # Draw the surface plot using a callable
    >>> mlab.surface(x, y, lambda x, y: np.sin(x) + np.cos(y))
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = _plot_args(args, fmt='xyzc')
    _plot_data(kind='surface')


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
    _plot_data(kind='plot3')


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
    _plot_data(kind='scatter3')


@_close_gks_on_error
def isosurface(v, **kwargs):
    """
    Draw an isosurface.

    This function can draw an image either from reading a file or using a
    two-dimensional array and the current colormap. Values greater than the
    isovalue will be seen as outside the isosurface, while values less than
    the isovalue will be seen as inside the isosurface.

    :param v: the volume data
    :param isovalue: the isovalue

    **Usage examples:**

    >>> # Create example data
    >>> x = np.linspace(-1, 1, 40)[:, np.newaxis, np.newaxis]
    >>> y = np.linspace(-1, 1, 40)[np.newaxis, :, np.newaxis]
    >>> z = np.linspace(-1, 1, 40)[np.newaxis, np.newaxis, :]
    >>> v = 1-(x**2 + y**2 + z**2)**0.5
    >>> # Draw an image from a 2d array
    >>> mlab.isosurface(v, isovalue=0.2)
    """
    global _plt
    _plt.kwargs.update(kwargs)
    _plt.args = [(None, None, v, None, '')]
    _plot_data(kind='isosurface')


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
    _plot_data(kind='imshow')


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
    _plot_data(title=title)


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
    _plot_data(xlabel=x_label)


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
    _plot_data(ylabel=y_label)


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
    _plot_data(zlabel=z_label)


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
    _plot_data(xlim=(x_min, x_max), adjust_xlim=adjust)


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
    _plot_data(ylim=(y_min, y_max), adjust_ylim=adjust)


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
    _plot_data(zlim=(z_min, z_max), adjust_zlim=adjust)


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
    _plot_data(xlog=xlog)


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
    _plot_data(ylog=ylog)


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
    _plot_data(zlog=zlog)


@_close_gks_on_error
def xflip(xflip=True):
    """
    Enable or disable x-axis flipping/reversal.

    :param xflip: whether or not the x-axis should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the x-axis
    >>> mlab.xlog()
    >>> # Restores the x-axis
    >>> mlab.xlog(False)
    """
    _plot_data(xflip=xflip)


@_close_gks_on_error
def yflip(yflip=True):
    """
    Enable or disable y-axis flipping/reversal.

    :param yflip: whether or not the y-axis should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the y-axis
    >>> mlab.ylog()
    >>> # Restores the y-axis
    >>> mlab.ylog(False)
    """
    _plot_data(yflip=yflip)


@_close_gks_on_error
def zflip(zflip=True):
    """
    Enable or disable z-axis flipping/reversal.

    :param zflip: whether or not the z-axis should be flipped

    **Usage examples:**

    >>> # Flips/Reverses the z-axis
    >>> mlab.zlog()
    >>> # Restores the z-axis
    >>> mlab.zlog(False)
    """
    _plot_data(zflip=zflip)


@_close_gks_on_error
def colormap(colormap=''):
    """
    Get or set the colormap for the current plot or enable manual colormap control.

    :param colormap:
        - The name of a gr colormap
        - One of the gr colormap constants (**gr.COLORMAP_...**)
        - A list of red-green-blue tuples as colormap
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
    _plot_data(colormap=colormap)


@_close_gks_on_error
def tilt(tilt):
    """
    Set the 3d axis tilt of the current plot.

    The tilt can be any value between 0 and 90, and controls the angle
    between the viewer and the X-Y-plane.

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
    _plot_data(tilt=tilt)


@_close_gks_on_error
def rotation(rotation):
    """
    Set the 3d axis rotation of the current plot.

    The rotation can be any value between 0 and 90, and controls the angle
    between the viewer projected onto the X-Y-plane and the x-axis.

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
    _plot_data(rotation=rotation)


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
    _plot_data(labels=labels, **kwargs)


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
    reds, greens, blues = list(zip(*colormap))[:3]
    if len(colormap) != 256:
        reds = np.interp(np.arange(256), np.linspace(0, 255, len(colormap)), reds)
        greens = np.interp(np.arange(256), np.linspace(0, 255, len(colormap)), greens)
        blues = np.interp(np.arange(256), np.linspace(0, 255, len(colormap)), blues)
    for i in range(256):
        gr.setcolorrep(1000 + i, reds[i], greens[i], blues[i])


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
        if dpi > 200:
            width, height = tuple(x * dpi / 100 for x in _plt.kwargs['size'])
        else:
            width, height = _plt.kwargs['size']

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

    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf'):
        if kind in ('surface', 'trisurf'):
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
    if kind in ('contour', 'contourf', 'heatmap', 'hexbin', 'quiver'):
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
            v_min -= 0.1 * v_min
            v_max += 0.1 * v_max
    return v_min, v_max


def _minmax(kind=None):
    global _plt
    x_min = y_min = z_min = float('infinity')
    x_max = y_max = z_max = float('-infinity')
    x_step = y_step = float('-infinity')

    for x, y, z, c, spec in _plt.args:
        x_min = min(np.nanmin(x), x_min)
        x_max = max(np.nanmax(x), x_max)
        y_min = min(np.nanmin(y), y_min)
        y_max = max(np.nanmax(y), y_max)
        if z is not None:
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
    x_min, x_max = _fix_minmax(x_min, x_max)
    y_min, y_max = _fix_minmax(y_min, y_max)
    z_min, z_max = _fix_minmax(z_min, z_max)
    x_range = _plt.kwargs.get('xlim', (x_min, x_max))
    y_range = _plt.kwargs.get('ylim', (y_min, y_max))
    z_range = _plt.kwargs.get('zlim', (z_min, z_max))

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

    _plt.kwargs['xrange'] = x_range
    _plt.kwargs['yrange'] = y_range
    _plt.kwargs['zrange'] = z_range


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
    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'polar', 'trisurf'):
        major_count = 2
    else:
        major_count = 5

    x_min, x_max = _plt.kwargs['xrange']
    if not scale & gr.OPTION_X_LOG:
        if _plt.kwargs.get('adjust_xlim', True):
            x_min, x_max = gr.adjustlimits(x_min, x_max)
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
    if kind in ('hist', 'stem') and 'ylim' not in _plt.kwargs:
        y_min = 0
    if not scale & gr.OPTION_Y_LOG:
        if _plt.kwargs.get('adjust_ylim', True):
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
    if kind == 'polar':
        gr.setwindow(-1, 1, -1, 1)
    else:
        gr.setwindow(x_min, x_max, y_min, y_max)

    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf'):
        z_min, z_max = _plt.kwargs['zrange']
        if not scale & gr.OPTION_Z_LOG:
            if _plt.kwargs.get('adjust_zlim', True):
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

    _plt.kwargs['scale'] = scale
    gr.setscale(scale)


def _draw_axes(kind, pass_=1):
    global _plt
    viewport = _plt.kwargs['viewport']
    vp = _plt.kwargs['vp']
    x_tick, x_org, x_major_count = _plt.kwargs['xaxis']
    y_tick, y_org, y_major_count = _plt.kwargs['yaxis']

    gr.setlinecolorind(1)
    gr.setlinewidth(1)
    diag = ((viewport[1] - viewport[0])**2 + (viewport[3] - viewport[2])**2)**0.5
    charheight = max(0.018 * diag, 0.012)
    gr.setcharheight(charheight)
    ticksize = 0.0075 * diag
    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf'):
        z_tick, z_org, z_major_count = _plt.kwargs['zaxis']
        if pass_ == 1:
            gr.grid3d(x_tick, 0, z_tick, x_org[0], y_org[1], z_org[0], 2, 0, 2)
            gr.grid3d(0, y_tick, 0, x_org[0], y_org[1], z_org[0], 0, 2, 0)
        else:
            gr.axes3d(x_tick, 0, z_tick, x_org[0], y_org[0], z_org[0], x_major_count, 0, z_major_count, -ticksize)
            gr.axes3d(0, y_tick, 0, x_org[1], y_org[0], z_org[0], 0, y_major_count, 0, ticksize)
    else:
        if kind in ('heatmap', 'shade'):
            ticksize = -ticksize
        else:
            gr.grid(x_tick, y_tick, 0, 0, x_major_count, y_major_count)
        gr.axes(x_tick, y_tick, x_org[0], y_org[0], x_major_count, y_major_count, ticksize)
        gr.axes(x_tick, y_tick, x_org[1], y_org[1], -x_major_count, -y_major_count, -ticksize)

    if 'title' in _plt.kwargs:
        gr.savestate()
        gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_TOP)
        gr.textext(0.5 * (viewport[0] + viewport[1]), vp[3], _plt.kwargs['title'])
        gr.restorestate()

    if kind in ('wireframe', 'surface', 'plot3', 'scatter3', 'trisurf'):
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


def _draw_polar_axes():
    global _plt
    viewport = _plt.kwargs['viewport']
    diag = ((viewport[1] - viewport[0])**2 + (viewport[3] - viewport[2])**2)**0.5
    charheight = max(0.018 * diag, 0.012)

    window = _plt.kwargs['window']
    r_min, r_max = window[2], window[3]

    gr.savestate()
    gr.setcharheight(charheight)
    gr.setlinetype(gr.LINETYPE_SOLID)

    tick = 0.5 * gr.tick(r_min, r_max)
    n = int(round((r_max - r_min) / tick + 0.5))
    for i in range(n + 1):
        r = i / n
        if i % 2 == 0:
            gr.setlinecolorind(88)
            if i > 0:
                gr.drawarc(-r, r, -r, r, 0, 180)
                gr.drawarc(-r, r, -r, r, 180, 360)
            gr.settextalign(gr.TEXT_HALIGN_LEFT, gr.TEXT_VALIGN_HALF)
            x, y = gr.wctondc(0.05, r)
            gr.text(x, y, "%g" % (r_min + i * tick))
        else:
            gr.setlinecolorind(90)
            gr.drawarc(-r, r, -r, r, 0, 180)
            gr.drawarc(-r, r, -r, r, 180, 360)
    for alpha in range(0, 360, 45):
        sinf = np.sin(np.radians(alpha + 90))
        cosf = np.cos(np.radians(alpha + 90))
        gr.polyline([sinf, 0], [cosf, 0])
        gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_HALF)
        x, y = gr.wctondc(1.1 * sinf, 1.1 * cosf)
        gr.textext(x, y, "%d\xb0" % alpha)
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


def _colorbar(off=0.0, colors=256):
    global _plt
    gr.savestate()
    viewport = _plt.kwargs['viewport']
    zmin, zmax = _plt.kwargs['zrange']
    gr.setwindow(0, 1, zmin, zmax)
    gr.setviewport(viewport[1] + 0.02 + off, viewport[1] + 0.05 + off,
                   viewport[2], viewport[3])

    if colors == 1:
        data = [1000]
    else:
        data = [1000 + int(255 * i / (colors - 1)) for i in range(colors)]

    gr.cellarray(0, 1, zmax, zmin, 1, colors, data)
    diag = ((viewport[1] - viewport[0])**2 + (viewport[3] - viewport[2])**2)**0.5
    charheight = max(0.016 * diag, 0.012)
    gr.setcharheight(charheight)
    if _plt.kwargs['scale'] & gr.OPTION_Z_LOG:
        gr.setscale(gr.OPTION_Y_LOG)
        gr.axes(0, 2, 1, zmin, 0, 1, 0.005)
    else:
        ztick = 0.5 * gr.tick(zmin, zmax)
        gr.axes(0, ztick, 1, zmin, 0, 1, 0.005)
    gr.restorestate()


def _plot_data(**kwargs):
    global _plt
    _plt.kwargs.update(kwargs)
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
        else:
            _draw_axes(kind)

    _set_colormap()
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
        elif kind == 'quiver':
            u = z
            v = c
            gr.quiver(len(x), len(y), x, y, u, v, True)
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
            h = [z_min + i / num_levels * (z_max - z_min) for i in range(num_levels)]
            if x.shape == y.shape == z.shape:
                x, y, z = gr.gridit(x, y, z, 200, 200)
                z = np.array(z)
            else:
                z = np.ascontiguousarray(z)
            z.shape = np.prod(z.shape)
            gr.contour(x, y, h, z, 1000)
            _colorbar(colors=num_levels)
        elif kind == 'contourf':
            z_min, z_max = _plt.kwargs['zrange']
            gr.setspace(z_min, z_max, 0, 90)
            scale = _plt.kwargs['scale']
            num_levels = _plt.kwargs.get('levels', 20)
            h = [z_min + i / num_levels * (z_max - z_min) for i in range(num_levels)]
            gr.setscale(scale)
            if x.shape == y.shape == z.shape:
                x, y, z = gr.gridit(x, y, z, 200, 200)
                z = np.array(z)
            else:
                z = np.ascontiguousarray(z)
            z.shape = np.prod(z.shape)
            _colorbar(colors=num_levels)
            gr.setlinecolorind(1)
            gr.contourf(x, y, h, z, 0)
        elif kind == 'hexbin':
            nbins = _plt.kwargs.get('nbins', 40)
            cntmax = gr.hexbin(x, y, nbins)
            if cntmax > 0:
                _plt.kwargs['zrange'] = (0, cntmax)
                _colorbar()
        elif kind == 'heatmap':
            x_min, x_max, y_min, y_max = _plt.kwargs['window']
            height, width = z.shape
            cmap = _colormap()
            icmap = np.zeros(256, np.uint32)
            for i in range(256):
                r, g, b, a = cmap[i]
                icmap[i] = (int(r * 255) << 0) + (int(g * 255) << 8) + (int(b * 255) << 16) + (int(a * 255) << 24)
            z_min, z_max = _plt.kwargs.get('zlim', (np.min(z), np.max(z)))
            if z_max < z_min:
                z_max, z_min = z_min, z_max
            if z_max > z_min:
                data = (z - z_min) / (z_max - z_min) * 255
            else:
                data = np.zeros((height, width))
            rgba = np.zeros((height, width), np.uint32)
            for x in range(width):
                for y in range(height):
                    rgba[y, x] = icmap[int(data[y, x])]
            gr.drawimage(x_min, x_max, y_min, y_max, width, height, rgba)
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
        elif kind == 'polar':
            gr.uselinespec(spec)
            _plot_polar(x, y)
        elif kind == 'trisurf':
            gr.trisurface(x, y, z)
            _draw_axes(kind, 2)
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


def _plot_polar(theta, rho):
    global _plt
    window = _plt.kwargs['window']
    r_min, r_max = window[2:]
    tick = 0.5 * gr.tick(r_min, r_max)
    n = int(round((r_max - r_min) / tick + 0.5))
    r_max = r_min + n * tick
    rho = (rho - r_min) / (r_max - r_min)
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
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
        a = np.array(a, copy=False)
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
        a = np.stack((np.real(a), np.imag(a)), axis=1)
        dimension = 2
    elif a.dtype != np.float64:
        try:
            a = a.astype(np.float64)
        except (TypeError, ValueError):
            raise TypeError("expected a sequence of real values, but got '{}'".format(a.dtype))
    return a


def _plot_args(args, fmt='xys'):
    global _plt
    args = list(args)
    parsed_args = []
    while args:
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
                x = np.arange(1, a.shape[0] + 1)
                y = np.arange(1, a.shape[1] + 1)
                z = a.astype(np.float64)
                args.pop(0)
            except TypeError:
                x = y = z = c = None

        if x is None:
            a = _convert_to_array(args.pop(0), may_be_2d=True)

            if len(a.shape) == 2:
                x, y = a[:, 0], a[:, 1]
            else:
                if fmt == 'xys':
                    try:
                        x = a
                        y = _convert_to_array(args[0], xvalues=x)
                        args.pop(0)
                    except (TypeError, IndexError):
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
                                    z.shape = (len(x), len(y))
                            else:
                                z = _convert_to_array(args[1], xvalues=x)
                        if len(args) >= 3:
                            if fmt == 'xyzc':
                                c = _convert_to_array(args[2], xvalues=xy, always_flatten=True)
                                c.shape = (len(x), len(y))
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
                if z.shape[0] > len(x):
                    z = z[:len(x), :]
                elif z.shape[0] < len(x):
                    x = x[:z.shape[0]]
                if len(z.shape) > 1 and z.shape[1] > len(y):
                    z = z[:, len(y)]
                elif len(z.shape) > 1 and z.shape[1] < len(y):
                    y = y[:z.shape[1]]
                if c is not None:
                    if c.shape[0] > len(x):
                        c = c[:len(x), :]
                    elif c.shape[0] < len(x):
                        x = x[:c.shape[0]]
                        z = z[:c.shape[0], 0]
                    if c.shape[1] > len(y):
                        c = c[:, len(y)]
                    elif c.shape[1] < len(y):
                        y = y[:c.shape[1]]
                        z = z[:, :c.shape[1]]
                if z is not None:
                    z = np.ascontiguousarray(z.T)
                if c is not None:
                    c = np.ascontiguousarray(c.T)
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
        parsed_args.append((x, y, z, c, spec))
    return parsed_args
