# -*- coding: utf-8 -*-
"""
This is a procedural interface to the GR plotting library,
which may be imported directly, e.g.:

import gr
"""
import collections
import functools
import os
import sys
import warnings
import numpy as np
from numpy import array, ndarray, float64, int32, empty, prod
from ctypes import c_int, c_double, c_char_p, c_void_p, c_uint8, c_uint, c_ulong
from ctypes import byref, POINTER, addressof, CDLL, CFUNCTYPE, Structure
from ctypes import create_string_buffer, cast
from sys import version_info, platform
from platform import python_implementation
# local library
try:
    from gr._version import __version__, __revision__
except ImportError:
    try:
        # If the _version module is not found, this might be a git clone and
        # vcversioner might find the version. Alternatively it might be a
        # source archive with no git information, in which case we do not want
        # vcversioner to print an error and exit. Also, we do not want
        # vcversioner to write out a version file, as this path might be read
        # only.
        import vcversioner
        vcversioner._print = lambda *args, **kwargs: None
        _version = vcversioner.find_version(version_file=None)
        __version__ = _version.version
        __revision__ = _version.sha
    except ImportError:
        __version__ = 'unknown'
        __revision__ = None
    except SystemExit:
        __version__ = 'unknown'
        __revision__ = None

from gr.runtime_helper import load_runtime, register_gksterm, version_string_to_tuple

# Detect whether this is a site-package installation
if os.path.isdir(os.path.join(os.path.dirname(__file__), "fonts")):
    # Set GRDIR environment accordingly to site-package installation.
    # (needed for finding GKSTerm on OSX)
    os.environ["GRDIR"] = os.getenv("GRDIR",
                                    os.path.realpath(os.path.dirname(__file__)))
    os.environ["GKS_FONTPATH"] = os.getenv("GKS_FONTPATH", os.environ["GRDIR"])

# The Python wrapper only passes UTF-8 encoded strings to the GR runtime
os.environ['GKS_ENCODING'] = 'utf-8'

_impl = python_implementation()
_mime_type = None

try:
    from IPython.display import clear_output, display, SVG, Image, HTML
    from base64 import b64encode
except ImportError:
    clear_output = None


def _require_runtime_version(*_minimum_runtime_version):
    """
    Decorator to add GR runtime version requirements to functions.

    :param _minimum_runtime_version: required version as integers
    :return: the wrapped function with a version check
    """
    def require_runtime_version_decorator(_func, _minimum_runtime_version=_minimum_runtime_version):
        # remove extraneous 0s from version
        while _minimum_runtime_version[-1] == 0:
            _minimum_runtime_version = _minimum_runtime_version[:-1]

        minimum_runtime_version_str = '.'.join(
            'post' + str(c) if i == 3 else str(c)
            for i, c in enumerate(_minimum_runtime_version)
        )
        _func.__doc__ += "\n\n    This function requires GR runtime version {} or higher.".format(minimum_runtime_version_str)

        # The runtime version check may need to be skipped in some situations.
        # Sphinx has issues parsing the decorated functions as the their
        # arguments will not match the documented arguments exactly.
        if os.environ.get('GR_SKIP_RUNTIME_VERSION_CHECK', ''):
            return _func

        @functools.wraps(_func)
        def wrapped_func(*args, **kwargs):
            global _RUNTIME_VERSION
            if _RUNTIME_VERSION == (0, 0, 0):
                raise RuntimeError("This function requires GR runtime version {} or higher, but the runtime version could not be detected.".format(minimum_runtime_version_str))
            if _RUNTIME_VERSION < _minimum_runtime_version:
                raise RuntimeError("This function requires GR runtime version {} or higher.".format(minimum_runtime_version_str))
            return _func(*args, **kwargs)

        return wrapped_func
    return require_runtime_version_decorator


class floatarray:
    def __init__(self, n, a):
        if isinstance(a, ndarray):
            if _impl == 'PyPy':
                self.array = array(a, float64)
                self.data = cast(self.array.__array_interface__['data'][0],
                                 POINTER(c_double))
            else:
                self.array = array(a, c_double)
                self.data = self.array.ctypes.data_as(POINTER(c_double))
        else:
            self.data = (c_double * n)()
            status = 0
            for i in range(n):
                try:
                    self.data[i] = a[i]
                except:
                    if not status:
                        status = 1
                        print('Float array lookup failure')
                    self.data[i] = 0


class intarray:
    def __init__(self, n, a):
        if isinstance(a, ndarray):
            if _impl == 'PyPy':
                self.array = array(a, int32)
                self.data = cast(self.array.__array_interface__['data'][0],
                                 POINTER(c_int))
            else:
                self.array = array(a, c_int)
                self.data = self.array.ctypes.data_as(POINTER(c_int))
        else:
            self.data = (c_int * n)()
            status = 0
            for i in range(n):
                try:
                    self.data[i] = a[i]
                except:
                    if not status:
                        status = 1
                        print('Integer array lookup failure')
                    self.data[i] = 0


class uint8array:
    def __init__(self, a):
        if _impl == 'PyPy':
            self.array = array(a, uint8)
            self.data = cast(self.array.__array_interface__['data'][0],
                             POINTER(c_uint8))
        else:
            self.array = array(a, c_uint8)
            self.data = self.array.ctypes.data_as(POINTER(c_uint8))


class nothing:
    def __init__(self):
        self.array = None
        self.data = None


def char(string):
    """
    Create a C string from a Python string, bytes or unicode object.
    """
    if version_info[0] == 2:
        string_is_binary = not isinstance(string, unicode)
    else:
        string_is_binary = isinstance(string, bytes)

    # first ensure string is not binary...
    if string_is_binary:
        try:
            string = string.decode('utf-8')
        except:
            string = string.decode('latin-1')
    # ... then encode it as utf-8, moving any encoding issues from C to Python.
    binary_string = string.encode('utf-8')
    c_string = create_string_buffer(binary_string)
    return cast(c_string, c_char_p)


def opengks():
    __gr.gr_opengks()


def closegks():
    __gr.gr_closegks()


def inqdspsize():
    mwidth = c_double()
    mheight = c_double()
    width = c_int()
    height = c_int()
    __gr.gr_inqdspsize(byref(mwidth), byref(mheight), byref(width), byref(height))
    return [mwidth.value, mheight.value, width.value, height.value]


@_require_runtime_version(0, 58, 0, 0)
def inqvpsize():
    """
    Get the size of the viewport in the currently active workstation.

    This function returns the width and height of the viewport in logical
    pixels, as well as the ratio of logical to device pixels for the
    currently active workstation. For those workstation types that work with
    windows such as GKSTerm / quartz (400) it may not be possible to
    precisely determine the size of the viewport if no window has been opened
    yet. Similarly, workstation types that create vector graphics can not
    return a precise pixel value either. In both of these cases, best guess
    values will be returned.
    """
    width = c_int()
    height = c_int()
    device_pixel_ratio = c_double()
    __gr.gr_inqvpsize(byref(width), byref(height), byref(device_pixel_ratio))
    return width.value, height.value, device_pixel_ratio.value


def openws(workstation_id, connection, workstation_type):
    """
    Open a graphical workstation.

    **Parameters:**

    `workstation_id` :
        A workstation identifier.
    `connection` :
        A connection identifier.
    `workstation_type` :
        The desired workstation type.

    Available workstation types:

    +-------------+------------------------------------------------------+
    |            5|Workstation Independent Segment Storage               |
    +-------------+------------------------------------------------------+
    |         7, 8|Computer Graphics Metafile (CGM binary, clear text)   |
    +-------------+------------------------------------------------------+
    |           41|Windows GDI                                           |
    +-------------+------------------------------------------------------+
    |           51|Mac Quickdraw                                         |
    +-------------+------------------------------------------------------+
    |      61 - 64|PostScript (b/w, color)                               |
    +-------------+------------------------------------------------------+
    |     101, 102|Portable Document Format (plain, compressed)          |
    +-------------+------------------------------------------------------+
    |    210 - 213|X Windows                                             |
    +-------------+------------------------------------------------------+
    |          214|Sun Raster file (RF)                                  |
    +-------------+------------------------------------------------------+
    |     215, 218|Graphics Interchange Format (GIF87, GIF89)            |
    +-------------+------------------------------------------------------+
    |          216|Motif User Interface Language (UIL)                   |
    +-------------+------------------------------------------------------+
    |          320|Windows Bitmap (BMP)                                  |
    +-------------+------------------------------------------------------+
    |          321|JPEG image file                                       |
    +-------------+------------------------------------------------------+
    |          322|Portable Network Graphics file (PNG)                  |
    +-------------+------------------------------------------------------+
    |          323|Tagged Image File Format (TIFF)                       |
    +-------------+------------------------------------------------------+
    |          370|Xfig vector graphics file                             |
    +-------------+------------------------------------------------------+
    |          371|Gtk                                                   |
    +-------------+------------------------------------------------------+
    |          380|wxWidgets                                             |
    +-------------+------------------------------------------------------+
    |          381|Qt4                                                   |
    +-------------+------------------------------------------------------+
    |          382|Scaleable Vector Graphics (SVG)                       |
    +-------------+------------------------------------------------------+
    |          390|Windows Metafile                                      |
    +-------------+------------------------------------------------------+
    |          400|Quartz                                                |
    +-------------+------------------------------------------------------+
    |          410|Socket driver                                         |
    +-------------+------------------------------------------------------+
    |          415|0MQ driver                                            |
    +-------------+------------------------------------------------------+
    |          420|OpenGL                                                |
    +-------------+------------------------------------------------------+
    |          430|HTML5 Canvas                                          |
    +-------------+------------------------------------------------------+

    """
    __gr.gr_openws(c_int(workstation_id), char(connection), c_int(workstation_type))


def closews(workstation_id):
    """
    Close the specified workstation.

    **Parameters:**

    `workstation_id` :
        A workstation identifier.

    """
    __gr.gr_closews(c_int(workstation_id))


def activatews(workstation_id):
    """
    Activate the specified workstation.

    **Parameters:**

    `workstation_id` :
        A workstation identifier.

    """
    __gr.gr_activatews(c_int(workstation_id))


def deactivatews(workstation_id):
    """
    Deactivate the specified workstation.

    **Parameters:**

    `workstation_id` :
        A workstation identifier.

    """
    __gr.gr_deactivatews(c_int(workstation_id))


def configurews():
    """
    Configure active workstations (reread displaysize).
    """
    __gr.gr_configurews()


def clearws():
    if isinline() and clear_output:
        clear_output(wait=True)
    __gr.gr_clearws()


def updatews():
    __gr.gr_updatews()


def _assertEqualLength(*args):
    if args and all(len(args[0]) == len(arg) for arg in args):
        return len(args[0])
    else:
        raise AttributeError("Sequences must have same length.")


def polyline(x, y):
    """
    Draw a polyline using the current line attributes, starting from the
    first data point and ending at the last data point.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates

    The values for `x` and `y` are in world coordinates. The attributes that
    control the appearance of a polyline are linetype, linewidth and color
    index.

    """
    n = _assertEqualLength(x, y)
    _x = floatarray(n, x)
    _y = floatarray(n, y)
    __gr.gr_polyline(c_int(n), _x.data, _y.data)


def quiver(nx, ny, x, y, u, v, color):
    """
    Draw a quiver plot on a grid of nx*ny points.

    **Parameters:**

    `nx` :
        The number of points along the x-axis of the grid
    `ny` :
        The number of points along the y-axis of the grid
    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `u` :
        A list containing the U component for each point on the grid
    `v` :
        A list containing the V component for each point on the grid
    `color` :
        A bool to indicate whether or not the arrows should be colored using
        the current colormap

    The values for `x` and `y` are in world coordinates.
    """
    _x = floatarray(nx, x)
    _y = floatarray(ny, y)
    _u = floatarray(nx * ny, u)
    _v = floatarray(nx * ny, v)
    __gr.gr_quiver(c_int(nx), c_int(ny), _x.data, _y.data, _u.data, _v.data, c_int(1 if color else 0))


def polymarker(x, y):
    """
    Draw marker symbols centered at the given data points.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates

    The values for `x` and `y` are in world coordinates. The attributes that
    control the appearance of a polymarker are marker type, marker size
    scale factor and color index.

    """
    n = _assertEqualLength(x, y)
    _x = floatarray(n, x)
    _y = floatarray(n, y)
    __gr.gr_polymarker(c_int(n), _x.data, _y.data)


def text(x, y, string):
    """
    Draw a text at position `x`, `y` using the current text attributes.

    **Parameters:**

    `x` :
        The X coordinate of starting position of the text string
    `y` :
        The Y coordinate of starting position of the text string
    `string` :
        The text to be drawn

    The values for `x` and `y` are in normalized device coordinates.
    The attributes that control the appearance of text are text font and precision,
    character expansion factor, character spacing, text color index, character
    height, character up vector, text path and text alignment.

    """
    __gr.gr_text(c_double(x), c_double(y), char(string))


def inqtext(x, y, string):
    tbx = (c_double * 4)()
    tby = (c_double * 4)()
    __gr.gr_inqtext(c_double(x), c_double(y), char(string), tbx, tby)
    return [[tbx[0], tbx[1], tbx[2], tbx[3]],
            [tby[0], tby[1], tby[2], tby[3]]]


def fillarea(x, y):
    """
    Allows you to specify a polygonal shape of an area to be filled.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates

    The attributes that control the appearance of fill areas are fill area interior
    style, fill area style index and fill area color index.

    """
    n = _assertEqualLength(x, y)
    _x = floatarray(n, x)
    _y = floatarray(n, y)
    __gr.gr_fillarea(c_int(n), _x.data, _y.data)


def cellarray(xmin, xmax, ymin, ymax, dimx, dimy, color):
    """
    Display rasterlike images in a device-independent manner. The cell array
    function partitions a rectangle given by two corner points into DIMX X DIMY
    cells, each of them colored individually by the corresponding color index
    of the given cell array.

    **Parameters:**

    `xmin`, `ymin` :
        Lower left point of the rectangle
    `xmax`, `ymax` :
        Upper right point of the rectangle
    `dimx`, `dimy` :
        X and Y dimension of the color index array
    `color` :
        Color index array

    The values for `xmin`, `xmax`, `ymin` and `ymax` are in world coordinates.

    """
    _color = intarray(dimx * dimy, color)
    __gr.gr_cellarray(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                      c_int(dimx), c_int(dimy), c_int(1), c_int(1),
                      c_int(dimx), c_int(dimy), _color.data)


def polarcellarray(x_org, y_org, phimin, phimax, rmin, rmax, dimphi, dimr, color):
    """
    Display a two dimensional color index array mapped to a disk using polar
    coordinates.

    **Parameters:**

    `x_org`, `y_org` :
        X and Y coordinate of the disk center in world coordinates
    `phimin`, `phimax` :
        start and end angle of the disk sector in degrees
    `rmin`, `rmax` :
        inner and outer radius of the (punctured) disk in world coordinates
    `dimphi`, `dimr` :
        Phi (X) and R (Y) dimension of the color index array
    `color` color index array
    
    The two dimensional color index array is mapped to the resulting image by
    interpreting the X-axis of the array as the angle and the Y-axis as the raidus.
    The center point of the resulting disk is located at `x_org`, `y_org` and the
    radius of the disk is `rmax`.
    
    To draw a contiguous array as a complete disk use:
    
        gr.polarcellarray(x_org, y_org, 0, 360, 0, rmax, dimphi, dimr, color)
    
    The additional parameters to the function can be used to further control the
    mapping from polar to cartesian coordinates.
    
    If `rmin` is greater than 0 the input data is mapped to a punctured disk (or
    annulus) with an inner radius of `rmin` and an outer radius `rmax`. If `rmin`
    is greater than `rmax` the Y-axis of the array is reversed.
    
    The parameter `phimin` and `phimax` can be used to map the data to a sector
    of the (punctured) disk starting at `phimin` and ending at `phimax`. If
    `phimin` is greater than `phimax` the X-axis is reversed. The visible sector
    is the one starting in mathematically positive direction (counterclockwise)
    at the smaller angle and ending at the larger angle. An example of the four
    possible options can be found below:
    
    +-----------+-----------+---------------------------------------------------+
    |**phimin** |**phimax** |**Result**                                         |
    +-----------+-----------+---------------------------------------------------+
    |90         |270        |Left half visible, mapped counterclockwise         |
    +-----------+-----------+---------------------------------------------------+
    |270        |90         |Left half visible, mapped clockwise                |
    +-----------+-----------+---------------------------------------------------+
    |-90        |90         |Right half visible, mapped counterclockwise        |
    +-----------+-----------+---------------------------------------------------+
    |90         |-90        |Right half visible, mapped clockwise               |
    +-----------+-----------+---------------------------------------------------+
    """
    _color = intarray(dimr * dimphi, color)
    __gr.gr_polarcellarray(c_double(x_org), c_double(y_org), c_double(phimin), c_double(phimax),
                           c_double(rmin), c_double(rmax), c_int(dimphi), c_int(dimr),
                           c_int(1), c_int(1), c_int(dimphi), c_int(dimr), _color.data)

def spline(px, py, m, method):
    """
    Generate a cubic spline-fit, starting from the first data point and
    ending at the last data point.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `m` :
        The number of points in the polygon to be drawn (`m` > len(`x`))
    `method` :
        The smoothing method

    The values for `x` and `y` are in world coordinates. The attributes that
    control the appearance of a spline-fit are linetype, linewidth and color
    index.

    If `method` is > 0, then a generalized cross-validated smoothing spline is calculated.
    If `method` is 0, then an interpolating natural cubic spline is calculated.
    If `method` is < -1, then a cubic B-spline is calculated.

    """
    n = _assertEqualLength(px, py)
    _px = floatarray(n, px)
    _py = floatarray(n, py)
    __gr.gr_spline(c_int(n), _px.data, _py.data, c_int(m), c_int(method))


def gridit(xd, yd, zd, nx, ny):
    nd = _assertEqualLength(xd, yd, zd)
    _xd = floatarray(nd, xd)
    _yd = floatarray(nd, yd)
    _zd = floatarray(nd, zd)
    x = (c_double * nx)()
    y = (c_double * ny)()
    z = (c_double * (nx * ny))()
    __gr.gr_gridit(c_int(nd), _xd.data, _yd.data, _zd.data,
                   c_int(nx), c_int(ny), x, y, z)
    return [x[:], y[:], z[:]]


