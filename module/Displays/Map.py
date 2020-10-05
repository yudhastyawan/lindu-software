import sys
from pyface.qt import QtGui, QtCore
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap

class SetView(QtGui.QMainWindow):
    def __init__(self, tab, parent=None):
        super(SetView, self).__init__(parent)
        mBar = self.menuBar()
        mOpt = mBar.addMenu("Options")
        mTest = mOpt.addAction("Testing the Example data")
        mTest.triggered.connect(self.act_mTest)
        self.Settings()
        self.setCentralWidget(self.SetWind)
        self.tab = tab

    def Settings(self):
        self.SetWind = QtGui.QWidget()
        self.SetLay = QtGui.QVBoxLayout()
        self.SetWind.setLayout(self.SetLay)

        # -> filled

        # Set Layout
        # -> input to layout
        self.SetLay.addStretch()

    def act_mTest(self):
        graph_widget = MainView()
        # dir, fil = os.path.split(self.line_vxyz.text())
        fil = "Basemap"
        graph_widget.setWindowTitle(fil)
        graph_widget.popIn.connect(self.addTab)
        graph_widget.popOut.connect(self.removeTab)
        self.tab.addTab(graph_widget,fil)

    def addTab(self, widget):
        if self.tab.indexOf(widget) == -1:
            widget.setWindowFlags(QtCore.Qt.Widget)
            self.tab.addTab(widget, widget.windowTitle())

    def removeTab(self, widget):
        index = self.tab.indexOf(widget)
        if index != -1:
            self.tab.removeTab(index)
            widget.setWindowFlags(QtCore.Qt.Window)
            widget.show()

class MainView(QtGui.QMainWindow):
    popOut = QtCore.Signal(QtGui.QWidget)
    popIn = QtCore.Signal(QtGui.QWidget)
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        mBar = self.menuBar()
        mWindow = mBar.addMenu("Window")
        mPopOut = mWindow.addAction("Pop Out")
        mPopIn = mWindow.addAction("Pop In")
        mPopOut.triggered.connect(lambda: self.popOut.emit(self))
        mPopIn.triggered.connect(lambda: self.popIn.emit(self))
        self.mplcanvas = MplCanvas(parent=self)
        self.setCentralWidget(self.mplcanvas)

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

        map = Basemap(ax=self.axes)
        map.drawcoastlines()
        map.drawcountries()
        map.drawmapboundary()
        map.fillcontinents(color='coral', lake_color='aqua')
        map.drawmapboundary(fill_color='aqua')