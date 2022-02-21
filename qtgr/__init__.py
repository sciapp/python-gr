# -*- coding: utf-8 -*-
"""PyQt, PySide GR module

Exported Classes:

"""
# standard library
import os
import math
import logging
import warnings
# local library
import gr
from gr.pygr import Plot, PlotAxes, RegionOfInterest, DeviceCoordConverter
from qtgr.backend import QtCore, QtGui
from qtgr.backend import QApplication, QWidget, QPainter, QPrinter, \
    QPrintDialog, getGKSConnectionId
from qtgr.events import MouseEvent, PickEvent, ROIEvent, \
    LegendEvent, MouseGestureEvent, WheelEvent, installEventFilter
from qtgr.events.gestures import PanGestureRecognizer, SelectGestureRecognizer
from gr import __version__, __revision__

__author__ = "Christian Felder <c.felder@fz-juelich.de>"
__copyright__ = """Copyright (c) 2012-2015: Josef Heinen, Florian Rhiem, Christian Felder,
and other contributors:

http://gr-framework.org/credits.html

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

_log = logging.getLogger(__name__)


class GRWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(GRWidget, self).__init__(*args, **kwargs)

        self._sizex, self._sizey = 1., 1.
        self._dwidth, self._dheight = self.width(), self.height()
        self._mwidth = self._dwidth * 2.54 / self.physicalDpiX() / 100.
        self._mheight = self._dheight * 2.54 / self.physicalDpiY() / 100.
        self._keepRatio = False
        self._bgColor = QtCore.Qt.white
        os.environ["GKS_WSTYPE"] = "381" # GKS Qt Plugin
        os.environ["GKS_DOUBLE_BUF"] = "True"

    def paintEvent(self, event):

        self._painter = QPainter()
        self._painter.begin(self)
        self._painter.fillRect(0, 0, self.width(), self.height(), self._bgColor)
        os.environ["GKSconid"] = getGKSConnectionId(self, self._painter)
        gr.clearws()
        self.draw()
        gr.updatews()
        self._painter.end()

    def resizeEvent(self, event):
        self._dwidth, self._dheight = self.width(), self.height()
        self._mwidth = self._dwidth * 2.54 / self.physicalDpiX() / 100.
        self._mheight = self._dheight * 2.54 / self.physicalDpiY() / 100.
        if self._mwidth > self._mheight:
            self._sizex = 1.
            if self.keepRatio:
                self._sizey = 1.
                self._mwidth = self._mheight
                self._dwidth = self._dheight
            elif self._mwidth > 0:
                self._sizey = self._mheight / self._mwidth
            else:
                self._sizey = 1.
        else:
            if self.keepRatio:
                self._sizex = 1.
                self._mheight = self._mwidth
                self._dheight = self._dwidth
            elif self._mheight > 0:
                self._sizex = self._mwidth / self._mheight
            else:
                self._sizex = 1.
            self._sizey = 1.

    def screenChangedEvent(self, event):
        gr.configurews()
        self.update()

    def setBackground(self, qcolor):
        self._bgColor = qcolor

    @property
    def mwidth(self):
        """Get metric width of the widget excluding any window frame."""
        return self._mwidth

    @property
    def mheight(self):
        """Get metric height of the widget excluding any window frame."""
        return self._mheight

    @property
    def dwidth(self):
        """Get device width in consideration of ratio (keepRatio)."""
        return self._dwidth

    @property
    def dheight(self):
        """Get device height in consideration of ratio (keepRatio)."""
        return self._dheight

    @property
    def sizex(self):
        """..."""
        return self._sizex

    @property
    def sizey(self):
        """..."""
        return self._sizey

    @property
    def keepRatio(self):
        return self._keepRatio

    @keepRatio.setter
    def keepRatio(self, bool):
        self._keepRatio = bool
        self.resizeEvent(None)
        self.update()

    def draw(self, clear=None, update=None):
        # obsolete kwargs clear, update (unused) just kept for compatibility
        if clear is not None or update is not None:
            warnings.warn("Clear and update kwargs do not affect draw "
                          "method anymore and will be removed in future "
                          "versions. Please remove these arguments from your "
                          "draw calls. A clear and update will be done "
                          "internally for each paintEvent.", FutureWarning)

    def save(self, path):
        (p, ext) = os.path.splitext(path)
        if ext.lower()[1:] == gr.GRAPHIC_GRX:
            gr.begingraphics(path)
            self.draw()
            gr.endgraphics()
        else:
            gr.beginprint(path)
            self.draw()
            gr.endprint()
        self.repaint()

    def printDialog(self, documentName="qtgr-untitled"):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setDocName(documentName)
        painter = QPainter()
        dlg = QPrintDialog(printer)
        if dlg.exec_() == QPrintDialog.Accepted:
            painter.begin(printer)
            os.environ["GKSconid"] = getGKSConnectionId(self, painter)

            # upscaling to paper size and
            # alignment (horizontal and vertical centering)
            xscale = printer.pageRect().width() / float(self.width())
            yscale = printer.pageRect().height() / float(self.height())
            scale = min(xscale, yscale)
            painter.translate(printer.paperRect().x() +
                              printer.pageRect().width() / 2,
                              printer.paperRect().y() +
                              printer.pageRect().height() / 2)
            painter.scale(scale, scale)
            painter.translate(-self.width() / 2, -self.height() / 2)
            gr.clearws()
            self.draw()
            gr.updatews()
            painter.end()


class InteractiveGRWidget(GRWidget):

    logXinDomain = QtCore.Signal(bool)
    logYinDomain = QtCore.Signal(bool)
    modePick = QtCore.Signal(bool)

    GESTURE_RECOGNIZERS = [PanGestureRecognizer, SelectGestureRecognizer]

    def __init__(self, *args, **kwargs):
        super(InteractiveGRWidget, self).__init__(*args, **kwargs)
        self._recognizers = []
        # register gesture recognizers
        for recognizer in self.GESTURE_RECOGNIZERS:
            instance = recognizer()
            self.grabGesture(recognizer.registerRecognizer(instance))
            # keep a reference on existing QGestureRecognizers in order
            # to circumvent that they will be accidentially freed when
            # using PyQt4 versions which will not handle the membership
            # correctly, e.g. PyQt4 4.9.1 shipped with Ubuntu 12.04.
            self._recognizers.append(instance)

        self._eventFilter = installEventFilter(self)
        self._eventFilterEnabled = True
        self.cbm.addHandler(MouseEvent.MOUSE_MOVE, self.mouseMove)
        self.cbm.addHandler(MouseEvent.MOUSE_PRESS, self.mousePress)
        self.cbm.addHandler(MouseEvent.MOUSE_RELEASE, self.mouseRelease)
        self.cbm.addHandler(WheelEvent.WHEEL_MOVE, self.wheelMove)
        self.cbm.addHandler(PickEvent.PICK_MOVE, self.pickMove)
        self.cbm.addHandler(MouseGestureEvent.MOUSE_PAN, self._mousePan)
        self.cbm.addHandler(MouseGestureEvent.MOUSE_SELECT, self._mouseSelect)
        self.setMouseTracking(True)
        self._tselect = None  # select point tuple
        self._logXinDomain = None
        self._logYinDomain = None
        self._pickMode = False
        self._pickEvent = None
        self._selectEnabled, self._panEnabled = True, True
        self._roiEnabled = True
        self._zoomEnabled = True
        self._lstPlot = []

    def draw(self, clear=None, update=None):
        # obsolete kwargs clear, update (unused) just kept for compatibility
        GRWidget.draw(self, clear, update)
        gr.setwsviewport(0, self.mwidth, 0, self.mheight)
        gr.setwswindow(0, self.sizex, 0, self.sizey)

        for plot in self._lstPlot:
            plot.sizex, plot.sizey = self.sizex, self.sizey
            plot.drawGR()
            # logDomainCheck
            logXinDomain = plot.logXinDomain()
            logYinDomain = plot.logYinDomain()
            if logXinDomain != self._logXinDomain:
                self._logXinDomain = logXinDomain
                self.logXinDomain.emit(self._logXinDomain)
            if logYinDomain != self._logYinDomain:
                self._logYinDomain = logYinDomain
                self.logYinDomain.emit(self._logYinDomain)

        if self._pickEvent:
            event = self._pickEvent
            gr.setviewport(*event.viewportscaled)
            wcPoint = event.getWC(event.viewport)
            window = gr.inqwindow()
            gr.setwindow(*event.getWindow())
            gr.setmarkertype(gr.MARKERTYPE_PLUS)
            gr.polymarker([wcPoint.x], [wcPoint.y])
            gr.setwindow(*window)

    def addPlot(self, *args, **kwargs):
        for plot in args:
            if plot and plot not in self._lstPlot:
                self._lstPlot.append(plot)
        self.update()
        return self._lstPlot

    @property
    def cbm(self):
        """Get CallbackManager used by EventFilter"""
        return self._eventFilter.manager

    def setEventFilterEnabled(self, flag):
        """Dis-/Enable QtGR events"""
        if self._eventFilterEnabled:
            if not flag:
                self.removeEventFilter(self._eventFilter)
        elif flag:
            self.installEventFilter(self._eventFilter)
        self._eventFilterEnabled = flag

    def plot(self, *args, **kwargs):
        plot = Plot()
        axes = PlotAxes(plot.viewport)
        axes.plot(*args, **kwargs)
        plot.addAxes(axes)
        return self.addPlot(plot)

    def adjustSelectRect(self, p0, p1):
        # can be used to restrict select rectangle, e.g. to given aspect ratio
        return p0, p1

    def paintEvent(self, event):
        super(InteractiveGRWidget, self).paintEvent(event)
        self._painter.begin(self)
        if self.getMouseSelectionEnabled() and self._tselect:
            p0, p1 = self._tselect
            coords = DeviceCoordConverter(self.dwidth, self.dheight)
            coords.setNDC(p0.x, p0.y)
            p0dc = coords.getDC()
            coords.setNDC(p1.x, p1.y)
            p1dc = coords.getDC()
            if self._getPlotsForPoint(p0):
                rect = QtCore.QRect(QtCore.QPoint(int(p0dc.x), int(p0dc.y)),
                                    QtCore.QPoint(int(p1dc.x), int(p1dc.y))).normalized()
                self._painter.setOpacity(.75)
                self._painter.drawRect(rect)
                self._painter.setOpacity(1.)

        self._painter.end()

    def setAutoScale(self, mask):
        for plot in self._lstPlot:
            plot.autoscale = mask

    def getPickMode(self):
        return self._pickMode

    def setPickMode(self, bool):
        self._pickMode = bool
        self.modePick.emit(self._pickMode)

    def getMouseSelectionEnabled(self):
        return self._selectEnabled

    def setMouseSelectionEnabled(self, flag):
        self._selectEnabled = flag

    def getMousePanEnabled(self):
        return self._panEnabled

    def setMousePanEnabled(self, flag):
        self._panEnabled = flag

    def getMouseZoomEnabled(self):
        return self._zoomEnabled

    def setMouseZoomEnabled(self, flag):
        self._zoomEnabled = flag

    def _getPlotsForPoint(self, p0):
        res = []
        for plot in self._lstPlot:
            xmin, xmax, ymin, ymax = plot.viewportscaled
            if p0.x >= xmin and p0.x <= xmax and p0.y >= ymin and p0.y <= ymax:
                res.append(plot)
        return res

    def _pick(self, p0, type):
        for plot in self._getPlotsForPoint(p0):
            (coord, axes, _curve) = plot.pick(p0, self.dwidth, self.dheight)
            if coord:
                dcPoint = coord.getDC()
                QApplication.sendEvent(self, PickEvent(type,
                                                             self.dwidth,
                                                             self.dheight,
                                                             dcPoint.x,
                                                             dcPoint.y,
                                                             plot.viewport,
                                                             coord.getWindow(),
                                                             sizex=axes.sizex,
                                                             sizey=axes.sizey))

    def _select(self, p0, p1):
        self._pickEvent = None
        change = False
        for plot in self._getPlotsForPoint(p0):
            plot.select(p0, p1, self.dwidth, self.dheight)
            change = True
        if change:
            self.update()

    def mouseSelect(self, event):
        p0 = event.getNDC()
        p0, p1 = self.adjustSelectRect(p0, p0 + event.getOffset())
        self._tselect = (p0, p1)
        if event.isFinished():
            self._tselect = None
            self._select(p0, p1)
        self.update()

    def _mouseSelect(self, event):
        if self.getMouseSelectionEnabled():
            self.mouseSelect(event)

    def _pan(self, p0, dp):
        self._pickEvent = None
        change = False
        for plot in self._getPlotsForPoint(p0):
            plot.pan(dp, self.dwidth, self.dheight)
            change = True
        if change:
            self.update()

    def mousePan(self, event):
        self._pan(event.getNDC(), event.getOffset())

    def _mousePan(self, event):
        if self.getMousePanEnabled():
            self.mousePan(event)
            # disable roi recognition during pannning
            self._roiEnabled = event.isFinished()

    def _zoom(self, dpercent, p0):
        self._pickEvent = None
        change = False
        for plot in self._getPlotsForPoint(p0):
            plot.zoom(dpercent, p0, self.dwidth, self.dheight)
            change = True
        if change:
            self.update()

    def _roi(self, p0, type, buttons, modifiers):
        if self._roiEnabled:
            for plot in self._lstPlot:
                roi = plot.getROI(p0)
                if roi:
                    if roi.regionType == RegionOfInterest.LEGEND:
                        eventObj = LegendEvent
                    else:
                        eventObj = ROIEvent
                    coords = DeviceCoordConverter(self.dwidth, self.dheight)
                    coords.setNDC(p0.x, p0.y)
                    p0dc = coords.getDC()
                    QApplication.sendEvent(self,
                                                 eventObj(type,
                                                          self.dwidth,
                                                          self.dheight,
                                                          p0dc.x, p0dc.y,
                                                          buttons, modifiers,
                                                          roi))

    def mousePress(self, event):
        if event.getButtons() & MouseEvent.LEFT_BUTTON:
            if self.getPickMode():
                self.setPickMode(False)
                self._pick(event.getNDC(), PickEvent.PICK_PRESS)
            else:
                if event.getModifiers() & MouseEvent.CONTROL_MODIFIER:
                    self.setPickMode(True)

    def mouseRelease(self, event):
        self._roi(event.getNDC(), ROIEvent.ROI_CLICKED, event.getButtons(),
                  event.getModifiers())

    def mouseMove(self, event):
        if self.getPickMode():
            self._pick(event.getNDC(), PickEvent.PICK_MOVE)
        self._roi(event.getNDC(), ROIEvent.ROI_OVER, event.getButtons(),
                  event.getModifiers())

    def wheelMove(self, event):
        if self.getMouseZoomEnabled():
            # delta percent
            dpercent = event.getSteps() * .1
            self._zoom(dpercent, event.getNDC())

    def pickMove(self, event):
        self._pickEvent = event
        self.update()


if __name__ == "__main__":
    import sys
    from gr import pygr
    logging.basicConfig(level=logging.CRITICAL)
    for name in [__name__, pygr.base.__name__, pygr.__name__]:
        logging.getLogger(name).setLevel(logging.DEBUG)
    app = QApplication(sys.argv)
    grw = InteractiveGRWidget()
    grw.resize(QtCore.QSize(500, 500))
    viewport = [0.1, 0.45, 0.1, 0.88]
    vp2 = [.6, .95, .1, .88]

    x = [-3.3 + t * .1 for t in range(66)]
    y = [t ** 5 - 13 * t ** 3 + 36 * t for t in x]

    n = 100
    pi2_n = 2.*math.pi / n
    x2 = [i * pi2_n for i in range(0, n + 1)]
    y2 = map(lambda xi: math.sin(xi), x2)

    plot = Plot(viewport).addAxes(PlotAxes(viewport).plot(x, y),
                                  PlotAxes(viewport).plot(x2, y2))
    plot.title, plot.subTitle = "foo", "bar"
    plot.xlabel, plot.ylabel = "x", "f(x)"

    plot2 = Plot(vp2).addAxes(PlotAxes(vp2).plot(x2, y2))
    plot2.title, plot2.subTitle = "Title", "Subtitle"
    plot2.xlabel = "x"

    grw.addPlot(plot)
    grw.addPlot(plot2)
    grw.show()
    grw.update()

    sys.exit(app.exec_())
