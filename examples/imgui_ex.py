import ctypes
import glfw  # type: ignore
import gr  # type: ignore
import imgui  # type: ignore
import math
import numpy as np
import OpenGL.GL as gl  # type: ignore
import os
import sys
from imgui.integrations.glfw import GlfwRenderer  # type: ignore
from typing import Callable, Iterator
from contextlib import contextmanager


@contextmanager
def print_to_texture(width: int, height: int) -> Iterator[None]:
    image_data = np.zeros((width, height, 4), gl.GLubyte)
    img_ptr = image_data.ctypes.data
    gr.beginprint(f"!{width}x{height}@{img_ptr:x}.mem")
    try:
        yield
    finally:
        gr.endprint()
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,  # target
            0,  # mipmap level
            gl.GL_RGBA,  # internal format
            width, height, 0,  # legacy param (must be 0)
            gl.GL_RGBA,  # user format
            gl.GL_UNSIGNED_BYTE,  # user type
            ctypes.c_void_p(img_ptr)
        )
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)


class TextWindow:
    formulae = (
        r"-\frac{{\hbar ^2}}{{2m}}"
        + r"\frac{{\partial ^2 \psi (x,t)}}{{\partial x^2}} + U(x)\psi (x,t)"
        + r"= i\hbar \frac{{\partial \psi (x,t)}}{{\partial t}}",
        r"\zeta \left({s}\right)"
        + r":= \sum_{n=1}^\infty \frac{1}{n^s} \quad \sigma = \Re(s) > 1",
        r"\zeta \left({s}\right)"
        + r":= \frac{1}{\gamma(s)} \int_{0}^\infty \frac{x^{s-1}}{e^x-1} dx",
    )

    def __init__(self) -> None:
        self._phi = 0
        self._img_size = -1

    def _draw_text(self) -> None:
        phi = self._phi * math.pi / 180
        gr.settextfontprec(232, 3)
        gr.settextalign(2, 3)
        gr.settextcolorind(0)  # white
        gr.setcharheight(.036)
        gr.setcharup(math.sin(phi), math.cos(phi))
        y = .75
        for s in self.formulae:
            gr.mathtex(.5, y, s)
            y -= .25
        gr.updatews()

    def __call__(self) -> None:
        imgui.set_next_window_size_constraints(
            (300, 200),
            (imgui.FLOAT_MAX, imgui.FLOAT_MAX),
        )
        imgui.set_next_window_size(550, 500, imgui.FIRST_USE_EVER)
        with imgui.begin("GR Demo") as win:
            if not win.expanded:
                return
            changed, self._phi = imgui.slider_float(
                "Angle", self._phi, 0, 360, "%.4f"
            )
            imgui.text(f"Cursor position: {imgui.get_mouse_pos()}")
            wh = min(map(int, imgui.get_content_region_available()))
            if wh != self._img_size or changed:
                self._img_size = wh
                with print_to_texture(wh, wh):
                    self._draw_text()
            x, y = imgui.get_cursor_pos()
            w, h = imgui.get_content_region_available()
            imgui.set_cursor_pos((x + (w - wh) / 2, y + (h - wh) / 2))
            imgui.image(gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D), wh, wh)


