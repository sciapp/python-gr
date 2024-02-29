import os
import sys

from PyQt6 import sip, QtWidgets
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt6.QtQuick import QQuickPaintedItem, QQuickWindow

from gr import panzoom, inqwindow, ndctowc
from gr.pygr import hexbin
from numpy.random import randn

os.environ["GKSwstype"] = "381"
os.environ["GKS_QT_VERSION"] = "6"

x = randn(1000000)
y = randn(1000000)

class GRWidget(QQuickPaintedItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = 640
        self.h = 450
        self.zoom = None
        self.setAcceptHoverEvents(True)
        self.xy = ""

    def paint(self, painter):
        os.environ['GKSconid'] = "%x#%d" % (sip.unwrapinstance(painter), QQuickWindow().effectiveDevicePixelRatio())

        self.w, self.h = self.width(), self.height()
        if self.zoom is None:
            xmin, xmax, ymin, ymax = (-5, 5, -5, 5)
        elif self.zoom != 0:
            xmin, xmax, ymin, ymax = panzoom(0, 0, self.zoom)
        else:
            xmin, xmax, ymin, ymax = inqwindow()

        self.nbins = self.property('nbins')
        hexbin(x, y, xlim=(xmin, xmax), ylim=(ymin, ymax), nbins=self.nbins, title=f"nbins: {self.nbins}", size=(self.w, self.h))

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