from __future__ import annotations

import os
import warnings

import numpy as np

import gr
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import (
    FigureCanvasBase,
    FigureManagerBase,
    GraphicsContextBase,
    RendererBase,
    register_backend,
)
from matplotlib.figure import Figure
from matplotlib.mathtext import MathTextParser
from matplotlib.texmanager import TexManager


linetype = {"solid": 1, "dashed": 2, "dashdot": 4, "dotted": 3}

os.environ["GKS_DOUBLE_BUF"] = "1"


class RendererGR(RendererBase):
    """Handle drawing/rendering operations using GR."""

    def __init__(self, width, height, dpi):
        super().__init__()
        self.dpi = dpi
        self.nominal_fontsize = 0.001625
        default_dpi = 100
        self.width = float(width) * dpi / default_dpi
        self.height = float(height) * dpi / default_dpi
        self.mathtext_parser = MathTextParser("agg")
        self.texmanager = TexManager()
        self._color_cache = {}
        self._next_color_index = 1000
        self.size = max(self.width, self.height)

    def configure(self):
        aspect_ratio = self.width / self.height
        if aspect_ratio > 1:
            rect = np.array([0.0, 1.0, 0.0, 1.0 / aspect_ratio])
            self.size = self.width
        else:
            rect = np.array([0.0, aspect_ratio, 0.0, 1.0])
            self.size = self.height

        mwidth, mheight, width, height = gr.inqdspsize()
        if width / (mwidth / 0.0256) < 200:
            mwidth *= self.width / width
            gr.setwsviewport(*(rect * mwidth))
        else:
            gr.setwsviewport(*(rect * 0.192))
        gr.setwswindow(*rect)
        gr.setviewport(*rect)
        gr.setwindow(0, self.width, 0, self.height)

    def _set_full_window(self):
        gr.setviewport(0, self.width / self.size, 0, self.height / self.size)
        gr.setwindow(0, self.width, 0, self.height)

    def _set_clip_window(self, gc):
        bbox = gc.get_clip_rectangle()
        if bbox is not None and not np.any(np.isnan(bbox.bounds)):
            x, y, w, h = bbox.bounds
            clrt = np.array([x, x + w, y, y + h], dtype=float)
        else:
            clrt = np.array([0.0, self.width, 0.0, self.height], dtype=float)
        gr.setviewport(*(clrt / self.size))
        gr.setwindow(*clrt)
        return clrt

    def _get_gr_color_index(self, rgba):
        rgb = tuple(round(float(c), 6) for c in rgba[:3])
        color = self._color_cache.get(rgb)
        if color is None:
            color = self._next_color_index
            self._next_color_index += 1
            gr.setcolorrep(color, *rgb)
            self._color_cache[rgb] = color
        return color

    def _set_line_style(self, gc):
        linestyle = getattr(gc, "_linestyle", None)
        if isinstance(linestyle, str) and linestyle in linetype:
            gr.setlinetype(linetype[linestyle])
        else:
            gr.setlinetype(linetype["solid"])

    def _stroke_path_segments(self, points, codes):
        if len(points) < 2:
            return False
        if codes is None:
            gr.polyline(points[:, 0], points[:, 1])
            return True

        MOVETO = 1
        LINETO = 2
        CLOSEPOLY = 79
        current = []
        stroked = False
        for point, code in zip(points, codes):
            code = MOVETO if code is None else int(code)
            if code == MOVETO:
                if len(current) >= 2:
                    seg = np.asarray(current, dtype=float)
                    gr.polyline(seg[:, 0], seg[:, 1])
                    stroked = True
                current = [point]
            elif code == LINETO:
                current.append(point)
            elif code == CLOSEPOLY:
                if current:
                    if not np.allclose(current[0], current[-1]):
                        current.append(current[0])
                    if len(current) >= 2:
                        seg = np.asarray(current, dtype=float)
                        gr.polyline(seg[:, 0], seg[:, 1])
                        stroked = True
                current = []
            else:
                return False
        if len(current) >= 2:
            seg = np.asarray(current, dtype=float)
            gr.polyline(seg[:, 0], seg[:, 1])
            stroked = True
        return stroked

    def draw_path(self, gc, path, transform, rgbFace=None):
        path = transform.transform_path(path)
        points = path.vertices
        codes = path.codes
        self._set_clip_window(gc)
        try:
            if rgbFace is not None and len(points) > 2 and rgbFace[3] > 0:
                color = self._get_gr_color_index(rgbFace)
                gr.settransparency(float(rgbFace[3]))
                gr.setfillintstyle(gr.INTSTYLE_SOLID)
                gr.setfillcolorind(color)
                gr.setbordercolorind(color)
                gr.drawpath(points, codes, fill=True)

            lw = gc.get_linewidth()
            rgba = gc.get_rgb()[:4]
            if lw > 0 and rgba[3] > 0:
                color = self._get_gr_color_index(rgba)
                gr.settransparency(float(rgba[3]))
                self._set_line_style(gc)
                gr.setlinewidth(float(lw))
                gr.setlinecolorind(color)
                if not self._stroke_path_segments(points, codes):
                    gr.setbordercolorind(color)
                    gr.drawpath(points, codes, fill=False)
        finally:
            self._set_full_window()

    def draw_quad_mesh(
        self,
        gc,
        master_transform,
        meshWidth,
        meshHeight,
        coordinates,
        offsets,
        offsetTrans,
        facecolors,
        antialiased,
        edgecolors,
    ):
        if offsets is not None:
            offsets = np.asarray(offsets)
            if offsets.size and not np.allclose(offsets, 0):
                return super().draw_quad_mesh(
                    gc,
                    master_transform,
                    meshWidth,
                    meshHeight,
                    coordinates,
                    offsets,
                    offsetTrans,
                    facecolors,
                    antialiased,
                    edgecolors,
                )

        facecolors = np.asarray(facecolors)
        if facecolors.ndim != 2 or facecolors.shape != (meshWidth * meshHeight, 4):
            return super().draw_quad_mesh(
                gc,
                master_transform,
                meshWidth,
                meshHeight,
                coordinates,
                offsets,
                offsetTrans,
                facecolors,
                antialiased,
                edgecolors,
            )

        lw = gc.get_linewidth()
        if edgecolors is not None:
            edgecolors = np.asarray(edgecolors)
            if edgecolors.size:
                edgecolors = edgecolors.reshape(-1, edgecolors.shape[-1])
                if edgecolors.shape[1] >= 4 and lw > 0 and np.any(edgecolors[:, 3] > 0):
                    return super().draw_quad_mesh(
                        gc,
                        master_transform,
                        meshWidth,
                        meshHeight,
                        coordinates,
                        offsets,
                        offsetTrans,
                        facecolors,
                        antialiased,
                        edgecolors,
                    )

        coords = np.asarray(coordinates)
        if coords.shape[:2] != (meshHeight + 1, meshWidth + 1) or coords.shape[-1] != 2:
            return super().draw_quad_mesh(
                gc,
                master_transform,
                meshWidth,
                meshHeight,
                coordinates,
                offsets,
                offsetTrans,
                facecolors,
                antialiased,
                edgecolors,
            )

        transformed = master_transform.transform(coords.reshape(-1, 2)).reshape(coords.shape)
        if not np.isfinite(transformed).all():
            return super().draw_quad_mesh(
                gc,
                master_transform,
                meshWidth,
                meshHeight,
                coordinates,
                offsets,
                offsetTrans,
                facecolors,
                antialiased,
                edgecolors,
            )

        xs = transformed[..., 0]
        ys = transformed[..., 1]
        tol = max(self.width, self.height) * 1e-9 + 1e-12
        x_edges = xs[0, :].copy()
        y_edges = ys[:, 0].copy()

        if not np.allclose(xs, x_edges[np.newaxis, :], rtol=0, atol=tol):
            return super().draw_quad_mesh(
                gc,
                master_transform,
                meshWidth,
                meshHeight,
                coordinates,
                offsets,
                offsetTrans,
                facecolors,
                antialiased,
                edgecolors,
            )
        if not np.allclose(ys, y_edges[:, np.newaxis], rtol=0, atol=tol):
            return super().draw_quad_mesh(
                gc,
                master_transform,
                meshWidth,
                meshHeight,
                coordinates,
                offsets,
                offsetTrans,
                facecolors,
                antialiased,
                edgecolors,
            )

        alpha = facecolors[:, 3]
        if not np.allclose(alpha, alpha[0]):
            return super().draw_quad_mesh(
                gc,
                master_transform,
                meshWidth,
                meshHeight,
                coordinates,
                offsets,
                offsetTrans,
                facecolors,
                antialiased,
                edgecolors,
            )

        facecolors_2d = facecolors.reshape(meshHeight, meshWidth, 4)
        color_indices = np.empty((meshHeight, meshWidth), dtype=np.int32)
        for i in range(meshHeight):
            for j in range(meshWidth):
                color_indices[i, j] = self._get_gr_color_index(facecolors_2d[i, j])

        self._set_clip_window(gc)
        try:
            gr.settransparency(float(alpha[0]))
            xmin = float(x_edges[0])
            xmax = float(x_edges[-1])
            ymin = float(y_edges[0])
            ymax = float(y_edges[-1])
            gr.cellarray(
                xmin,
                xmax,
                ymin,
                ymax,
                meshWidth,
                meshHeight,
                np.ascontiguousarray(color_indices[::-1, :]).ravel(),
            )
        finally:
            self._set_full_window()

    def draw_image(self, gc, x, y, im, transform=None):
        if transform is not None and not transform.is_identity:
            warnings.warn(
                "RendererGR ignores non-identity image transforms.",
                stacklevel=2,
            )

        if hasattr(im, "as_rgba_str"):
            h, w, s = im.as_rgba_str()
            img = np.frombuffer(s, np.uint32).copy()
            img.shape = (h, w)
        elif isinstance(im, np.ndarray) and im.ndim == 3 and im.shape[2] == 4 and im.dtype == np.uint8:
            img = np.ascontiguousarray(im).view(np.uint32)
            img.shape = im.shape[:2]
            h, w = img.shape
        else:
            type_info = repr(type(im))
            if hasattr(im, "shape"):
                type_info += " shape=" + repr(im.shape)
            if hasattr(im, "dtype"):
                type_info += " dtype=" + repr(im.dtype)
            warnings.warn(
                "Unsupported image type ({}). Please report this at "
                "https://github.com/sciapp/python-gr/issues".format(type_info),
                stacklevel=2,
            )
            return

        gr.drawimage(x, x + w, y + h, y, w, h, img)

    def draw_mathtext_image(self, x, y, angle, Z):
        h, w = Z.shape
        img = np.zeros((h, w), np.uint32)
        for i in range(h):
            for j in range(w):
                b = np.uint32(Z[i, j])
                img[i, j] = 0xFF000000 | (b << 16) | (b << 8) | b

        a = int(angle) % 360
        if a == 90:
            gr.drawimage(x - h, x, y, y + w, h, w, np.resize(np.rot90(img, 1), (h, w)))
        elif a == 180:
            gr.drawimage(x - w, x, y - h, y, w, h, np.rot90(img, 2))
        elif a == 270:
            gr.drawimage(x, x + h, y - w, y, h, w, np.resize(np.rot90(img, 3), (h, w)))
        else:
            gr.drawimage(x, x + w, y, y + h, w, h, img)

    def draw_tex(self, gc, x, y, s, prop, angle, *, mtext=None):
        size = prop.get_size_in_points()
        Z = self.get_texmanager().get_grey(s, size, self.dpi)
        Z = np.array(255.0 - Z * 255.0, np.uint8)
        self.draw_mathtext_image(x, y, angle, Z)

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        gr.settextfontprec(233, 3)

        if ismath:
            self._draw_text_as_path(gc, x, y, s, prop, angle, ismath)
            return

        self._set_full_window()
        x, y = gr.wctondc(x, y)
        fontsize = prop.get_size_in_points()
        rgba = gc.get_rgb()[:4]
        color = self._get_gr_color_index(rgba)
        gr.settransparency(float(rgba[3]))
        gr.setcharheight(fontsize * self.nominal_fontsize)
        gr.settextcolorind(color)
        if angle != 0:
            gr.setcharup(-np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180))
        else:
            gr.setcharup(0, 1)
        gr.text(x, y, s)

    def flipy(self):
        return False

    def get_canvas_width_height(self):
        return self.width, self.height

    def get_text_width_height_descent(self, s, prop, ismath):
        if ismath == "TeX":
            fontsize = prop.get_size_in_points()
            return self.get_texmanager().get_text_width_height_descent(
                s, fontsize, renderer=self
            )
        if ismath:
            parsed = self.mathtext_parser.parse(s, dpi=self.dpi, prop=prop)
            return parsed.width, parsed.height, parsed.depth

        fontsize = prop.get_size_in_points()

        self._set_full_window()
        gr.setcharheight(fontsize * self.nominal_fontsize)
        gr.setcharup(0, 1)

        tbx, tby = gr.inqtextext(0, 0, s)

        width = (max(tbx) - min(tbx))
        height = (max(tby) - min(tby))
        descent = 0.2 * height

        return width, height, descent

    def new_gc(self):
        return GraphicsContextGR()

    def points_to_pixels(self, points):
        return points * self.dpi / 72.0


