"""
A demo showing how to use gr.camerainteraction with PyQt5
"""

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import sip
import gr


class Gr3DInteractionWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.setMinimumSize(500, 500)
        self.setMaximumSize(500, 500)
        self.setWindowTitle("Press P to switch between projections")

        os.environ["GKS_WSTYPE"] = "381"
        os.environ["GKS_DOUBLE_BUF"] = "True"
        os.environ["GKS_QT_VERSION"] = "5"

        self._width = 500
        self._height = 500
        self._sizex = 1
        self._sizey = 1

        self._previous_mouse_position = None
        self._projection = 'orthographic'

        gr.setwindow3d(
            x_min=0, x_max=100,
            y_min=0, y_max=100,
            z_min=-50, z_max=50
        )
        gr.settransformationparameters(
            camera_position_x=350, camera_position_y=350, camera_position_z=0,
            up_vector_x=0, up_vector_y=0, up_vector_z=1,
            focus_point_x=50, focus_point_y=50, focus_point_z=0
        )

        try:
            self.devicePixelRatioF()
        except AttributeError:
            try:
                self.devicePixelRatio()
            except AttributeError:
                self.devicePixelRatio = lambda: 1
            self.devicePixelRatioF = lambda: float(self.devicePixelRatio())

        self._currentDevicePixelRatio = self.devicePixelRatioF()

    def draw(self):
        gr.clearws()
        self._currentDevicePixelRatio = self.devicePixelRatioF()
        mwidth = self._width * 2.54 / self.physicalDpiX() / 100 / self._currentDevicePixelRatio
        mheight = self._height * 2.54 / self.physicalDpiY() / 100 / self._currentDevicePixelRatio
        gr.setwsviewport(0, mwidth, 0, mheight)
        gr.setwswindow(0, self._sizex, 0, self._sizey)
        gr.setviewport(0, self._sizex, 0, self._sizey)
        if self._projection == 'perspective':
            gr.setperspectiveprojection(
                near_plane=0.1,
                far_plane=1000,
                fov=15
            )
        else:
            gr.setorthographicprojection(
                left=-60, right=60,
                bottom=-60, top=60,
                near_plane=-60, far_plane=60
            )
        gr.axes3d(10, 10, 10, 50, 50, 0, 2, 2, 2, -0.0075)
        self.update()

    def resizeEvent(self, event):
        self._width = event.size().width()
        self._height = event.size().height()
        if self._width > self._height:
            self._sizex = 1
            self._sizey = float(self._height) / self._width
        else:
            self._sizex = float(self._width) / self._height
            self._sizey = 1
        self.draw()

    def paintEvent(self, ev) :
        self.painter = QtGui.QPainter()
        self.painter.begin(self)
        os.environ['GKSconid'] = "%x!%x" % (sip.unwrapinstance(self), sip.unwrapinstance(self.painter))
        gr.updatews()
        self.painter.end()

    def moveEvent(self, event):
        if self.devicePixelRatioF() != self._currentDevicePixelRatio:
            self.draw()

    def mousePressEvent(self, event):
        x, y = float(event.x()) / self.width(), float(event.y()) / self.height()
        self._previous_mouse_position = (x, y)

    def mouseMoveEvent(self, event):
        if self._previous_mouse_position is None:
            return
        x, y = float(event.x()) / self.width(), float(event.y()) / self.height()
        mouse_position = (x, y)
        gr.camerainteraction(
            start_mouse_position_x=self._previous_mouse_position[0],
            start_mouse_position_y=1 - self._previous_mouse_position[1],
            end_mouse_position_x=mouse_position[0],
            end_mouse_position_y=1 - mouse_position[1]
        )
        self._previous_mouse_position = mouse_position
        self.draw()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_P:
            if self._projection == 'perspective':
                self._projection = 'orthographic'
            else:
                self._projection = 'perspective'
            self.draw()


app = QtWidgets.QApplication(sys.argv)
if not sys.platform == "linux2" :
    app.setStyle('Windows')

w = Gr3DInteractionWidget()
w.show()

sys.exit(app.exec_())