def setlinetype(style):
    """
    Specify the line style for polylines.

    **Parameters:**

    `style` :
        The polyline line style

    The available line types are:

    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_SOLID             |   1|Solid line                                         |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_DASHED            |   2|Dashed line                                        |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_DOTTED            |   3|Dotted line                                        |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_DASHED_DOTTED     |   4|Dashed-dotted line                                 |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_DASH_2_DOT        |  -1|Sequence of one dash followed by two dots          |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_DASH_3_DOT        |  -2|Sequence of one dash followed by three dots        |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_LONG_DASH         |  -3|Sequence of long dashes                            |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_LONG_SHORT_DASH   |  -4|Sequence of a long dash followed by a short dash   |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_SPACED_DASH       |  -5|Sequence of dashes double spaced                   |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_SPACED_DOT        |  -6|Sequence of dots double spaced                     |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_DOUBLE_DOT        |  -7|Sequence of pairs of dots                          |
    +---------------------------+----+---------------------------------------------------+
    |LINETYPE_TRIPLE_DOT        |  -8|Sequence of groups of three dots                   |
    +---------------------------+----+---------------------------------------------------+

    """
    __gr.gr_setlinetype(c_int(style))


def inqlinetype():
    ltype = c_int()
    __gr.gr_inqlinetype(byref(ltype))
    return ltype.value


def setlinewidth(width):
    """
    Define the line width of subsequent polyline output primitives.

    **Parameters:**

    `width` :
        The polyline line width scale factor

    The line width is calculated as the nominal line width generated
    on the workstation multiplied by the line width scale factor.
    This value is mapped by the workstation to the nearest available line width.
    The default line width is 1.0, or 1 times the line width generated on the graphics device.

    """
    __gr.gr_setlinewidth(c_double(width))


def inqlinewidth():
    width = c_double()
    __gr.gr_inqlinewidth(byref(width))
    return width.value


def setlinecolorind(color):
    """
    Define the color of subsequent polyline output primitives.

    **Parameters:**

    `color` :
        The polyline color index (COLOR < 1256)

    """
    __gr.gr_setlinecolorind(c_int(color))


def inqlinecolorind():
    coli = c_int()
    __gr.gr_inqlinecolorind(byref(coli))
    return coli.value


def setmarkertype(style):
    """
    Specifiy the marker type for polymarkers.

    **Parameters:**

    `style` :
        The polymarker marker type

    The available marker types are:

    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_DOT               |    1|Smallest displayable dot                        |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_PLUS              |    2|Plus sign                                       |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_ASTERISK          |    3|Asterisk                                        |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_CIRCLE            |    4|Hollow circle                                   |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_DIAGONAL_CROSS    |    5|Diagonal cross                                  |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_CIRCLE      |   -1|Filled circle                                   |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_TRIANGLE_UP       |   -2|Hollow triangle pointing upward                 |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_TRI_UP      |   -3|Filled triangle pointing upward                 |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_TRIANGLE_DOWN     |   -4|Hollow triangle pointing downward               |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_TRI_DOWN    |   -5|Filled triangle pointing downward               |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SQUARE            |   -6|Hollow square                                   |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_SQUARE      |   -7|Filled square                                   |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_BOWTIE            |   -8|Hollow bowtie                                   |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_BOWTIE      |   -9|Filled bowtie                                   |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_HGLASS            |  -10|Hollow hourglass                                |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_HGLASS      |  -11|Filled hourglass                                |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_DIAMOND           |  -12|Hollow diamond                                  |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_DIAMOND     |  -13|Filled Diamond                                  |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_STAR              |  -14|Hollow star                                     |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_STAR        |  -15|Filled Star                                     |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_TRI_UP_DOWN       |  -16|Hollow triangles pointing up and down overlaid  |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_TRI_RIGHT   |  -17|Filled triangle point right                     |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID_TRI_LEFT    |  -18|Filled triangle pointing left                   |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_HOLLOW PLUS       |  -19|Hollow plus sign                                |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_SOLID PLUS        |  -20|Solid plus sign                                 |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_PENTAGON          |  -21|Pentagon                                        |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_HEXAGON           |  -22|Hexagon                                         |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_HEPTAGON          |  -23|Heptagon                                        |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_OCTAGON           |  -24|Octagon                                         |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_STAR_4            |  -25|4-pointed star                                  |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_STAR_5            |  -26|5-pointed star (pentagram)                      |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_STAR_6            |  -27|6-pointed star (hexagram)                       |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_STAR_7            |  -28|7-pointed star (heptagram)                      |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_STAR_8            |  -29|8-pointed star (octagram)                       |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_VLINE             |  -30|verical line                                    |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_HLINE             |  -31|horizontal line                                 |
    +-----------------------------+-----+------------------------------------------------+
    |MARKERTYPE_OMARK             |  -32|o-mark                                          |
    +-----------------------------+-----+------------------------------------------------+

    Polymarkers appear centered over their specified coordinates.

    """
    __gr.gr_setmarkertype(c_int(style))


def inqmarkertype():
    mtype = c_int()
    __gr.gr_inqmarkertype(byref(mtype))
    return mtype.value


def setmarkersize(size):
    """
    Specify the marker size for polymarkers.

    **Parameters:**

    `size` :
        Scale factor applied to the nominal marker size

    The polymarker size is calculated as the nominal size generated on the graphics device
    multiplied by the marker size scale factor.

    """
    __gr.gr_setmarkersize(c_double(size))


@_require_runtime_version(0, 41, 5, 47)
def inqmarkersize():
    """
    Inquire the marker size for polymarkers.
    """
    size = c_double()
    __gr.gr_inqmarkersize(byref(size))
    return size.value


def setmarkercolorind(color):
    """
    Define the color of subsequent polymarker output primitives.

    **Parameters:**

    `color` :
        The polymarker color index (COLOR < 1256)

    """
    __gr.gr_setmarkercolorind(c_int(color))


def inqmarkercolorind():
    coli = c_int()
    __gr.gr_inqmarkercolorind(byref(coli))
    return coli.value


def settextfontprec(font, precision):
    """
    Specify the text font and precision for subsequent text output primitives.

    **Parameters:**

    `font` :
        Text font (see tables below)
    `precision` :
        Text precision (see table below)

    The available text fonts are:

    +--------------------------------------+-----+
    |FONT_TIMES_ROMAN                      |  101|
    +--------------------------------------+-----+
    |FONT_TIMES_ITALIC                     |  102|
    +--------------------------------------+-----+
    |FONT_TIMES_BOLD                       |  103|
    +--------------------------------------+-----+
    |FONT_TIMES_BOLDITALIC                 |  104|
    +--------------------------------------+-----+
    |FONT_HELVETICA                        |  105|
    +--------------------------------------+-----+
    |FONT_HELVETICA_OBLIQUE                |  106|
    +--------------------------------------+-----+
    |FONT_HELVETICA_BOLD                   |  107|
    +--------------------------------------+-----+
    |FONT_HELVETICA_BOLDOBLIQUE            |  108|
    +--------------------------------------+-----+
    |FONT_COURIER                          |  109|
    +--------------------------------------+-----+
    |FONT_COURIER_OBLIQUE                  |  110|
    +--------------------------------------+-----+
    |FONT_COURIER_BOLD                     |  111|
    +--------------------------------------+-----+
    |FONT_COURIER_BOLDOBLIQUE              |  112|
    +--------------------------------------+-----+
    |FONT_SYMBOL                           |  113|
    +--------------------------------------+-----+
    |FONT_BOOKMAN_LIGHT                    |  114|
    +--------------------------------------+-----+
    |FONT_BOOKMAN_LIGHTITALIC              |  115|
    +--------------------------------------+-----+
    |FONT_BOOKMAN_DEMI                     |  116|
    +--------------------------------------+-----+
    |FONT_BOOKMAN_DEMIITALIC               |  117|
    +--------------------------------------+-----+
    |FONT_NEWCENTURYSCHLBK_ROMAN           |  118|
    +--------------------------------------+-----+
    |FONT_NEWCENTURYSCHLBK_ITALIC          |  119|
    +--------------------------------------+-----+
    |FONT_NEWCENTURYSCHLBK_BOLD            |  120|
    +--------------------------------------+-----+
    |FONT_NEWCENTURYSCHLBK_BOLDITALIC      |  121|
    +--------------------------------------+-----+
    |FONT_AVANTGARDE_BOOK                  |  122|
    +--------------------------------------+-----+
    |FONT_AVANTGARDE_BOOKOBLIQUE           |  123|
    +--------------------------------------+-----+
    |FONT_AVANTGARDE_DEMI                  |  124|
    +--------------------------------------+-----+
    |FONT_AVANTGARDE_DEMIOBLIQUE           |  125|
    +--------------------------------------+-----+
    |FONT_PALATINO_ROMAN                   |  126|
    +--------------------------------------+-----+
    |FONT_PALATINO_ITALIC                  |  127|
    +--------------------------------------+-----+
    |FONT_PALATINO_BOLD                    |  128|
    +--------------------------------------+-----+
    |FONT_PALATINO_BOLDITALIC              |  129|
    +--------------------------------------+-----+
    |FONT_ZAPFCHANCERY_MEDIUMITALIC        |  130|
    +--------------------------------------+-----+
    |FONT_ZAPFDINGBATS                     |  131|
    +--------------------------------------+-----+
    |FONT_COMPUTERMODERN                   |  232|
    +--------------------------------------+-----+
    |FONT_DEJAVUSANS                       |  233|
    +--------------------------------------+-----+

    The available text precisions are:

    +---------------------------+---+--------------------------------------+
    |TEXT_PRECISION_STRING      |  0|String precision (higher quality)     |
    +---------------------------+---+--------------------------------------+
    |TEXT_PRECISION_CHAR        |  1|Character precision (medium quality)  |
    +---------------------------+---+--------------------------------------+
    |TEXT_PRECISION_STROKE      |  2|Stroke precision (lower quality)      |
    +---------------------------+---+--------------------------------------+
    |TEXT_PRECISION_OUTLINE     |  3|Outline precision (highest quality)   |
    +---------------------------+---+--------------------------------------+

    The appearance of a font depends on the text precision value specified.
    STRING, CHARACTER or STROKE precision allows for a greater or lesser
    realization of the text primitives, for efficiency. STRING is the
    default precision for GR and produces the high quality output using either
    native font rendering or FreeType. OUTLINE uses the GR path rendering
    functions to draw individual glyphs and produces the highest quality
    output.
    """
    __gr.gr_settextfontprec(c_int(font), c_int(precision))


@_require_runtime_version(0, 56, 0, 0)
def loadfont(filename):
    """
    Load a font file from a given filename.

    **Parameters:**

    `filename` :
        The filename of the font

    This function loads a font from a given filename and returns the font index
    that has been assigned to it or `None` if the font could not be found.
    To use the loaded font call `gr.settextfontprec` using the resulting font
    index and precision 3.

         gr.settextfontprec(gr.loadfont(filename), 3)

    The filename can either be an absolute path or a filename like `Arial.ttf`.
    Font files are searched in the directories specified by the `GKS_FONT_DIRS`
    environment variable and the operating system's default font locations.

    """
    result = c_int()
    __gr.gr_loadfont(char(filename), byref(result))
    if result.value >= 0:
        return result.value


def setcharexpan(factor):
    """
    Set the current character expansion factor (width to height ratio).

    **Parameters:**

    `factor` :
        Text expansion factor applied to the nominal text width-to-height ratio

    `setcharexpan` defines the width of subsequent text output primitives. The expansion
    factor alters the width of the generated characters, but not their height. The default
    text expansion factor is 1, or one times the normal width-to-height ratio of the text.

    """
    __gr.gr_setcharexpan(c_double(factor))


def setcharspace(spacing):
    __gr.gr_setcharspace(c_double(spacing))


def settextcolorind(color):
    """
    Sets the current text color index.

    **Parameters:**

    `color` :
        The text color index (COLOR < 1256)

    `settextcolorind` defines the color of subsequent text output primitives.
    GR uses the default foreground color (black=1) for the default text color index.

    """
    __gr.gr_settextcolorind(c_int(color))


def setcharheight(height):
    """
    Set the current character height.

    **Parameters:**

    `height` :
        Text height value

    `setcharheight` defines the height of subsequent text output primitives. Text height
    is defined as a percentage of the default window. GR uses the default text height of
    0.027 (2.7% of the height of the default window).

    """
    __gr.gr_setcharheight(c_double(height))


def setwscharheight(chh, height):
    __gr.gr_setwscharheight(c_double(chh), c_double(height))


def setcharup(ux, uy):
    """
    Set the current character text angle up vector.

    **Parameters:**

    `ux`, `uy` :
        Text up vector

    `setcharup` defines the vertical rotation of subsequent text output primitives.
    The text up vector is initially set to (0, 1), horizontal to the baseline.

    """
    __gr.gr_setcharup(c_double(ux), c_double(uy))


def settextpath(path):
    """
    Define the current direction in which subsequent text will be drawn.

    **Parameters:**

    `path` :
        Text path (see table below)

    +----------------------+---+---------------+
    |TEXT_PATH_RIGHT       |  0|left-to-right  |
    +----------------------+---+---------------+
    |TEXT_PATH_LEFT        |  1|right-to-left  |
    +----------------------+---+---------------+
    |TEXT_PATH_UP          |  2|downside-up    |
    +----------------------+---+---------------+
    |TEXT_PATH_DOWN        |  3|upside-down    |
    +----------------------+---+---------------+

    """
    __gr.gr_settextpath(c_int(path))


def settextalign(horizontal, vertical):
    """
    Set the current horizontal and vertical alignment for text.

    **Parameters:**

    `horizontal` :
        Horizontal text alignment (see the table below)
    `vertical` :
        Vertical text alignment (see the table below)

    `settextalign` specifies how the characters in a text primitive will be aligned
    in horizontal and vertical space. The default text alignment indicates horizontal left
    alignment and vertical baseline alignment.

    +-------------------------+---+----------------+
    |TEXT_HALIGN_NORMAL       |  0|                |
    +-------------------------+---+----------------+
    |TEXT_HALIGN_LEFT         |  1|Left justify    |
    +-------------------------+---+----------------+
    |TEXT_HALIGN_CENTER       |  2|Center justify  |
    +-------------------------+---+----------------+
    |TEXT_HALIGN_RIGHT        |  3|Right justify   |
    +-------------------------+---+----------------+

    +-------------------------+---+------------------------------------------------+
    |TEXT_VALIGN_NORMAL       |  0|                                                |
    +-------------------------+---+------------------------------------------------+
    |TEXT_VALIGN_TOP          |  1|Align with the top of the characters            |
    +-------------------------+---+------------------------------------------------+
    |TEXT_VALIGN_CAP          |  2|Aligned with the cap of the characters          |
    +-------------------------+---+------------------------------------------------+
    |TEXT_VALIGN_HALF         |  3|Aligned with the half line of the characters    |
    +-------------------------+---+------------------------------------------------+
    |TEXT_VALIGN_BASE         |  4|Aligned with the base line of the characters    |
    +-------------------------+---+------------------------------------------------+
    |TEXT_VALIGN_BOTTOM       |  5|Aligned with the bottom line of the characters  |
    +-------------------------+---+------------------------------------------------+

    """
    __gr.gr_settextalign(c_int(horizontal), c_int(vertical))


def setfillintstyle(style):
    """
    Set the fill area interior style to be used for fill areas.

    **Parameters:**

    `style` :
        The style of fill to be used

    `setfillintstyle` defines the interior style  for subsequent fill area output
    primitives. The default interior style is HOLLOW.

    +---------+---+--------------------------------------------------------------------------------+
    |HOLLOW   |  0|No filling. Just draw the bounding polyline                                     |
    +---------+---+--------------------------------------------------------------------------------+
    |SOLID    |  1|Fill the interior of the polygon using the fill color index                     |
    +---------+---+--------------------------------------------------------------------------------+
    |PATTERN  |  2|Fill the interior of the polygon using the style index as a pattern index       |
    +---------+---+--------------------------------------------------------------------------------+
    |HATCH    |  3|Fill the interior of the polygon using the style index as a cross-hatched style |
    +---------+---+--------------------------------------------------------------------------------+

    """
    __gr.gr_setfillintstyle(c_int(style))


def inqfillintstyle():
    """
    Returns the fill area interior style to be used for fill areas.
    """
    style = c_int()
    __gr.gr_inqfillintstyle(byref(style))
    return style.value


def setfillstyle(index):
    """
    Sets the fill style to be used for subsequent fill areas.

    **Parameters:**

    `index` :
        The fill style index to be used

    `setfillstyle` specifies an index when PATTERN fill or HATCH fill is requested by the
    `setfillintstyle` function. If the interior style is set to PATTERN, the fill style
    index points to a device-independent pattern table. If interior style is set to HATCH
    the fill style index indicates different hatch styles. If HOLLOW or SOLID is specified
    for the interior style, the fill style index is unused.

    """
    __gr.gr_setfillstyle(c_int(index))


def inqfillstyle():
    """
    Returns the current fill area color index.
    """
    index = c_int()
    __gr.gr_inqfillstyle(byref(index))
    return index.value


def setfillcolorind(color):
    """
    Sets the current fill area color index.

    **Parameters:**

    `color` :
        The fill area color index (COLOR < 1256)

    `setfillcolorind` defines the color of subsequent fill area output primitives.
    GR uses the default foreground color (black=1) for the default fill area color index.

    """
    __gr.gr_setfillcolorind(c_int(color))


def inqfillcolorind():
    """
    Returns the current fill area color index.
    """
    color = c_int()
    __gr.gr_inqfillcolorind(byref(color))
    return color.value


def setresizebehaviour(flag):
    __gr.gr_setresizebehaviour(1 if flag else 0)


def inqresizebehaviour():
    flag = c_int()
    __gr.gr_inqresizebehaviour(byref(flag))
    return True if flag else False


def setcolorrep(index, red, green, blue):
    """
    `setcolorrep` allows to redefine an existing color index representation by specifying
    an RGB color triplet.

    **Parameters:**

    `index` :
        Color index in the range 0 to 1256
    `red` :
        Red intensity in the range 0.0 to 1.0
    `green` :
        Green intensity in the range 0.0 to 1.0
    `blue`:
        Blue intensity in the range 0.0 to 1.0

    """
    __gr.gr_setcolorrep(c_int(index), c_double(red), c_double(green), c_double(blue))


def setscale(options):
    """
    `setscale` sets the type of transformation to be used for subsequent GR output
    primitives.

    **Parameters:**

    `options` :
        Scale specification (see Table below)

    +---------------+--------------------+
    |OPTION_X_LOG   |Logarithmic X-axis  |
    +---------------+--------------------+
    |OPTION_Y_LOG   |Logarithmic Y-axis  |
    +---------------+--------------------+
    |OPTION_Z_LOG   |Logarithmic Z-axis  |
    +---------------+--------------------+
    |OPTION_FLIP_X  |Flip X-axis         |
    +---------------+--------------------+
    |OPTION_FLIP_Y  |Flip Y-axis         |
    +---------------+--------------------+
    |OPTION_FLIP_Z  |Flip Z-axis         |
    +---------------+--------------------+

    `setscale` defines the current transformation according to the given scale
    specification which may be or'ed together using any of the above options. GR uses
    these options for all subsequent output primitives until another value is provided.
    The scale options are used to transform points from an abstract logarithmic or
    semi-logarithmic coordinate system, which may be flipped along each axis, into the
    world coordinate system.

    Note: When applying a logarithmic transformation to a specific axis, the system
    assumes that the axes limits are greater than zero.

    """
    return __gr.gr_setscale(c_int(options))