class GraphicsContextGR(GraphicsContextBase):
    pass


class FigureManagerGR(FigureManagerBase):
    def show(self):
        self.canvas.draw()


class FigureCanvasGR(FigureCanvasBase):
    manager_class = FigureManagerGR
    filetypes = {
        "gr": "GR Graphics",
        "pdf": "Portable Document Format",
        "png": "Portable Network Graphics",
        "svg": "Scalable Vector Graphics",
    }

    register_backend("gr", __name__, "GR File Format")

    def __init__(self, figure=None):
        super().__init__(figure)
        width, height = self.get_width_height()
        self.renderer = RendererGR(width, height, self.figure.dpi)

    def get_renderer(self):
        width, height = self.get_width_height()
        renderer_width = float(width) * self.figure.dpi / 100
        renderer_height = float(height) * self.figure.dpi / 100
        if (
            self.renderer.width != renderer_width
            or self.renderer.height != renderer_height
            or self.renderer.dpi != self.figure.dpi
        ):
            self.renderer = RendererGR(width, height, self.figure.dpi)
        return self.renderer

    def draw(self):
        flags = gr.inqregenflags()
        if not (flags & gr.MPL_SUPPRESS_CLEAR):
            gr.clearws()

        renderer = self.get_renderer()
        renderer.configure()
        self.figure.draw(renderer)
        super().draw()

        if not (flags & gr.MPL_POSTPONE_UPDATE):
            gr.updatews()

    def print_gr(self, filename, *args, **kwargs):
        gr.begingraphics(filename)
        self.draw()
        gr.endgraphics()

    def print_svg(self, filename, *args, **kwargs):
        gr.beginprint(filename)
        self.draw()
        gr.endprint()

    def print_png(self, filename, *args, **kwargs):
        gr.beginprint(filename)
        self.draw()
        gr.endprint()

    def print_pdf(self, filename, *args, **kwargs):
        gr.beginprint(filename)
        self.draw()
        gr.endprint()


FigureCanvas = FigureCanvasGR
FigureManager = FigureManagerGR


def draw_if_interactive():
    pass


def show():
    return FigureManagerGR.pyplot_show()


def new_figure_manager(num, *args, FigureClass=Figure, **kwargs):
    figure = FigureClass(*args, **kwargs)
    return FigureCanvasGR.new_manager(figure, num)


def new_figure_manager_given_figure(num, figure):
    return FigureCanvasGR.new_manager(figure, num)