class GR3dWindow:
    def __init__(self) -> None:
        self._rot = -30
        self._tilt = 45
        self._fov = 45
        self._cam_dist = 5
        self._size: tuple[int, int] | None = None
        self._x = np.linspace(-np.pi, np.pi, 100)
        xv, yv = np.meshgrid(self._x, self._x)
        self._z = np.sin(xv) * np.sin(yv)
        self._active = False
        self._uvs: tuple[tuple[float, float], tuple[float, float]]

    def _process_input(self) -> None:
        # is_item_active() is broken somehow
        # is_item_activated() / is_item_deactivated() spuriously fail
        self._active = self._active and imgui.is_mouse_down()
        self._active = self._active or imgui.is_item_active()
        if not imgui.is_mouse_dragging(0) or not self._active:
            return
        delta = imgui.get_io().mouse_delta
        self._rot -= .2 * delta.x
        self._tilt += .2 * delta.y
        self._size = None  # force redraw

    def _draw_surface(self) -> None:
        assert self._size is not None
        w, h = self._size
        if w > h:
            self._uvs = (0, 0), (1, h / w)
            gr.setviewport(0, 1, 1 - h / w, 1)
        else:
            self._uvs = (0, 0), (w / h, 1)
            gr.setviewport(0, w / h, 0, 1)
        lo, hi = self._x[0], self._x[-1]
        lims = math.floor(lo * 10) / 10, math.ceil(hi * 10) / 10
        loz, hiz = np.min(self._z), np.max(self._z)
        limsz = math.floor(loz * 10) / 10, math.ceil(hiz * 10) / 10
        rot = self._rot % 360
        tilt = self._tilt % 360
        xtick, ytick, ztick = .5, .5, .2
        z = limsz[90 < tilt]

        gr.setlinewidth(.5)
        gr.setresamplemethod(0x2020202)
        gr.settextfontprec(232, 4)
        gr.settextcolorind(1)  # black
        gr.setcharup(0, 1)
        gr.setwindow3d(*lims, *lims, *limsz)
        gr.setspace3d(self._rot, self._tilt, self._fov, self._cam_dist)
        gr.settransparency(.5)
        gr.grid3d(xtick, ytick, ztick,
                  lims[90 < rot <= 270], lims[180 < rot], z,
                  2, 2, 2)
        gr.setcharheight(.024)
        gr.titles3d("X title", "Y title", "Z title")
        gr.settransparency(.3)
        gr.surface(self._x, self._x, self._z, gr.OPTION_COLORED_MESH)
        gr.settransparency(.8)
        gr.setcharheight(.016)

        x1 = xtick if 90 < rot % 180 else 0
        xorg1 = lims[rot <= 180]
        yorg1 = lims[90 < rot <= 270]
        x2 = xtick - x1
        xorg2 = lims[not (90 < rot <= 270)]
        yorg2 = lims[rot <= 90]
        size = (1 if 90 < rot <= 180 else -1) * .01
        gr.axes3d(x1, 0, ztick, xorg1, yorg1, z, 2, 2, 2,  size)
        gr.axes3d(x2, ytick, 0, xorg2, yorg2, z, 2, 2, 2, -size)
        gr.updatews()

    def __call__(self) -> None:
        imgui.set_next_window_position(
            700, 100,
            imgui.FIRST_USE_EVER,
        )
        imgui.set_next_window_size_constraints(
            (400, 500),
            (imgui.FLOAT_MAX, imgui.FLOAT_MAX),
        )
        imgui.set_next_window_size(
            500, 550,
            imgui.FIRST_USE_EVER,
        )
        with imgui.begin("GR interactive 3D") as win:
            if not win.expanded:
                return
            c_fov, self._fov = imgui.slider_float("FOV", self._fov, 0, 100)
            c_cam, self._cam_dist = imgui.slider_float(
                "Cam distance", self._cam_dist, 0, 10
            )
            imgui.text(f"Rotation: {self._rot:.3f} - Tilt: {self._tilt:.3f}")
            size = imgui.get_content_region_available()
            size = int(size[0]), int(size[1])
            if size != self._size or c_fov or c_cam:
                self._size = size
                with print_to_texture(max(size), max(size)):
                    self._draw_surface()
            imgui.push_style_color(imgui.COLOR_BUTTON, 1, 1, 1, 1)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 1, 1, 1, 1)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0, 0, 0, 0)
            imgui.image_button(
                gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D),
                *size,
                *self._uvs,
                frame_padding=0
            )
            imgui.pop_style_color(3)
            self._process_input()


def main() -> None:
    width, height = 1280, 720
    window_name = "GR + ImGui/GLFW3 example"
    clear_color = .45, .55, .6, 1
    os.environ["GKS_WSTYPE"] = "100"  # no visible workstation

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    window = glfw.create_window(width, height, window_name, None, None)
    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)
    glfw.make_context_current(window)

    gl.glActiveTexture(gl.GL_TEXTURE0)
    texture_ids = gl.glGenTextures(2)

    imgui.create_context()
    io = imgui.get_io()
    io.ini_file_name = None
    backend = GlfwRenderer(window)

    text_window: Callable[[], None] = TextWindow()
    gr3_window: Callable[[], None] = GR3dWindow()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        backend.process_inputs()
        imgui.new_frame()

        # imgui.show_demo_window()
        for i, fn in enumerate((text_window, gr3_window)):
            assert 0 <= i < len(texture_ids), "not enough texture ids"
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture_ids[i])
            fn()

        gl.glClearColor(*clear_color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        backend.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    gl.glDeleteTextures(2, texture_ids)
    imgui.destroy_context(imgui.get_current_context())
    glfw.terminate()


if __name__ == "__main__":
    main()