def inqscale():
    options = c_int()
    __gr.gr_inqscale(byref(options))
    return options.value


def setwindow(xmin, xmax, ymin, ymax):
    """
    `setwindow` establishes a window, or rectangular subspace, of world coordinates to be
    plotted. If you desire log scaling or mirror-imaging of axes, use the SETSCALE function.

    **Parameters:**

    `xmin` :
        The left horizontal coordinate of the window (`xmin` < `xmax`).
    `xmax` :
        The right horizontal coordinate of the window.
    `ymin` :
        The bottom vertical coordinate of the window (`ymin` < `ymax`).
    `ymax` :
        The top vertical coordinate of the window.

    `setwindow` defines the rectangular portion of the World Coordinate space (WC) to be
    associated with the specified normalization transformation. The WC window and the
    Normalized Device Coordinates (NDC) viewport define the normalization transformation
    through which all output primitives are mapped. The WC window is mapped onto the
    rectangular NDC viewport which is, in turn, mapped onto the display surface of the
    open and active workstation, in device coordinates. By default, GR uses the range
    [0,1] x [0,1], in world coordinates, as the normalization transformation window.

    """
    __gr.gr_setwindow(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))


def inqwindow():
    xmin = c_double()
    xmax = c_double()
    ymin = c_double()
    ymax = c_double()
    __gr.gr_inqwindow(byref(xmin), byref(xmax), byref(ymin), byref(ymax))
    return [xmin.value, xmax.value, ymin.value, ymax.value]


def setviewport(xmin, xmax, ymin, ymax):
    """
    `setviewport` establishes a rectangular subspace of normalized device coordinates.

    **Parameters:**

    `xmin` :
        The left horizontal coordinate of the viewport.
    `xmax` :
        The right horizontal coordinate of the viewport (0 <= `xmin` < `xmax` <= 1).
    `ymin` :
        The bottom vertical coordinate of the viewport.
    `ymax` :
        The top vertical coordinate of the viewport (0 <= `ymin` < `ymax` <= 1).

    `setviewport` defines the rectangular portion of the Normalized Device Coordinate
    (NDC) space to be associated with the specified normalization transformation. The
    NDC viewport and World Coordinate (WC) window define the normalization transformation
    through which all output primitives pass. The WC window is mapped onto the rectangular
    NDC viewport which is, in turn, mapped onto the display surface of the open and active
    workstation, in device coordinates.

    """
    assert not np.isnan(xmin)
    __gr.gr_setviewport(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))


def inqviewport():
    xmin = c_double()
    xmax = c_double()
    ymin = c_double()
    ymax = c_double()
    __gr.gr_inqviewport(byref(xmin), byref(xmax), byref(ymin), byref(ymax))
    return [xmin.value, xmax.value, ymin.value, ymax.value]


def selntran(transform):
    """
    `selntran` selects a predefined transformation from world coordinates to normalized
    device coordinates.

    **Parameters:**

    `transform` :
        A normalization transformation number.

    +------+----------------------------------------------------------------------------------------------------+
    |     0|Selects the identity transformation in which both the window and viewport have the range of 0 to 1  |
    +------+----------------------------------------------------------------------------------------------------+
    |  >= 1|Selects a normalization transformation as defined by `setwindow` and `setviewport`                  |
    +------+----------------------------------------------------------------------------------------------------+

    """
    __gr.gr_selntran(c_int(transform))


def setclip(indicator):
    """
    Set the clipping indicator.

    **Parameters:**

    `indicator` :
        An indicator specifying whether clipping is on or off.

    +----+---------------------------------------------------------------+
    |   0|Clipping is off. Data outside of the window will be drawn.     |
    +----+---------------------------------------------------------------+
    |   1|Clipping is on. Data outside of the window will not be drawn.  |
    +----+---------------------------------------------------------------+

    `setclip` enables or disables clipping of the image drawn in the current window.
    Clipping is defined as the removal of those portions of the graph that lie outside of
    the defined viewport. If clipping is on, GR does not draw generated output primitives
    past the viewport boundaries. If clipping is off, primitives may exceed the viewport
    boundaries, and they will be drawn to the edge of the workstation window.
    By default, clipping is on.

    """
    __gr.gr_setclip(c_int(indicator))


def setwswindow(xmin, xmax, ymin, ymax):
    """
    Set the area of the NDC viewport that is to be drawn in the workstation window.

    **Parameters:**

    `xmin` :
        The left horizontal coordinate of the workstation window.
    `xmax` :
        The right horizontal coordinate of the workstation window (0 <= `xmin` < `xmax` <= 1).
    `ymin` :
        The bottom vertical coordinate of the workstation window.
    `ymax` :
        The top vertical coordinate of the workstation window (0 <= `ymin` < `ymax` <= 1).

    `setwswindow` defines the rectangular area of the Normalized Device Coordinate space
    to be output to the device. By default, the workstation transformation will map the
    range [0,1] x [0,1] in NDC onto the largest square on the workstation’s display
    surface. The aspect ratio of the workstation window is maintained at 1 to 1.

    """
    __gr.gr_setwswindow(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))


def setwsviewport(xmin, xmax, ymin, ymax):
    """
    Define the size of the workstation graphics window in meters.

    **Parameters:**

    `xmin` :
        The left horizontal coordinate of the workstation viewport.
    `xmax` :
        The right horizontal coordinate of the workstation viewport.
    `ymin` :
        The bottom vertical coordinate of the workstation viewport.
    `ymax` :
        The top vertical coordinate of the workstation viewport.

    `setwsviewport` places a workstation window on the display of the specified size in
    meters. This command allows the workstation window to be accurately sized for a
    display or hardcopy device, and is often useful for sizing graphs for desktop
    publishing applications.

    """
    __gr.gr_setwsviewport(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))


def createseg(segment):
    __gr.gr_createseg(c_int(segment))


def copysegws(segment):
    __gr.gr_copysegws(c_int(segment))


def redrawsegws():
    __gr.gr_redrawsegws()


def setsegtran(segment, fx, fy, transx, transy, phi, scalex, scaley):
    __gr.gr_setsegtran(c_int(segment), c_double(fx), c_double(fy),
                       c_double(transx), c_double(transy), c_double(phi),
                       c_double(scalex), c_double(scaley))


def closeseg():
    __gr.gr_closegks()


def emergencyclosegks():
    __gr.gr_emergencyclosegks()


def updategks():
    __gr.gr_updategks()


def setspace(zmin, zmax, rotation, tilt):
    """
    Set the abstract Z-space used for mapping three-dimensional output primitives into
    the current world coordinate space.

    **Parameters:**

    `zmin` :
        Minimum value for the Z-axis.
    `zmax` :
        Maximum value for the Z-axis.
    `rotation` :
        Angle for the rotation of the X axis, in degrees.
    `tilt` :
        Viewing angle of the Z axis in degrees.

    `setspace` establishes the limits of an abstract Z-axis and defines the angles for
    rotation and for the viewing angle (tilt) of a simulated three-dimensional graph,
    used for mapping corresponding output primitives into the current window.
    These settings are used for all subsequent three-dimensional output primitives until
    other values are specified. Angles of rotation and viewing angle must be specified
    between 0° and 90°.

    """
    return __gr.gr_setspace(c_double(zmin), c_double(zmax),
                            c_int(rotation), c_int(tilt))


def inqspace():
    zmin = c_double()
    zmax = c_double()
    rotation = c_int()
    tilt = c_int()
    __gr.gr_inqspace(byref(zmin), byref(zmax), byref(rotation), byref(tilt))
    return [zmin.value, zmax.value, rotation.value, tilt.value]


def textext(x, y, string):
    """
    Draw a text at position `x`, `y` using the current text attributes. Strings can be
    defined to create basic mathematical expressions and Greek letters.

    **Parameters:**

    `x` :
        The X coordinate of starting position of the text string
    `y` :
        The Y coordinate of starting position of the text string
    `string` :
        The text to be drawn

    The values for X and Y are in normalized device coordinates.
    The attributes that control the appearance of text are text font and precision,
    character expansion factor, character spacing, text color index, character
    height, character up vector, text path and text alignment.

    The character string is interpreted to be a simple mathematical formula.
    The following notations apply:

    Subscripts and superscripts: These are indicated by carets ('^') and underscores
    ('_'). If the sub/superscript contains more than one character, it must be enclosed
    in curly braces ('{}').

    Fractions are typeset with A '/' B, where A stands for the numerator and B for the
    denominator.

    To include a Greek letter you must specify the corresponding keyword after a
    backslash ('\') character. The text translator produces uppercase or lowercase
    Greek letters depending on the case of the keyword.

    +--------+---------+
    |Letter  |Keyword  |
    +--------+---------+
    |Α α     |alpha    |
    +--------+---------+
    |Β β     |beta     |
    +--------+---------+
    |Γ γ     |gamma    |
    +--------+---------+
    |Δ δ     |delta    |
    +--------+---------+
    |Ε ε     |epsilon  |
    +--------+---------+
    |Ζ ζ     |zeta     |
    +--------+---------+
    |Η η     |eta      |
    +--------+---------+
    |Θ θ     |theta    |
    +--------+---------+
    |Ι ι     |iota     |
    +--------+---------+
    |Κ κ     |kappa    |
    +--------+---------+
    |Λ λ     |lambda   |
    +--------+---------+
    |Μ μ     |mu       |
    +--------+---------+
    |Ν ν     |Nu / v   |
    +--------+---------+
    |Ξ ξ     |xi       |
    +--------+---------+
    |Ο ο     |omicron  |
    +--------+---------+
    |Π π     |pi       |
    +--------+---------+
    |Ρ ρ     |rho      |
    +--------+---------+
    |Σ σ     |sigma    |
    +--------+---------+
    |Τ τ     |tau      |
    +--------+---------+
    |Υ υ     |upsilon  |
    +--------+---------+
    |Φ φ     |phi      |
    +--------+---------+
    |Χ χ     |chi      |
    +--------+---------+
    |Ψ ψ     |psi      |
    +--------+---------+
    |Ω ω     |omega    |
    +--------+---------+

    Note: :code:`\\v` is a replacement for :code:`\\nu` which would conflict with :code:`\\n` (newline)

    For more sophisticated mathematical formulas, you should use the `gr.mathtex`
    function.

    """
    return __gr.gr_textext(c_double(x), c_double(y), char(string))


def inqtextext(x, y, string):
    tbx = (c_double * 4)()
    tby = (c_double * 4)()
    __gr.gr_inqtextext(c_double(x), c_double(y), char(string), tbx, tby)
    return [[tbx[0], tbx[1], tbx[2], tbx[3]],
            [tby[0], tby[1], tby[2], tby[3]]]


_axeslbl_callback = CFUNCTYPE(c_void_p, c_double, c_double, c_char_p, c_double)


def setscientificformat(format_option):
    """
    Specify the format to be used when scientific notation is used.

    **Parameters:**

    `format_option` :
        Format option to be used

    Available format options:

    +-----------------------------------+-------+
    |format option                      |Value  |
    +-----------------------------------+-------+
    |SCIENTIFIC_FORMAT_OPTION_E         |1      |
    +-----------------------------------+-------+
    |SCIENTIFIC_FORMAT_OPTION_TEXTEX    |2      |
    +-----------------------------------+-------+
    |SCIENTIFIC_FORMAT_OPTION_MATHTEX   |3      |
    +-----------------------------------+-------+
    """
    __gr.gr_setscientificformat(c_int(format_option))


def axeslbl(x_tick, y_tick, x_org, y_org, major_x, major_y, tick_size,
            fpx=0, fpy=0):
    if fpx is None:
        fpx = 0
    if fpy is None:
        fpy = 0

    cfpx = _axeslbl_callback(fpx)
    cfpy = _axeslbl_callback(fpy)
    __gr.gr_axeslbl(c_double(x_tick), c_double(y_tick),
                    c_double(x_org), c_double(y_org),
                    c_int(major_x), c_int(major_y), c_double(tick_size),
                    cfpx, cfpy)


def axes(x_tick, y_tick, x_org, y_org, major_x, major_y, tick_size):
    """
    Draw X and Y coordinate axes with linearly and/or logarithmically spaced tick marks.

    **Parameters:**

    `x_tick`, `y_tick` :
        The interval between minor tick marks on each axis.
    `x_org`, `y_org` :
        The world coordinates of the origin (point of intersection) of the X
        and Y axes.
    `major_x`, `major_y` :
        Unitless integer values specifying the number of minor tick intervals
        between major tick marks. Values of 0 or 1 imply no minor ticks.
        Negative values specify no labels will be drawn for the associated axis.
    `tick_size` :
        The length of minor tick marks specified in a normalized device
        coordinate unit. Major tick marks are twice as long as minor tick marks.
        A negative value reverses the tick marks on the axes from inward facing
        to outward facing (or vice versa).

    Tick marks are positioned along each axis so that major tick marks fall on the axes
    origin (whether visible or not). Major tick marks are labeled with the corresponding
    data values. Axes are drawn according to the scale of the window. Axes and tick marks
    are drawn using solid lines; line color and width can be modified using the
    `setlinetype` and `setlinewidth` functions. Axes are drawn according to
    the linear or logarithmic transformation established by the `setscale` function.

    """
    __gr.gr_axes(c_double(x_tick), c_double(y_tick),
                 c_double(x_org), c_double(y_org),
                 c_int(major_x), c_int(major_y), c_double(tick_size))


def grid(x_tick, y_tick, x_org, y_org, major_x, major_y):
    """
    Draw a linear and/or logarithmic grid.

    **Parameters:**

    `x_tick`, `y_tick` :
        The length in world coordinates of the interval between minor grid
        lines.
    `x_org`, `y_org` :
        The world coordinates of the origin (point of intersection) of the grid.
    `major_x`, `major_y` :
        Unitless integer values specifying the number of minor grid lines
        between major grid lines. Values of 0 or 1 imply no grid lines.

    Major grid lines correspond to the axes origin and major tick marks whether visible
    or not. Minor grid lines are drawn at points equal to minor tick marks. Major grid
    lines are drawn using black lines and minor grid lines are drawn using gray lines.

    """
    __gr.gr_grid(c_double(x_tick), c_double(y_tick),
                 c_double(x_org), c_double(y_org),
                 c_int(major_x), c_int(major_y))


def grid3d(x_tick, y_tick, z_tick, x_org, y_org, z_org,
           major_x, major_y, major_z):
    """
    Draw a linear and/or logarithmic grid.

    **Parameters:**

    `x_tick`, `y_tick`, `z_tick` :
        The length in world coordinates of the interval between minor grid
        lines.
    `x_org`, `y_org`, `z_org` :
        The world coordinates of the origin (point of intersection) of the grid.
    `major_x`, `major_y`, `major_z` :
        Unitless integer values specifying the number of minor grid lines
        between major grid lines. Values of 0 or 1 imply no grid lines.

    Major grid lines correspond to the axes origin and major tick marks whether visible
    or not. Minor grid lines are drawn at points equal to minor tick marks. Major grid
    lines are drawn using black lines and minor grid lines are drawn using gray lines.

    """
    __gr.gr_grid3d(c_double(x_tick), c_double(y_tick), c_double(z_tick),
                   c_double(x_org), c_double(y_org), c_double(z_org),
                   c_int(major_x), c_int(major_y), c_int(major_z))


def verrorbars(px, py, e1, e2):
    """
    Draw a standard vertical error bar graph.

    **Parameters:**

    `px` :
        A list of length N containing the X coordinates
    `py` :
        A list of length N containing the Y coordinates
    `e1` :
         The absolute values of the lower error bar data
    `e2` :
         The absolute values of the upper error bar data

    """
    n = _assertEqualLength(px, py, e1, e2)
    _px = floatarray(n, px)
    _py = floatarray(n, py)
    _e1 = floatarray(n, e1)
    _e2 = floatarray(n, e2)
    __gr.gr_verrorbars(c_int(n), _px.data, _py.data, _e1.data, _e2.data)


def herrorbars(px, py, e1, e2):
    """
    Draw a standard horizontal error bar graph.

    **Parameters:**

    `px` :
        A list of length N containing the X coordinates
    `py` :
        A list of length N containing the Y coordinates
    `e1` :
         The absolute values of the lower error bar data
    `e2` :
         The absolute values of the upper error bar data

    """
    n = _assertEqualLength(px, py, e1, e2)
    _px = floatarray(n, px)
    _py = floatarray(n, py)
    _e1 = floatarray(n, e1)
    _e2 = floatarray(n, e2)
    __gr.gr_herrorbars(c_int(n), _px.data, _py.data, _e1.data, _e2.data)


def polyline3d(px, py, pz):
    """
    Draw a 3D curve using the current line attributes, starting from the
    first data point and ending at the last data point.

    **Parameters:**

    `x` :
        A list of length N containing the X coordinates
    `y` :
        A list of length N containing the Y coordinates
    `z` :
        A list of length N containing the Z coordinates

    The values for `x`, `y` and `z` are in world coordinates. The attributes that
    control the appearance of a polyline are linetype, linewidth and color
    index.

    """
    n = _assertEqualLength(px, py, pz)
    _px = floatarray(n, px)
    _py = floatarray(n, py)
    _pz = floatarray(n, pz)
    __gr.gr_polyline3d(c_int(n), _px.data, _py.data, _pz.data)


def polymarker3d(px, py, pz):
    """
    Draw marker symbols centered at the given 3D data points.

    **Parameters:**

    `x` :
        A list of length N containing the X coordinates
    `y` :
        A list of length N containing the Y coordinates
    `z` :
        A list of length N containing the Z coordinates

    The values for `x`, `y` and `z` are in world coordinates. The attributes
    that control the appearance of a polymarker are marker type, marker size
    scale factor and color index.

    """
    n = _assertEqualLength(px, py, pz)
    _px = floatarray(n, px)
    _py = floatarray(n, py)
    _pz = floatarray(n, pz)
    __gr.gr_polymarker3d(c_int(n), _px.data, _py.data, _pz.data)


