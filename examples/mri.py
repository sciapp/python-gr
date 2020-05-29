#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- no-plot -*-
"""
Simple MRI visualization example
    - drag the mouse to move the camera
    - use the mousewheel to change the threshold value for densities
"""

import os
import sys

have_pyside = True
try:
    from PySide import shiboken
except ImportError:
    try:
        import shiboken
    except ImportError:
        have_pyside = False
if have_pyside:
    from PySide import QtCore
    from PySide.QtGui import QWidget, QApplication, QPainter
else:
    try:
        from PyQt4 import QtCore
        from PyQt4.QtGui import QWidget, QApplication, QPainter
        from sip import unwrapinstance
    except ImportError:
        try:
            from PyQt5 import QtCore
            from PyQt5.QtGui import QPainter
            from PyQt5.QtWidgets import QWidget, QApplication
            from sip import unwrapinstance
        except ImportError:
            print('Unable to load Qt binding')
            exit(-1)


import numpy as np
import gr
import gr3
from ctypes import c_int


data = np.fromfile("mri.raw", np.uint16)
data = data.reshape((64, 64, 93))


def spherical_to_cartesian(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z


class GrWidget(QWidget):
    def __init__(self):
        super(GrWidget, self).__init__()

        self.setup_ui(self)

        os.environ["GKS_WSTYPE"] = "381"
        os.environ["GKS_DOUBLE_BUF"] = "True"

        self.w = 500
        self.h = 500
        self.beginx = self.x = 0
        self.beginy = self.y = 0
        self.painter = QPainter()
        self.isolevel = (data.min() + data.max()) // 2
        self.export = False
        self.needs_refresh = True
        
    @staticmethod
    def setup_ui(form):
        form.setWindowTitle("GrWidget")
        form.resize(QtCore.QSize(500, 500).expandedTo(form.minimumSizeHint()))

    def draw_image(self):
        if not self.needs_refresh:
            return
        self.needs_refresh = False
        gr.clearws()
        gr.setwindow(0, self.w, 0, self.h)
        gr.setviewport(0, 1, 0, 1)

        gr3.setbackgroundcolor(1, 1, 1, 0)
        vertices, normals = gr3.triangulate(data, (1.0/64, 1.0/64, 1.0/128), (-0.5, -0.5, -0.5), self.isolevel)
        mesh = gr3.createmesh(len(vertices)*3, vertices, normals, np.ones(vertices.shape))
        gr3.drawmesh(mesh, 1, (0,0,0), (0,0,1), (0,1,0), (1,1,1), (1,1,1))
        center = spherical_to_cartesian(-2, np.pi*self.y / self.h+np.pi/2, np.pi*self.x / self.w)
        up = spherical_to_cartesian(1, np.pi*self.y / self.h+np.pi, np.pi*self.x / self.w)
        gr3.cameralookat(center[0], center[1], -0.25+center[2], 0, 0, -0.25, up[0], up[1], up[2])
        gr3.drawimage(0, self.w, 0, self.h, self.w, self.h, gr3.GR3_Drawable.GR3_DRAWABLE_GKS)
        if self.export:
            gr3.export("mri.html", 800, 800)
            print("Saved current isosurface to mri.html")
            self.export = False
        gr3.clear()
        gr3.deletemesh(c_int(mesh.value))

    def mouseMoveEvent(self, event):
        self.x += event.pos().x() - self.beginx
        self.y -= event.pos().y() - self.beginy
        self.beginx = event.pos().x()
        self.beginy = event.pos().y()
        self.needs_refresh = True
        self.update()

    def mousePressEvent(self, event):
        self.beginx = event.pos().x()
        self.beginy = event.pos().y()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.text() == 'h':
            self.export = True
        self.needs_refresh = True
        self.update()

    def wheelEvent(self, ev):
        if hasattr(ev, 'delta'):
            delta = ev.delta()
        else:
            delta = ev.angleDelta().y()
        if delta > 0:
            if self.isolevel * 1.01 < data.max():
                self.isolevel *= 1.01
        else:
            if self.isolevel * 0.99 > data.min():
                self.isolevel *= 0.99
        self.isolevel = int(self.isolevel + 0.5)
        self.needs_refresh = True
        self.update()

    def resizeEvent(self, event):
        self.needs_refresh = True
        self.update()

    def paintEvent(self, ev):
        self.painter.begin(self)
        if have_pyside:
            os.environ['GKSconid'] = "%x!%x" % (
                int(shiboken.getCppPointer(self)[0]),
                int(shiboken.getCppPointer(self.painter)[0]))
        else:
            os.environ["GKSconid"] = "%x!%x" % (unwrapinstance(self),
                                             unwrapinstance(self.painter))
        self.draw_image()
        gr.updatews()
        self.painter.end()


app = QApplication(sys.argv)
win = GrWidget()
win.show()

exit(app.exec_())
