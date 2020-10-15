from lindugui import LMainWindow
import os
from pyface.qt.QtCore import *
from pyface.qt.QtGui import *
from obspy import read
import obspy as ob
import os
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_qt4agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import \
    NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D

class MainWindow(LMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Seismo View (BETA)')
        self.menubar()
        self.mainWidget()
        self.setCentralWidget(self.mainWin)
        self.showMaximized()

    def menubar(self):
        self.mOpen = self.mFile.addAction('Open')
        self.mHelp = self.mbar.addMenu('Help')

        self.mOpen.triggered.connect(self.act_mOpen)

        self.mHelp.setDisabled(True)

    def mainWidget(self):
        self.mainWin = QWidget()
        self.mainLayout = QHBoxLayout()
        self.mainWin.setLayout(self.mainLayout)
        self.mainViewGroup = QGroupBox()
        self.mainViewGroup.setTitle("Views")
        self.mainLayout.addWidget(self.mainViewGroup)
        mainViewLayout = QVBoxLayout()
        self.mainViewGroup.setLayout(mainViewLayout)
        self.tabMainView = QTabWidget()
        mainViewLayout.addWidget(self.tabMainView)
        self.tabMainView.setTabsClosable(True)
        self.tabMainView.tabCloseRequested.connect(self.closeTab)

    def closeTab (self, currentIndex):
        currentQWidget = self.tabMainView.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabMainView.removeTab(currentIndex)

    def act_mOpen(self):
        opendialog = QFileDialog()
        open_file = opendialog.getOpenFileName(self, 'Open Seismogram File', '/', "Format File (*.seed *.mseed *.SAC)")
        graph_widget = MainView(open_file)
        # dir, fil = os.path.split(self.line_vxyz.text())
        fil = os.path.split(open_file)[-1]
        graph_widget.setWindowTitle(fil)
        graph_widget.popIn.connect(self.addTab)
        graph_widget.popOut.connect(self.removeTab)
        self.tabMainView.addTab(graph_widget, fil)

    def addTab(self, widget):
        if self.tabMainView.indexOf(widget) == -1:
            widget.setWindowFlags(Qt.Widget)
            self.tabMainView.addTab(widget, widget.windowTitle())

    def removeTab(self, widget):
        index = self.tabMainView.indexOf(widget)
        if index != -1:
            self.tabMainView.removeTab(index)
            widget.setWindowFlags(Qt.Window)
            widget.show()

class MainView(LMainWindow):
    popOut = Signal(QWidget)
    popIn = Signal(QWidget)
    def __init__(self, open_file, parent=None):
        LMainWindow.__init__(self, parent)
        mWindow = self.mbar.addMenu("Window")
        mPopOut = mWindow.addAction("Pop Out")
        mPopIn = mWindow.addAction("Pop In")
        mOptions = self.mbar.addMenu("Options")
        self.mSingle = mOptions.addAction("Single Selection")
        self.mMultiple = mOptions.addAction("Multi Selection")
        self.mDeselect = mOptions.addAction("Deselect All")
        mPopOut.triggered.connect(lambda: self.popOut.emit(self))
        mPopIn.triggered.connect(lambda: self.popIn.emit(self))
        self.tbl_info = QTableWidget()
        self.setCentralWidget(self.tbl_info)
        self.setTable()
        self.open_file = open_file
        self.file_data = read(self.open_file)
        for i in range(int(self.file_data.count())):
            self.tr_data = self.file_data.pop(0)
            self.input_to_informationtable(self.tbl_info, self.tr_data)
        self.tbl_info.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_info.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.mSingle.setDisabled(True)
        self.mMultiple.setDisabled(False)
        self.mSingle.triggered.connect(self.act_mSingle)
        self.mMultiple.triggered.connect(self.act_mMultiple)
        self.mDeselect.triggered.connect(self.act_mDeselect)

    def act_mSingle(self):
        self.mSingle.setDisabled(True)
        self.mMultiple.setDisabled(False)
        self.tbl_info.setSelectionMode(QAbstractItemView.SingleSelection)

    def act_mMultiple(self):
        self.mSingle.setDisabled(False)
        self.mMultiple.setDisabled(True)
        self.tbl_info.setSelectionMode(QAbstractItemView.MultiSelection)

    def act_mDeselect(self):
        self.tbl_info.clearSelection()

    def setTable(self):
        self.tbl_info.clear()
        self.tbl_info.setRowCount(0)
        self.tbl_info.setColumnCount(11)
        self.tbl_info.setHorizontalHeaderLabels(
            ["Network", "Station", "Location", "Channel", "Start Time",
             "End Time", "Sampling Rate", "Delta", "NPTS", "Calib", "Format"])
        self.tbl_info.setAlternatingRowColors(True)
        self.tbl_info.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbl_info.setSelectionBehavior(QTableWidget.SelectRows)
        self.tbl_info.setSelectionMode(QTableWidget.MultiSelection)
        selected = None

    def input_to_informationtable(self,tbl_info, tr_data):
        n = tbl_info.rowCount()
        tbl_info.insertRow(n)

        # Set table
        tbl_info.setItem(n, 0, QTableWidgetItem(str(tr_data.stats.network)))
        tbl_info.setItem(n, 1, QTableWidgetItem(str(tr_data.stats.station)))
        tbl_info.setItem(n, 2, QTableWidgetItem(str(tr_data.stats.location)))
        tbl_info.setItem(n, 3, QTableWidgetItem(str(tr_data.stats.channel)))
        tbl_info.setItem(n, 4, QTableWidgetItem(str(tr_data.stats.starttime)))
        tbl_info.setItem(n, 5, QTableWidgetItem(str(tr_data.stats.endtime)))
        tbl_info.setItem(n, 6, QTableWidgetItem(str(tr_data.stats.sampling_rate)))
        tbl_info.setItem(n, 7, QTableWidgetItem(str(tr_data.stats.delta)))
        tbl_info.setItem(n, 8, QTableWidgetItem(str(tr_data.stats.npts)))
        tbl_info.setItem(n, 9, QTableWidgetItem(str(tr_data.stats.calib)))
        tbl_info.setItem(n, 10, QTableWidgetItem(str(tr_data.stats._format)))

    def contextMenuEvent(self, event):
        self.menu = QMenu(self.tbl_info)
        self.plot_menu = self.menu.addAction("Plot")
        self.plot_menu.triggered.connect(self.index_selected)
        self.menu.exec_(event.globalPos())

    def index_selected(self):
        indexes = set()
        for currentQTableWidgetItem in self.tbl_info.selectedItems():
            indexes.add(currentQTableWidgetItem.row())
        indexes = list(indexes)
        MplWindow = LMainWindow(self)
        MplWindow.setWindowTitle('plot - Seismo View')
        MplWid = QWidget()
        MplWindow.setCentralWidget(MplWid)
        MplLayout = QVBoxLayout()
        MplWid.setLayout(MplLayout)
        NewCanvas = MplCanvas(self.open_file, indexes)
        NewToolbar = NavigationToolbar(NewCanvas,MplWindow)
        MplLayout.addWidget(NewCanvas)
        MplLayout.addWidget(NewToolbar)
        MplWindow.showMaximized()


class MplCanvas(FigureCanvas):
    def __init__(self, path, indexes, parent = None):
        data = ob.read(path)
        n = data.count()

        with plt.rc_context({'axes.edgecolor':'white','xtick.color':'white','ytick.color':'white'}):
            self.fig = Figure(constrained_layout=True)
            self.fig.autofmt_xdate()
            self.fig.patch.set_facecolor((0,0,0))
            self.ax = self.fig.subplots(len(indexes),1,sharex=True)
            self.fig.tight_layout()
            self.fig.subplots_adjust(wspace=0, hspace=0)

            idx = 0
            for i in range(n):
                tr = data.pop(0)
                if i in indexes:
                    if len(indexes) != 1:
                        x = tr.data
                        t = tr.times('matplotlib')
                        self.ax[idx].set_title("seismogram: {}".format(indexes[idx]+1))
                        self.ax[idx].plot(t,x,'r')
                        self.ax[idx].set_facecolor((0,0,0))
                        self.ax[idx].xaxis_date()
                        self.ax[idx].ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
                        idx += 1
                    else:
                        x = tr.data
                        t = tr.times('matplotlib')
                        self.ax.set_title("seismogram: {}".format(indexes[idx]+1))
                        self.ax.plot(t, x, 'r')
                        self.ax.set_facecolor((0, 0, 0))
                        self.ax.xaxis_date()
                        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))


        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())