def axes3d(x_tick, y_tick, z_tick, x_org, y_org, z_org,
           major_x, major_y, major_z, tick_size):
    """
    Draw X, Y and Z coordinate axes with linearly and/or logarithmically
    spaced tick marks.

    **Parameters:**

    `x_tick`, `y_tick`, `z_tick` :
        The interval between minor tick marks on each axis.
    `x_org`, `y_org`, `z_org` :
        The world coordinates of the origin (point of intersection) of the X
        and Y axes.
    `major_x`, `major_y`, `major_z` :
        Unitless integer values specifying the number of minor tick intervals
        between major tick marks. Values of 0 or 1 imply no minor ticks.
        Negative values specify no labels will be drawn for the associated axis.
    `tick_size` :
        The length of minor tick marks specified in a normalized device
        coordinate unit. Major tick marks are twice as long as minor tick marks.
        A negative value reverses the tick marks on the axes from inward facing
        to outward facing (or vice versa).

    Tick marks are positioned along each axis so that major tick marks fall on the axes
    origin (whether visible or not). Major tick marks are labeled with the corresponding
    data values. Axes are drawn according to the scale of the window. Axes and tick marks
    are drawn using solid lines; line color and width can be modified using the
    `setlinetype` and `setlinewidth` functions. Axes are drawn according to
    the linear or logarithmic transformation established by the `setscale` function.

    """
    __gr.gr_axes3d(c_double(x_tick), c_double(y_tick), c_double(z_tick),
                   c_double(x_org), c_double(y_org), c_double(z_org),
                   c_int(major_x), c_int(major_y), c_int(major_z),
                   c_double(tick_size))


def titles3d(x_title, y_title, z_title):
    """
    Display axis titles just outside of their respective axes.

    **Parameters:**

    `x_title`, `y_title`, `z_title` :
        The text to be displayed on each axis

    """
    __gr.gr_titles3d(char(x_title), char(y_title), char(z_title))


def surface(px, py, pz, option):
    """
    Draw a three-dimensional surface plot for the given data points.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `z` :
        A list of length `len(x)` * `len(y)` or an appropriately dimensioned
        array containing the Z coordinates
    `option` :
        Surface display option (see table below)

    `x` and `y` define a grid. `z` is a singly dimensioned array containing at least
    `nx` * `ny` data points. Z describes the surface height at each point on the grid.
    Data is ordered as shown in the following table:

    +------------------+--+--------------------------------------------------------------+
    |LINES             | 0|Use X Y polylines to denote the surface                       |
    +------------------+--+--------------------------------------------------------------+
    |MESH              | 1|Use a wire grid to denote the surface                         |
    +------------------+--+--------------------------------------------------------------+
    |FILLED_MESH       | 2|Applies an opaque grid to the surface                         |
    +------------------+--+--------------------------------------------------------------+
    |Z_SHADED_MESH     | 3|Applies Z-value shading to the surface                        |
    +------------------+--+--------------------------------------------------------------+
    |COLORED_MESH      | 4|Applies a colored grid to the surface                         |
    +------------------+--+--------------------------------------------------------------+
    |CELL_ARRAY        | 5|Applies a grid of individually-colored cells to the surface   |
    +------------------+--+--------------------------------------------------------------+
    |SHADED_MESH       | 6|Applies light source shading to the 3-D surface               |
    +------------------+--+--------------------------------------------------------------+

    """
    nx = len(px)
    ny = len(py)
    nz = len(pz)
    if isinstance(pz, ndarray):
        if len(pz.shape) == 1:
            out_of_bounds = nz != nx * ny
        elif len(pz.shape) == 2:
            out_of_bounds = pz.shape[0] != nx or pz.shape[1] != ny
        else:
            out_of_bounds = True
    else:
        out_of_bounds = nz != nx * ny
    if not out_of_bounds:
        _px = floatarray(nx, px)
        _py = floatarray(ny, py)
        _pz = floatarray(nx * ny, pz)
        __gr.gr_surface(c_int(nx), c_int(ny), _px.data, _py.data, _pz.data,
                        c_int(option))
    else:
        raise AttributeError("Sequences have incorrect length or dimension.")


def contour(px, py, h, pz, major_h):
    """
    Draw contours of a three-dimensional data set whose values are specified over a
    rectangular mesh. Contour lines may optionally be labeled.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `h` :
        A list containing the Z coordinate for the height values
    `z` :
        A list of length `len(x)` * `len(y)` or an appropriately dimensioned
        array containing the Z coordinates
    `major_h` :
        Directs GR to label contour lines. For example, a value of 3 would label
        every third line. A value of 1 will label every line. A value of 0
        produces no labels. To produce colored contour lines, add an offset
        of 1000 to `major_h`.

    """
    nx = len(px)
    ny = len(py)
    nz = len(pz)
    nh = len(h)
    if isinstance(pz, ndarray):
        if len(pz.shape) == 1:
            out_of_bounds = nz != nx * ny
        elif len(pz.shape) == 2:
            out_of_bounds = pz.shape[0] != nx or pz.shape[1] != ny
        else:
            out_of_bounds = True
    else:
        out_of_bounds = nz != nx * ny
    if not out_of_bounds:
        _px = floatarray(nx, px)
        _py = floatarray(ny, py)
        _h = floatarray(nh, h)
        _pz = floatarray(nz, pz)
        __gr.gr_contour(c_int(nx), c_int(ny), c_int(nh),
                        _px.data, _py.data, _h.data, _pz.data, c_int(major_h))
    else:
        raise AttributeError("Sequences have incorrect length or dimension.")


def contourf(px, py, h, pz, major_h=0):
    """
    Draw filled contours of a three-dimensional data set whose values are specified over a
    rectangular mesh.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `h` :
        A list containing the Z coordinate for the height values or the number
        of contour lines which will be evenly distributed between minimum and
        maximum Z value
    `z` :
        A list of length `len(x)` * `len(y)` or an appropriately dimensioned
        array containing the Z coordinates

    """
    nx = len(px)
    ny = len(py)
    nz = len(pz)
    if isinstance(h, int):
        nh = h
        h = None
    else:
        nh = len(h)
    if isinstance(pz, ndarray):
        if len(pz.shape) == 1:
            out_of_bounds = nz != nx * ny
        elif len(pz.shape) == 2:
            out_of_bounds = pz.shape[0] != nx or pz.shape[1] != ny
        else:
            out_of_bounds = True
    else:
        out_of_bounds = nz != nx * ny
    if not out_of_bounds:
        _px = floatarray(nx, px)
        _py = floatarray(ny, py)
        _pz = floatarray(nz, pz)
        if major_h:
            z_min, z_max, rotation, tilt = inqspace()
            setspace(np.min(pz), np.max(pz), 0, 90)
        if h:
            _h = floatarray(nh, h)
            __gr.gr_contourf(c_int(nx), c_int(ny), c_int(nh),
                             _px.data, _py.data, _h.data, _pz.data, c_int(major_h))
        else:
            __gr.gr_contourf(c_int(nx), c_int(ny), c_int(nh),
                             _px.data, _py.data, None, _pz.data, c_int(major_h))
        if major_h:
            setspace(z_min, z_max, rotation, tilt)
    else:
        raise AttributeError("Sequences have incorrect length or dimension.")


def hexbin(x, y, nbins):
    n = _assertEqualLength(x, y)
    _x = floatarray(n, x)
    _y = floatarray(n, y)
    return __gr.gr_hexbin(c_int(n), _x.data, _y.data, c_int(nbins))


def setcolormap(index):
    """
    Set the current GR colormap.

    **Parameters:**

    `index` :
        The colormap index, e.g. one of the `gr.COLORMAP_*` constants

    For a list of built-in colormaps, see https://gr-framework.org/colormaps.html.
    """
    __gr.gr_setcolormap(c_int(index))


def setcolormapfromrgb(colors, positions=None):
    """
    Define a linear interpolated colormap by a list of RGB colors.

    **Parameters:**

    `colors` :
        A list of RGB tuples containing the normalized color intensities
    `positions` :
        An optional list of length `len(colors)` containing the normalized positions where the corresponding colors
        are applied. The first element must be 0.0, the last element 1.0.

    If no `positions` are given the `colors` are evenly distributed in the linear interpolated colormap.
    Otherwise the values of `positions` define the particular position of the color in the colormap.
    """
    if positions:
        n = _assertEqualLength(colors, positions)
        _positions = floatarray(n, positions)
    else:
        n = len(colors)
        _positions = None
    _red = floatarray(n, [c[0] for c in colors])
    _green = floatarray(n, [c[1] for c in colors])
    _blue = floatarray(n, [c[2] for c in colors])
    __gr.gr_setcolormapfromrgb(c_int(n), _red.data, _green.data, _blue.data, _positions.data if _positions else None)


def colorbar():
    __gr.gr_colorbar()


def inqcolor(color):
    rgb = c_int()
    __gr.gr_inqcolor(c_int(color), byref(rgb))
    return rgb.value


def inqcolorfromrgb(red, green, blue):
    return __gr.gr_inqcolorfromrgb(c_double(red),
                                   c_double(green),
                                   c_double(blue))


def hsvtorgb(h, s, v):
    r = c_double()
    g = c_double()
    b = c_double()
    __gr.gr_hsvtorgb(c_double(h), c_double(s), c_double(v),
                     byref(r), byref(g), byref(b))
    return [r.value, g.value, b.value]

def tick(amin, amax):
    return __gr.gr_tick(c_double(amin), c_double(amax))


def validaterange(amin, amax):
    return __gr.gr_validaterange(c_double(amin), c_double(amax))


def adjustlimits(amin, amax):
    _amin = c_double(amin)
    _amax = c_double(amax)
    __gr.gr_adjustlimits(byref(_amin), byref(_amax))
    return [_amin.value, _amax.value]


def adjustrange(amin, amax):
    _amin = c_double(amin)
    _amax = c_double(amax)
    __gr.gr_adjustrange(byref(_amin), byref(_amax))
    return [_amin.value, _amax.value]


def beginprint(pathname):
    """
    Open and activate a print device.

    **Parameters:**

    `pathname` :
        Filename for the print device.

    `beginprint` opens an additional graphics output device. The device type is obtained
    from the given file extension. The following file types are supported:

    +-------------+---------------------------------------+
    |.ps, .eps    |PostScript                             |
    +-------------+---------------------------------------+
    |.pdf         |Portable Document Format               |
    +-------------+---------------------------------------+
    |.bmp         |Windows Bitmap (BMP)                   |
    +-------------+---------------------------------------+
    |.jpeg, .jpg  |JPEG image file                        |
    +-------------+---------------------------------------+
    |.png         |Portable Network Graphics file (PNG)   |
    +-------------+---------------------------------------+
    |.tiff, .tif  |Tagged Image File Format (TIFF)        |
    +-------------+---------------------------------------+
    |.fig         |Xfig vector graphics file              |
    +-------------+---------------------------------------+
    |.svg         |Scalable Vector Graphics               |
    +-------------+---------------------------------------+
    |.wmf         |Windows Metafile                       |
    +-------------+---------------------------------------+

    """
    __gr.gr_beginprint(char(pathname))


def beginprintext(pathname, mode, fmt, orientation):
    """
    Open and activate a print device with the given layout attributes.

    **Parameters:**

    `pathname` :
        Filename for the print device.
    `mode` :
        Output mode (Color, GrayScale)
    `fmt` :
        Output format (see table below)
    `orientation` :
        Page orientation (Landscape, Portait)

    The available formats are:

    +-----------+---------------+
    |A4         |0.210 x 0.297  |
    +-----------+---------------+
    |B5         |0.176 x 0.250  |
    +-----------+---------------+
    |Letter     |0.216 x 0.279  |
    +-----------+---------------+
    |Legal      |0.216 x 0.356  |
    +-----------+---------------+
    |Executive  |0.191 x 0.254  |
    +-----------+---------------+
    |A0         |0.841 x 1.189  |
    +-----------+---------------+
    |A1         |0.594 x 0.841  |
    +-----------+---------------+
    |A2         |0.420 x 0.594  |
    +-----------+---------------+
    |A3         |0.297 x 0.420  |
    +-----------+---------------+
    |A5         |0.148 x 0.210  |
    +-----------+---------------+
    |A6         |0.105 x 0.148  |
    +-----------+---------------+
    |A7         |0.074 x 0.105  |
    +-----------+---------------+
    |A8         |0.052 x 0.074  |
    +-----------+---------------+
    |A9         |0.037 x 0.052  |
    +-----------+---------------+
    |B0         |1.000 x 1.414  |
    +-----------+---------------+
    |B1         |0.500 x 0.707  |
    +-----------+---------------+
    |B10        |0.031 x 0.044  |
    +-----------+---------------+
    |B2         |0.500 x 0.707  |
    +-----------+---------------+
    |B3         |0.353 x 0.500  |
    +-----------+---------------+
    |B4         |0.250 x 0.353  |
    +-----------+---------------+
    |B6         |0.125 x 0.176  |
    +-----------+---------------+
    |B7         |0.088 x 0.125  |
    +-----------+---------------+
    |B8         |0.062 x 0.088  |
    +-----------+---------------+
    |B9         |0.044 x 0.062  |
    +-----------+---------------+
    |C5E        |0.163 x 0.229  |
    +-----------+---------------+
    |Comm10E    |0.105 x 0.241  |
    +-----------+---------------+
    |DLE        |0.110 x 0.220  |
    +-----------+---------------+
    |Folio      |0.210 x 0.330  |
    +-----------+---------------+
    |Ledger     |0.432 x 0.279  |
    +-----------+---------------+
    |Tabloid    |0.279 x 0.432  |
    +-----------+---------------+

    """
    __gr.gr_beginprintext(char(pathname), char(mode), char(fmt), char(orientation))


def endprint():
    __gr.gr_endprint()


def ndctowc(x, y):
    _x = c_double(x)
    _y = c_double(y)
    __gr.gr_ndctowc(byref(_x), byref(_y))
    return [_x.value, _y.value]


def wctondc(x, y):
    _x = c_double(x)
    _y = c_double(y)
    __gr.gr_wctondc(byref(_x), byref(_y))
    return [_x.value, _y.value]


def wc3towc(x, y, z):
    _x = c_double(x)
    _y = c_double(y)
    _z = c_double(z)
    __gr.gr_wc3towc(byref(_x), byref(_y), byref(_z))
    return [_x.value, _y.value, _z.value]


def drawrect(xmin, xmax, ymin, ymax):
    """
    Draw a rectangle using the current line attributes.

    **Parameters:**

    `xmin` :
        Lower left edge of the rectangle
    `xmax` :
        Lower right edge of the rectangle
    `ymin` :
        Upper left edge of the rectangle
    `ymax` :
        Upper right edge of the rectangle

    """
    __gr.gr_drawrect(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))


def fillrect(xmin, xmax, ymin, ymax):
    """
    Draw a filled rectangle using the current fill attributes.

    **Parameters:**

    `xmin` :
        Lower left edge of the rectangle
    `xmax` :
        Lower right edge of the rectangle
    `ymin` :
        Upper left edge of the rectangle
    `ymax` :
        Upper right edge of the rectangle

    """
    __gr.gr_fillrect(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax))


def drawarc(xmin, xmax, ymin, ymax, a1, a2):
    """
    Draw a circular or elliptical arc covering the specified rectangle.

    **Parameters:**

    `xmin` :
        Lower left edge of the rectangle
    `xmax` :
        Lower right edge of the rectangle
    `ymin` :
        Upper left edge of the rectangle
    `ymax` :
        Upper right edge of the rectangle
    `a1` :
        The start angle
    `a2` :
        The end angle

    The resulting arc begins at `a1` and ends at `a2` degrees. Angles are interpreted
    such that 0 degrees is at the 3 o'clock position. The center of the arc is the center
    of the given rectangle.

    """
    __gr.gr_drawarc(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                    c_double(a1), c_double(a2))


def fillarc(xmin, xmax, ymin, ymax, a1, a2):
    """
    Fill a circular or elliptical arc covering the specified rectangle.

    **Parameters:**

    `xmin` :
        Lower left edge of the rectangle
    `xmax` :
        Lower right edge of the rectangle
    `ymin` :
        Upper left edge of the rectangle
    `ymax` :
        Upper right edge of the rectangle
    `a1` :
        The start angle
    `a2` :
        The end angle

    The resulting arc begins at `a1` and ends at `a2` degrees. Angles are interpreted
    such that 0 degrees is at the 3 o'clock position. The center of the arc is the center
    of the given rectangle.

    """
    __gr.gr_fillarc(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                    c_double(a1), c_double(a2))


def drawpath(points, codes, fill):
    """
    Draw simple and compound outlines consisting of line segments and bezier curves.

    **Parameters:**

    `points` :
        (N, 2) array of (x, y) vertices
    `codes` :
        N-length array of path codes
    `fill` :
        A flag indication whether resulting path is to be filled or not

    The following path codes are recognized:

    +----------+-----------------------------------------------------------+
    |      STOP|end the entire path                                        |
    +----------+-----------------------------------------------------------+
    |    MOVETO|move to the given vertex                                   |
    +----------+-----------------------------------------------------------+
    |    LINETO|draw a line from the current position to the given vertex  |
    +----------+-----------------------------------------------------------+
    |    CURVE3|draw a quadratic Bézier curve                              |
    +----------+-----------------------------------------------------------+
    |    CURVE4|draw a cubic Bézier curve                                  |
    +----------+-----------------------------------------------------------+
    | CLOSEPOLY|draw a line segment to the start point of the current path |
    +----------+-----------------------------------------------------------+

    """
    _len = len(points)
    _points = floatarray(_len, points)
    if codes is not None:
        _codes = uint8array(codes)
    else:
        _codes = nothing()
    __gr.gr_drawpath(c_int(_len), _points.data, _codes.data, c_int(fill))


def setarrowstyle(style):
    """
    Set the arrow style to be used for subsequent arrow commands.

    **Parameters:**

    `style` :
        The arrow style to be used

    `setarrowstyle` defines the arrow style for subsequent arrow primitives.
    The default arrow style is 1.

    +---+----------------------------------+
    |  1|simple, single-ended              |
    +---+----------------------------------+
    |  2|simple, single-ended, acute head  |
    +---+----------------------------------+
    |  3|hollow, single-ended              |
    +---+----------------------------------+
    |  4|filled, single-ended              |
    +---+----------------------------------+
    |  5|triangle, single-ended            |
    +---+----------------------------------+
    |  6|filled triangle, single-ended     |
    +---+----------------------------------+
    |  7|kite, single-ended                |
    +---+----------------------------------+
    |  8|filled kite, single-ended         |
    +---+----------------------------------+
    |  9|simple, double-ended              |
    +---+----------------------------------+
    | 10|simple, double-ended, acute head  |
    +---+----------------------------------+
    | 11|hollow, double-ended              |
    +---+----------------------------------+
    | 12|filled, double-ended              |
    +---+----------------------------------+
    | 13|triangle, double-ended            |
    +---+----------------------------------+
    | 14|filled triangle, double-ended     |
    +---+----------------------------------+
    | 15|kite, double-ended                |
    +---+----------------------------------+
    | 16|filled kite, double-ended         |
    +---+----------------------------------+
    | 17|double line, single-ended         |
    +---+----------------------------------+
    | 18|double line, double-ended         |
    +---+----------------------------------+

    """
    __gr.gr_setarrowstyle(c_int(style))


