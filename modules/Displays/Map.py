import sys
from pyface.qt import QtGui, QtCore
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

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
        self.n = 1

    def Settings(self):
        self.SetWind = QtGui.QWidget()
        self.SetLay = QtGui.QFormLayout()
        self.SetWind.setLayout(self.SetLay)

        # -> filled
        lb_llcrnrlon = QtGui.QLabel()
        lb_llcrnrlon.setText('longitude of lower left hand corner (deg)')
        self.llcrnrlon = QtGui.QLineEdit()
        self.llcrnrlon.setText('-180')

        lb_urcrnrlon = QtGui.QLabel()
        lb_urcrnrlon.setText('longitude of upper right hand corner (deg)')
        self.urcrnrlon = QtGui.QLineEdit()
        self.urcrnrlon.setText('180')

        lb_llcrnrlat = QtGui.QLabel()
        lb_llcrnrlat.setText('latitude of lower left hand corner (deg)')
        self.llcrnrlat = QtGui.QLineEdit()
        self.llcrnrlat.setText('-80')

        lb_urcrnrlat = QtGui.QLabel()
        lb_urcrnrlat.setText('latitude of upper right hand corner (deg)')
        self.urcrnrlat = QtGui.QLineEdit()
        self.urcrnrlat.setText('80')

        lb_resolution = QtGui.QLabel()
        lb_resolution.setText('resolution')
        self.resolution = QtGui.QComboBox()
        item = ['crude','low','intermediate','high','full']
        for i in range(len(item)):
            self.resolution.addItem(item[i])

        btn_enter_view = QtGui.QCommandLinkButton()
        icon = QtGui.QIcon(os.path.join(os.getcwd(),'subroutine','icon','Icon_Files','view.ico'))
        btn_enter_view.setIcon(icon)
        btn_enter_view.setText('View!')
        btn_enter_view.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        btn_enter_view.clicked.connect(self.btn_enter_view_clicked)

        # Set Layout
        # -> input to layout
        # build group of parameters
        group_parameters = QtGui.QGroupBox()
        group_parameters.setTitle('Settings of Parameters')
        layout_parameters = QtGui.QFormLayout()
        layout_parameters.addRow(lb_llcrnrlon, self.llcrnrlon)
        layout_parameters.addRow(lb_urcrnrlon, self.urcrnrlon)
        layout_parameters.addRow(lb_llcrnrlat, self.llcrnrlat)
        layout_parameters.addRow(lb_urcrnrlat, self.urcrnrlat)
        layout_parameters.addRow(lb_resolution, self.resolution)
        group_parameters.setLayout(layout_parameters)
        self.SetLay.addWidget(group_parameters)
        self.SetLay.addRow(btn_enter_view)
        # self.SetLay.addStretch()

    def act_mTest(self):
        graph_widget = MainViewExample()
        # dir, fil = os.path.split(self.line_vxyz.text())
        fil = "Basemap"
        graph_widget.setWindowTitle(fil)
        graph_widget.popIn.connect(self.addTab)
        graph_widget.popOut.connect(self.removeTab)
        self.tab.addTab(graph_widget,fil)

    def btn_enter_view_clicked(self):
        graph_widget = MainView(llcrnrlat=float(self.llcrnrlat.text()), urcrnrlat=float(self.urcrnrlat.text()),
                    llcrnrlon=float(self.llcrnrlon.text()), urcrnrlon=float(self.urcrnrlon.text()), resolution=str(self.resolution.currentText())[0])
        # dir, fil = os.path.split(self.line_vxyz.text())
        fil = "Map {}".format(self.n)
        self.n += 1
        graph_widget.setWindowTitle(fil)
        graph_widget.popIn.connect(self.addTab)
        graph_widget.popOut.connect(self.removeTab)
        self.tab.addTab(graph_widget, fil)

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

class MainViewExample(QtGui.QMainWindow):
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
        self.mplcanvas = MplCanvasExample(parent=self)
        self.setCentralWidget(self.mplcanvas)

class MainView(QtGui.QMainWindow):
    popOut = QtCore.Signal(QtGui.QWidget)
    popIn = QtCore.Signal(QtGui.QWidget)
    def __init__(self, projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, resolution='c',
                 color='tan', lake_color='lightblue', title="Mercator Projection",
                 fill_color='lightblue', parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        mBar = self.menuBar()
        mWindow = mBar.addMenu("Window")
        mPopOut = mWindow.addAction("Pop Out")
        mPopIn = mWindow.addAction("Pop In")
        mPopOut.triggered.connect(lambda: self.popOut.emit(self))
        mPopIn.triggered.connect(lambda: self.popIn.emit(self))
        self.mplcanvas = MplCanvas(parent=self, projection=projection, llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
                    llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon, resolution=resolution)
        self.setCentralWidget(self.mplcanvas)

class MplCanvasExample(FigureCanvas):
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

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100,
                 projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, resolution='c',
                 color='tan', lake_color='lightblue', title="Mercator Projection",
                 fill_color='lightblue'):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

        m = Basemap(ax=self.axes,projection=projection, llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
                    llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon, resolution=resolution)
        m.drawcoastlines()
        m.fillcontinents(color=color, lake_color=lake_color)
        # draw parallels and meridians.
        m.drawparallels(np.linspace(llcrnrlat, urcrnrlat, 10), labels=[True, True, False, False], dashes=[2, 2])
        m.drawmeridians(np.linspace(llcrnrlon, urcrnrlon, 10), labels=[False, False, False, True], dashes=[2, 2])
        m.drawmapboundary(fill_color=fill_color)
        fig.suptitle(title)