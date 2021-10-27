# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from yubundle import check_package

from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget, QTableWidget, \
    QAbstractItemView, QTableWidgetItem, QVBoxLayout, QMenu
from PySide2.QtCore import QFile, Signal
from PySide2.QtGui import Qt
from PySide2.QtUiTools import QUiLoader

class LSeismoView(QMainWindow):
    def __init__(self, parent = None):
        super(LSeismoView, self).__init__(parent)
        self.load_ui()
        self.ui_settings()
        self.menu_settings()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent.parent / "ui/LSeismoView.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        self.setCentralWidget(self.ui)
        self.setGeometry(self.ui.geometry())
        center = QApplication.primaryScreen().availableGeometry().center()
        frameGeom = self.frameGeometry()
        frameGeom.moveCenter(center)
        self.move(frameGeom.topLeft())
        ui_file.close()

    def ui_settings(self):
        self.ui.seis_tab.tabCloseRequested.connect(self.close_tab)
    
    def menu_settings(self):
        self.ui.actionOpen.triggered.connect(self.actionOpen_clicked)

    def close_tab(self, currentIndex):
        curr_widget = self.ui.seis_tab.widget(currentIndex)
        curr_widget.deleteLater()
        self.ui.seis_tab.removeTab(currentIndex)
    
    def actionOpen_clicked(self):
        if (check_package("obspy") == False):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("you need to install obspy on you environment")
            msg.setInformativeText("pip install obspy")
            msg.setWindowTitle("Obspy is not found")
            msg.setDetailedText("pip install obspy")
            msg.show()
        else:
            openDial = QFileDialog()
            openFile = openDial.getOpenFileName(self, 'Open Seismogram File', '/', "Format File (*.seed *.mseed *.SAC)")[0]
            if (openFile != ""):
                graph_widget = MainView(openFile)
                fil = os.path.split(openFile)[-1]
                graph_widget.setWindowTitle(fil)
                graph_widget.popIn.connect(self.addTab)
                graph_widget.popOut.connect(self.removeTab)
                self.ui.seis_tab.addTab(graph_widget, fil)
    
    def addTab(self, widget):
        if self.ui.seis_tab.indexOf(widget) == -1:
            widget.setWindowFlags(Qt.Widget)
            self.ui.seis_tab.addTab(widget, widget.windowTitle())

    def removeTab(self, widget):
        index = self.ui.seis_tab.indexOf(widget)
        if index != -1:
            self.ui.seis_tab.removeTab(index)
            widget.setWindowFlags(Qt.Window)
            widget.show()

class MainView(QMainWindow):
    popOut = Signal(QWidget)
    popIn = Signal(QWidget)
    def __init__(self, open_file, parent=None):
        QMainWindow.__init__(self, parent)
        self.mbar = self.menuBar()
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

        from obspy import read
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
        if(check_package("matplotlib") == False):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("you need to install matplotlib on you environment")
            msg.setInformativeText("pip install matplotlib")
            msg.setWindowTitle("matplotlib is not found")
            msg.setDetailedText("pip install matplotlib")
            msg.show()
        else:
            indexes = set()
            for currentQTableWidgetItem in self.tbl_info.selectedItems():
                indexes.add(currentQTableWidgetItem.row())
            indexes = list(indexes)
            MplWindow = QMainWindow(self)
            MplWindow.setWindowTitle('plot - Seismo View')
            MplWid = QWidget()
            MplWindow.setCentralWidget(MplWid)
            MplLayout = QVBoxLayout()
            MplLayout.setContentsMargins(0,0,0,0)
            MplLayout.setSpacing(0)
            MplWid.setLayout(MplLayout)
            from lindu.Widgets.Displays.MplCanvas import MplCanvas
            from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolbar
            NewCanvas = MplCanvas(self.open_file, indexes)
            NewToolbar = NavToolbar(NewCanvas,MplWindow)
            MplLayout.addWidget(NewCanvas)
            MplLayout.addWidget(NewToolbar)
            MplWindow.show()