def setarrowsize(size):
    """
    Set the arrow size to be used for subsequent arrow commands.

    **Parameters:**

    `size` :
        The arrow size to be used

    `setarrowsize` defines the arrow size for subsequent arrow primitives.
    The default arrow size is 1.

    """
    __gr.gr_setarrowsize(c_double(size))


def drawarrow(x1, y1, x2, y2):
    """
    Draw an arrow between two points.

    **Parameters:**

    `x1`, `y1` :
        Starting point of the arrow (tail)
    `x2`, `y2` :
        Head of the arrow

    Different arrow styles (angles between arrow tail and wing, optionally filled
    heads, double headed arrows) are available and can be set with the `setarrowstyle`
    function.

    """
    __gr.gr_drawarrow(c_double(x1), c_double(y1), c_double(x2), c_double(y2))


def readimage(path):
    width = c_int()
    height = c_int()
    _data = POINTER(c_int)()
    __gr.gr_readimage(char(path), byref(width), byref(height), byref(_data))
    _type = (c_int * (width.value * height.value))
    try:
        data = _type.from_address(addressof(_data.contents))
    except:
        data = []
    return [width.value, height.value, data]


def drawimage(xmin, xmax, ymin, ymax, width, height, data, model=0):
    """
    Draw an image into a given rectangular area.

    **Parameters:**

    `xmin`, `ymin` :
        First corner point of the rectangle
    `xmax`, `ymax` :
        Second corner point of the rectangle
    `width`, `height` :
        The width and the height of the image
    `data` :
        An array of color values dimensioned `width` by `height`
    `model` :
        Color model (default=0)

    The available color models are:

    +-----------------------+---+-----------+
    |MODEL_RGB              |  0|   AABBGGRR|
    +-----------------------+---+-----------+
    |MODEL_HSV              |  1|   AAVVSSHH|
    +-----------------------+---+-----------+


    The points (`xmin`, `ymin`) and (`xmax`, `ymax`) are world coordinates defining
    diagonally opposite corner points of a rectangle. This rectangle is divided into
    `width` by `height` cells. The two-dimensional array `data` specifies colors
    for each cell.

    """
    _data = intarray(width * height, data)
    __gr.gr_drawimage(c_double(xmin), c_double(xmax), c_double(ymin), c_double(ymax),
                      c_int(width), c_int(height), _data.data, c_int(model))


def importgraphics(path):
    return __gr.gr_importgraphics(char(path))


def setshadow(offsetx, offsety, blur):
    """
    `setshadow` allows drawing of shadows, realized by images painted underneath,
    and offset from, graphics objects such that the shadow mimics the effect of a light
    source cast on the graphics objects.

    **Parameters:**

    `offsetx` :
        An x-offset, which specifies how far in the horizontal direction the
        shadow is offset from the object
    `offsety` :
        A y-offset, which specifies how far in the vertical direction the shadow
        is offset from the object
    `blur` :
        A blur value, which specifies whether the object has a hard or a diffuse
        edge

    """
    __gr.gr_setshadow(c_double(offsetx), c_double(offsety), c_double(blur))


def settransparency(alpha):
    """
    Set the value of the alpha component associated with GR colors.

    **Parameters:**

    `alpha` :
        An alpha value (0.0 - 1.0)

    """
    __gr.gr_settransparency(c_double(alpha))


def setcoordxform(mat):
    """
    Change the coordinate transformation according to the given matrix.

    **Parameters:**

    `mat[3][2]` :
        2D transformation matrix

    """
    _mat = floatarray(6, mat)
    __gr.gr_setcoordxform(_mat.data)


def begingraphics(path):
    """
    Open a file for graphics output.

    **Parameters:**

    `path` :
        Filename for the graphics file.

    `begingraphics` allows to write all graphics output into a XML-formatted file until
    the `endgraphics` functions is called. The resulting file may later be imported with
    the `importgraphics` function.

    """
    __gr.gr_begingraphics(char(path))


def endgraphics():
    __gr.gr_endgraphics()


def getgraphics():
    _string = c_char_p();
    _string = __gr.gr_getgraphics()
    return _string


def drawgraphics(string):
    return __gr.gr_drawgraphics(char(string))


def mathtex(x, y, string):
    """
    Generate a character string starting at the given location. Strings can be defined
    to create mathematical symbols and Greek letters using LaTeX syntax.

    **Parameters:**

    `x`, `y` :
        Position of the text string specified in world coordinates
    `string` :
        The text string to be drawn

    """
    return __gr.gr_mathtex(c_double(x), c_double(y), char(string))


def beginselection(index, kind):
    __gr.gr_beginselection(c_int(index), c_int(kind))


def endselection():
    __gr.gr_endselection()


def moveselection(x, y):
    __gr.gr_moveselection(c_double(x), c_double(y))


def resizeselection(kind, x, y):
    __gr.gr_resizeselection(c_int(kind), c_double(x), c_double(y))


def inqbbox():
    xmin = c_double()
    xmax = c_double()
    ymin = c_double()
    ymax = c_double()
    __gr.gr_inqbbox(byref(xmin), byref(xmax), byref(ymin), byref(ymax))
    return [xmin.value, xmax.value, ymin.value, ymax.value]


def mimetype():
    global _mime_type
    return _mime_type


def isinline():
    global _mime_type
    return (_mime_type and _mime_type not in ("mov", "webm"))


def inline(mime="svg"):
    global _mime_type
    if _mime_type != mime:
        os.environ["GKS_WSTYPE"] = mime
        emergencyclosegks()
        _mime_type = mime


def show():
    global _mime_type
    emergencyclosegks()
    if _mime_type == 'svg':
        try:
            data = open('gks.svg', 'rb').read()
        except IOError:
            return None
        if not data:
            return None
        content = SVG(data=data)
        display(content)
    elif _mime_type == 'png':
        try:
            data = open('gks.png', 'rb').read()
        except IOError:
            return None
        if not data:
            return None
        content = Image(data=data, width=465, height=465)
        display(content)
    elif _mime_type == 'mov':
        try:
            data = open('gks.mov', 'rb').read()
        except IOError:
            return None
        if not data:
            return None
        content = HTML(data='<video controls autoplay type="video/mp4" src="data:video/mp4;base64,{0}">'.format(b64encode(data).decode('ascii')))
        return content
    elif _mime_type == 'webm':
        try:
            data = open('gks.webm', 'rb').read()
        except IOError:
            return None
        if not data:
            return None
        content = HTML(data='<video controls autoplay type="video/webm" src="data:video/webm;base64,{0}">'.format(b64encode(data).decode('ascii')))
        return content
    return None


def setregenflags(flags):
    __gr.gr_setregenflags(c_int(flags))


def inqregenflags():
    return __gr.gr_inqregenflags()


def savestate():
    __gr.gr_savestate()


def restorestate():
    __gr.gr_restorestate()


def selectcontext(context):
    __gr.gr_selectcontext(c_int(context))


def destroycontext(context):
    __gr.gr_destroycontext(c_int(context))


def uselinespec(linespec):
    return __gr.gr_uselinespec(char(linespec))


def trisurface(px, py, pz):
    """
    Draw a triangular surface plot for the given data points.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `z` :
        A list containing the Z coordinates

    """
    nx = len(px)
    ny = len(py)
    nz = len(pz)
    _px = floatarray(nx, px)
    _py = floatarray(ny, py)
    _pz = floatarray(nz, pz)
    n = min(nx, ny, nz)
    __gr.gr_trisurface(c_int(n), _px.data, _py.data, _pz.data)


def tricontour(px, py, pz, levels):
    """
    Draw a contour plot for the given triangle mesh.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `z` :
        A list containing the Z coordinates
    `levels` :
        A list containing the contour levels

    """
    nx = len(px)
    ny = len(py)
    nz = len(pz)
    nlevels = len(levels)
    _px = floatarray(nx, px)
    _py = floatarray(ny, py)
    _pz = floatarray(nz, pz)
    _levels = floatarray(nlevels, levels)
    n = min(nx, ny, nz)
    __gr.gr_tricontour(c_int(n), _px.data, _py.data, _pz.data, c_int(nlevels), _levels.data)

def interp2(x, y, z, xq, yq, method, extrapval, flatten=True):
    """
    Interpolation in two dimensions using one of four different methods. The
    input points are located on a grid, described by `x`, `y` and `z`.
    The target grid ist described by `xq` and `yq`.
    Returns an array containing the resulting z-values.

    **Parameters**
    `x` :
        Array containing the input grid's x-values
    `y` :
        Array containing the input grid's y-values
    `z` :
        Array containing the input grid's z-values (number of values: nx * ny)
    `xq` :
        Array containing the target grid's x-values
    `yq` :
        Array containing the target grid's y-values
    `method` :
        Used method for interpolation
    `extrapval` :
        The extrapolation value
    `flatten` (optional):
        Default: `True`
        If `flatten=True` the resulting NumPy Array is flat [...]
        If `flatten=False` the resulting NumPy Array is a
        2-dimensional array [[], ..., []]

    The available methods for interpolation are the following:

    +-----------------+---+-------------------------------------------+
    | INTERP2_NEAREST | 0 | Nearest neighbour interpolation           |
    +-----------------+---+-------------------------------------------+
    | INTERP2_LINEAR  | 1 | Linear interpolation                      |
    +-----------------+---+-------------------------------------------+
    | INTERP_2_SPLINE | 2 | Interpolation using natural cubic splines |
    +-----------------+---+-------------------------------------------+
    | INTERP2_CUBIC   | 3 | Cubic interpolation                       |
    +-----------------+---+-------------------------------------------+

    """
    nx = len(x)
    ny = len(y)
    nz = len(z)
    nxq = len(xq)
    nyq = len(yq)
    _x = floatarray(nx, x)
    _y = floatarray(ny, y)
    _z = floatarray(nz, z)
    _xq = floatarray(nxq, xq)
    _yq = floatarray(nyq, yq)
    zq = empty([nxq, nyq], dtype=float64)
    __gr.gr_interp2(c_int(nx), c_int(ny), _x.data, _y.data, _z.data, c_int(nxq), c_int(nyq), _xq.data, _yq.data, zq.ctypes.data_as(POINTER(c_double)), c_int(method), c_double(extrapval))
    if flatten:
        zq.shape = prod(zq.shape)
    return zq


def shadepoints(x, y, dims=(1200, 1200), xform=1):
    """
    Display a point set as an aggregated and rasterized image using the current GR colormap.

    **Parameters:**

    `x` :
        A pointer to the X coordinates
    `y` :
        A pointer to the Y coordinates
    `dims` :
        The size of the grid used for rasterization
    `xform` :
        The transformation type used for color mapping

    The values for `x` and `y` are in world coordinates.

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
    """
    assert len(x) == len(y)
    n = len(x)
    w, h = dims
    _x = floatarray(n, x)
    _y = floatarray(n, y)
    __gr.gr_shadepoints(c_int(n), _x.data, _y.data, xform, w, h)


def shadelines(x, y, dims=(1200, 1200), xform=1):
    """
    Display a line set as an aggregated and rasterized image using the current GR colormap.

    **Parameters:**

    `x` :
        A pointer to the X coordinates
    `y` :
        A pointer to the Y coordinates
    `dims` :
        The size of the grid used for rasterization
    `xform` :
        The transformation type used for color mapping

    The values for `x` and `y` are in world coordinates.
    NaN values can be used to separate the point set into line segments.

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
    """
    assert len(x) == len(y)
    n = len(x)
    w, h = dims
    _x = floatarray(n, x)
    _y = floatarray(n, y)
    __gr.gr_shadelines(c_int(n), _x.data, _y.data, xform, w, h)


def volume(data, algorithm=0, dmin=-1, dmax=-1):
    """
    Draw volume data using the given algorithm and apply the current GR colormap.
    Returns the minimum and maximum data value that were used when applying the colormap.

    **Parameters:**

    `data` :
        3D numpy array containing the intensities for each point
    `algorithm` :
        The algorithm used to reduce the volume data
    `dmin` :
        The minimum data value when applying the colormap. If it is negative, the actual occurring minimum is used.
    `dmax` :
        The maximum data value when applying the colormap. If it is negative, the actual occurring maximum is used.

    Available algorithms are:

    +------------------+---+-----------------------------+
    |VOLUME_EMISSION   |  0|emission model               |
    +------------------+---+-----------------------------+
    |VOLUME_ABSORPTION |  1|absorption model             |
    +------------------+---+-----------------------------+
    |VOLUME_MIP        |  2|maximum intensity projection |
    +------------------+---+-----------------------------+
    """
    import gr3
    data = np.array(data, copy=False, ndmin=3)
    nz, ny, nx = data.shape
    _data = floatarray(nx * ny * nz, data)
    _dmin = c_double(dmin)
    _dmax = c_double(dmax)
    gr3._gr3.gr_volume(nx, ny, nz, _data.data, c_int(algorithm), byref(_dmin),  byref(_dmax))
    return _dmin.value, _dmax.value


@_require_runtime_version(0, 41, 5, 43)
def setresamplemethod(resample_method):
    """
    Set the resample method used for gr.drawimage().

    :param resample_method: the new resample method

    The available options are:

    +------------------+------------+--------------------+
    |RESAMPLE_DEFAULT  | 0x00000000 |default             |
    +------------------+------------+--------------------+
    |RESAMPLE_NEAREST  | 0x01010101 |nearest neighbour   |
    +------------------+------------+--------------------+
    |RESAMPLE_LINEAR   | 0x02020202 |linear              |
    +------------------+------------+--------------------+
    |RESAMPLE_LANCZOS  | 0x03030303 |Lanczos             |
    +------------------+------------+--------------------+

    Alternatively, combinations of these methods can be selected for horizontal or vertical upsampling or downsampling:

    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_VERTICAL_DEFAULT     | 0x00000000 | default for vertical upsampling              |
    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_HORIZONTAL_DEFAULT   | 0x00000000 | default for horizontal upsampling            |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_VERTICAL_DEFAULT   | 0x00000000 | default for vertical downsampling            |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_HORIZONTAL_DEFAULT | 0x00000000 | default for horizontal downsampling          |
    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_VERTICAL_NEAREST     | 0x00000001 | nearest neighbor for vertical upsampling     |
    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_HORIZONTAL_NEAREST   | 0x00000100 | nearest neighbor for horizontal upsampling   |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_VERTICAL_NEAREST   | 0x00010000 | nearest neighbor for vertical downsampling   |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_HORIZONTAL_NEAREST | 0x01000000 | nearest neighbor for horizontal downsampling |
    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_VERTICAL_LINEAR      | 0x00000002 | linear for vertical upsampling               |
    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_HORIZONTAL_LINEAR    | 0x00000200 | linear for horizontal upsampling             |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_VERTICAL_LINEAR    | 0x00020000 | linear for vertical downsampling             |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_HORIZONTAL_LINEAR  | 0x02000000 | linear for horizontal downsampling           |
    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_VERTICAL_LANCZOS     | 0x00000003 | lanczos for vertical upsampling              |
    +-------------------------------+------------+----------------------------------------------+
    | UPSAMPLE_HORIZONTAL_LANCZOS   | 0x00000300 | lanczos for horizontal upsampling            |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_VERTICAL_LANCZOS   | 0x00030000 | lanczos for vertical downsampling            |
    +-------------------------------+------------+----------------------------------------------+
    | DOWNSAMPLE_HORIZONTAL_LANCZOS | 0x03000000 | lanczos for horizontal downsampling          |
    +-------------------------------+------------+----------------------------------------------+
    """
    __gr.gr_setresamplemethod(c_uint(resample_method))


@_require_runtime_version(0, 41, 5, 43)
def inqresamplemethod():
    """
    Inquire the resample method used for gr.drawimage().

    :return: the current resample method
    """
    _resample_method = c_uint(0)
    __gr.gr_inqresamplemethod(byref(_resample_method))
    return _resample_method.value


