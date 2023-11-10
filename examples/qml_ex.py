import os
import sys

from PyQt6 import sip, QtWidgets
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt6.QtQuick import QQuickPaintedItem, QQuickWindow

from gr.pygr import *
from gr import __gr as c_gr
import numpy as np
from ctypes import POINTER, c_double, byref

c_gr.gr_panzoom.argtypes = [c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]

def panzoom(x, y, zoom):
    xmin = c_double()
    xmax = c_double()
    ymin = c_double()
    ymax = c_double()
    c_gr.gr_panzoom(x, y, zoom, zoom, byref(xmin), byref(xmax), byref(ymin), byref(ymax))
    return [xmin.value, xmax.value, ymin.value, ymax.value]

os.environ["GKSwstype"] = "381"
os.environ["GKS_QT_VERSION"] = "6"

x = np.random.randn(1000000)
y = np.random.randn(1000000)

class GRWidget(QQuickPaintedItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = 500
        self.h = 500
        self.sizex = 1
        self.sizey = 1
        self.zoom = None
        self.setAcceptHoverEvents(True)
        self.xy = ""

    def draw(self) :
        self.nbins = self.property('nbins')
        gr.clearws()

        if self.zoom is None:
            xmin, xmax, ymin, ymax = (-5, 5, -5, 5)
        elif self.zoom != 0:
            xmin, xmax, ymin, ymax = panzoom(0, 0, self.zoom)
        else:
            xmin, xmax, ymin, ymax = gr.inqwindow()

        hexbin(x, y, xlim=(xmin, xmax), ylim=(ymin, ymax), nbins=self.nbins, title=f"nbins: {self.nbins}")

    def resize(self):
        self.w = self.size().width()
        self.h = self.size().height()
        if self.w > self.h:
            self.sizex = 1
            self.sizey = float(self.h)/self.w
        else:
            self.sizex = float(self.w)/self.h
            self.sizey = 1

    def paint(self, painter):
        self.resize()
        os.environ['GKSconid'] = "%x#%d" % (sip.unwrapinstance(painter), QQuickWindow().effectiveDevicePixelRatio())
        self.draw()
        gr.updatews()
        return

    @pyqtSlot(int, int, result=str)
    def getXY(self, x, y):
        if self.w > self.h:
             xn = x / self.w
             yn = (self.h - y) / self.w
        else:
             xn = x / self.h
             yn = (self.h - y) / self.h
        x, y = ndctowc(xn, yn)
        self.xy = f'{x:.4f}, {y:.4f}'
        return self.xy

    def wheelEvent(self, event):
        if event.angleDelta().y() != 0:
            self.zoom = 1.02 if event.angleDelta().y() < 0 else 1/1.02
        else:
            self.zoom = 0
        self.update()


app = QGuiApplication(sys.argv)
qmlRegisterType(GRWidget, 'GRWidget', 1, 0, 'GRWidget')
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('qml_ex.qml')

sys.exit(app.exec())