@_require_runtime_version(0, 45, 0)
def path(x, y, codes):
    """
    Draw paths using the given vertices and path codes.

    **Parameters:**

    `x` :
        A list containing the X coordinates
    `y` :
        A list containing the Y coordinates
    `codes` :
        A list containing the path codes

    The values for `x` and `y` are in world coordinates.
    The `codes` describe several path primitives that can be used to create compound paths.

    The following path codes are recognized:


    +----------+---------------------------------+-------------------+-------------------+
    | **Code** | **Description**                 | **x**             | **y**             |
    +----------+---------------------------------+-------------------+-------------------+
    |     M, m | move                            | x                 | y                 |
    +----------+---------------------------------+-------------------+-------------------+
    |     L, l | line                            | x                 | y                 |
    +----------+---------------------------------+-------------------+-------------------+
    |     Q, q | quadratic Bezier                | x1, x2            | y1, y2            |
    +----------+---------------------------------+-------------------+-------------------+
    |     C, c | cubic Bezier                    | x1, x2, x3        | y1, y2, y3        |
    +----------+---------------------------------+-------------------+-------------------+
    |     A, a | arc                             | rx, a1, reserved  | ry, a2, reserved  |
    +----------+---------------------------------+-------------------+-------------------+
    |        Z | close path                      |                   |                   |
    +----------+---------------------------------+-------------------+-------------------+
    |        S | stroke                          |                   |                   |
    +----------+---------------------------------+-------------------+-------------------+
    |        s | close path and stroke           |                   |                   |
    +----------+---------------------------------+-------------------+-------------------+
    |        f | close path and fill             |                   |                   |
    +----------+---------------------------------+-------------------+-------------------+
    |        F | close path, fill and stroke     |                   |                   |
    +----------+---------------------------------+-------------------+-------------------+


     - Move: `M`, `m`

        Moves the current position to (`x`, `y`). The new position is either absolute (`M`) or relative to the current
        position (`m`). The initial position of :py:func:`gr.path` is (0, 0).

        Example:

        >>> gr.path([0.5, -0.1], [0.2, 0.1], "Mm")

        The first move command in this example moves the current position to the absolute coordinates (0.5, 0.2). The
        second move to performs a movement by (-0.1, 0.1) relative to the current position resulting in the point
        (0.4, 0.3).


     - Line: `L`, `l`

        Draws a line from the current position to the given position (`x`, `y`). The end point of the line is either
        absolute (`L`) or relative to the current position (`l`). The current position is set to the end point of the
        line.

        Example:

        >>> gr.path([0.1, 0.5, 0.0], [0.1, 0.1, 0.2], "MLlS")

        The first line to command draws a straight line from the current position (0.1, 0.1) to the absolute position
        (0.5, 0.1) resulting in a horizontal line. The second line to command draws a vertical line relative to the
        current position resulting in the end point (0.5, 0.3).


     - Quadratic Bezier curve: `Q`, `q`

        Draws a quadratic bezier curve from the current position to the end point (`x2`, `y2`) using (`x1`, `y1`) as the
        control point. Both points are either absolute (`Q`) or relative to the current position (`q`). The current
        position is set to the end point of the bezier curve.

        Example:

        >>> gr.path([0.1, 0.3, 0.5, 0.2, 0.4], [0.1, 0.2, 0.1, 0.1, 0.0], "MQqS")

        This example will generate two bezier curves whose start and end points are each located at y=0.1. As the control
        points are horizontally in the middle of each bezier curve with a higher y value both curves are symmetrical
        and bend slightly upwards in the middle. The current position is set to (0.9, 0.1) at the end.


     - Cubic Bezier curve: `C`, `c`

        Draws a cubic bezier curve from the current position to the end point (`x3`, `y3`) using (`x1`, `y1`) and
        (`x2`, `y2`) as the control points. All three points are either absolute (`C`) or relative to the current position
        (`c`). The current position is set to the end point of the bezier curve.

        Example:

        >>> gr.path(
        ...     [0.1, 0.2, 0.3, 0.4, 0.1, 0.2, 0.3],
        ...     [0.1, 0.2, 0.0, 0.1, 0.1, -0.1, 0.0],
        ...     "MCcS"
        ... )

        This example will generate two bezier curves whose start and end points are each located at y=0.1. As the control
        points are equally spaced along the x-axis and the first is above and the second is below the start and end
        points this creates a wave-like shape for both bezier curves. The current position is set to (0.8, 0.1) at the
        end.


     - Ellipctical arc: `A`, `a`

        Draws an elliptical arc starting at the current position. The major axis of the ellipse is aligned with the x-axis
        and the minor axis is aligned with the y-axis of the plot. `rx` and `ry` are the ellipses radii along the major
        and minor axis. `a1` and `a2` define the start and end angle of the arc in radians. The current position is set
        to the end point of the arc. If `a2` is greater than `a1` the arc is drawn counter-clockwise, otherwise it is
        drawn clockwise. The `a` and `A` commands draw the same arc. The third coordinates of the `x` and `y` array are
        ignored and reserved for future use.

        Examples:


        >>> gr.path([0.1, 0.2, -3.14159 / 2, 0.0], [0.1, 0.4, 3.14159 / 2, 0.0], "MAS")

        This example draws an arc starting at (0.1, 0.1). As the start angle -pi/2 is smaller than the end angle pi/2 the
        arc is drawn counter-clockwise. In this case the right half of an ellipse with an x radius of 0.2 and a y radius
        of 0.4 is shown. Therefore the current position is set to (0.1, 0.9) at the end.

        >>> gr.path([0.1, 0.2, 3.14159 / 2, 0.0], [0.9, 0.4, -3.14159 / 2, 0.0], "MAS")

        This examples draws the same arc as the previous one. The only difference is that the starting point is now at
        (0.1, 0.9) and the start angle pi/2 is greater than the end angle -pi/2 so that the ellipse arc is drawn
        clockwise. Therefore the current position is set to (0.1, 0.1) at the end.


     - Close path: `Z`

        Closes the current path by connecting the current position to the target position of the last move command
        (`m` or `M`) with a straight line. If no move to was performed in this path it connects the current position to
        (0, 0). When the path is stroked this line will also be drawn.


     - Stroke path: `S`, `s`

        Strokes the path with the current border width and border color (set with :py:func:`gr.setborderwidth` and
        :py:func:`gr.setbordercolorind`). In case of `s` the path is closed beforehand, which is equivalent to `ZS`.


     - Fill path: `F`, `f`

        Fills the current path using the even-odd-rule using the current fill color. Filling a path implicitly closes
        the path. The fill color can be set using :py:func:`gr.setfillcolorind`. In case of `F` the path is also
        stroked using the current border width and color afterwards.
    """
    n = _assertEqualLength(x, y)
    _x = floatarray(n, x)
    _y = floatarray(n, y)
    _codes = create_string_buffer(''.join(codes).encode('ascii'))
    __gr.gr_path(c_int(n), _x.data, _y.data, _codes)


@_require_runtime_version(0, 45, 0)
def setborderwidth(width):
    """
    Defines the width of subsequent path borders.

    **Parameters:**

    `width` :
        The border width
    """
    __gr.gr_setborderwidth(c_double(width))


@_require_runtime_version(0, 45, 0)
def inqborderwidth():
    """
    Returns the width of path borders.
    """
    width = c_double()
    __gr.gr_inqborderwidth(byref(width))
    return width.value


@_require_runtime_version(0, 45, 0)
def setbordercolorind(color):
    """
    Defines the color of subsequent path borders.

    **Parameters:**

    `color` :
        The border color index (COLOR < 1256)
    """
    __gr.gr_setbordercolorind(c_int(color))


@_require_runtime_version(0, 45, 0)
def inqbordercolorind():
    """
    Returns the color index of path borders.
    """
    coli = c_int()
    __gr.gr_inqbordercolorind(byref(coli))
    return coli.value


@_require_runtime_version(0, 46, 0, 76)
def setprojectiontype(projection_type):
    """
    Set the projection type with this flag.

    `projection_type` :
        Projection type

    The available options are:

    +------------------------+---+--------------+
    |PROJECTION_DEFAULT      |  0|default       |
    +------------------------+---+--------------+
    |PROJECTION_ORTHOGRAPHIC |  1|orthographic  |
    +------------------------+---+--------------+
    |PROJECTION_PERSPECTIVE  |  2|perspective   |
    +------------------------+---+--------------+

    """
    __gr.gr_setprojectiontype(c_int(projection_type))


@_require_runtime_version(0, 46, 0, 76)
def inqprojectiontype():
    """
    Return the projection type.
    """
    projection_type = c_int()
    __gr.gr_inqprojectiontype(byref(projection_type))
    return projection_type.value


@_require_runtime_version(0, 46, 0, 76)
def setperspectiveprojection(near_plane, far_plane, fov):
    """
    Set the far and near clipping planes and the vertical field of view.

    **Parameters:**

    `near_plane` :
        distance to near clipping plane
    `far_plane` :
        distance to far clipping plane
    `fov` :
        vertical field of view, must be between 0 and 180 degrees

    Switches projection type to perspective.
    """
    __gr.gr_setperspectiveprojection(c_double(near_plane), c_double(far_plane), c_double(fov))


@_require_runtime_version(0, 46, 0, 76)
def setorthographicprojection(left, right, bottom, top, near_plane, far_plane):
    """
    Set parameters for orthographic transformation.

    **Parameters:**

    `left` :
        xmin of the volume in world coordinates
    `right` :
        xmax of volume in world coordinates
    `bottom` :
        ymin of volume in world coordinates
    `top` :
        ymax of volume in world coordinates
    `near_plane` :
        distance to near clipping plane
    `far_plane` :
        distance to far clipping plane

    Switches projection type to orthographic.
    """
    __gr.gr_setorthographicprojection(c_double(left), c_double(right), c_double(bottom), c_double(top), c_double(near_plane), c_double(far_plane))


@_require_runtime_version(0, 46, 0, 76)
def settransformationparameters(camera_position_x, camera_position_y, camera_position_z, up_vector_x, up_vector_y, up_vector_z, focus_point_x, focus_point_y, focus_point_z):
    """
    Method to set the camera position, the upward facing direction and the focus point of the shown volume.

    **Parameters:**

    `camera_position_x` :
        x component of the camera position in world coordinates
    `camera_position_y` :
        y component of the camera position in world coordinates
    `camera_position_z` :
        z component of the camera position in world coordinates
    `up_vector_x` :
        x component of the up vector
    `up_vector_y` :
        y component of the up vector
    `up_vector_z` :
        z component of the up vector
    `focus_point_x` :
        x component of focus-point inside volume
    `focus_point_y` :
        y component of focus-point inside volume
    `focus_point_z` :
        z component of focus-point inside volume
    """
    __gr.gr_settransformationparameters(c_double(camera_position_x), c_double(camera_position_y), c_double(camera_position_z), c_double(up_vector_x), c_double(up_vector_y), c_double(up_vector_z), c_double(focus_point_x), c_double(focus_point_y), c_double(focus_point_z))


@_require_runtime_version(0, 46, 0, 76)
def inqtransformationparameters():
    """
    Return the camera position, up vector and focus point.
    """
    camera_position_x = c_double()
    camera_position_y = c_double()
    camera_position_z = c_double()
    up_vector_x = c_double()
    up_vector_y = c_double()
    up_vector_z = c_double()
    focus_point_x = c_double()
    focus_point_y = c_double()
    focus_point_z = c_double()
    __gr.gr_inqtransformationparameters(byref(camera_position_x), byref(camera_position_y), byref(camera_position_z), byref(up_vector_x), byref(up_vector_y), byref(up_vector_z), byref(focus_point_x), byref(focus_point_y), byref(focus_point_z))
    return [camera_position_x.value, camera_position_y.value, camera_position_z.value, up_vector_x.value, up_vector_y.value, up_vector_z.value, focus_point_x.value, focus_point_y.value, focus_point_z.value]


@_require_runtime_version(0, 46, 0, 76)
def inqorthographicprojection():
    """
    Return the parameters for the orthographic projection.
    """
    left = c_double()
    right = c_double()
    bottom = c_double()
    top = c_double()
    near_plane = c_double()
    far_plane = c_double()
    __gr.gr_inqorthographicprojection(byref(left), byref(right), byref(bottom), byref(top), byref(near_plane), byref(far_plane))
    return [left.value, right.value, bottom.value, top.value, near_plane.value, far_plane.value]


@_require_runtime_version(0, 46, 0, 76)
def inqperspectiveprojection():
    """
    Return the parameters for the perspective projection.
    """
    near_plane = c_double()
    far_plane = c_double()
    fovy = c_double()
    __gr.gr_inqperspectiveprojection(byref(near_plane), byref(far_plane), byref(fovy))
    return [near_plane.value, far_plane.value, fovy.value]


@_require_runtime_version(0, 46, 0, 76)
def camerainteraction(start_mouse_position_x, start_mouse_position_y, end_mouse_position_x, end_mouse_position_y):
    """
    Interface for interaction with the rotation of the model. For this a virtual Arcball is used.

    **Parameters:**

    `start_mouse_position_x` :
        x component of the start mouse position
    `start_mouse_position_y` :
        y component of the start mouse position
    `end_mouse_position_x` :
        x component of the end mouse position
    `end_mouse_position_y` :
        y component of the end mouse position

    """
    __gr.gr_camerainteraction(c_double(start_mouse_position_x), c_double(start_mouse_position_y), c_double(end_mouse_position_x), c_double(end_mouse_position_y))


@_require_runtime_version(0, 46, 0, 76)
def setwindow3d(x_min, x_max, y_min, y_max, z_min, z_max):
    """
    Set the three dimensional window. Only used for perspective and orthographic projection.

    **Parameters:**

    `xmin` :
        min x-value
    `xmax` :
        max x-value
    `ymin` :
        min y-value
    `ymax` :
        max y-value
    `zmin` :
        min z-value
    `zmax` :
        max z-value
    """
    __gr.gr_setwindow3d(c_double(x_min), c_double(x_max), c_double(y_min), c_double(y_max), c_double(z_min), c_double(z_max))


@_require_runtime_version(0, 46, 0, 76)
def inqwindow3d():
    """
    Return the three dimensional window.
    """
    xmin = c_double()
    xmax = c_double()
    ymin = c_double()
    ymax = c_double()
    zmin = c_double()
    zmax = c_double()
    __gr.gr_inqwindow3d(byref(xmin), byref(xmax), byref(ymin), byref(ymax), byref(zmin), byref(zmax))
    return [xmin.value, xmax.value, ymin.value, ymax.value, zmin.value, zmax.value]


@_require_runtime_version(0, 48, 0, 0)
def setscalefactors3d(x_axis_scale, y_axis_scale, z_axis_scale):
    """
    Set the scaling factor for each axis.

    The scaling factors must not be zero.

    **Parameters:**

    `x_axis_scale` :
        x axis scaling factor
    `y_axis_scale` :
        y axis scaling factor
    `z_axis_scale` :
        z axis scaling factor
    """
    __gr.gr_setscalefactors3d(c_double(x_axis_scale), c_double(y_axis_scale), c_double(z_axis_scale))


@_require_runtime_version(0, 48, 0, 0)
def inqscalefactors3d():
    """
    Return the scaling factor for each axis.
    """
    x_axis_scale = c_double()
    y_axis_scale = c_double()
    z_axis_scale = c_double()
    __gr.gr_inqscalefactors3d(byref(x_axis_scale), byref(y_axis_scale), byref(z_axis_scale))
    return [x_axis_scale.value, y_axis_scale.value, z_axis_scale.value]


@_require_runtime_version(0, 48, 0, 0)
def setspace3d(phi, theta, fov, camera_distance):
    """
    Set the camera for orthographic or perspective projection.

    The center of the 3d window is used as the focus point and the camera is
    positioned relative to it, using camera distance, rotation and tilt similar
    to gr_setspace. This function can be used if the user prefers spherical
    coordinates to setting the camera position directly, but has reduced
    functionality in comparison to gr.settransformationparameters,
    gr.setscalefactors3d, gr.setperspectiveprojection and
    gr.setorthographicprojection.

    **Parameters:**

    `phi` :
        azimuthal angle of the spherical coordinates
    `theta` :
        polar angle of the spherical coordinates
    `fov` :
        vertical field of view
        (0 or NaN for orthographic projection)
    `camera distance` :
        distance between the camera and the focus point
        (in arbitrary units, 0 or NaN for the radius of the object's smallest bounding sphere)
    """
    __gr.gr_setspace3d(c_double(phi), c_double(theta), c_double(fov), c_double(camera_distance))


@_require_runtime_version(0, 58, 0, 0)
def setthreadnumber(num):
    """
    Set the number of threads which can run parallel.

    The default value is the number of threads the cpu has. The only usage
    right now is inside gr_cpubasedvolume.

    **Parameters:**

    `num` :
        number of threads
    """
    __gr.gr_setthreadnumber(c_int(num))


@_require_runtime_version(0, 58, 0, 0)
def setpicturesizeforvolume(width, height):
    """
    Set the width and height of the resulting picture. These values are only used for gr_volume and gr_cpubasedvolume.

    The default values are 1000 for both.

    **Parameters:**

    `width` :
        width of the resulting image
    `height` :
        height of the resulting image
    """
    __gr.gr_setpicturesizeforvolume(c_int(width), c_int(height))


@_require_runtime_version(0, 58, 0, 0)
def setvolumebordercalculation(flag):
    """
    Set the gr_volume border type with this flag.

    This influences how the volume is calculated. When the flag is set to
    VOLUME_WITH_BORDER the border will be calculated the same as the points
    inside the volume.

    **Parameters:**

    `flag` :
        calculation of the gr.volume border

    The available options are:

    +---------------------------+---+-----------------------+
    |VOLUME_WITHOUT_BORDER   |  0|default value          |
    +---------------------------+---+-----------------------+
    |VOLUME_WITH_BORDER      |  1|gr_volume with border  |
    +---------------------------+---+-----------------------+
    """
    __gr.gr_setvolumebordercalculation(c_int(flag))


@_require_runtime_version(0, 58, 0, 0)
def setapproximativecalculation(approximative_calculation):
    """
    Set if gr_cpubasedvolume is calculated approximative or exact.

    To use the exact calculation set approximative_calculation to 0. The
    default value is the approximative version, which can be set with the
    number 1.

    **Parameters:**

    `approximative_calculation` :
        exact or approximative calculation of the volume
    """
    if isinstance(approximative_calculation, bool):
        approximative_calculation = 1 if approximative_calculation else 0
    __gr.gr_setapproximativecalculation(c_int(approximative_calculation))


@_require_runtime_version(0, 58, 0, 0)
def inqvolumeflags():
    """
    Returns the parameters which can be set for gr_cpubasedvolume.

    The following parameters are returned as a tuple:

    - volume border type (VOLUME_WITHOUT_BORDER or VOLUME_WITH_BORDER)
    - maximum number of threads used
    - picture width in pixels
    - picture height in pixels
    - whether or not the approximative calculation is used
    """
    border = c_int()
    max_threads = c_int()
    picture_width = c_int()
    picture_height = c_int()
    approximative_calculation = c_int()
    __gr.gr_inqvolumeflags(byref(border), byref(max_threads), byref(picture_width), byref(picture_height), byref(approximative_calculation))

    return (
        border.value,
        max_threads.value,
        picture_width.value,
        picture_height.value,
        True if approximative_calculation.value else False
    )


@_require_runtime_version(0, 58, 0, 0)
def cpubasedvolume(data, algorithm, dmin, dmax, min_val, max_val):
    """
    Draw volume data with raycasting using the given algorithm and apply the current GR colormap.

    The minimum and maximum values used for the colormap are returned as a tuple.

    **Parameters:**

    `data` :
        a three-dimensional numpy array containing the intensities for each point
    `algorithm` :
        the algorithm to reduce the volume data
    `dmin` :
        minimum value when applying the colormap, or None to use the actual occuring minimum
    `dmax` :
        maximum value when applying the colormap, or None to use the actual occuring maximum
    `min_val` :
        array with the minimum coordinates of the volume data, or None to use -1 for each axis
    `max_val` :
        array with the maximum coordinates of the volume data, or None to use 1 for each axis

    Available algorithms are:

    +---------------------+---+-----------------------------+
    |VOLUME_EMISSION   |  0|emission model               |
    +---------------------+---+-----------------------------+
    |VOLUME_ABSORPTION |  1|absorption model             |
    +---------------------+---+-----------------------------+
    |VOLUME_MIP        |  2|maximum intensity projection |
    +---------------------+---+-----------------------------+
    """

    data = np.array(data, copy=False, ndmin=3)
    nz, ny, nx = data.shape
    _data = floatarray(nx * ny * nz, data)
    if dmin is None:
        dmin = c_double(-1)
    else:
        dmin = c_double(dmin)
    if dmax is None:
        dmax = c_double(-1)
    else:
        dmax = c_double(dmax)
    if min_val is None:
        min_val_ptr = cast(c_void_p(0), POINTER(c_double))
    else:
        min_val_ptr = (c_double * 3)(min_val[0], min_val[1], min_val[2])
    if max_val is None:
        max_val_ptr = cast(c_void_p(0), POINTER(c_double))
    else:
        max_val_ptr = (c_double * 3)(max_val[0], max_val[1], max_val[2])

    __gr.gr_cpubasedvolume(c_int(nx), c_int(ny), c_int(nz), _data.data, c_int(algorithm), byref(dmin), byref(dmax), min_val_ptr, max_val_ptr)

    return dmin.value, dmax.value

class _point3d_t(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]

class _data_point3d_t(Structure):
    _fields_ = [("pt", _point3d_t),
                ("data", c_double),
                ("extra_data", c_void_p)]

_kernel_f = CFUNCTYPE(c_double, POINTER(_data_point3d_t), c_void_p, POINTER(_point3d_t), POINTER(_point3d_t))
_radius_f = CFUNCTYPE(c_double, POINTER(_data_point3d_t), c_void_p)


@_require_runtime_version(0, 67, 0, 0)
def volume_nogrid(data, algorithm, kernel, radius, extra_data=None):
    """
    Draws a volume that is represented without a grid using Splatting and the given algorithm.

    See also `volume_interp_tri_linear_init` to initialize trilinear interpolation and `volume_interp_gauss_init`.

    **Parameters:**

    `data` :
        a list of points to be drawn, e.g. [(x, y, z, intensity), (x, y, z, intensity), ...]
    `algorithm` :
        the algorithm to reduce the volume data. Selectable options are `VOLUME_EMISSION` and `VOLUME_ABSORPTION`
    `kernel` :
        The interpolation kernel to use. Can be "trilinear" or "gauss" or custom, but performance will be low using a custom kernel
    `radius` :
        Radius of each data point to be taken into account. Intensity outside of the radius can be left out.
    `extra_data` :
        Custom data to be passed to a custom kernel function.
    """
    if kernel == "trilinear":
        kernel = cast(__gr.gr_volume_interp_tri_linear, _kernel_f)
    elif kernel == "gauss":
        kernel = cast(__gr.gr_volume_interp_gauss, _kernel_f)
    else:
        kernel = _kernel_f(kernel)

    radius_d = 1
    radius_f = 0

    if type(radius) == int or type(radius) == float:
        radius_d = radius
    else:
        radius_f = radius

    radius_f = _radius_f(radius_f)

    dmin = c_double(-1)
    dmax = c_double(-1)

    data = np.array(data, copy=False, ndmin=2)
    shape = data.shape
    if len(shape) != 2 and shape[1] != 4:
        raise ValueError("Data must be in shape (n, 4)!")

    cnt = shape[0]
    _data = floatarray(cnt * 4, data)

    __gr.gr_volume_nogrid(cnt, cast(_data.data, POINTER(_data_point3d_t)), c_void_p(extra_data), algorithm, kernel, byref(dmin), byref(dmax), radius_d, radius_f)

    return dmin.value, dmax.value


@_require_runtime_version(0, 67, 0, 0)
def volume_interp_tri_linear_init(dist_x, dist_y, dist_z):
    """
    Initializes the trilinear interpolation funciton for `volume_nogrid` with the three axis-aligned distances

    **Parameters:**

    `dist_x`, `dist_y`, `dist_z` :
        The distance between two density points. The extent of one point is 2 * dist_x, 2 * dist_y, 2 * dist_z
    """
    __gr.gr_volume_interp_tri_linear_init(c_double(dist_x), c_double(dist_y), c_double(dist_z))

@_require_runtime_version(0, 67, 0, 0)
def volume_interp_gauss_init(det, sigma_inv_1_2):
    """
    Initializes the gaussian interpolation kernel with the given covariance matrix (as sigma^(-1/2)) and det as `|sigma|`

    The density of a data point will be distributed according to a gaussian density with the given matrix.

    **Parameters:**

    `det` :
        The determinant of the covariance matrix
    `sigma_inv_1_2` :
        The inverted and square rooted covariance matrix.
    """
    sigma_inv_1_2 = np.array(sigma_inv_1_2, copy=False, ndmin=3)
    _s = floatarray(9, sigma_inv_1_2)

    __gr.gr_volume_interp_gauss_init(c_double(det), _s.data)

def wrapper_version():
    """
    Returns the version string of the Python package gr.
    """
    return __version__


def runtime_version():
    """
    Returns the version string of the GR runtime.
    """
    global _RUNTIME_VERSION_STR
    return _RUNTIME_VERSION_STR


def version():
    """
    Returns the combined version strings of the GR runtime and Python package.
    """
    return 'Runtime: {} / Python: {}'.format(runtime_version(), wrapper_version())


_grPkgDir = os.path.realpath(os.path.dirname(__file__))
_gksFontPath = os.path.join(_grPkgDir, "fonts")
if os.access(_gksFontPath, os.R_OK):
    os.environ["GKS_FONTPATH"] = os.getenv("GKS_FONTPATH", _grPkgDir)

__gr = load_runtime()
if __gr is None:
    raise ImportError('Failed to load GR runtime!')
register_gksterm()

__gr.gr_opengks.argtypes = []
__gr.gr_closegks.argtypes = []
__gr.gr_inqdspsize.argtypes = [POINTER(c_double), POINTER(c_double),
                               POINTER(c_int), POINTER(c_int)]
__gr.gr_openws.argtypes = [c_int, c_char_p, c_int]
__gr.gr_closews.argtypes = [c_int]
__gr.gr_activatews.argtypes = [c_int]
__gr.gr_deactivatews.argtypes = [c_int]
__gr.gr_configurews.argtypes = []
__gr.gr_clearws.argtypes = []
__gr.gr_updatews.argtypes = []
__gr.gr_polyline.argtypes = [c_int, POINTER(c_double), POINTER(c_double)]
__gr.gr_polymarker.argtypes = [c_int, POINTER(c_double), POINTER(c_double)]
__gr.gr_text.argtypes = [c_double, c_double, c_char_p]
__gr.gr_fillarea.argtypes = [c_int, POINTER(c_double), POINTER(c_double)]
__gr.gr_cellarray.argtypes = [
    c_double, c_double, c_double, c_double, c_int, c_int, c_int, c_int, c_int, c_int,
    POINTER(c_int)]
__gr.gr_polarcellarray.argtypes = [
    c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int,
    c_int, c_int, c_int, POINTER(c_int)]
__gr.gr_spline.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, c_int]
__gr.gr_gridit.argtypes = [
    c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int,
    POINTER(c_double), POINTER(c_double), POINTER(c_double)]
__gr.gr_setlinetype.argtypes = [c_int]
__gr.gr_inqlinetype.argtypes = [POINTER(c_int)]
__gr.gr_setlinewidth.argtypes = [c_double]
__gr.gr_inqlinewidth.argtypes = [POINTER(c_double)]
__gr.gr_setlinecolorind.argtypes = [c_int]
__gr.gr_inqlinecolorind.argtypes = [POINTER(c_int)]
__gr.gr_setmarkertype.argtypes = [c_int]
__gr.gr_inqmarkertype.argtypes = [POINTER(c_int)]
__gr.gr_setmarkersize.argtypes = [c_double]
__gr.gr_setmarkercolorind.argtypes = [c_int]
__gr.gr_inqmarkercolorind.argtypes = [POINTER(c_int)]
__gr.gr_settextfontprec.argtypes = [c_int, c_int]
__gr.gr_setcharexpan.argtypes = [c_double]
__gr.gr_setcharspace.argtypes = [c_double]
__gr.gr_settextcolorind.argtypes = [c_int]
__gr.gr_setcharheight.argtypes = [c_double]
__gr.gr_setwscharheight.argtypes = [c_double, c_double]
__gr.gr_setcharup.argtypes = [c_double, c_double]
__gr.gr_settextpath.argtypes = [c_int]
__gr.gr_settextalign.argtypes = [c_int, c_int]
__gr.gr_setfillintstyle.argtypes = [c_int]
__gr.gr_inqfillintstyle.argtypes = [POINTER(c_int)]
__gr.gr_setfillstyle.argtypes = [c_int]
__gr.gr_inqfillstyle.argtypes = [POINTER(c_int)]
__gr.gr_setfillcolorind.argtypes = [c_int]
__gr.gr_inqfillcolorind.argtypes = [POINTER(c_int)]
__gr.gr_setresizebehaviour.argtypes = [c_int]
__gr.gr_inqresizebehaviour.argtypes = [POINTER(c_int)]
__gr.gr_setcolorrep.argtypes = [c_int, c_double, c_double, c_double]
__gr.gr_setwindow.argtypes = [c_double, c_double, c_double, c_double]
__gr.gr_inqwindow.argtypes = [POINTER(c_double), POINTER(c_double),
                              POINTER(c_double), POINTER(c_double)]
__gr.gr_setviewport.argtypes = [c_double, c_double, c_double, c_double]
__gr.gr_inqviewport.argtypes = [POINTER(c_double), POINTER(c_double),
                                POINTER(c_double), POINTER(c_double)]
__gr.gr_selntran.argtypes = [c_int]
__gr.gr_setclip.argtypes = [c_int]
__gr.gr_setwswindow.argtypes = [c_double, c_double, c_double, c_double]
__gr.gr_setwsviewport.argtypes = [c_double, c_double, c_double, c_double]
__gr.gr_createseg.argtypes = [c_int]
__gr.gr_copysegws.argtypes = [c_int]
__gr.gr_redrawsegws.argtypes = []
__gr.gr_setsegtran.argtypes = [
    c_int, c_double, c_double, c_double, c_double, c_double, c_double, c_double]
__gr.gr_closeseg.argtypes = []
__gr.gr_emergencyclosegks.argtypes = []
__gr.gr_updategks.argtypes = []
__gr.gr_setspace.argtypes = [c_double, c_double, c_int, c_int]
__gr.gr_inqspace.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_int),
                             POINTER(c_int)]
__gr.gr_setscale.argtypes = [c_int]
__gr.gr_inqscale.argtypes = [POINTER(c_int)]
__gr.gr_textext.argtypes = [c_double, c_double, c_char_p]
__gr.gr_inqtextext.argtypes = [c_double, c_double, c_char_p, POINTER(c_double),
                               POINTER(c_double)]
__gr.gr_axeslbl.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int,
                            c_double, _axeslbl_callback, _axeslbl_callback]
__gr.gr_axes.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int, c_double]
__gr.gr_grid.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int]
__gr.gr_verrorbars.argtypes = [c_int, POINTER(c_double), POINTER(c_double),
                               POINTER(c_double), POINTER(c_double)]
__gr.gr_herrorbars.argtypes = [c_int, POINTER(c_double), POINTER(c_double),
                               POINTER(c_double), POINTER(c_double)]
__gr.gr_polyline3d.argtypes = [c_int, POINTER(c_double), POINTER(c_double),
                               POINTER(c_double)]
__gr.gr_polymarker3d.argtypes = [c_int, POINTER(c_double), POINTER(c_double),
                                 POINTER(c_double)]
__gr.gr_axes3d.argtypes = [
    c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int,
    c_double]
__gr.gr_grid3d.argtypes = [
    c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int]
__gr.gr_titles3d.argtypes = [c_char_p, c_char_p, c_char_p]
__gr.gr_surface.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double),
                            POINTER(c_double), c_int]
__gr.gr_contour.argtypes = [
    c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double),
    POINTER(c_double), c_int]
__gr.gr_contourf.argtypes = [
    c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double),
    POINTER(c_double), c_int]
__gr.gr_hexbin.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int]
__gr.gr_hexbin.restype = c_int
__gr.gr_setcolormap.argtypes = [c_int]
__gr.gr_setcolormapfromrgb.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
__gr.gr_colorbar.argtypes = []
__gr.gr_inqcolor.argtypes = [c_int, POINTER(c_int)]
__gr.gr_inqcolorfromrgb.argtypes = [c_double, c_double, c_double]
__gr.gr_inqcolorfromrgb.restype = c_int
__gr.gr_hsvtorgb.argtypes = [c_double, c_double, c_double]
__gr.gr_tick.argtypes = [c_double, c_double]
__gr.gr_tick.restype = c_double
__gr.gr_validaterange.argtypes = [c_double, c_double]
__gr.gr_validaterange.restype = c_int
__gr.gr_adjustlimits.argtypes = [POINTER(c_double), POINTER(c_double)]
__gr.gr_adjustrange.argtypes = [POINTER(c_double), POINTER(c_double)]
__gr.gr_beginprint.argtypes = [c_char_p]
__gr.gr_beginprintext.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
__gr.gr_endprint.argtypes = []
__gr.gr_ndctowc.argtypes = [POINTER(c_double), POINTER(c_double)]
__gr.gr_wctondc.argtypes = [POINTER(c_double), POINTER(c_double)]
__gr.gr_wc3towc.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double)]
__gr.gr_drawrect.argtypes = [c_double, c_double, c_double, c_double]
__gr.gr_fillrect.argtypes = [c_double, c_double, c_double, c_double]
__gr.gr_drawarc.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
__gr.gr_fillarc.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
__gr.gr_drawpath.argtypes = [c_int, POINTER(c_double), POINTER(c_uint8), c_int]
__gr.gr_setarrowstyle.argtypes = [c_int]
__gr.gr_setarrowsize.argtypes = [c_double]
__gr.gr_drawarrow.argtypes = [c_double, c_double, c_double, c_double]
__gr.gr_readimage.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int),
                              POINTER(POINTER(c_int))]
__gr.gr_drawimage.argtypes = [c_double, c_double, c_double, c_double,
                              c_int, c_int, POINTER(c_int), c_int]
__gr.gr_importgraphics.argtypes = [c_char_p]
__gr.gr_importgraphics.restype = c_int
__gr.gr_setshadow.argtypes = [c_double, c_double, c_double]
__gr.gr_settransparency.argtypes = [c_double]
__gr.gr_setcoordxform.argtypes = [POINTER(c_double)]
__gr.gr_begingraphics.argtypes = [c_char_p]
__gr.gr_endgraphics.argtypes = []
__gr.gr_getgraphics.argtypes = []
__gr.gr_getgraphics.restype = c_char_p
__gr.gr_drawgraphics.argtypes = [c_char_p]
__gr.gr_drawgraphics.restype = c_int
__gr.gr_mathtex.argtypes = [c_double, c_double, c_char_p]
__gr.gr_beginselection.argtypes = [c_int, c_int]
__gr.gr_endselection.argtypes = []
__gr.gr_moveselection.argtypes = [c_double, c_double]
__gr.gr_resizeselection.argtypes = [c_int, c_double, c_double]
__gr.gr_inqbbox.argtypes = [POINTER(c_double), POINTER(c_double),
                            POINTER(c_double), POINTER(c_double)]
__gr.gr_precision.argtypes = []
__gr.gr_precision.restype = c_double
__gr.gr_text_maxsize.argtypes = []
__gr.gr_text_maxsize.restype = c_int
__gr.gr_setregenflags.argtypes = [c_int]
__gr.gr_inqregenflags.argtypes = []
__gr.gr_inqregenflags.restype = c_int
__gr.gr_savestate.argtypes = []
__gr.gr_restorestate.argtypes = []
__gr.gr_selectcontext.argtypes = [c_int]
__gr.gr_destroycontext.argtypes = [c_int]
__gr.gr_uselinespec.argtypes = [c_char_p]
__gr.gr_uselinespec.restype = c_int
__gr.gr_trisurface.argtypes = [
    c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
__gr.gr_tricontour.argtypes = [
    c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double),
    c_int, POINTER(c_double)]
__gr.gr_version.argtypes = []
__gr.gr_version.restype = c_char_p
__gr.gr_quiver.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
__gr.gr_shadepoints.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
__gr.gr_shadelines.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]

# detect runtime version and use it for version dependent features
_RUNTIME_VERSION_STR = str(__gr.gr_version().decode('ascii'))
try:
    _RUNTIME_VERSION = version_string_to_tuple(_RUNTIME_VERSION_STR)
except TypeError:
    # runtime version is unknown, so disable all version dependent features
    _RUNTIME_VERSION = (0, 0, 0)
    warnings.warn('Unable to detect GR runtime version. Some features may not be available.')

if _RUNTIME_VERSION >= (0, 41, 5, 43):
    __gr.gr_setresamplemethod.argtypes = [c_uint]
    __gr.gr_setresamplemethod.restype = None
    __gr.gr_inqresamplemethod.argtypes = [POINTER(c_uint)]
    __gr.gr_inqresamplemethod.restype = None

if _RUNTIME_VERSION >= (0, 41, 5, 47):
    __gr.gr_inqmarkersize.argtypes = [POINTER(c_double)]
    __gr.gr_inqmarkersize.restype = None

if _RUNTIME_VERSION >= (0, 45, 0, 0):
    __gr.gr_path.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_char_p]
    __gr.gr_path.restype = None
    __gr.gr_setborderwidth.argtypes = [c_double]
    __gr.gr_setborderwidth.restype = None
    __gr.gr_inqborderwidth.argtypes = [POINTER(c_double)]
    __gr.gr_inqborderwidth.restype = None
    __gr.gr_setbordercolorind.argtypes = [c_int]
    __gr.gr_setbordercolorind.restype = None
    __gr.gr_inqbordercolorind.argtypes = [POINTER(c_int)]
    __gr.gr_inqbordercolorind.restype = None

if _RUNTIME_VERSION >= (0, 46, 0, 76):
    __gr.gr_setprojectiontype.argtypes = [c_int]
    __gr.gr_setprojectiontype.restype = None
    __gr.gr_inqprojectiontype.argtypes = [POINTER(c_int)]
    __gr.gr_inqprojectiontype.restype = None
    __gr.gr_setperspectiveprojection.argtypes = [c_double, c_double, c_double]
    __gr.gr_setperspectiveprojection.restype = None
    __gr.gr_setorthographicprojection.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
    __gr.gr_setorthographicprojection.restype = None
    __gr.gr_settransformationparameters.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double]
    __gr.gr_settransformationparameters.restype = None
    __gr.gr_inqtransformationparameters.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    __gr.gr_inqtransformationparameters.restype = None
    __gr.gr_inqorthographicprojection.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    __gr.gr_inqorthographicprojection.restype = None
    __gr.gr_inqperspectiveprojection.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    __gr.gr_inqperspectiveprojection.restype = None
    __gr.gr_camerainteraction.argtypes = [c_double, c_double, c_double, c_double]
    __gr.gr_camerainteraction.restype = None
    __gr.gr_setwindow3d.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
    __gr.gr_setwindow3d.restype = None
    __gr.gr_inqwindow3d.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    __gr.gr_inqwindow3d.restype = None

if _RUNTIME_VERSION >= (0, 48, 0, 0):
    __gr.gr_setscalefactors3d.argtypes = [c_double, c_double, c_double]
    __gr.gr_setscalefactors3d.restype = None
    __gr.gr_inqscalefactors3d.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    __gr.gr_inqscalefactors3d.restype = None
    if not hasattr(__gr, 'gr_setspace3d'):
        # gr_setspace3d used to be gr_transformationinterfaceforrepl
        __gr.gr_setspace3d = __gr.gr_transformationinterfaceforrepl
    __gr.gr_setspace3d.argtypes = [c_double, c_double, c_double, c_double]
    __gr.gr_setspace3d.restype = None

if _RUNTIME_VERSION >= (0, 56, 0, 0):
    __gr.gr_loadfont.argtypes = [c_char_p, POINTER(c_int)]
    __gr.gr_loadfont.restype = None

if _RUNTIME_VERSION >= (0, 58, 0, 0):
    __gr.gr_inqvpsize.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_double)]
    __gr.gr_inqvpsize.restype = None
    __gr.gr_setthreadnumber.argtypes = [c_int]
    __gr.gr_setthreadnumber.restype = None
    __gr.gr_setpicturesizeforvolume.argtypes = [c_int, c_int]
    __gr.gr_setpicturesizeforvolume.restype = None
    __gr.gr_setvolumebordercalculation.argtypes = [c_int]
    __gr.gr_setvolumebordercalculation.restype = None
    __gr.gr_setapproximativecalculation.argtypes = [c_int]
    __gr.gr_setapproximativecalculation.restype = None
    __gr.gr_inqvolumeflags.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    __gr.gr_inqvolumeflags.restype = None
    __gr.gr_cpubasedvolume.argtypes = [c_int, c_int, c_int, POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
    __gr.gr_cpubasedvolume.restype = None

if _RUNTIME_VERSION >= (0, 64, 2, 35):
    __gr.gr_setscientificformat.argtypes = [c_int]
    __gr.gr_setscientificformat.restype = None

if _RUNTIME_VERSION >= (0, 67, 0, 0):
    __gr.gr_volume_nogrid.argtypes = [c_ulong, POINTER(_data_point3d_t), c_void_p, c_int, _kernel_f, POINTER(c_double), POINTER(c_double), c_double, c_void_p]
    __gr.gr_volume_nogrid.restype = None

    __gr.gr_volume_interp_tri_linear_init.argtypes = [c_double, c_double, c_double]
    __gr.gr_volume_interp_tri_linear_init.restype = None

    __gr.gr_volume_interp_tri_linear.argtypes = [POINTER(_data_point3d_t), c_void_p, POINTER(_point3d_t), POINTER(_point3d_t)]
    __gr.gr_volume_interp_tri_linear.restype = c_double

    __gr.gr_volume_interp_gauss_init.argtypes = [c_double, POINTER(c_double)]
    __gr.gr_volume_interp_gauss_init.restype = None

    __gr.gr_volume_interp_gauss.argtypes = [POINTER(_data_point3d_t), c_void_p, POINTER(_point3d_t), POINTER(_point3d_t)]
    __gr.gr_volume_interp_gauss.restype = c_double

precision = __gr.gr_precision()
text_maxsize = __gr.gr_text_maxsize()

ASF_BUNDLED = 0
ASF_INDIVIDUAL = 1

NOCLIP = 0
CLIP = 1

COORDINATES_WC = 0
COORDINATES_NDC = 1

INTSTYLE_HOLLOW = 0
INTSTYLE_SOLID = 1
INTSTYLE_PATTERN = 2
INTSTYLE_HATCH = 3

TEXT_HALIGN_NORMAL = 0
TEXT_HALIGN_LEFT = 1
TEXT_HALIGN_CENTER = 2
TEXT_HALIGN_RIGHT = 3
TEXT_VALIGN_NORMAL = 0
TEXT_VALIGN_TOP = 1
TEXT_VALIGN_CAP = 2
TEXT_VALIGN_HALF = 3
TEXT_VALIGN_BASE = 4
TEXT_VALIGN_BOTTOM = 5

TEXT_PATH_RIGHT = 0
TEXT_PATH_LEFT = 1
TEXT_PATH_UP = 2
TEXT_PATH_DOWN = 3

TEXT_PRECISION_STRING = 0
TEXT_PRECISION_CHAR = 1
TEXT_PRECISION_STROKE = 2
TEXT_PRECISION_OUTLINE = 3

LINETYPE_SOLID = 1
LINETYPE_DASHED = 2
LINETYPE_DOTTED = 3
LINETYPE_DASHED_DOTTED = 4
LINETYPE_DASH_2_DOT = -1
LINETYPE_DASH_3_DOT = -2
LINETYPE_LONG_DASH = -3
LINETYPE_LONG_SHORT_DASH = -4
LINETYPE_SPACED_DASH = -5
LINETYPE_SPACED_DOT = -6
LINETYPE_DOUBLE_DOT = -7
LINETYPE_TRIPLE_DOT = -8

MARKERTYPE_DOT = 1
MARKERTYPE_PLUS = 2
MARKERTYPE_ASTERISK = 3
MARKERTYPE_CIRCLE = 4
MARKERTYPE_DIAGONAL_CROSS = 5
MARKERTYPE_SOLID_CIRCLE = -1
MARKERTYPE_TRIANGLE_UP = -2
MARKERTYPE_SOLID_TRI_UP = -3
MARKERTYPE_TRIANGLE_DOWN = -4
MARKERTYPE_SOLID_TRI_DOWN = -5
MARKERTYPE_SQUARE = -6
MARKERTYPE_SOLID_SQUARE = -7
MARKERTYPE_BOWTIE = -8
MARKERTYPE_SOLID_BOWTIE = -9
MARKERTYPE_HOURGLASS = -10
MARKERTYPE_SOLID_HGLASS = -11
MARKERTYPE_DIAMOND = -12
MARKERTYPE_SOLID_DIAMOND = -13
MARKERTYPE_STAR = -14
MARKERTYPE_SOLID_STAR = -15
MARKERTYPE_TRI_UP_DOWN = -16
MARKERTYPE_SOLID_TRI_RIGHT = -17
MARKERTYPE_SOLID_TRI_LEFT = -18
MARKERTYPE_HOLLOW_PLUS = -19
MARKERTYPE_SOLID_PLUS = -20
MARKERTYPE_PENTAGON = -21
MARKERTYPE_HEXAGON = -22
MARKERTYPE_HEPTAGON = -23
MARKERTYPE_OCTAGON = -24
MARKERTYPE_STAR_4 = -25
MARKERTYPE_STAR_5 = -26
MARKERTYPE_STAR_6 = -27
MARKERTYPE_STAR_7 = -28
MARKERTYPE_STAR_8 = -29
MARKERTYPE_VLINE = -30
MARKERTYPE_HLINE = -31
MARKERTYPE_OMARK = -32

OPTION_X_LOG = 1
OPTION_Y_LOG = 2
OPTION_Z_LOG = 4
OPTION_FLIP_X = 8
OPTION_FLIP_Y = 16
OPTION_FLIP_Z = 32

OPTION_LINES = 0
OPTION_MESH = 1
OPTION_FILLED_MESH = 2
OPTION_Z_SHADED_MESH = 3
OPTION_COLORED_MESH = 4
OPTION_CELL_ARRAY = 5
OPTION_SHADED_MESH = 6

MODEL_RGB = 0
MODEL_HSV = 1

COLORMAP_UNIFORM = 0
COLORMAP_TEMPERATURE = 1
COLORMAP_GRAYSCALE = 2
COLORMAP_GLOWING = 3
COLORMAP_RAINBOWLIKE = 4
COLORMAP_GEOLOGIC = 5
COLORMAP_GREENSCALE = 6
COLORMAP_CYANSCALE = 7
COLORMAP_BLUESCALE = 8
COLORMAP_MAGENTASCALE = 9
COLORMAP_REDSCALE = 10
COLORMAP_FLAME = 11
COLORMAP_BROWNSCALE = 12
COLORMAP_PILATUS = 13
COLORMAP_AUTUMN = 14
COLORMAP_BONE = 15
COLORMAP_COOL = 16
COLORMAP_COPPER = 17
COLORMAP_GRAY = 18
COLORMAP_HOT = 19
COLORMAP_HSV = 20
COLORMAP_JET = 21
COLORMAP_PINK = 22
COLORMAP_SPECTRAL = 23
COLORMAP_SPRING = 24
COLORMAP_SUMMER = 25
COLORMAP_WINTER = 26
COLORMAP_GIST_EARTH = 27
COLORMAP_GIST_HEAT = 28
COLORMAP_GIST_NCAR = 29
COLORMAP_GIST_RAINBOW = 30
COLORMAP_GIST_STERN = 31
COLORMAP_AFMHOT = 32
COLORMAP_BRG = 33
COLORMAP_BWR = 34
COLORMAP_COOLWARM = 35
COLORMAP_CMRMAP = 36
COLORMAP_CUBEHELIX = 37
COLORMAP_GNUPLOT = 38
COLORMAP_GNUPLOT2 = 39
COLORMAP_OCEAN = 40
COLORMAP_RAINBOW = 41
COLORMAP_SEISMIC = 42
COLORMAP_TERRAIN = 43
COLORMAP_VIRIDIS = 44
COLORMAP_INFERNO = 45
COLORMAP_PLASMA = 46
COLORMAP_MAGMA = 47

COLORMAPS = [("UNIFORM", COLORMAP_UNIFORM),
             ("TEMPERATURE", COLORMAP_TEMPERATURE),
             ("GRAYSCALE", COLORMAP_GRAYSCALE),
             ("GLOWING", COLORMAP_GLOWING),
             ("RAINBOWLIKE", COLORMAP_RAINBOWLIKE),
             ("GEOLOGIC", COLORMAP_GEOLOGIC),
             ("GREENSCALE", COLORMAP_GREENSCALE),
             ("CYANSCALE", COLORMAP_CYANSCALE),
             ("BLUESCALE", COLORMAP_BLUESCALE),
             ("MAGENTASCALE", COLORMAP_MAGENTASCALE),
             ("REDSCALE", COLORMAP_REDSCALE),
             ("FLAME", COLORMAP_FLAME),
             ("BROWNSCALE", COLORMAP_BROWNSCALE),
             ("PILATUS", COLORMAP_PILATUS),
             ("AUTUMN", COLORMAP_AUTUMN),
             ("BONE", COLORMAP_BONE),
             ("COOL", COLORMAP_COOL),
             ("COPPER", COLORMAP_COPPER),
             ("GRAY", COLORMAP_GRAY),
             ("HOT", COLORMAP_HOT),
             ("HSV", COLORMAP_HSV),
             ("JET", COLORMAP_JET),
             ("PINK", COLORMAP_PINK),
             ("SPECTRAL", COLORMAP_SPECTRAL),
             ("SPRING", COLORMAP_SPRING),
             ("SUMMER", COLORMAP_SUMMER),
             ("WINTER", COLORMAP_WINTER),
             ("GIST_EARTH", COLORMAP_GIST_EARTH),
             ("GIST_HEAT", COLORMAP_GIST_HEAT),
             ("GIST_NCAR", COLORMAP_GIST_NCAR),
             ("GIST_RAINBOW", COLORMAP_GIST_RAINBOW),
             ("GIST_STERN", COLORMAP_GIST_STERN),
             ("AFMHOT", COLORMAP_AFMHOT),
             ("BRG", COLORMAP_BRG),
             ("BWR", COLORMAP_BWR),
             ("COOLWARM", COLORMAP_COOLWARM),
             ("CMRMAP", COLORMAP_CMRMAP),
             ("CUBEHELIX", COLORMAP_CUBEHELIX),
             ("GNUPLOT", COLORMAP_GNUPLOT),
             ("GNUPLOT2", COLORMAP_GNUPLOT2),
             ("OCEAN", COLORMAP_OCEAN),
             ("RAINBOW", COLORMAP_RAINBOW),
             ("SEISMIC", COLORMAP_SEISMIC),
             ("TERRAIN", COLORMAP_TERRAIN),
             ("VIRIDIS", COLORMAP_VIRIDIS),
             ("INFERNO", COLORMAP_INFERNO),
             ("PLASMA", COLORMAP_PLASMA),
             ("MAGMA", COLORMAP_MAGMA),
            ]

FONT_TIMES_ROMAN = 101
FONT_TIMES_ITALIC = 102
FONT_TIMES_BOLD = 103
FONT_TIMES_BOLDITALIC = 104
FONT_HELVETICA = 105
FONT_HELVETICA_OBLIQUE = 106
FONT_HELVETICA_BOLD = 107
FONT_HELVETICA_BOLDOBLIQUE = 108
FONT_COURIER = 109
FONT_COURIER_OBLIQUE = 110
FONT_COURIER_BOLD = 111
FONT_COURIER_BOLDOBLIQUE = 112
FONT_SYMBOL = 113
FONT_BOOKMAN_LIGHT = 114
FONT_BOOKMAN_LIGHTITALIC = 115
FONT_BOOKMAN_DEMI = 116
FONT_BOOKMAN_DEMIITALIC = 117
FONT_NEWCENTURYSCHLBK_ROMAN = 118
FONT_NEWCENTURYSCHLBK_ITALIC = 119
FONT_NEWCENTURYSCHLBK_BOLD = 120
FONT_NEWCENTURYSCHLBK_BOLDITALIC = 121
FONT_AVANTGARDE_BOOK = 122
FONT_AVANTGARDE_BOOKOBLIQUE = 123
FONT_AVANTGARDE_DEMI = 124
FONT_AVANTGARDE_DEMIOBLIQUE = 125
FONT_PALATINO_ROMAN = 126
FONT_PALATINO_ITALIC = 127
FONT_PALATINO_BOLD = 128
FONT_PALATINO_BOLDITALIC = 129
FONT_ZAPFCHANCERY_MEDIUMITALIC = 130
FONT_ZAPFDINGBATS = 131
FONT_COMPUTERMODERN = 232
FONT_DEJAVUSANS = 233

SCIENTIFIC_FORMAT_OPTION_E = 1
SCIENTIFIC_FORMAT_OPTION_TEXTEX = 2
SCIENTIFIC_FORMAT_OPTION_MATHTEX = 3

# gr.beginprint types
PRINT_PS = "ps"
PRINT_EPS = "eps"
PRINT_PDF = "pdf"
PRINT_PGF = "pgf"
PRINT_BMP = "bmp"
PRINT_JPEG = "jpeg"
PRINT_JPG = "jpg"
PRINT_PNG = "png"
PRINT_TIFF = "tiff"
PRINT_TIF = "tif"
PRINT_FIG = "fig"
PRINT_SVG = "svg"
PRINT_WMF = "wmf"

PRINT_TYPE = {PRINT_PS: "PostScript (*.ps)",
              PRINT_EPS: "Encapsulated PostScript (*.eps)",
              PRINT_PDF: "Portable Document Format (*.pdf)",
              PRINT_PGF: "PGF/TikZ Graphics Format for TeX (*.pgf)",
              PRINT_BMP: "Windows Bitmap (*.bmp)",
              PRINT_JPEG: "JPEG image (*.jpg *.jpeg)",
              PRINT_PNG: "Portable Network Graphics (*.png)",
              PRINT_TIFF: "Tagged Image File Format (*.tif *.tiff)",
              PRINT_FIG: "Figure (*.fig)",
              PRINT_SVG: "Scalable Vector Graphics (*.svg)",
              PRINT_WMF: "Windows Metafile (*.wmf)"}

# multiple keys
PRINT_TYPE[PRINT_JPG] = PRINT_TYPE[PRINT_JPEG]
PRINT_TYPE[PRINT_TIF] = PRINT_TYPE[PRINT_TIFF]

# gr.begingraphics types
GRAPHIC_GRX = "grx"

GRAPHIC_TYPE = {GRAPHIC_GRX: "Graphics Format (*.grx)"}

# regeneration flags
MPL_SUPPRESS_CLEAR = 1
MPL_POSTPONE_UPDATE = 2

# interp2 methods
INTERP2_NEAREST = 0
INTERP2_LINEAR = 1
INTERP2_CUBIC = 3
INTERP2_SPLINE = 2

VOLUME_EMISSION = 0
VOLUME_ABSORPTION = 1
VOLUME_MIP = 2

if _RUNTIME_VERSION >= (0, 41, 5, 43):
    UPSAMPLE_VERTICAL_DEFAULT = 0x00000000
    UPSAMPLE_HORIZONTAL_DEFAULT = 0x00000000
    DOWNSAMPLE_VERTICAL_DEFAULT = 0x00000000
    DOWNSAMPLE_HORIZONTAL_DEFAULT = 0x00000000
    UPSAMPLE_VERTICAL_NEAREST = 0x00000001
    UPSAMPLE_HORIZONTAL_NEAREST = 0x00000100
    DOWNSAMPLE_VERTICAL_NEAREST = 0x00010000
    DOWNSAMPLE_HORIZONTAL_NEAREST = 0x01000000
    UPSAMPLE_VERTICAL_LINEAR = 0x00000002
    UPSAMPLE_HORIZONTAL_LINEAR = 0x00000200
    DOWNSAMPLE_VERTICAL_LINEAR = 0x00020000
    DOWNSAMPLE_HORIZONTAL_LINEAR = 0x02000000
    UPSAMPLE_VERTICAL_LANCZOS = 0x00000003
    UPSAMPLE_HORIZONTAL_LANCZOS = 0x00000300
    DOWNSAMPLE_VERTICAL_LANCZOS = 0x00030000
    DOWNSAMPLE_HORIZONTAL_LANCZOS = 0x03000000

    RESAMPLE_DEFAULT = (
            UPSAMPLE_VERTICAL_DEFAULT | UPSAMPLE_HORIZONTAL_DEFAULT | DOWNSAMPLE_VERTICAL_DEFAULT | DOWNSAMPLE_HORIZONTAL_DEFAULT
    )
    RESAMPLE_NEAREST = (
            UPSAMPLE_VERTICAL_NEAREST | UPSAMPLE_HORIZONTAL_NEAREST | DOWNSAMPLE_VERTICAL_NEAREST | DOWNSAMPLE_HORIZONTAL_NEAREST
    )
    RESAMPLE_LINEAR = (
            UPSAMPLE_VERTICAL_LINEAR | UPSAMPLE_HORIZONTAL_LINEAR | DOWNSAMPLE_VERTICAL_LINEAR | DOWNSAMPLE_HORIZONTAL_LINEAR
    )
    RESAMPLE_LANCZOS = (
            UPSAMPLE_VERTICAL_LANCZOS | UPSAMPLE_HORIZONTAL_LANCZOS | DOWNSAMPLE_VERTICAL_LANCZOS | DOWNSAMPLE_HORIZONTAL_LANCZOS
    )

if _RUNTIME_VERSION >= (0, 46, 0, 76):
    PROJECTION_DEFAULT = 0
    PROJECTION_ORTHOGRAPHIC = 1
    PROJECTION_PERSPECTIVE = 2

if _RUNTIME_VERSION >= (0, 58, 0, 0):
    VOLUME_WITHOUT_BORDER = 0
    VOLUME_WITH_BORDER = 1

# automatically switch to inline graphics in Jupyter Notebooks
if 'ipykernel' in sys.modules:
    inline()
